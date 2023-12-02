# ChangeSSHpwds（线程一对一）

一款SSH批量改密，并持续监控的程序，可以实现改密时RCE，密码权限维持

```
-i (指定他的IP，可以是多个IP,也可以用*来标识0~255的IP段，必填)
-d(指定VPS的默认密码，必填)
-u(指定SSH的用户名)
-p(要修改的密码，默认为：byechopwdsec)
-t(指定线程数，默认为10线程)
-o(指定端口，默认22)

flagVPS.txt ----->目标服务器，生成后可以更改
common.txt ----->每次改密后执行的操作，一行一行执行
commonResult.txt ----->common执行操作的输出结果
result.txt ----->改密的机器

```

当有确定的SSH地址的时候，可以生成后再flagVPS.txt中进行CRUD，来提高效率

common.txt用于改密后的RCE操作

tips:

​	1.当网络连接比较慢的时候可以适当增加timeout的大小

​	2.也可以添加一个自己的IP来避免重置的时候被他人改密

​	3.由于未知的原因，有时候因为莫名奇妙的问题会出现except拦截错误(这里如果有师傅知道可以告知一下)，不用管就好，看result.txt里面的就行

​	4.可以通过只设置自己的ssh密码来避免重置被别人改密码

**Usage** 

```
python3 .\EchoPwdSSHSUOHA.py -i targetIP -d OldPassword
```

**Example**

```
python .\EchoPwdSSHSUOHA.py -i 192.168.213.132 192.168.213.* -d adminadmin
```

进阶技巧：

程序生成flagVPS后，可以在监控之前数据清洗：
![image](https://github.com/PlusTop/SSHsuoha/assets/105430146/cf5466f7-9563-493e-bfe7-36dc5b85d9bb)
运行过程中可以更改common.txt的命令，会在下一次ssh连接成功执行（命令是一行一行调用，可以写入mm操作）:
![image](https://github.com/PlusTop/SSHsuoha/assets/105430146/95f7bf0d-2895-4eac-8668-8645e2a2916b)
运行结果：
![image](https://github.com/PlusTop/SSHsuoha/assets/105430146/7dda52ba-d178-41cd-83e2-0f1eac3a4f04)
