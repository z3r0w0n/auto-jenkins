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

if __name__ == "__main__":
    try:
        print("Generating inventory file for Ansible ##########################")
        state_file = vars.state_file
        out_file = os.path.join(vars.config_dir, "hosts")
        in_file = os.path.join(vars.config_dir, "hosts.tmpl")

        private_key_path = vars.private_key_path
        ssh_user = vars.ssh_user

        master_ips = get_terraform_vars('master_ip')
        wserver_ips = get_terraform_vars('wserver_ip')

        mip_str = ""
        wip_str = ""
        for mip in master_ips['value']:
            mip_str += mip+"\n"
        for wip in wserver_ips['value']:
            wip_str += wip+"\n"

        replacements = {'ansible_ssh_private_key_file':'ansible_ssh_private_key_file='+private_key_path,
                        'ansible_ssh_user':'ansible_ssh_user='+ssh_user,
                        'mmm.mmm.mmm.mmm': mip_str,
                        'www.www.www.www': wip_str,}

        with open(in_file) as infile, open(out_file, 'w') as outfile:
            for line in infile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                outfile.write(line)
    except:
        sys.exit(1)
