"""
import socket

print("---> 欢迎来到成人聊天室！")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input("请输入要进行通信的地址：")
port = 8080

# 连接服务器
server.connect((host, port))
try:
    while True:
        message = input(">>: ")
        server.send(bytes(message, encoding='utf-8'))
        recv_data = server.recv(1024).decode('utf-8')
        print(">>: {}".format(recv_data))
except KeyboardInterrupt:
    server.close()
    print("会话已终止...")
"""
from socket import *
from threading import Thread
import cv2
import re
import time
import sys
import os
import struct
import pickle
import zlib
import wave

class Sender_Server(Thread):
    def __init__(self, ip, port, version) :
        super().__init__()
        self.setDaemon(True)
        # self.ADDR = ('', port)
        self.ip = ip
        self.port = port
        if version == 4:
            self.sock = socket(AF_INET ,SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6 ,SOCK_STREAM)
        self.stream = None
        
    def __del__(self):
        self.sock.close()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()

    def run(self):
        print("---> 文字聊天服务初始化中...")
        server = self.sock

        # 连接服务器
        server.connect((self.ip, self.port))
        try:
            while True:
                message = input(">>: ")
                server.send(bytes(message, encoding='utf-8'))
                recv_data = server.recv(1024).decode('utf-8')
                # print(">>: {}".format(recv_data))
        except KeyboardInterrupt:
            server.close()
            print("---> 会话已终止...")

class Receiver_Server(Thread):
    def __init__(self, ip, port, version) :
        super().__init__()
        self.setDaemon(True)
        # self.ADDR = ('', port)
        self.ip = ip
        self.port = port
        if version == 4:
            self.sock = socket(AF_INET ,SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6 ,SOCK_STREAM)
        self.stream = None
        
    def __del__(self):
        self.sock.close()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()

    def run(self):
        server = self.sock
        server.bind((self.ip, self.port)) 
        server.listen(5)

        conn, addr = server.accept()
        try:
            while True:
                # 接收消息
                recv_data = conn.recv(1024).decode('utf-8')
                print("{} >>: {}".format(self.ip, recv_data))
                conn.send(bytes("服务器已成功接收到信息..", encoding="utf-8"))
        except:
            server.close()