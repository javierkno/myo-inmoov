# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myo.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(500, 400)
        self.btn_connect = QtGui.QPushButton(Dialog)
        self.btn_connect.setGeometry(QtCore.QRect(30, 30, 93, 30))
        self.btn_connect.setStyleSheet(_fromUtf8(""))
        self.btn_connect.setObjectName(_fromUtf8("btn_connect"))
        self.btn_disconnect = QtGui.QPushButton(Dialog)
        self.btn_disconnect.setGeometry(QtCore.QRect(30, 80, 93, 30))
        self.btn_disconnect.setStyleSheet(_fromUtf8(""))
        self.btn_disconnect.setObjectName(_fromUtf8("btn_disconnect"))
        self.btn_sleep = QtGui.QPushButton(Dialog)
        self.btn_sleep.setGeometry(QtCore.QRect(370, 30, 93, 30))
        self.btn_sleep.setObjectName(_fromUtf8("btn_sleep"))
        self.lbl_pose = QtGui.QLabel(Dialog)
        self.lbl_pose.setGeometry(QtCore.QRect(30, 290, 81, 81))
        self.lbl_pose.setObjectName(_fromUtf8("lbl_pose"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.btn_connect.setText(_translate("Dialog", "Connect", None))
        self.btn_disconnect.setText(_translate("Dialog", "Disconnect", None))
        self.btn_sleep.setText(_translate("Dialog", "Deep Sleep", None))
        self.lbl_pose.setText(_translate("Dialog", "   Label", None))

