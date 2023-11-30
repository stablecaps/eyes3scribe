#!/bin/bash
#
# -binaryanomaly

cite about-alias
about-alias 'Apt & dpkg aliases for Ubuntu and Debian distros.'

alias apts='apt-cache search'
alias aptshow='apt-cache show'
alias aptinst='sudo apt-get install -V'
alias aptupd='sudo apt-get update'
alias aptupg='sudo apt-get dist-upgrade -V && sudo apt-get autoremove'
alias aptupgd='sudo apt-get update && sudo apt-get dist-upgrade -V && sudo apt-get autoremove'
alias aptrm='sudo apt-get remove'
alias aptpurge='sudo apt-get remove --purge'

alias chkup='/usr/lib/update-notifier/apt-check -p --human-readable'
alias chkboot='cat /var/run/reboot-required'

alias pkgfiles='dpkg --listfiles'


function ubupdate() {
    about 'Ubdate & upgrade ubuntu via apt. Then run apt auto-remove'
	group 'base'
    example 'ubupdate'

    sudo apt update
    sudo apt upgrade -y
    sudo apt auto-remove
}
