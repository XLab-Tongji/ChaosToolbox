#!/bin/bash

/code/shell/chown.sh `id -u` `id -g` /code mypasswd
if [ $? -ne 0 ]; then
  echo "failed to chown /code"
  exit -1
fi

/code/shell/chown.sh `id -u` `id -g` /home/code mypasswd
if [ $? -ne 0 ]; then
  echo "failed to chown /home/code"
  exit -1
fi

chmod 600 /home/code/.ssh/id_rsa
if [ $? -ne 0 ]; then
  ehco "failed to chmod 600 /home/code/.ssh/id_rsa"
  exit -1
fi

chmod 644 /home/code/.ssh/id_rsa.pub
if [ $? -ne 0 ]; then
  echo "failed to chmod 644 /home/code/.ssh/id_rsa.pub"
  exit -1
fi

chmod 700 /home/code/.ssh
if [ $? -ne 0 ]; then
  echo "failed to chmod 700 /home/code/.ssh"
  exit -1
fi

/code/shell/useradd.sh `id -u` `id -g` code mypasswd
if [ $? -ne 0 ]; then
  echo "failed to useradd code"
  exit -1
fi

flask run --host=0.0.0.0 --port 8080
