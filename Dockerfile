FROM python/python:3.8


RUN sudo apt-get update 
RUN rm /etc/apt/sources.list
RUN echo "deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse" \
	 "deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse" \
	 "deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse" \
	 "deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse" \
 	> /etc/apt/sources.list

RUN sudo apt-get update
RUN sudo apt upgrade -y
RUN sudo apt install apt-transport-https ca-certificates -y
RUN apt-get install -y --no-install-recommends --fix-missing tcl tk expect 
RUN git clone https://github.com/XLab-Tongji/ChaosToolbox.git ~/ChaosToolbox
RUN git checkout lxd

