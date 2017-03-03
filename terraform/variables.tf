variable "aws_region" {
  description = "AWS region to launch servers."
  default     = "us-west-2"
}

variable "azs" {
  description = "Run the EC2 Instances in these Availability Zones"
  default = {
    master = "us-west-2a"
    slave = "us-west-2b"
    }
}

# Ubuntu Precise 12.04 LTS (x64)
variable "aws_amis" {
  default = {
    eu-west-1 = "ami-b1cf19c6"
    us-east-1 = "ami-de7ab6b6"
    us-west-1 = "ami-3f75767a"

    us-west-2 = "ami-d2c924b2"
  }
}

variable "clustername" {}
variable "jmaster_count" {}
variable "jslave_count" {}
variable "wserver_count" {}
variable "instance_type" {}

variable "key_name" {
  default = "demokp"
}

variable "ssh_user" {}
