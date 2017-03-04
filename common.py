#!/usr/bin/env python
import variables as vars
import subprocess
import json
import yaml
import sys

def scale_slaves_config(type, count):
    var_name="jslave_count"
    cur_count = get_config(var_name)[var_name]

    if count > 0:
        if type == "up":
            exp_count = cur_count + count
        elif type == "down":
            if count >= cur_count:
                print("ERROR: Can NOT scale down to more than current number of servers")
                sys.exit(1)
            exp_count = cur_count - count

        if mod_config(var_name, exp_count):
            return True
        print("ERROR: Scaling failed!")
    else:
        print("ERROR: Please enter a positive Integer")
    return False


def get_ip(type):
    if type in ["wserver", "master", "slave"]:
        terr_opvar = type+"_ip"
        get_op = subprocess.Popen("terraform output -state="+vars.state_file+" -json "+terr_opvar, stdout=subprocess.PIPE, shell=True)
        (out, err) = get_op.communicate()
        ec2_ips = json.loads(out)
        if type == "wserver":
            for ip in ec2_ips['value']:
                public_ip = ip
            return public_ip
        else:
            return ec2_ips['value']
    else:
        print("Address not found: Unknown server type")
        return False

def mod_config(var_name, val):
    config_val = get_config(var_name)[var_name]
    if config_val!="":
        print("Modifying config: "+var_name+":"+str(val))
        config = get_config()
        config[var_name] = val
        with open(vars.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
            print("Success")
            return True
    else:
        print("ERROR: Config element '"+var_name+"' NOT found")
        return False

def get_config(var_name=""):
    with open(vars.config_file, 'r') as yml_config:
        config = yaml.load(yml_config)
    if not var_name:
        return config
    else:
        if var_name in config.keys():
            return {var_name: config[var_name]}
        return {var_name: ""}
