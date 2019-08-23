import sys
import time
import re
import pickle
import os
import struct
import zlib
import socket
import argparse
from message.message import Sender_Server, Receiver_Server

if __name__ == '__main__':
    def get_host_ip():
        """
        查询本机ip地址
        :return:
        """
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(('8.8.8.8',80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip
    # 参数设置
    parser = argparse.ArgumentParser()
    receiver_ip = input("请输入要进行通信的地址：")
    sender_ip = get_host_ip()
    parser.add_argument('--receiver_ip', type=str, default=receiver_ip)
    parser.add_argument('--sender_ip', type=str, default=sender_ip)
    parser.add_argument('--port', type=int, default=10087)
    parser.add_argument('--level', type=int, default=1)
    parser.add_argument('-v', '--version', type=int, default=4)
    args = parser.parse_args()

    SENDER_IP = args.sender_ip
    RECEIVER_IP = receiver_ip
    PORT = args.port
    VERSION = args.version
    LEVEL = args.level

    senderServer = Sender_Server(RECEIVER_IP, PORT, VERSION)
    receiverServer = Receiver_Server(RECEIVER_IP, PORT, VERSION)
    
    senderServer.start()
    receiverServer.start()
    

    while True:
        time.sleep(1)
        if not senderServer.isAlive():
            print("---> 连接已断开...")
            sys.exit(0)
        if not receiverServer.isAlive() :
            print("---> 连接已断开...")
            sys.exit(0)