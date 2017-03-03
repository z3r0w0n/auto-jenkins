#!/usr/bin/env python
import variables as vars
import subprocess
import json
import yaml

def get_publicip():
    get_op = subprocess.Popen("terraform output -state="+vars.state_file+" -json wserver_ip", stdout=subprocess.PIPE, shell=True)
    (out, err) = get_op.communicate()
    ec2_ips = json.loads(out)
    for ip in ec2_ips['value']:
        public_ip = ip
    return public_ip

def get_config(var_name=""):
    with open(vars.config_file, 'r') as yml_config:
        config = yaml.load(yml_config)
    if not var_name:
        return config
    else:
        for key,val in config.items():
            if key == var_name:
                return {key: val}
        return {var_name: ""}
