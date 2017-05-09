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

import serial, time, glob
import serial.tools.list_ports

import enum
import math
import collections
import numpy as np

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
        self.emit(QtCore.SIGNAL("imu(QString)"),'0')
        print(quat)

    def connect(self):
        self.m = myo.MyoRaw(sys.argv[1] if len(sys.argv) >= 2 else None)
        #self.m.add_arm_handler(lambda arm, xdir: print('arm', arm, 'xdir', xdir))
        #self.m.add_pose_handler(lambda p: print('pose', p))
        self.m.add_pose_handler(lambda p: self.save_pose(p))
        self.m.add_imu_handler(lambda quat, acc, gyro: self.save_imu(quat, acc, gyro))
        #self.m.add_imu_handler(lambda quat, acc, gyro: print('quat', quat, 'acc', acc, 'gyro', gyro))
        self.m.connect()

    def run(self):
        self.set_myo_stop_signal(False)

        t = time.clock()
        try:
            while self.myo_stop_signal==False:
                    self.m.run(1)
                    t2 = time.clock()
                    #print(t2)
                    #print(t)
                    if t2-t>0.2:
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


class Joint(enum.Enum) :
    SHOULDER_FB = 0
    SHOULDER_UD = 1
    ELBOW = 2

class MyForm(QtGui.QMainWindow):

    x = 0
    joint = 0

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
        QtCore.QObject.connect(self.ui.cb_port,QtCore.SIGNAL("clicked()"), self.serial_ports)
        QtCore.QObject.connect(self.ui.btn_connectArduino,QtCore.SIGNAL("clicked()"), self.serial_connect)
        QtCore.QObject.connect(self.ui.cb_myo2,QtCore.SIGNAL("clicked()"), self.enable_myo)


        self.connect(self.thread, QtCore.SIGNAL("pose_px(QString)"), self.set_pose_px)
        self.connect(self.thread, QtCore.SIGNAL("imu(QString)"), self.show_angles)
        #self.connect(self.thread, QtCore.SIGNAL("imu(QString)"), self.draw)

        self.init_buttons(False)

        self.set_pose_px('0')

        # plot
        self.figure = plt.figure()
        plt.ion() # funciona?
        self.canvas = FigureCanvas(self.figure)
        self.ui.mplvl.addWidget(self.canvas)
        self.ui.mplvl.setSizeConstraint
        # create an axis
        self.ax = self.figure.add_subplot(111, projection='3d')
        #self.ax.patch.set_facecolor('black')

        self.serial_ports()

        self.ui.lbl_art.setText("joint 1")


    def serial_ports(self):
        #ports = glob.glob('/dev/tty[A-Za-z]*')
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print(p)
            self.ui.cb_port.addItem(p[0])

    def serial_connect(self):
        self.arduino = serial.Serial(self.ui.cb_port.currentText(), 9600)
        time.sleep(2)
        # arduino.write(b'9')
        # arduino.close()
        b = [65, 66, 67, 198]
        self.send(b, 4)

    def send(self, cmd, cmdLength):
    	# self.arduino.write(b'94')
    	# for i in range(0, cmdLength):
    	# 	self.arduino.write(cmd[i])
    	# self.arduino.write(b'10')
        self.arduino.write(b'94')
        self.arduino.write(b'65')
        self.arduino.write(b'66')
        self.arduino.write(b'67')
        self.arduino.write(b'198')
        self.arduino.write(b'10')

    def resizeEvent(self, e):
        self.setMinimumWidth(self.height())

    def draw(self):

        #data = [random.random() for i in range(10)]
        #data2 = [random.random() for i in range(10)]

        data = [0, 0, 0.5]
        data1 = [0, 0, self.x]
        self.x = self.x + 0.2
        data2 = [0, -1, -0.5]

        # discards the old graph
        self.ax.cla()
        # plot data
        self.ax.plot(data,data1,data2, '*-')
        # refresh canvas
        self.canvas.draw()


    def set_pose_px(self, pose):
        n = int(pose)
        if n!=255:
            self.ui.lbl_pose.setPixmap(self.poses[n])
        if n==myo.Pose.THUMB_TO_PINKY.value:
            self.joint+=1
            if self.joint>2:
                self.joint=0
            print(self.joint)
            self.ui.lbl_art.setText("joint " + str(self.joint))


    def init_buttons(self, bool):
        self.ui.btn_disconnect.setEnabled(bool)
        self.ui.btn_sleep.setEnabled(bool)

        self.ui.btn_connect2.setEnabled(False)
        self.ui.btn_disconnect2.setEnabled(False)
        self.ui.btn_sleep2.setEnabled(False)

    def enable_myo(self): #TODO
        if self.ui.cb_myo2.isChecked():
            self.ui.btn_connect2.setEnabled(True)
            self.ui.btn_disconnect2.setEnabled(False)
            self.ui.btn_sleep2.setEnabled(False)
        else:
            self.ui.btn_connect2.setEnabled(False)
            self.ui.btn_disconnect2.setEnabled(False)
            self.ui.btn_sleep2.setEnabled(False)

    def myo_run(self):
        try:
            self.thread.connect()
            self.init_buttons(True)
            self.thread.start()
        except Exception as e:
            print("error")

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

    def show_angles(self):
        angles = self.toEulerianAngle(self.thread.quat)
        self.ui.lbl_mov.setText("roll = " + str(angles.roll) + "\npitch = " + str(angles.pitch) + "\nyaw = " + str(angles.yaw))

    def toEulerianAngle(self, q):

        # # roll (x-axis rotation)
        # ysqr = q[1] * q[1]
        # t0 = +2.0 * (q[3] * q[0] + q[1] * q[2])
        # t1 = +1.0 - 2.0 * (q[0] * q[0] + ysqr)
        #
        # roll = math.atan2(t0, t1)
        #
        # # pitch (y-axis rotation)
        # t2 = +2.0 * (q[3] * q[1] - q[2] * q[0])
        #
        # if t2 > 1.0:
        #    t2 = 1.0
        # if t2 < -1.0:
        #    t2 = -1.0
        # pitch = math.asin(t2)
        #
        # # yaw (z-axis rotation)
        # t3 = +2.0 * (q[3] * q[2] + q[0] * q[1])
        # t4 = +1.0 - 2.0 * (ysqr + q[2] * q[2])
        # yaw = math.atan2(t3, t4)

        quat = np.array(q)
        quat = quat / np.sqrt(np.dot(quat, quat))

        print(quat)


        w = quat.item(0)
        x = quat.item(1)
        y = quat.item(2)
        z = quat.item(3)

        xx = x*x
        yy = y*y
        zz = z*z
        ww = w*w

        # euler Z
        # roll = math.atan2(2.0 * (x*y + z*w),
        #                   (xx - yy - zz + ww)) * (180.0 / 3.1415)
        # a = -2.0 * (y*w - x*z)
        # # if a > 1.0:
        # #     a = 1.0
        # # if a < -1.0:
        # #     a = -1.0
        # #
        # # pitch = math.asin(a) * (180.0 / 3.1415)
        #
        # yaw = math.atan2(2.0 * (y*z + x*w),
        #                    (-xx - yy + zz + ww)) * (180.0 / 3.1415)



        roll = math.atan2(2.0 * (w * x + y * z),
                           1.0 - 2.0 * (x * x + y * y)) * (180 / 3.1415)

        pitch = math.asin(max(-1.0, min(1.0, 2.0 * (-w * y + z * x)))) * (180 / 3.1415)

        yaw = math.atan2(2.0 * (w * z + x * y),
                        1.0 - 2.0 * (y * y + z * z)) * (180 / 3.1415)

        euler_angles = collections.namedtuple('euler_angles', ['roll', 'pitch', 'yaw'])
        return euler_angles(int(roll), int(pitch), int(yaw))



if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    #myapp.setFixedSize(500,300)
    myapp.show()
    sys.exit(app.exec_())
