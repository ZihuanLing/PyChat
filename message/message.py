# coding:utf-8
from threading import Thread
from socket import *
import sys
from time import gmtime, strftime
import win32api
import win32con

class Messager(Thread):
    def __init__(self, ip, port, version):
        super().__init__()
        self.connect_end = False
        self.ip = ip
        self.port = port
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6, SOCK_STREAM)

    def __del__(self):
        self.sock.close()

    def msg_receiver(self):
        print('---> 正在等待对方确认...')
        self.sock.bind(('', self.port))
        self.sock.listen(5)
        self.conn, self.addr = self.sock.accept()
        while not self.connect_end:
            recv_data = self.conn.recv(1024).decode('utf-8')
            if recv_data == "##":
                # 自身连接
                self.client.close()
                self.sock.close()
                self.connect_end = True
                print('\n---> 与 {} 断开的连接已中断... '.format(self.receiverIP))
                win32api.keybd_event(13,0,0,0)
                sys.exit(0)
                break
            elif recv_data:
                print('\b\b\b\b{} >>: {}\t{}\n\n>>: '.format(self.receiverIP, recv_data,strftime("%Y/%m/%d %H:%M:%S", gmtime())), end="")

    def run(self):
        print('---> 初始化服务中...')
        self.client = socket(AF_INET, SOCK_STREAM)
        self.receiverIP = input('---> 请输入联系人的ip: ')
        server = Thread(target=self.msg_receiver)
        server.start()
        self.client.connect((self.receiverIP, self.port))
        print('---> 连接成功')
        try:
            while True:
                # 发送
                msg = input('\b\b\b\b>>：')
                self.client.send(bytes(msg, encoding='utf-8'))
                if msg == '##':
                    self.client.close()
                    self.sock.close()
                    self.connect_end = True
                    sys.exit(0)
                    break
        except:
            print('---> 服务已断开...')
            self.sock.close()

