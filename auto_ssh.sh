#!/usr/bin/expect
set timeout 10
set username [lindex $argv 0]
set password [lindex $argv 1]
set hostname [lindex $argv 2]
set port [lindex $argv 3]
spawn ssh-copy-id -i /root/.ssh/id_rsa.pub -p $port $username@$hostname
expect {
    #first connect, no public key in ~/.ssh/known_hosts
    "Are you sure you want to continue connecting (yes/no)?" {
        send "yes\r"
        expect "root@10.60.38.181\'s password:"
        send "$password\r"
        }
    #already has public key in ~/.ssh/known_hosts
    "root@10.60.38.181\'s password:" {
        send "$password\r"
        }
    "Now try logging into the machine" {
        #it has authorized, do nothing!
        }
    }
expect eof
