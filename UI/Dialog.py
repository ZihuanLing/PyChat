# 重写closeEvent方法，实现dialog窗体关闭时执行一些代码
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Dialog(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.callback = None

    def get_thread(self, main_thread):
        self.main_thread = main_thread

    def set_close_callback(self, callback):
        # 设置关闭事件的回调函数
        self.callback = callback

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            if self.callback != None:
                print('callback is ok!')
                self.callback()
            print('Trying to close Dialog')
            sys.exit(0)
        else:
            event.ignore()
