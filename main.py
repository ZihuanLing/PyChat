from UI import untitled
from PyQt5 import QtWidgets,QtCore
import sys
import argparse
from message.UI_message import Messager
class UI(object):
    def __init__(self):

        self.others()

    def others(self):
        # self.buttonConnect()
        self.argu_setting()

    # def buttonConnect(self):
    #     self.ui.pushButton.clicked.connect(self.send)
    #
    # def send(self):
    #     self.ui.textBrowser.append(self.ui.label.text()+": "+self.ui.lineEdit.text())
    #
    # def getText(self):
    #     return self.ui.lineEdit.text()

    def argu_setting(self):
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
if __name__ == '__main__':
    # import reInterpreter as inter
    ui = UI()
