# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myo2.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(679, 521)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plot = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setMinimumSize(QtCore.QSize(200, 200))
        self.plot.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.mplvl = QtGui.QVBoxLayout(self.plot)
        self.mplvl.setMargin(0)
        self.mplvl.setObjectName(_fromUtf8("mplvl"))
        self.gridLayout.addWidget(self.plot, 0, 0, 1, 4)
        self.lbl_pose = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_pose.sizePolicy().hasHeightForWidth())
        self.lbl_pose.setSizePolicy(sizePolicy)
        self.lbl_pose.setMinimumSize(QtCore.QSize(150, 150))
        self.lbl_pose.setMaximumSize(QtCore.QSize(150, 150))
        self.lbl_pose.setObjectName(_fromUtf8("lbl_pose"))
        self.gridLayout.addWidget(self.lbl_pose, 1, 0, 1, 1)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btn_connect2 = QtGui.QPushButton(self.frame)
        self.btn_connect2.setObjectName(_fromUtf8("btn_connect2"))
        self.gridLayout_2.addWidget(self.btn_connect2, 3, 0, 1, 1)
        self.myo_1 = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myo_1.sizePolicy().hasHeightForWidth())
        self.myo_1.setSizePolicy(sizePolicy)
        self.myo_1.setMinimumSize(QtCore.QSize(50, 20))
        self.myo_1.setMaximumSize(QtCore.QSize(50, 20))
        self.myo_1.setObjectName(_fromUtf8("myo_1"))
        self.gridLayout_2.addWidget(self.myo_1, 0, 0, 1, 1)
        self.btn_connect = QtGui.QPushButton(self.frame)
        self.btn_connect.setStyleSheet(_fromUtf8(""))
        self.btn_connect.setObjectName(_fromUtf8("btn_connect"))
        self.gridLayout_2.addWidget(self.btn_connect, 1, 0, 1, 1)
        self.btn_sleep = QtGui.QPushButton(self.frame)
        self.btn_sleep.setObjectName(_fromUtf8("btn_sleep"))
        self.gridLayout_2.addWidget(self.btn_sleep, 1, 3, 1, 1)
        self.btn_disconnect = QtGui.QPushButton(self.frame)
        self.btn_disconnect.setStyleSheet(_fromUtf8(""))
        self.btn_disconnect.setObjectName(_fromUtf8("btn_disconnect"))
        self.gridLayout_2.addWidget(self.btn_disconnect, 1, 1, 1, 1)
        self.myo_2 = QtGui.QLabel(self.frame)
        self.myo_2.setMinimumSize(QtCore.QSize(50, 20))
        self.myo_2.setMaximumSize(QtCore.QSize(50, 20))
        self.myo_2.setObjectName(_fromUtf8("myo_2"))
        self.gridLayout_2.addWidget(self.myo_2, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 2, 1, 1)
        self.btn_disconnect2 = QtGui.QPushButton(self.frame)
        self.btn_disconnect2.setObjectName(_fromUtf8("btn_disconnect2"))
        self.gridLayout_2.addWidget(self.btn_disconnect2, 3, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 3, 2, 1, 1)
        self.btn_sleep2 = QtGui.QPushButton(self.frame)
        self.btn_sleep2.setObjectName(_fromUtf8("btn_sleep2"))
        self.gridLayout_2.addWidget(self.btn_sleep2, 3, 3, 1, 1)
        self.myo_1_name = QtGui.QLabel(self.frame)
        self.myo_1_name.setText(_fromUtf8(""))
        self.myo_1_name.setObjectName(_fromUtf8("myo_1_name"))
        self.gridLayout_2.addWidget(self.myo_1_name, 0, 1, 1, 1)
        self.myo_2_name = QtGui.QLabel(self.frame)
        self.myo_2_name.setText(_fromUtf8(""))
        self.myo_2_name.setObjectName(_fromUtf8("myo_2_name"))
        self.gridLayout_2.addWidget(self.myo_2_name, 2, 1, 1, 1)
        self.myo_1.raise_()
        self.btn_connect.raise_()
        self.myo_2.raise_()
        self.btn_connect2.raise_()
        self.btn_disconnect.raise_()
        self.btn_sleep.raise_()
        self.btn_disconnect2.raise_()
        self.btn_sleep2.raise_()
        self.myo_1_name.raise_()
        self.myo_2_name.raise_()
        self.gridLayout.addWidget(self.frame, 1, 1, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 679, 30))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Myo Viewer", None))
        self.lbl_pose.setText(_translate("MainWindow", "   Label", None))
        self.btn_connect2.setText(_translate("MainWindow", "Connect", None))
        self.myo_1.setText(_translate("MainWindow", "Myo 1:", None))
        self.btn_connect.setText(_translate("MainWindow", "Connect", None))
        self.btn_sleep.setText(_translate("MainWindow", "Deep Sleep", None))
        self.btn_disconnect.setText(_translate("MainWindow", "Disconnect", None))
        self.myo_2.setText(_translate("MainWindow", "Myo 2:", None))
        self.btn_disconnect2.setText(_translate("MainWindow", "Disconnect", None))
        self.btn_sleep2.setText(_translate("MainWindow", "Deep Sleep", None))

