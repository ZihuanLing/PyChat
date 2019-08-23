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
from vchat import Video_Server, Video_Client
from achat import Audio_Server, Audio_Client

parser = argparse.ArgumentParser()

parser.add_argument('--host', type=str, default='192.168.1.101')
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
    #vserver = Video_Server(PORT, VERSION)
    aclient = Audio_Client(IP, PORT+1, VERSION)
    #aserver = Audio_Server(PORT+1, VERSION)
    vclient.start()
    aclient.start()
    time.sleep(1)    # make delay to start server
    #vserver.start()
    #aserver.start()
    while True:

        time.sleep(1)
        if not vclient.isAlive():
            print("Video connection lost...")
            sys.exit(0)
        if not aclient.isAlive():
            print("Audio connection lost...")
            sys.exit(0)