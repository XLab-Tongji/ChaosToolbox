容器云：容器云以容器为资源分割和调度的基本单位，封装整个软件运行时环境，为开发者和系统管理员提供用于构建，发布和运行分布式应用的平台。

Docker是以Docker容器为资源分割和调度的基本单位，封装整个软件运行时环境，为开发者和系统管理员设计的，用于构建，发布和运行分布式应用的平台。



-i：选项表示使用交互模式，始终保持输入流开放

-t：选项表示分配一个伪终端，一般两个参数结合时使用-it，即可在容器中利用打开的伪终端进行交互操作



docker start

docker stop

docker restart



docker registry：存锤容器镜像的额仓库；用户可以通过docker client与docker registry进行通信



docker pull

docker push

docker images

docker ps -a

docker rm 

docker rmi



\#容器运维操作

docker attach [OPTIONS] CONTAINER： 连接到正在运行的容器，观察该容器的运行情况，或与容器的主进程进行交互



docker inspect [OPTIONS] CONTAINER | IMAGE [CONTAINER | IMAGE .. ]

该命令可以查看镜像和容器的详细信息，默认会列出全部信息，可以通过—format参数来指定输出的的模板格式，以便输出特定信息



sudo docker inspect --format='{{.NetworkSettings.IPAddress}}’ mydb2

172.17.0.2



docker ps -a

docker ps -l

docker events

docker history IMAGE

docker logs CONTAINER



\#建立容器间的互联关系： 

docker run —link选项能够进行容器间安全的交互通信，使用格式为name:alias(别名) 

示例： 

sudo docker run —link redis:redis —name console ubuntu bash 



可以将--link设置理解为一条IP地址的单向记录信息，硬刺在搭建容器应用栈时，需要注意各个容器节点的启动顺序，以及对应的--link参数设置。 

应用栈各节点的连接信息如下： 

- 启动redis-master容器节点 
   
- 两个redis-slave容器接待你启动时要连接在redis-master上 
   
- 两个APP容器节点启动时要连接到redia-master上 
   
- HAProxy容器启动启动时要链接到两个APP节点上 
   



容器启动顺序： 

redis-master——redis-slave——APP——HAProxy 