#!/usr/bin/env python

import sys
sys.path.append('./')

import os
import subprocess
import json
import variables as vars

def get_terraform_vars(var_name):
    cmd = "terraform output -state="+state_file+" -json "+var_name
    get_op = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = get_op.communicate()
    return json.loads(out)

def list_to_str(iplist):
    ip_str = ""
    for ip in iplist['value']:
        ip_str += ip+"\n"
    return ip_str

if __name__ == "__main__":
    try:
        print("Generating inventory file for Ansible ##########################")
        state_file = vars.state_file
        out_file = os.path.join(vars.config_dir, "hosts")
        in_file = os.path.join(vars.config_dir, "hosts.tmpl")

        private_key_path = vars.private_key_path
        ssh_user = vars.ssh_user

        master_ips = get_terraform_vars('master_ip')
        slave_ips = get_terraform_vars('slave_ip')
        wserver_ips = get_terraform_vars('wserver_ip')

        mip_str = list_to_str(master_ips)
        sip_str = list_to_str(slave_ips)
        wip_str = list_to_str(wserver_ips)

        replacements = {'ansible_ssh_private_key_file':'ansible_ssh_private_key_file='+private_key_path,
                        'ansible_ssh_user':'ansible_ssh_user='+ssh_user,
                        'mmm.mmm.mmm.mmm': mip_str,
                        'sss.sss.sss.sss': sip_str,
                        'www.www.www.www': wip_str,}

        with open(in_file) as infile, open(out_file, 'w') as outfile:
            for line in infile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                outfile.write(line)
    except:
        sys.exit(1)
