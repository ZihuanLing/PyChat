from UI import untitled
from PyQt5 import QtWidgets,QtCore
import sys
class UI(object):
    def __init__(self):
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        self.app = QtWidgets.QApplication(sys.argv)  # 生成应用
        self.window = QtWidgets.QMainWindow()  # 生成窗口q
        self.ui = untitled.Ui_MainWindow()  # 使用QTdesigner自动创建的类
        self.ui.setupUi(self.window)
        self.win_adjust()
        self.window.show()
        self.others()
        sys.exit(self.app.exec_())

    def others(self):
        self.buttonConnect()
        self.argu_setting()

    def win_adjust(self):
        import win32api, win32con
        # self.window.resize(win32api.GetSystemMetrics(win32con.SM_CXSCREEN) / 2,
        #                    win32api.GetSystemMetrics(win32con.SM_CYSCREEN) / 2)

    def buttonConnect(self):
        self.ui.pushButton.clicked.connect(self.send)

    def send(self):
        self.ui.textBrowser.append(self.ui.label.text()+": "+self.ui.lineEdit.text())

    def argu_setting(self):
        # 参数设置
        import argparse
        from message.message import Messager
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
        Msg.connect_UI(self.ui)
        Msg.start()

if __name__ == '__main__':
    # import reInterpreter as inter
    ui = UI()
