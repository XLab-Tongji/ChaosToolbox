Kubernetes是什么？

Kubernetes是一个全新的基于容器技术的分布式架构领先方案。

Kubernetes是一个开放的开发平台。

Kubernetes是一个完备的分布式系统支撑平台。



Service（服务）：分布式集群架构的核心

Service对象拥有如下关键特征：

- 一个唯一指定的名字（比如mysql-server）
- 一个虚拟IP（Cluster IP、Service IP 或VIP）和端口号
- 能够提供某种远程服务的功能
- 被映射到了提供这种服务能力的一组容器应用上



Kubernetes能够让我们通过Service（虚拟Cluster IP + Service Port）连接到指定的Service上。

Service一旦创建就不会变化。



Pod对象，把为Service提供服务的进程放入容器中进行隔离：将每个服务进程包装到相应的Pod中，使其成为Pod中运行的一个容器（Container）

- Pod运行在节点中
- 每个Pod里运行着一个特殊的Pause容器
- 还有其他业务容器（共享Pause容器的网络栈和Volume挂载卷）
- 只有提供服务的一组Pod才会被映射成一个服务



Kubernetes将集群中的机器划分为：

- 一个Master节点
- 一群工作节点（Node）



在一个RC（Replication Controller）定义文件中包括以下3个关键信息：

- 目标Pod的定义
- 目标Pod需要运行的副本数量
- 要监控的目标Pod的标签（Label）



Master：集群控制点 

- 每个Kubernetes集群里需要一个Master节点来负责整个集群的管理和控制 
  
- Master节点通常会占据一个独立的X86服务器（或一个虚拟机） 
  
- Master节点上运行着以下一组关键进程： 
  
- - Kubernetes API Server(kube-apiserver) 
    
  - Kubernetes Controller Manager(kube-controller-manager) 
    
  - Kubernetes Scheduler(kube-scheduler) 
    
  - etcd Server进程 
    

Node: 

- Node节点是Kubernetes集群中的工作负载节点 
  
- 每个Node节点上都运行着以下一组关键进程： 
  
- - kubelet 
    
  - kube-proxy 
    
  - Docker Engine(docker) 
    

- node(not Ready)：某个Node超贵欧指定时间不上报信息，被Master判定为“失联”，之后，Master会吹法“工作负载大转移”的自动流程 
  
- - kubectl get nodes 
    
  - kubeectl describe node kuberneetes-minion1 
    

Pod: 

- 每个Pod都分配了唯一的IP地址（PodIP） 
  
- 一个Pod里多个容器共享PodIP地址 
  
- 虚拟二层网络技术 
  
- - 底层网络支持集群内任意两个Pod之间的TCP/IP直接通信（Flannel、Openvswitch） 
    

- 两种类型： 
  
- - 普通Pod 
    
  - 静态Pod 
    

- Pod的IP加上容器端口（contrinerPort），就组成了一个新的概念——Endpoint 
  
- - EndPoint代表此Pod里的一个服务进程的对外通信地址（Pod IP+ContainerPort) 
    

- Pod Volume 
  

Event: 

- 是一个事件的记录，记录时间的最早产生时间，最后重现时间等（是排查故障的重要参考信息） 
  



Kubernetes资源配额： 

- 以千分之一的CPU配额为最小单位 
  
- 进行配额限定需要设定的两个参数： 
  
- - Requests：该资源的最小申请量，系统必须满足要求 
    
  - Limits：资源最大允许使用的量，不能被突破，当容器试图使用超过这个量的资源，会被Kill重启 
    



Label（标签）： 

- 一个value：一个key=value的键值对 
  
- 一个资源对象定义任意数量的Label 
  
- 例： 
  
- - name=redis-slave：匹配所有具有该标签的资源对象 
    

- Label Selector 
  



RC（Replication Controller） 

-  Pod期待的副本数（replicas） 
  
- 用于筛选目标Pod的Label Selector 
  
- 当Pod的副本数量小于于预期数量的时候，用于创建新Pod的Pod模板（template） 
  
- Pod的动态缩放： 
  
- - kubectl scale rc redis-slave —replicas=3：即通过RC的副本数量实现Pod的扩容或缩容 
    
  - 滚动升级（保持RC的数量，以旧换新） 
    

- ReplicaSet： 
  
- - 下一代的RC 



Deployment：

- 目的：

- - 解决Pod的编排问题

- 场景：

- - 生成对应Replica Set并完成Pod副本的创建

- - 检查Deployment状态来看部署侗族欧是否完成

- - 更新D以创建新的Pod

- - 回滚
  - 挂起或恢复

Horizontal Pod Autoscaler(HPA)

- 意为Pod的横向自动扩容

- 两种作为Pod负载度量单位的方式：

- - CPUUtilizationPercentage

  - - 目标Pod所有副本自身的CPU利用率的平均值

  - 应用程序自定义的度量指标，比如服务在每秒内的相应的请求数（TPS或QPS）

- kubectl autoscale deployment php-apache —cpu-percent=90 —min=1 —max=10



Service(服务） 

- Kubernetes里的每个Service就是微服务欧架构中的一个“微服务” 

- Service定义了一个服务的访问入口地址 
- frontend pod通过Service入口地址访问被背后一组Pod副本组成的集群 
- Service与Pod通过Label Selector实现“无缝对接” 
- RC保证Service的服务能力和服务质量始终处于预期的标准 

- 微服务单元通过TCP/IP进行通信

- 负载均衡器

- - 为一组Pod提供一个对外的服务端口如8000端口
  - 运行在每个Node上的kube-proxy进程就是一个智能软件负载均衡器

- 每个Service分配一个全剧唯一的虚拟IP地址Cluster IP，在Service的整个生命周期不改变

- - kubectl get svc tomcat-service -o yaml

  - - targetPort（默认与port相同）

- Service的Name和Service的Cluster IP地址做一个DNS域名映射

- Kubernetes服务发现机制在:

- - 每个Kubernetes中的Service都有一个唯一的Cluster IP以及唯一的名字
  - Kubernetes通过Add-On增值包的方式引入了DNS系统，把服务名作为DNS域名

- 外部系统访问Service问题

- - Kubernetes的三种IP：

  - - Node IP

    - - 是Kubernetes集群中每个节点的物理网卡的IP地址，这是一个真实存在的物理网络，所有术语这个网络的服务器之间都能通过这个网络直接通信
      - Kubernetes里的一个Pod里的容器访问另一个Pod里的容器，就是通过Pod IP所在的虚拟二层网络进行通信
      - 真实的TCP/IP流量是通过Node IP所在的物理网卡流出

    - Pod IP

    - Cluster IP

    - - 虚拟的IP，无法被ping
      - Kubernetes集群内部的地址，无法在集群外部直接使用这个地址
      - 使用NodePort

    - 负载均衡问题

    - - 外部请求只需访问负载均衡器的IP地址，由其负责转发流量到后面某个Node的NodePort上

Volume（存储卷）

- Volume是Pod中能够被多个容器访问的共享目录

- - Kubernetes支持多种类型的Volume，例如ClusterFS、Ceph等先进的额分布式文件系统

- 使用：

- - 先在Pod上声明一个Volume
  - 在容器中引用该Volumn并Mount到容器里的某个目录上

- 多种Volume类型：

- - emptyDir
  - hostPath
  - gcePersistentDisk
  - awsElasticBlockStore
  - NFS
  - 。。。

- Persistent Volume

- - 在使用虚机的情况下，定义一个网络存储，然后从中划出一个“网盘”并挂接到虚拟机上

  - PV是有状态的对象，它有以下几种状态：

  - - Available：空闲状态
    - Bound：已经绑定到某个PVC上
    - Released：对应的PVC已经删除，但资源还没有被集群收回
    - Failed：PV自动回收失败



Namespace（命名空间）

- 用于实现多租户的资源隔离
- Namespace通过将集群内部的资源对象“分配”到不同的Namespac中，形成逻辑上分组的不同项目，小组或用户组
- 如果不加参数，则kubectl get命令将仅显示属于“default”命名空间的资源对象



Annotation（注解）

- 用户任意定义的“附加”信息