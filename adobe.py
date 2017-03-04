#!/usr/bin/env python

import os
import sys
import yaml
import json

import variables as vars
import common

def print_urls():
    wserver_ip = common.get_ip("wserver")
    master_ips = common.get_ip("master")

    if wserver_ip:
        print("WebApp URL: http://"+wserver_ip)

    if master_ips:
        print("Jenkins Dashboard: http://"+master_ips[0]+":8080\n")

    print_servers()

def print_servers():
    master_ips = common.get_ip("master")
    slave_ips = common.get_ip("slave")
    if master_ips:
        print("Jenkins Servers:")
        print("Masters:")
        print(master_ips)
    if slave_ips:
        print("Slaves:")
        print(slave_ips)

def print_usage():
    print("Usage: ./rescale.py [up, down, config]\n\t\
            jenkins [scaleup, scaledown] [count]\n\t\
            wserver [start503, stop503]\n\t\
            print [urls, servers]")

def check_command():
    clen = len(sys.argv)
    if clen > 1 and clen < 5:
        prop = sys.argv[1]
        if prop in vars.actions or prop in vars.props:
            if clen == 2 and prop in vars.actions:
                return
            elif clen == 3:
                if prop in ["wserver"] and sys.argv[2] in ["start503", "stop503"]:
                    return
                if prop in ["print"] and sys.argv[2] in ["urls", "servers"]:
                    return
            elif clen == 4:
                if prop in ["jenkins"] and sys.argv[2] in ["scaleup", "scaledown"]:
                    return
    print_usage()
    sys.exit(1)


def gen_tfvars(var_file):
    try:
        print("Generating tfvars file for Terraform ###########################")
        config = common.get_config()

        tfvars_contents = ""
        for key,val in config.items():
            if key == "private_key_path":
                val = os.path.abspath(val)
            tfvars_contents = tfvars_contents + key + "=\"" + str(val) + "\"\n"

        with open(var_file, 'w') as tf_writer:
                tf_writer.write(tfvars_contents)
        return True
    except:
        return False


def run_ansible(config_dir, mflag=0, tags=""):
    ret = os.system("python utils/gen_inventory.py")
    if ret != 0:
        print("ERROR: Error creating Ansible inventory")
        return False
    print("Success: hosts file created")

    ansible_inventory = os.path.join(config_dir, 'hosts')

    extra_vars = {}
    public_ip = common.get_ip("wserver")
    extra_vars['public_ip'] = public_ip
    extra_vars['public_ip_httpd'] = public_ip.replace('.','\.' )
    extra_vars['mflag'] = mflag

    extra_vars.update(common.get_config('webapp_repo'))

    cmd = "ansible-playbook --extra-vars '"+ str(json.dumps(extra_vars)) +"' -i "+ansible_inventory+" play.yml"
    if tags:
        cmd += ' --tags "'+tags+'"'

    ret = os.system(cmd)
    if ret != 0:
        print("ERROR: Error running Ansible playbook")
        return False
    return True

def run_terraform(action, terraform_dir):
    ret = 1
    if action=="up":
        if gen_tfvars(var_file):
            print("Success: tfvars file created")
            cmd = "terraform apply -var-file " + var_file + " -state " + state_file + " -state-out " + out_state_file + " " + terraform_dir
    elif action=="down":
        cmd = "terraform destroy -var-file " + var_file + " -state " + state_file + " -state-out " + out_state_file + " " + terraform_dir
    ret = os.system(cmd)
    if ret != 0 :
        print("ERROR [Terraform]: Failure while running Terraform. Exiting.")
        sys.exit(1)
    return True

if __name__ == "__main__":
    # Validate command usage
    check_command()

    prop = sys.argv[1]

    config_dir = vars.config_dir
    terraform_dir = vars.terraform_dir

    var_file = vars.var_file
    state_file = vars.state_file
    out_state_file = vars.out_state_file

    if prop == "up":
        if run_terraform("up", terraform_dir):
            if run_ansible(config_dir):
                print("Hosts configured successfully ###################################")
                print_urls()

    if prop == "down":
        run_terraform("down", terraform_dir)

    if prop == "config":
        run_ansible(config_dir)

    if prop in vars.props:
        action = sys.argv[2]
        if prop == "wserver":
            if action == "start503":
                run_ansible(config_dir, mflag=1, tags="maintenance")
            if action == "stop503":
                run_ansible(config_dir, mflag=0, tags="maintenance")
        if prop == "print":
            if action == "urls":
                print_urls()
            if action == "servers":
                print_servers()
        if prop == "jenkins":
            try:
                count = int(sys.argv[3])
                if action == "scaleup":
                    cmd = "up"
                if action == "scaledown":
                    cmd = "down"

                if common.scale_slaves_config(cmd, count):
                    if run_terraform("up", terraform_dir):
                        if run_ansible(config_dir):
                            print("Hosts configured successfully ###################################")
                            print_urls()

            except ValueError:
                print("ERROR: Please provide an Integer for count")
                print_usage()
