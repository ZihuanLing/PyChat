import sys
import time
import argparse
import cv2
import re
import pyaudio
import pickle
import os
import struct
import zlib
import wave
from video.vchat1 import Video_Server, Video_Client

parser = argparse.ArgumentParser()

parser.add_argument('--host', type=str, default='192.168.1.110')
parser.add_argument('--port', type=int, default=10087)
parser.add_argument('--level', type=int, default=1)
parser.add_argument('-v', '--version', type=int, default=4)

args = parser.parse_args()

IP = args.host
PORT = args.port
VERSION = args.version
LEVEL = args.level

if __name__ == '__main__':
    vclient = Video_Client(IP, PORT, LEVEL, VERSION)
    vserver = Video_Server(PORT, VERSION)
    vclient.start()
    time.sleep(1)    # make delay to start server
    vserver.start()
    while True:

        time.sleep(1)
        if not vserver.isAlive() or not vclient.isAlive():
            print("Video connection lost...")
            sys.exit(0)
        
