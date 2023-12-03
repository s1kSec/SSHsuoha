#!/usr/bin/env python
# -*-coding:utf-8-*-
# Anthor: EchoPwdSec
# 按装订区域中的绿色按钮以运行脚本。
import datetime
import optparse
import re
import socket
import threading
import queue

import paramiko

pwd = "byechopwdsec"  # 默认密码
flagStatushelp = """
        执行改密操作      循环执行        命令执行
            1             1             1       =>(默认值)无限执行并改密加命令执行
            0             1             1       =>批量重复执行某个命令
            1             1             0       =>批量改密
            0             0             1       =>只执行一次命令(这里执行命令后，程序才会自动结束)
            1             0             0       =>只执行一次改密操作
"""
flagStatus = "111"

class monitorVPS():
    # 分别给入线程数,旧密码，账户名，密码，端口
    def __init__(self, oldpassword, password, user, port):
        self.flags = queue.Queue()
        with open('flagVPS.txt', 'r') as f:
            lines = f.read().splitlines()
        self.flags = lines
        self.threads_num = len(lines)
        self.password = password
        self.user = user
        self.port = port
        self.oldpassword = oldpassword

    def monitor(self, i):
        while True:
            ip = self.flags[i]
            try:
                # 建立一个sshclient对象
                ssh = paramiko.SSHClient()
                # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip, port=self.port, username=self.user, password=self.oldpassword)
                # 判断是否改密
                if flagStatus[0] == '1':
                    print("执行改密操作")
                    # root用户和非root用户使用不同的方式更改密码
                    if self.user == "root":
                        ssh.exec_command('echo "%s:%s" | chpasswd' % (self.user, self.password))
                    else:
                        command = "passwd\n"
                        stdin, stdout, stderr = ssh.exec_command(command)
                        # \n模拟回车 输两次密码
                        stdin.write(self.oldpassword + '\n' + self.password + '\n' + self.password + '\n')
                    print("改密成功:"+ip+"新密码:"+self.password)
                    with open("result.txt", "ab") as save:
                        save.write(
                            str(datetime.datetime.today()).encode("utf-8") + " | ".encode("utf-8") + ip.encode(
                                "utf-8") + " | ".encode("utf-8") + self.user.encode("utf-8") + " | ".encode(
                                "utf-8") + self.password.encode("utf-8") + "\n".encode("utf-8"))
                # 读取命令
                if flagStatus[2] == '1':
                    with open("command.txt", 'r') as comond:
                        commands = comond.readlines()
                        comond.close()
                    for command in commands:
                        stdin, stdout, stderr = ssh.exec_command(command)
                        with open("commandResult.txt", "ab") as saveCommand:
                            saveCommand.write(
                                "--执行命令的IP-->".encode("utf-8") + ip.encode("utf-8") + "\n".encode("utf-8") +
                                command.encode("utf-8") +
                                str(datetime.datetime.today()).encode("utf-8") + "\n".encode("utf-8") +
                                str(stdout.read().decode("utf-8")).encode("utf-8") + "\n".encode("utf-8")
                            )
                if flagStatus[1] == '0':
                    break
            except Exception as e:
                pass
            except socket.timeout as e:
                pass

    def run(self):
        for i in range(self.threads_num):
            t = threading.Thread(target=self.monitor, args={i})
            t.start()


def CreateFlagVPS(temp):
    for temp in lists:
        with open("flagVPS.txt", "ab") as f:
            if temp is not None and re.compile(r'\*').search(temp):
                Clist = []
                # 统计*出现的次数，一个ip的循环次数为i*j
                for i in range(1, 256):
                    f.write(str(temp).replace('*', str(i), 1).encode('utf-8') + "\n".encode('utf-8'))
                # f.writelines(Clist)
            else:
                f.write(str(temp).encode('utf-8') + "\n".encode('utf-8'))
        f.close()


if __name__ == '__main__':
    # 初始化解释器
    # 如果是IP地址段的话，会对IP地址段进行批量改密操作
    parser = optparse.OptionParser("Usage: %prog [options] target")
    parser.add_option("-i", "--ip", action="store", type="string", dest="ips",
                      help="指定一或者多个ip或者使用一个<*>来标识整个1~255的ip段，或者使    用<:端口>来指定端口，默认22"
                      )
    parser.add_option("-d", "--oldpassword", action="store", type="string", dest="oldpassword",
                      help="指定旧密码(默认旧密码=root)"
                      )
    parser.add_option("-u", "--user", action="store", type="string", dest="user", default="root",
                      help="指定用户名(默认用户名=root)"
                      )
    parser.add_option("-p", "--password", action="store", type="string", dest="password", default=pwd,
                      help="指定批量更改的默认密码(默认密码=byechopwdsec)"
                      )
    parser.add_option("-o", "--port", action="store", type=int, default=22, dest="port",
                      help="指定端口")
    parser.add_option("-c", "--command", action="store", type="string", dest="status", default=flagStatus,
                      help=flagStatushelp)
    (options, args) = parser.parse_args()
    flagStatus = options.status
    # 未指定参数的情况
    if options.ips is None or options.oldpassword is None:
        print("\033[0;31;40m旧密码或者目标地址池未指定!!请检查你的参数\033[0m")
        print(options)
        exit()
    banner = """
           ██████  ██        ███████   ███████                  ██  ████████                
          ██░░░░██░██       ██░░░░░██ ░██░░░░██                ░██ ██░░░░░░                 
  █████  ██    ░░ ░██      ██     ░░██░██   ░██ ███     ██     ░██░██         █████   █████ 
 ██░░░██░██       ░██████ ░██      ░██░███████ ░░██  █ ░██  ██████░█████████ ██░░░██ ██░░░██
░███████░██       ░██░░░██░██      ░██░██░░░░   ░██ ███░██ ██░░░██░░░░░░░░██░███████░██  ░░ 
░██░░░░ ░░██    ██░██  ░██░░██     ██ ░██       ░████░████░██  ░██       ░██░██░░░░ ░██   ██
░░██████ ░░██████ ░██  ░██ ░░███████  ░██       ███░ ░░░██░░██████ ████████ ░░██████░░█████ 
 ░░░░░░   ░░░░░░  ░░   ░░   ░░░░░░░   ░░       ░░░    ░░░  ░░░░░░ ░░░░░░░░   ░░░░░░  ░░░░░  
    """
    print(banner)
    with open("flagVPS.txt", "w") as ftemp:
        ftemp.close()
    # 待处理的ip列表池
    lists = list(args)
    lists.append(options.ips)
    CreateFlagVPS(lists)
    print(options)
    print("\033[0;31;40m因为多线程并且减少开支没有异步判断超时，出现报错是正常的，注意看追加的文件即可！\033[0m")
    s = monitorVPS(oldpassword=options.oldpassword, password=options.password,
                   user=options.user, port=options.port) if input(
        "\033[0;32;40mIP字典生成成功！立刻对指定IP进行监控改密(Y/N)？(如需手动修改现在可打开flagVPS.txt):\033[0m").upper() == "Y" else exit()
    print("|    程序运行中，可在result.txt/commandResult.txt查看结果,command.txt修改执行命令    |")
    print(flagStatus)
    s.run()
