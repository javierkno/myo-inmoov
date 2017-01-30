import sys, time

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from PyQt4.QtCore import QSize

from myo_ui import Ui_MainWindow

import myo_raw as myo

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import random

#pyuic4 myo.ui > myo_ui.py

#ln -s /usr/lib/python3.6/site-packages/PyQt4/ ~/.virtualenvs/seagull/lib/python3.6/site-packages/
#ln -s /usr/lib/python3.6/site-packages/sip.so ~/.virtualenvs/seagull/lib/python3.6/site-packages/

class MyoThread(QtCore.QThread):

    myo_stop_signal = False

    pose = []

    quat = []
    acc = []
    gyro = []

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.m = []

    def set_myo_stop_signal(self, bool):
        self.myo_stop_signal = bool

    def save_pose(self, p):
        self.pose = p
        print(p)
        self.emit(QtCore.SIGNAL("pose_px(QString)"),str(p.value))

    def save_imu(self, quat, acc, gyro):
        self.quat = quat
        self.acc = acc
        self.gyro = gyro
        #self.emit(QtCore.SIGNAL("imu(QString)"),'0')

    def run(self):
        self.set_myo_stop_signal(False)
        self.m = myo.MyoRaw(sys.argv[1] if len(sys.argv) >= 2 else None)
        #self.m.add_arm_handler(lambda arm, xdir: print('arm', arm, 'xdir', xdir))
        #self.m.add_pose_handler(lambda p: print('pose', p))
        self.m.add_pose_handler(lambda p: self.save_pose(p))
        self.m.add_imu_handler(lambda quat, acc, gyro: self.save_imu(quat, acc, gyro))
        #self.m.add_imu_handler(lambda quat, acc, gyro: print('quat', quat, 'acc', acc, 'gyro', gyro))
        self.m.connect()
        t = time.clock()
        try:
            while self.myo_stop_signal==False:
                    self.m.run(1)
                    t2 = time.clock()
                    print(t2)
                    print(t)
                    if t2-t>0.3:
                        self.emit(QtCore.SIGNAL("imu(QString)"),'0')
                        t = t2;
        except Exception as e:
            #print(str(e))
            pass
        finally:
            self.disconnect()
            print()

    def disconnect(self):
        self.m.disconnect()
        print('Myo disconnected')

    def sleep_mode(self):
        self.set_myo_stop_signal(True)
        self.m.deep_sleep()
        print('Deep sleep activated')


class MyForm(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.poses=[QtGui.QPixmap('media/rest.svg'),
                    QtGui.QPixmap('media/make-fist.svg'),
                    QtGui.QPixmap('media/wave-left.svg'),
                    QtGui.QPixmap('media/wave-right.svg'),
                    QtGui.QPixmap('media/spread-fingers.svg'),
                    QtGui.QPixmap('media/double-tap.svg'),
                    QtGui.QPixmap('media/pan.svg'),
                    QtGui.QPixmap('media/rotate.svg')]

        self.thread = MyoThread()

        QtCore.QObject.connect(self.ui.btn_connect,QtCore.SIGNAL("clicked()"), self.myo_run)
        QtCore.QObject.connect(self.ui.btn_disconnect,QtCore.SIGNAL("clicked()"), self.myo_disconnect)
        QtCore.QObject.connect(self.ui.btn_sleep,QtCore.SIGNAL("clicked()"), self.myo_deep_sleep)

        self.connect(self.thread, QtCore.SIGNAL("pose_px(QString)"), self.set_pose_px)

        self.connect(self.thread, QtCore.SIGNAL("imu(QString)"), self.draw)

        self.init_buttons(False)
        self.ui.lbl_pose.setScaledContents(True)
        self.set_pose_px('0')

        # plot

        self.figure = plt.figure()
        plt.ion() # funciona?
        self.canvas = FigureCanvas(self.figure)
        self.ui.mplvl.addWidget(self.canvas)
        self.ui.mplvl.setSizeConstraint

        # create an axis
        self.ax = self.figure.add_subplot(111, projection='3d')

    def resizeEvent(self, e):
        self.setMinimumWidth(self.height())

    def draw(self):

        #data = [random.random() for i in range(10)]
        #data2 = [random.random() for i in range(10)]

        data = [0, 0, 0.5]

        data1 = [0, 0, random.random()]

        data2 = [0, -1, -0.5]

        # discards the old graph
        self.ax.hold(False)

        # plot data
        self.ax.plot(data,data1,data2, '*-')

        # refresh canvas
        self.canvas.draw()


    def set_pose_px(self, pose):
        n = int(pose)
        if n!=255:
            self.ui.lbl_pose.setPixmap(self.poses[n])
        else:
            pass

    def init_buttons(self, bool):
        self.ui.btn_disconnect.setEnabled(bool)
        self.ui.btn_sleep.setEnabled(bool)

    def myo_run(self):
        self.init_buttons(True)
        self.thread.start()

    def myo_deep_sleep(self):
        choice = QtGui.QMessageBox.question(self, 'Deep Sleep Mode!',
                                            "Enable Deep Sleep? (Useful to conserve battery during transport)",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            self.init_buttons(False)
            self.thread.sleep_mode()
        else:
            pass

    def myo_disconnect(self):
        self.init_buttons(False)
        self.thread.set_myo_stop_signal(True);
        #self.thread.disconnect()


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    #myapp.setFixedSize(500,300)
    myapp.show()
    sys.exit(app.exec_())
