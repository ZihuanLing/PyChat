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
    # 参数设置
    parser = argparse.ArgumentParser()
    receiver_ip = input("请输入要进行通信的地址：")
    sender_ip = socket.gethostname()
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

    senderServer = Sender_Server(SENDER_IP, PORT, VERSION)
    receiverServer = Sender_Server(RECEIVER_IP, PORT, VERSION)
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