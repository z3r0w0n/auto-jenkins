#!/usr/bin/env python

import os
import sys
import yaml
import json

import variables as vars
import common

def print_url():
    public_ip = common.get_publicip()
    if public_ip:
        print("WebApp URL: http://"+public_ip)

def print_usage():
    print("Usage: ./rescale.py [up, down, config, start503, stop503]")

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
    public_ip = common.get_publicip()
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
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    action = sys.argv[1]

    config_dir = vars.config_dir
    terraform_dir = vars.terraform_dir

    var_file = vars.var_file
    state_file = vars.state_file
    out_state_file = vars.out_state_file

    if action == "up":
        if run_terraform("up", terraform_dir):
            if run_ansible(config_dir):
                print("Webapp deployed successfully ###################################")
                print_url()

    if action == "down":
        run_terraform("down", terraform_dir)

    if action == "config":
        run_ansible(config_dir)

    if action == "start503":
        run_ansible(config_dir, mflag=1, tags="maintenance")

    if action == "stop503":
        run_ansible(config_dir, mflag=0, tags="maintenance")
