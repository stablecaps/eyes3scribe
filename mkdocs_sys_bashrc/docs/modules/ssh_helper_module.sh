cite about-module
about-module 'Install additional packages'

function sshub() {
    about 'Signs into AWS EC2 instance using pattern ubuntu@${address}'
    group 'ssh'
    param 'Ip address or FQDN'
    example 'sshub 172.17.0.1'

    HOST_ADDR="$1"
    ssh -A ubuntu@${HOST_ADDR}
}

function sshec2() {
    about 'Signs into AWS EC2 instance using pattern ec2-user@${address}'
    group 'ssh'
    param 'Ip address or FQDN'
    example 'sshec2 172.17.0.1'

    HOST_ADDR="$1"
    ssh -A ec2-user@${HOST_ADDR}
}

function sshbast() {
    about 'ssh via jump host. You need to have added your .pem key via ssh-add -k. Edit this function ($USERNAME) to have the machine you want to jump to'
    group 'ssh'
    param 'Ip address or FQDN'
    example 'sshbast ${MachineYouWantToJumpTo}'
    example 'sshbast 185.22.33.68'

    HOST_ADDR="$1"
    ssh -A -J USERNAME@bastion.com ubuntu@${HOST_ADDR}
}

function qssh() {
    about 'Quick ssh using faster, less secure ssh ciphers'
    group 'ssh'
    param '$username@$yourhost.com'
    example 'qssh $username@$yourhost.com'
    example 'qssh johng@185.22.33.68'

    USER_HOST_VAR="$1"

    ssh -Y -C -c blowfish-cbc,arcfour $USER_HOST_VAR
}
