#!/bin/bash

<<<<<<< HEAD:entrypoint.sh
/code/chown.sh `id -u` `id -g` /code mypasswd
if [ $? -ne 0 ]; then
  echo "failed to chown /code"
  return -1
fi

/code/chown.sh `id -u` `id -g` /home/code mypasswd
if [ $? -ne 0 ]; then
  echo "failed to chown /home/code"
  return -1
fi

chmod 600 /home/code/.ssh/id_rsa
if [ $? -ne 0 ]; then
  ehco "failed to chmod 600 /home/code/.ssh/id_rsa"
  return -1
fi

chmod 644 /home/code/.ssh/id_rsa.pub
if [ $? -ne 0 ]; then
  echo "failed to chmod 644 /home/code/.ssh/id_rsa.pub"
  return -1
fi

chmod 700 /home/code/.ssh
if [ $? -ne 0 ]; then
  echo "failed to chmod 700 /home/code/.ssh"
  return -1
fi
=======
/code/shell/chown.sh `id -u` `id -g` /code mypasswd
>>>>>>> cfa095d1b3c2c1b01fec1d420a3833dfaf0dbea5:shell/entrypoint.sh

/code/useradd.sh `id -u` `id -g` code mypasswd
if [ $? -ne 0 ]; then
  echo "failed to useradd code"
  return -1
fi

flask run --host=0.0.0.0 --port 8080
