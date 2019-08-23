# 不需要整天右键，直接执行该文件即可重新得到界面文件
class UI(object):
    def __init__(self):
        from untitled import Ui_MainWindow
        from PyQt5 import QtWidgets
        import sys
        self.app = QtWidgets.QApplication(sys.argv)  # 生成应用
        self.window = QtWidgets.QMainWindow()  # 生成窗口q
        self.ui = Ui_MainWindow()  # 使用QTdesigner自动创建的类
        self.ui.setupUi(self.window)
        self.win_adjust()
        self.window.show()
        self.others()
        sys.exit(self.app.exec_())

    def others(self):
        self.buttonConnect()

    def win_adjust(self):
        import win32api, win32con
        self.window.resize(win32api.GetSystemMetrics(win32con.SM_CXSCREEN) / 2,
                           win32api.GetSystemMetrics(win32con.SM_CYSCREEN) / 2)

    def buttonConnect(self):
        self.ui.pushButton.clicked.connect(self.send)

    def send(self):
        self.ui.textBrowser.append(self.ui.label.text()+": "+self.ui.lineEdit.text())


if __name__ == '__main__':
    # import reInterpreter as inter
    ui = UI()
