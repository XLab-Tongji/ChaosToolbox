import json
import shutil
from ansible.module_utils.common.collections import ImmutableDict  #用于添加选项。比如: 指定远程用户remote_user=None
from ansible.parsing.dataloader import DataLoader                  #读取 json/ymal/ini 格式的文件的数据解析器
from ansible.vars.manager import VariableManager                   #管理主机和主机组的变量管理器
from ansible.inventory.manager import InventoryManager             #管理资源库的，可以指定一个 inventory 文件等
from ansible.playbook.play import Play                             #用于执行 Ad-hoc 的类 ,需要传入相应的参数
from ansible.executor.task_queue_manager import TaskQueueManager   #ansible 底层用到的任务队列管理器
from ansible.plugins.callback import CallbackBase                  #处理任务执行后返回的状态,用于处理执行结果的。 后面我们可以继承改写这个类用作回调插件，以便满足我们的需求。
from ansible import context                                        #上下文管理器，他就是用来接收 ImmutableDict 的示例对象
import ansible.constants as C                                      #用于获取 ansible 产生的临时文档
from ansible.executor.playbook_executor import PlaybookExecutor  # 执行 playbook 的核心类
from ansible.inventory.host import Group                           #对 主机组 执行操作 ，可以给组添加变量等操作，扩展
from ansible.inventory.host import Host                            #对 主机 执行操作 ，可以给主机添加变量等操作，扩展


import time
import datetime

class ResultCallback(CallbackBase):
    """
    重写callbackBase类的部分方法,可以获得执行后返回的结果和状态
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #参考的博客中原本定义的，信息不准确,{ip:result}
        #以ip为key，result信息为value，存进字典中，但如果执行了多个任务只能收集到最后执行的任务的结果，之前的执行信息会被覆盖,所以后面我改了下收集信息的方式
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

        #重新定义的收集结果信息的方法，可以收集到所有的执行信息，按执行的顺序放入列表，但缺点是没有按ip来进行分类
        self.host_all_info=[]   #存放所有的执行结果信息的列表[{reslut1},{reslut2}]
        self.host_failed_iplist=[]
        self.host_unreachabled_iplist=[]

    #机器不可达的时候,result参数里是执行的结果信息等
    def v2_runner_on_unreachable(self, result):
        #以ip为key，result信息为value，存进字典中，但如果执行了多个任务只能收集到最后执行的任务的结果，所以后面我改了下收集信息的方式
        self.host_unreachable[result._host.get_name()] = result

        exec_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  #执行时间
        host_ip=result._host.get_name()    #主机ip
        task_name=result.task_name         #任务名称
        result_info=result._result         #执行的结果信息

        #获取任务执行的相关信息，放入字典
        result_dict={"exec_time":exec_time,"host_ip":host_ip,"task_name":task_name,"status":"unreachable","result_info":result_info}
        #print(result_dict)
        #然后再讲字典放入存放全部信息的列表中
        self.host_all_info.append(result_dict)

    #任务成功的时候回调函数
    #在ad-hoc下每个ip成功，都会执行这个函数，而在playbook状态下，每个action都会执行这个函数，例如，全部ip第一个action执行完才会继续执行下一个action
    def v2_runner_on_ok(self, result, **kwargs):
        # 以ip为key，result信息为value，存进字典中，但如果执行了多个任务只能收集到最后执行的任务的结果，所以后面我改了下收集信息的方式
        self.host_ok[result._host.get_name()] = result


        exec_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        host_ip=result._host.get_name()
        task_name=result.task_name
        result_info=result._result
        # 获取任务执行的相关信息，放入字典
        result_dict={"exec_time":exec_time,"host_ip":host_ip,"task_name":task_name,"status":"success","result_info":result_info}
        #print(result_dict)
        # 然后再讲字典放入存放全部信息的列表中
        self.host_all_info.append(result_dict)


    #任务执行失败时的回调函数
    def v2_runner_on_failed(self, result, ignore_errors=False,**kwargs):

        self.host_failed[result._host.get_name()] = result

        exec_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        host_ip=result._host.get_name()
        task_name=result.task_name
        result_info=result._result
        result_dict={"exec_time":exec_time,"host_ip":host_ip,"task_name":task_name,"status":"failed","result_info":result_info}
        #print(result_dict)
        self.host_all_info.append(result_dict)


        # print("failed:",end="")
        # print(result._host.get_name(),end=" ")
        # print(result.task_name,end=" ")
        # print(result._result)

    #任务被skip时的回调函数
    def v2_runner_on_skipped(self, result,**kwargs):
        exec_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        host_ip=result._host.get_name()
        task_name=result.task_name
        result_info=result._result
        result_dict={"exec_time":exec_time,"host_ip":host_ip,"task_name":task_name,"status":"skip","result_info":result_info}
        #print(result_dict)
        self.host_all_info.append(result_dict)

    #task中每个action都会执行这个函数，可以用task.name获取action的名称,只执行一次
    def v2_playbook_on_task_start(self, task, is_conditional):
        pass
        #print(task.name)
        #print(task._uuid)

    def v2_playbook_on_play_start(self, play):
        pass
        #print(play.name)

    #获取playbook执行的状态，在playbook执行完后执行该函数，可以获取该playbook中执行的主机，以及每个主机执行该playbook中action成功失败的个数
    def v2_playbook_on_stats(self, stats):
        #print(stats.processed)   #{'10.104.114.197': 1, '10.104.113.129': 1, '10.104.113.130': 1}
        #print(stats.processed.keys())             #dict_keys(['10.104.114.197', '10.104.113.129', '10.104.113.130'])
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)                #{'ok': 1, 'failures': 0, 'unreachable': 0, 'changed': 0, 'skipped': 0, 'rescued': 0, 'ignored': 0}
            if t["failures"]!=int(0):
                self.host_failed_iplist.append(h)
            if t["unreachable"]!=int(0):
                self.host_unreachabled_iplist.append(h)
            #print(t)

    # task中每个action都会执行这个函数，可以用task.name获取action的名称，每个ip都执行一次
    def v2_runner_on_start(self, host, task):
        pass
        #print(task.name)


    # def v2_playbook_on_stats(self, stats):
    #     print(stats.processed.keys())
    #     print(stats.processed)
    #     print(sorted(stats.processed.keys()))
    #     print(stats.summarize(sorted(stats.processed.keys())[0]))

    # def v2_playbook_on_play_start(self, play):
    #     print(play.name)


class MyAnsiable():

    #自定义类的一些初始化信息,在下面的context.CLIARGS初始化函数中使用这些初始化属性
    # 在初始化的这个类时候可以传参，以便覆盖默认选项的值,我们可以自己传参数，否则使用定义的默认值
    def __init__(self,
                 connection='ssh',  # 连接方式 local 本地方式，smart ssh方式
                 remote_user="None",  # 远程用户
                 ack_pass=None,  # 提示输入密码
                 sudo=None, sudo_user=None, ask_sudo_pass=None,
                 module_path=None,  # 模块路径，可以指定一个自定义模块的路径
                 become=None,  # 是否提权
                 become_method=None,  # 提权方式 默认 sudo 可以是 su
                 become_user=None,  # 提权后，要成为的用户，并非登录用户
                 check=False, diff=False,
                 listhosts=None, listtasks=None, listtags=None,
                 forks=5,      #同时执行的主机数量
                 tags=[],      #执行的tags列表
                 skip_tags=[], #skip跳过的tags列表
                 verbosity=3,
                 syntax=None,
                 start_at_task=None,
                 inventory=None,
                 passwords=None):


        #上下文管理器，用来接收 ImmutableDict 的示例对象,ImmutableDict用于添加选项
        #2.7 和 2.8 版本有一些差异： 2.7 使用了 Python 标准库里的 命名元组来初始化选项，而 2.8 是 Ansible 自己封装了一个 ImmutableDict,要和 context 结合使用的
        context.CLIARGS = ImmutableDict(
            connection=connection,
            remote_user=remote_user,
            ack_pass=ack_pass,
            sudo=sudo,
            sudo_user=sudo_user,
            ask_sudo_pass=ask_sudo_pass,
            module_path=module_path,
            become=become,
            become_method=become_method,
            become_user=become_user,
            verbosity=verbosity,
            listhosts=listhosts,
            listtasks=listtasks,
            listtags=listtags,
            forks=forks,
            tags=tags,
            skip_tags=skip_tags,
            syntax=syntax,
            start_at_task=start_at_task,
        )

        # 三元表达式，假如没有传递 inventory文件, 就使用 "localhost,"
        # 这里需要注意如果不使用host文件，即inventory未传入，直接动态传入host列表的情况，这里会将localhost加入主机中，所以执行all主机组也会执行本机，所以要么改为未传入就为“”，要么就设置其他的主机组名称，不使用all执行全部
        # inventory 就是平时用到的存放主机ip以及变量的资源库文件，-i 参数后面跟的文件
        self.inventory = inventory if inventory else "localhost,"

        # 实例化数据解析器,用于解析 存放主机列表的资源库文件 （比如： /etc/ansible/hosts） 中的数据和变量数据的
        self.loader = DataLoader()

        # 实例化 资产配置对象,InventoryManager管理资源库，可以指定一个loader数据解析器和一个inventory文件
        self.inv_obj = InventoryManager(loader=self.loader, sources=self.inventory)

        # 设置密码，可以为空字典，但必须有此参数
        self.passwords = {"conn_pass":passwords}

        # 实例化回调插件对象
        self.results_callback = ResultCallback()

        # 变量管理器,假如有变量，所有的变量应该交给他管理。 这里他会从 inventory 对象中获取到所有已定义好的变量。 这里也需要数据解析器。
        self.variable_manager = VariableManager(self.loader, self.inv_obj)


    #用来执行 Ad-hoc 的方法
    def run(self, hosts='all', gether_facts="no", module="ping", args=''):

        #定义一个字典，来设置主机组、是否获取机器信息、以及执行的模块及参数,
        #参数可以在执行run()函数的时候传入
        play_source = dict(
            name="Ad-hoc",
            hosts=hosts,
            gather_facts=gether_facts,
            tasks=[
                # 这里每个 task 就是这个列表中的一个元素，格式是嵌套的字典
                # 也可以作为参数传递过来，这里就简单化了。
                {"action": {"module": module, "args": args}},
            ])

        #Play()是用于执行 Ad-hoc 的类 ,这里传入一个上面的play_source字典参数 VariableManager变量管理器  DataLoader数据解析器
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        # 先定义一个值，防止代码出错后，   `finally` 语句中的 `tqm` 未定义。
        tqm = None
        try:
            #TaskQueueManager是底层用到的任务队列管理器
            #要想执行 Ad-hoc ，需要把上面的 play 对象交给任务队列管理器的 run 方法去运行
            tqm = TaskQueueManager(
                inventory=self.inv_obj,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
                stdout_callback=self.results_callback)

            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    #用来执行 playbook 的方法
    def playbook(self, playbooks,extra_vars={}):

        #自定义变量是用一个字典保存的
        #使用变量管理器VariableManager().extra_vars.update(extra_vars_dict)的方法进行添加
        self.variable_manager.extra_vars.update(extra_vars)

        #PlaybookExecutor是执行playbook 的核心类,这里实例化一个PlaybookExecutor对象
        playbook = PlaybookExecutor(playbooks=playbooks,  #playbook yaml文件列表,注意这里是一个列表
                                    inventory=self.inv_obj,  # InventoryManager资产配置对象
                                    variable_manager=self.variable_manager,  #VariableManager变量管理器
                                    loader=self.loader,     #DataLoader数据解析器
                                    passwords=self.passwords)   #密码

        # 使用回调函数
        playbook._tqm._stdout_callback = self.results_callback

        #执行PlaybookExecutor类的run方法
        result = playbook.run()

    #这个获取执行状态和信息的函数是不准确的，如果一个playbook中有多个action，
    #用ip做key，key值是唯一的，但value可以改变，获取到的信息只能是最后一个，所以不准确
    def get_result(self):
        result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}

        # print(self.results_callback.host_ok)
        for host, result in self.results_callback.host_ok.items():
            result_raw['success'][host] = result._result
        for host, result in self.results_callback.host_failed.items():
            result_raw['failed'][host] = result._result
        for host, result in self.results_callback.host_unreachable.items():
            result_raw['unreachable'][host] = result._result
        return result_raw

        # 最终打印结果，并且使用 JSON 继续格式化
        #print(json.dumps(result_raw, indent=4))


    #动态添加主机，传入主机列表和组名
    def add_dynamic_hosts(self, hostip_list, groupname=None, groupvars=None):
        """
            add hosts to a group
        """
        #如果有传入组名，则添加组，并创建Group实例
        if groupname:
            self.inv_obj.add_group(groupname)
            my_group = Group(name=groupname)
        #如果有传入组变量，则将组变量设置给上面创建的Group实例
        if groupvars:
            for key, value in groupvars.iteritems():
                my_group.set_variable(key, value)

        # add hosts to group
        # 如果有传入组名，则遍历主机列表，添加主机并且设置组
        if groupname:
            for hostip in hostip_list:
                self.inv_obj.add_host(host=hostip,group=groupname)
        #如果没有传入组名，则遍历主机列表，只添加主机
        else:
            for hostip in hostip_list:
                self.inv_obj.add_host(host=hostip)

if __name__ == '__main__':
        #实例化
    ansible1 = MyAnsiable(inventory='/code/chaostoolbox/hosts', remote_user="root",connection='ssh',forks=1,passwords=None)
    #执行 ad-hoc
    print("执行ad-hoc的结果")
    ansible1.run(hosts= "remote", module="shell", args='pwd')
    #打印结果
    print(ansible1.get_result())
    print(ansible1.results_callback.host_all_info)
