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


class Video_Client(Thread):
    # 视频客户端
    def __init__(self ,ip, port, level, version):
        # Thread.__init__(self)
        super().__init__()
        self.setDaemon(True)    # 守护进程
        self.ADDR = (ip, port)  # 连接地址
        if level <= 3:
            self.interval = level
        else:
            self.interval = 3
        self.fx = 1 / (self.interval + 1)
        if self.fx < 0.3:
            self.fx = 0.3
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6, SOCK_STREAM)
        self.cap = cv2.VideoCapture(0)

    def __del__(self) :
        self.sock.close()
        self.cap.release()

    def run(self):
        print("VEDIO client starts...")
        while True:
            # 循环连接，如果连接不上，间隔一秒后再次连接
            try:
                self.sock.connect(self.ADDR)
                break
            except:
                time.sleep(1)
                continue
        print("VEDIO client connected...")
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            # 一个矩形窗口
            sframe = cv2.resize(frame, (0,0), fx=self.fx, fy=self.fx)
            data = pickle.dumps(sframe)
            zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            try:
                self.sock.sendall(struct.pack("L", len(zdata)) + zdata)
            except:
                break
            for i in range(self.interval):
                self.cap.read()

class Video_Server(Thread):
    # 服务器端最终代码如下，增加了对接收到数据的解压缩处理。
    def __init__(self, port, version) :
        # Thread.__init__(self)
        super().__init__()
        self.setDaemon(True)
        self.ADDR = ('', port)
        if version == 4:
            self.sock = socket(AF_INET ,SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6 ,SOCK_STREAM)

    def __del__(self):
        self.sock.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass
            
    def run(self):
        print("VEDIO server starts...")
        self.sock.bind(self.ADDR)
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        print("remote VEDIO client success connected...")
        data = "".encode("utf-8")
        payload_size = struct.calcsize("L")
        cv2.namedWindow('Remote', cv2.WINDOW_NORMAL)
        while True:
            while len(data) < payload_size:
                data += conn.recv(81920)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_size)[0]
            while len(data) < msg_size:
                data += conn.recv(81920)
            zframe_data = data[:msg_size]
            data = data[msg_size:]
            frame_data = zlib.decompress(zframe_data)
            frame = pickle.loads(frame_data)
            cv2.imshow('Remote', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

