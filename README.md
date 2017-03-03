# auto-jenkins
Simple automation code to deploy a web application on AWS infrastructure

This application deploys the below infrastructure (using Terraform):
 - 1 VPC
 - 1 Subnet
 - 1 Security Group
 - 1 Gateway
 - 1 EC2 Instance

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
# Deploy infrastructure, configure and deploy WebApp
$ ./adobe.py up

# Destroy all the infrastructure
$ ./adobe.py down

# Run only ansible part for configuration management (Runs play.yml)
$ ./adobe.py config

# Only after running "up" command successfully
# Enable Maintenance mode
$ ./adobe.py start503

# Disable Maintenance mode
$ ./adobe.py stop503
```
