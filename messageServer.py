import sys
import time
import re
import pickle
import os
import struct
import zlib
import socket
import argparse
from message.message import Messager

if __name__ == '__main__':
    # 参数设置
    parser = argparse.ArgumentParser()
    sender_ip = "127.0.0.1"
    parser.add_argument('--sender_ip', type=str, default=sender_ip)
    parser.add_argument('--port', type=int, default=10087)
    parser.add_argument('-v', '--version', type=int, default=4)
    args = parser.parse_args()

    SENDER_IP = args.sender_ip
    PORT = args.port
    VERSION = args.version

    Msg = Messager(SENDER_IP, PORT, VERSION)
    Msg.start()