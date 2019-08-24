# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ip.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ip(object):
    def setupUi(self, ip):
        ip.setObjectName("ip")
        ip.resize(324, 67)
        self.centralwidget = QtWidgets.QWidget(ip)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setPlaceholderText("")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        ip.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ip)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 324, 18))
        self.menubar.setObjectName("menubar")
        ip.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ip)
        self.statusbar.setObjectName("statusbar")
        ip.setStatusBar(self.statusbar)

        self.retranslateUi(ip)
        QtCore.QMetaObject.connectSlotsByName(ip)

    def retranslateUi(self, ip):
        _translate = QtCore.QCoreApplication.translate
        ip.setWindowTitle(_translate("ip", "MainWindow"))
        self.pushButton.setText(_translate("ip", "确认"))

