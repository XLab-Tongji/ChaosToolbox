FROM ansible/ansible:ubuntu1604


RUN sudo apt-get update \
    && apt-get install -y --no-install-recommends --fix-missing tcl tk expect \
    && git clone https://github.com/baiyanquan/2019-XLab-KubernetesTools.git ~/Ansible_Operator \
    && chmod 777 ~/Ansible_Operator/auto_ssh.sh \
    && rm /etc/ansible/hosts \
    && cp ~/Ansible_Operator/hosts /etc/ansible/ \
    && pip install --upgrade pip \
    && pip2 install ansible==2.7.10 \
    && pip2 install flask \
    && pip2 install flask_httpauth \
    && pip2 install requests \
    && pip2 install apscheduler \
    && pip2 install pika \
    && pip2 install influxdb \
    && git -C /root/Ansible_Operator pull \
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root tongji409 10.60.38.181 2331\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root tongji409 192.168.199.31 22\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root tongji409 192.168.199.41 22\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root tongji409 192.168.199.32 22\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root tongji409 192.168.199.42 22\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root tongji409 192.168.199.33 22\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root tongji409 192.168.199.43 22\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root tongji409 192.168.199.34 22\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root tongji409 192.168.199.44 22\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root tongji409 192.168.199.35 22\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root tongji409 192.168.199.45 22\
    && chmod 777 ~/Ansible_Operator/run.sh


CMD ["sh", "/root/Ansible_Operator/run.sh"]
