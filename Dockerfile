FROM ansible/ansible:ubuntu1604


RUN sudo apt-get update \
    && apt-get install -y --no-install-recommends --fix-missing tcl tk expect \
    && git clone -b ansible_operator_hm https://github.com/XLab-Tongji/Ansible_Operator.git ~/Ansible_Operator \
    && chmod 777 ~/Ansible_Operator/auto_ssh.sh \
    && rm /etc/ansible/hosts \
    && cp ~/Ansible_Operator/hosts /etc/ansible/ \
    && pip install --upgrade pip \
    && pip2 install ansible==2.7.10 \
    && pip2 install flask \
    && pip2 install flask_httpauth \
    && pip2 install requests \
    && git -C /root/Ansible_Operator pull \
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root 123456 10.60.38.181 2331\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root 123456 192.168.199.31\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root 123456 192.168.199.41\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root 123456 192.168.199.32\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root 123456 192.168.199.42\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root 123456 192.168.199.33\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root 123456 192.168.199.43\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root 123456 192.168.199.34\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root 123456 192.168.199.44\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root 123456 192.168.199.35\
    && /usr/bin/expect /root/Ansible_Operator/auto_ssh.sh root 123456 192.168.199.45\
    && chmod 777 ~/Ansible_Operator/run.sh


CMD ["sh", "/root/Ansible_Operator/run.sh"]





