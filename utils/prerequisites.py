#!/usr/bin/env python

# Assuming this is being run on Mac OS X
import os

packages = {"easy_install": ["pip"],
            "brew": ["terraform", "awscli"],
            "pip": ["ansible"]}

def install_packages(ptype, pname):
    cmd = ""
    if ptype == "brew":
        cmd = "brew install "+pname
        # Checking and installing homebrew, if NOT installed
        if not os.system("brew info cask &>/dev/null"):
            print("Brew installed")
        else:
            print("Brew NOT installed")
            os.system('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')

    elif ptype == "pip":
        cmd = "sudo pip install "+pname
        if pname == "ansible":
            cmd = "sudo pip install ansible --ignore-installed six"

    elif ptype == "easy_install":
        cmd = "sudo easy_install "+pname

    if cmd:
        os.system(cmd)

def run():
    for ptype, pnames in packages.items():
        for pname in pnames:
            install_packages(ptype, pname)
