FROM python:3.8

RUN rm /etc/apt/sources.list
RUN echo "deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse" \
	 "deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse" \
	 "deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse" \
	 "deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse" \
 	> /etc/apt/sources.list
     
RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 40976EAF437D05B5
RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 3B4FE6ACC0B21F32
RUN apt-get update 

RUN apt upgrade -y
# RUN apt install apt-transport-https ca-certificates -y --allow-remove-essential
RUN apt-get install  --no-install-recommends --fix-missing tcl tk expect -y
RUN apt-get install git
RUN git config --global http.postBuffer 20000000
RUN git clone --depth=1 https://github.com/XLab-Tongji/ChaosToolbox.git ~/ChaosToolbox
RUN cd /root/ChaosToolbox
RUN pip3 install --upgrade pip
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install ansible
RUN pip3 install flask

