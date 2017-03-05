# auto-jenkins
Simple automation code to deploy Jenkins and a web application on AWS infrastructure

This application deploys the below infrastructure (using Terraform):
 - 1 VPC
 - 3 Subnets
 - 3 Security Groups
 - 1 Gateway
 - 3 EC2 Instances

Later, it also configures the AWS CentOS instance to deploy the WebApp with Ansible

##### Prerequisites:
- Run prerequisites.py (Installs all required packages to run this code)
```
  $ python utils/prerequisites.py
```

- Export your AWS credentials
```
  # Get temp credentials
  $ aws sts get-session-token --duration-seconds 3600 --serial-number [IAM_USERID] --token-code [MFA_TOKEN]

  # Export the acquired temp credentials
  export AWS_SESSION_TOKEN=
  export AWS_SECRET_ACCESS_KEY=
  export AWS_REGION=
  export AWS_ACCESS_KEY_ID=
```

- Edit the `config.yml` file with appropriate values

##### Usage:
```

$ ./rescale.py [up, down, config]
	            jenkins [scaleup, scaledown] [count]
	            wserver [start503, stop503]
	            print [urls, servers]

# Deploy infrastructure, configure and deploy WebApp
$ ./adobe.py up

# Destroy all the infrastructure
$ ./adobe.py down

# Run only ansible part for configuration management (Runs play.yml)
$ ./adobe.py config

# Print public/accessible URLs after a successful deployment
$ ./adobe.py print urls

# Print Jenkins server IP Addresses
$ ./adobe.py print servers

# Scaling EC2 instances on demand
# ScaleUp
$ ./adobe.py jenkins scaleup [count]
# ScaleDown
$ ./adobe.py jenkins scaledown [count]

# Only after running "up" command successfully
# Enable Maintenance mode on webserver
$ ./adobe.py wserver start503

# Disable Maintenance mode on webserver
$ ./adobe.py wserver stop503
```
