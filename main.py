from UI import untitled
from PyQt5 import QtWidgets,QtCore
import sys
import argparse
from message.UI_message import Messager
from UI import Dialog
class UI(object):
    def __init__(self):

        self.argu_setting()

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
        # diag=Dialog.Dialog()#声明窗口类
        # diag.get_thread(Msg)#把线程传给窗口，以便重写窗口类
        Msg.start()

if __name__ == '__main__':
    # import reInterpreter as inter
    ui = UI()
