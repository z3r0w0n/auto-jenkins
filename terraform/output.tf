output "master_ip" {
    value = ["${join(",", aws_instance.jmaster.*.public_ip)}"]
}

output "slave_ip" {
    value = ["${join(",", aws_instance.jslave.*.public_ip)}"]
}

output "wserver_ip" {
    value = ["${join(",", aws_instance.wserver.*.public_ip)}"]
}
