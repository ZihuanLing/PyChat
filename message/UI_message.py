# coding:utf-8
from threading import Thread
from socket import *
import sys
from time import gmtime, strftime
import win32api
import win32con
from PyQt5 import QtWidgets, QtCore
from UI import untitled,ip,Dialog


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
            if recv_data == "##":
                # 自身连接
                self.client.close()
                self.sock.close()
                self.connect_end = True
                self.ui.textBrowser.append('---> 与 {} 断开的连接已中断... '.format(self.receiverIP))
                # print('\n---> 与 {} 断开的连接已中断... '.format(self.receiverIP))
                win32api.keybd_event(13, 0, 0, 0)
                sys.exit(0)
                break
            elif recv_data:
                self.ui.textBrowser.append('<font color="gray">{}    {}<font>'.format(nick_name, strftime("%H:%M:%S", gmtime())))
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
        self.ui.label.setText(self.receiverIP)
        self.ui.pushButton.disconnect()
        self.ui.pushButton.clicked.connect(self.send_message)

    def send_message(self):
        try:
            msg = self.ui.lineEdit.text()
            if msg:
                self.client.send(bytes(msg, encoding='utf-8'))
                self.ui.textBrowser.append('<font color="gray">{}    {}<font>'.format(self.nick_name,strftime("%H:%M:%S", gmtime())))
                self.ui.textBrowser.append('{}\n'.format(msg))
                self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
                self.ui.lineEdit.clear()
            else:
                self.ui.textBrowser.append('<font color="gray">{}    {}<font>'.format("系统提示",strftime("%H:%M:%S", gmtime())))
                self.ui.textBrowser.append('{}\n'.format("消息不能为空哦"))
                self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
            if msg == '##':
                self.client.close()
                self.sock.close()
                self.connect_end = True
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
            self.nick_name=self.ui.lineEdit.text()
            self.main_window()
        self.ui.pushButton.clicked.connect(get_ip)
        self.ui.pushButton.setShortcut('enter')
        self.window.show()
        sys.exit(self.app.exec_())
