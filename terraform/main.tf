# Specify the provider and access details
provider "aws" {
  region = "${var.aws_region}"
}

# Create a VPC to launch our instances into
resource "aws_vpc" "default" {
  cidr_block = "10.0.0.0/16"
}

# Create an internet gateway to give our subnet access to the outside world
resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.default.id}"
}

# Grant the VPC internet access on its main route table
resource "aws_route" "internet_access" {
  route_table_id         = "${aws_vpc.default.main_route_table_id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.default.id}"
}

# Create a subnet to launch our jenkins master instances into
resource "aws_subnet" "jmaster" {
  vpc_id                  = "${aws_vpc.default.id}"
  availability_zone       = "${var.azs["master"]}"
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

# Create a subnet to launch our jenkins slave instances into
resource "aws_subnet" "jslave" {
  vpc_id                  = "${aws_vpc.default.id}"
  availability_zone       = "${var.azs["slave"]}"
  cidr_block              = "10.0.2.0/24"
}

# Create a subnet to launch our webserver instances into
resource "aws_subnet" "wserver" {
  vpc_id                  = "${aws_vpc.default.id}"
  cidr_block              = "10.0.10.0/24"
  map_public_ip_on_launch = true
}

# Our default security group to access
# the instances over SSH and HTTP
resource "aws_security_group" "default" {
  name        = "${var.clustername}-sg"
  description = "Used in the terraform"
  vpc_id      = "${aws_vpc.default.id}"

  # SSH access from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP access from the VPC
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # outbound internet access
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "jmaster" {
  count = "${var.jmaster_count}"
  instance_type = "${var.instance_type}"
  availability_zone = "${var.azs["master"]}"

  # Lookup the correct AMI based on the region
  ami = "${lookup(var.aws_amis, var.aws_region)}"

  # The name of our SSH keypair that you want to use.
  key_name = "${var.key_name}"

  # Our Security group to allow HTTP and SSH access
  vpc_security_group_ids = ["${aws_security_group.default.id}"]

  # Subnet ID
  subnet_id = "${aws_subnet.jmaster.id}"

  tags {
    Name = "${var.clustername}-jmaster-${count.index + 1}"
    CreatedBy = "Terraform"
    ClusterName = "${var.clustername}"
    sshUser = "${var.ssh_user}"
  }
}

resource "aws_instance" "jslave" {
  count = "${var.jslave_count}"
  instance_type = "${var.instance_type}"
  availability_zone = "${var.azs["slave"]}"

  # Lookup the correct AMI based on the region
  ami = "${lookup(var.aws_amis, var.aws_region)}"

  # The name of our SSH keypair that you want to use.
  key_name = "${var.key_name}"

  # Our Security group to allow HTTP and SSH access
  vpc_security_group_ids = ["${aws_security_group.default.id}"]

  # Subnet ID
  subnet_id = "${aws_subnet.jslave.id}"

  tags {
    Name = "${var.clustername}-jslave-${count.index + 1}"
    CreatedBy = "Terraform"
    ClusterName = "${var.clustername}"
    sshUser = "${var.ssh_user}"
  }
}

resource "aws_instance" "wserver" {
  count = "${var.wserver_count}"
  instance_type = "${var.instance_type}"

  # Lookup the correct AMI based on the region
  ami = "${lookup(var.aws_amis, var.aws_region)}"

  # The name of our SSH keypair that you want to use.
  key_name = "${var.key_name}"

  # Our Security group to allow HTTP and SSH access
  vpc_security_group_ids = ["${aws_security_group.default.id}"]

  # Subnet ID
  subnet_id = "${aws_subnet.wserver.id}"

  tags {
    Name = "${var.clustername}-wserver-${count.index + 1}"
    CreatedBy = "Terraform"
    ClusterName = "${var.clustername}"
    sshUser = "${var.ssh_user}"
  }
}
