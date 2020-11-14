#!/bin/bash

/code/shell/chown.sh `id -u` `id -g` /code mypasswd

if [ $? -ne 0 ]; then
  return -1
fi

flask run --host=0.0.0.0 --port 8080
