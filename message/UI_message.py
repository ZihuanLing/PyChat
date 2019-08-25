# coding:utf-8
from threading import Thread
from socket import *
import sys
from time import gmtime, strftime, sleep
import win32api
import win32con
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
import argparse
import cv2
import re
import pyaudio
import pickle
import os
import struct
import zlib
import wave

sys.path.append("../video/")
from video.vchat import Video_Server, Video_Client
from video.achat import Audio_Server, Audio_Client

from UI import untitled, ip, Dialog


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
        self.ui.textBrowser.append('---> 等待对方确认...')
        self.sock.bind(('', self.port))
        self.sock.listen(5)
        self.conn, self.addr = self.sock.accept()
        nick_name = self.conn.recv(1024).decode('utf-8')
        self.ui.label.setText(nick_name)
        while not self.connect_end:
            recv_data = self.conn.recv(1024).decode('utf-8')
            if recv_data == "VIDEO_REQUEST":
                self.video_request()

            elif recv_data == "VIDEO_RESPONED":
                parser = argparse.ArgumentParser()
                parser.add_argument('--host', type=str, default=self.receiverIP)
                parser.add_argument('--port', type=int, default=8087)
                parser.add_argument('--level', type=int, default=1)
                parser.add_argument('-v', '--version', type=int, default=4)
                args = parser.parse_args()
                IP = args.host
                PORT = args.port
                VERSION = args.version
                LEVEL = args.level

                vclient = Video_Client(IP, PORT, LEVEL, VERSION)
                vserver = Video_Server(PORT, VERSION)
                vclient.start()
                sleep(1)    # make delay to start server
                vserver.start()
                # while True:
                #     sleep(1)
                #     if not vserver.isAlive() or not vclient.isAlive():
                #         print("Video connection lost...")
                #         sys.exit(0)
                # break
            elif recv_data:
                self.ui.textBrowser.append(
                    '<font color="gray">{}    {}<font>'.format(nick_name, strftime("%H:%M:%S", gmtime())))
                # print('\b\b\b\b{} >>: {}\t{}\n\n>>: '.format(self.receiverIP, recv_data,
                #                                              strftime("%Y/%m/%d %H:%M:%S", gmtime())), end="")
                self.ui.textBrowser.append('{}\n'.format(recv_data))
                self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

    def main_window(self):
        # print(self.receiverIP)

        self.window = Dialog.Dialog()  # 生成窗口q
        self.ui = untitled.Ui_MainWindow()  # 使用QTdesigner自动创建的类
        self.ui.setupUi(self.window)
        self.window.show()

        self.ui.textBrowser.append('---> 初始化服务中...')
        self.client = socket(AF_INET, SOCK_STREAM)
        server = Thread(target=self.msg_receiver)
        server.start()
        self.client.connect((self.receiverIP, self.port))
        self.client.send(bytes(self.nick_name, encoding='utf-8'))
        self.ui.textBrowser.append('---> 连接成功')
        # self.ui.label.setText(self.receiverIP)
        self.ui.pushButton.disconnect()
        self.ui.pushButton.clicked.connect(self.send_message)
        self.ui.pushButton_2.clicked.connect(self.video_launch)  # 点击视频聊天按钮触发video_connect方法

    def video_request(self):#接受到聊天，调用该方法
        reply = QMessageBox.question(self.window,
                                     '视频聊天',
                                     "是否接受？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            parser = argparse.ArgumentParser()
            parser.add_argument('--host', type=str, default=self.receiverIP)
            parser.add_argument('--port', type=int, default=8087)
            parser.add_argument('--level', type=int, default=1)
            parser.add_argument('-v', '--version', type=int, default=4)
            args = parser.parse_args()
            IP = args.host
            PORT = args.port
            VERSION = args.version
            LEVEL = args.level
            vclient = Video_Client(IP, PORT, LEVEL, VERSION)
            vserver = Video_Server(PORT, VERSION)
            vclient.start()
            sleep(1)    # make delself.sock.connectay to start server
            vserver.start()
            self.client.send(bytes("VIDEO_RESPONED", encoding='utf-8'))
        else:
            pass

    def video_launch(self):#发起视频调用
        self.client.send(bytes("VIDEO_REQUEST", encoding='utf-8'))

    def send_message(self):
        try:
            msg = self.ui.lineEdit.text()
            if msg:
                self.client.send(bytes(msg, encoding='utf-8'))
                self.ui.textBrowser.append(
                    '<font color="gray">{}    {}<font>'.format(self.nick_name, strftime("%H:%M:%S", gmtime())))
                self.ui.textBrowser.append('{}\n'.format(msg))
                self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
                self.ui.lineEdit.clear()
            else:
                self.ui.textBrowser.append(
                    '<font color="gray">{}    {}<font>'.format("系统提示", strftime("%H:%M:%S", gmtime())))
                self.ui.textBrowser.append('{}\n'.format("消息不能为空哦"))
                self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)

        except:
            self.ui.textBrowser.append('---> 服务已断开...')
            self.sock.close()

    def run(self):
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        self.app = QtWidgets.QApplication(sys.argv)  # 生成应用
        self.window = QtWidgets.QMainWindow()  # 生成窗口q
        self.ui = ip.Ui_ip()  # 使用QTdesigner自动创建的类
        self.ui.setupUi(self.window)

        def get_ip():
            self.receiverIP = self.ui.lineEdit_2.text()
            self.nick_name = self.ui.lineEdit.text()
            self.main_window()

        self.ui.pushButton.clicked.connect(get_ip)
        self.ui.pushButton.setShortcut('enter')
        self.window.show()
        sys.exit(self.app.exec_())
