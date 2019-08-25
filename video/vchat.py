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
        super().__init__()
        # self.setDaemon(True)    # 守护进程
        self.setName('Video Client')
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

    def close_listener(self):
        # 监听服务器发过来的摄像头关闭事件
        while True:
            try:
                msg = self.sock.recv(1024).decode('utf-8')
                if msg == 'CLOSE_VIDEO_SESSION':
                    print('Receive close request, try to close')
                    self.sock.close()
                    self.cap.release()
                    print('Close done')
                    # break
            except:
                self.sock.close()
                self.cap.release()
            finally:
                print('self.cap.isOpened(): ', self.cap.isOpened())
                break
                pass
                # break

    def run(self):
        print("VEDIO client starts...")
        while True:
            # 循环连接，如果连接不上，间隔一秒后再次连接
            try:
                self.sock.connect(self.ADDR)
                break
            except:
                time.sleep(1)
                # continue
        print("VEDIO client connected...")
        
        # 同步监听摄像头关闭请求
        cl = Thread(target=self.close_listener)
        cl.setName('Close listener')
        cl.start()

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            # 一个矩形窗口，即相机所拍摄的窗口大小
            sframe = cv2.resize(frame, (0,0), fx=self.fx, fy=self.fx)
            data = pickle.dumps(sframe)
            zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            try:
                # 将图像数据压缩后发送到服务端
                self.sock.sendall(struct.pack("L", len(zdata)) + zdata)
            except:
                break
            for i in range(self.interval):
                self.cap.read()

class Video_Server(Thread):
    # 服务器端最终代码如下，增加了对接收到数据的解压缩处理。
    # 服务器是用来接收Client发送的图像数据并且显示的
    def __init__(self, port, version) :
        super().__init__()
        # self.setDaemon(True)
        self.setName('Video Server')
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
        print('Server started, waiting for connection...')
        conn, addr = self.sock.accept()
        print("remote VEDIO client success connected...")
        data = "".encode("utf-8")
        payload_size = struct.calcsize("L")
        winname = 'VChat'
        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
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
            cv2.imshow(winname, frame)
            # 通过按Esc或者点击x可以关闭窗口
            keyCode = cv2.waitKey(1)
            prop = cv2.getWindowProperty(winname, cv2.WND_PROP_AUTOSIZE)
            if keyCode != -1 or prop == -1:
                # 退出后，向Client发送一个关闭信号
                try:
                    conn.send(bytes('CLOSE_VIDEO_SESSION', encoding='utf-8'))
                except:
                    print('Try to tell client close, but failed')
                finally:
                    conn.close()
                    break


if __name__ == "__main__":
    # This is the demo to test the vedio chat file
    vServer = Video_Server(5556, 4)
    vServer.start()
    vClient = Video_Client('127.0.0.1', 5556, 1, 4)
    vClient.start()
    print('Main thread OK.')