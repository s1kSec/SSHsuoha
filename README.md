# BatchSSH（线程一对一）

免责声明：

一. 此软件仅供学习使用，使用者使用本款软件出现任何问题均与本人无关，请使用者使用本软件前有阅读源代码的能力，并理解源代码可能造成的后果.

二. 本软件绝对不针对任何一个厂商、公司.

三. 因使用本软件而引致的任何意外、疏忽、合约毁坏、诽谤、版权或知识产权侵犯及其所造成的任何损失，本人概不负责，亦概不承担任何民事或刑事法律责任。

四. 当你第一次开始使用本人所提供的任何软件及资源的那一刻起就将被视为对本声明全部内容的认可。同时您必须认可上述免责条款，方可使用本软件及资源。如有任何异议，建议立刻删除本软件及资源并且停止使用. 

五. 本工具仅面向合法授权的企业安全建设行为与个人学习行为，如您需要测试本工具的可用性，请自行搭建靶机环境。

六. 在使用本工具进行检测时，您应确保该行为符合当地的法律法规，并且已经取得了足够的授权。请勿对非授权目标进行扫描。

五. 以上内容，本人保留最终解释权。

————————————————


一款SSH批量操作的程序，可以按运行模式实现SSH批量命令执行、权限维持、批量改密、C段监控批量命令执行、C段监控批量改密、C段字典生成
```
-i(指定他的IP，可以是多个IP,也可以用*来标识0~255的IP段，必填)
-d(指定VPS的默认密码，必填)
-c(运行模式，必填)
-u(指定SSH的用户名)
-p(要修改的密码，默认为：byechopwdsec)
-o(指定端口，默认22)

运行模式：
 执行改密操作      循环执行        命令执行
      1             1             1       =>无限执行并改密加命令执行
      0             1             1       =>批量重复执行某个命令
      1             1             0       =>批量改密
      0             0             1       =>只执行一次命令(这里执行命令后，程序才会自动结束)
      1             0             0       =>只执行一次改密操作

flagVPS.txt ----->目标服务器，生成后可以更改
common.txt ----->每次改密后执行的操作，一行一行执行
commonResult.txt ----->common执行操作的输出结果
result.txt ----->改密的机器

```
部署：
1.建议使用Venv环境进行部署，需要的包在requirements.txt中(不知道Venv部署可以看下这个师傅的文章[Venv部署](https://blog.csdn.net/m0_61155226/article/details/131670779))
```
pip install -r requirements.txt
```
2.直接使用Python部署，安装包之后直接Usage
```
pip install -r requirements.txt
```

**Usage** 

```
python .\SSHSUOHA.py -i targetIP -d OldPassword -c XXX
```

**Example**

```
python .\SSHSUOHA.py -i 192.168.213.132 -d adminadmin -c 111
python .\SSHSUOHA.py -i 192.168.213.132 192.168.212.* -d adminadmin -u usertest -c 111
python .\SSHSUOHA.py -i 192.168.213.* -d adminadmin -c 111
```

tips:

​	1.当网络连接比较慢的时候可以适当增加timeout的大小

  2.当有确定的SSH地址的时候，可以生成后再flagVPS.txt中进行CRUD，来提高效率

​	3.由于paramiko超时的原因，有时候因为莫名奇妙的问题会出现except拦截错误(这里如果有师傅知道可以告知一下)，不用管就好，看result.txt里面的就行

​	4.在某些比赛也可以添加一个自己的IP来避免重置的时候被他人改密

​	5.在某些比赛可以通过循环改密自己的ssh密码来避免重置的时候被别人改密码

进阶技巧：

程序生成flagVPS后，可以在监控之前数据清洗：

![image](https://github.com/PlusTop/SSHsuoha/assets/105430146/cf5466f7-9563-493e-bfe7-36dc5b85d9bb)

运行过程中可以更改common.txt的命令，会在下一次ssh连接成功执行（命令是一行一行调用）:
![image](https://github.com/PlusTop/SSHsuoha/assets/105430146/95f7bf0d-2895-4eac-8668-8645e2a2916b)
运行结果：
![image](https://github.com/PlusTop/SSHsuoha/assets/105430146/7dda52ba-d178-41cd-83e2-0f1eac3a4f04)

运行模式111(批量改密+批量命令执行):![111](https://github.com/PlusTop/SSHsuoha/assets/105430146/6a11e7c2-54d2-4059-9051-051bf6556441)
运行模式011(批量命令执行):![011](https://github.com/PlusTop/SSHsuoha/assets/105430146/d88f4cfd-947d-4bcd-a321-3aca1f38d552)


