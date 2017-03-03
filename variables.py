#!/usr/bin/env python

import yaml
import os

with open("config.yml", 'r') as yml_config:
    try:
        config = yaml.load(yml_config)

        config_dir = os.path.abspath(config["config_dir"])
        terraform_dir = os.path.abspath(config["terraform_dir"])

        config_file = os.path.abspath("config.yml")
        var_file = os.path.join(terraform_dir, config["tfvar_file_name"])
        state_file = os.path.join(terraform_dir, config["tfstate_file"])
        out_state_file = state_file

        private_key_path = config["private_key_path"]
        # key_name = os.path.basename(private_key_path)

        ssh_user = config["ssh_user"]

    except yaml.YAMLError as exc:
        print(exc)
