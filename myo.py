
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from PyQt4.QtCore import QSize

from myo_ui import Ui_MainWindow

import myo_raw as myo

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import random, serial, time, glob, enum, math, collections, sys, re
import serial.tools.list_ports
import numpy as np

from serial.tools.list_ports import comports

import threading

#pyuic4 myo.ui > myo_ui.py

#ln -s /usr/lib/python3.6/site-packages/PyQt4/ ~/.virtualenvs/seagull/lib/python3.6/site-packages/
#ln -s /usr/lib/python3.6/site-packages/sip.so ~/.virtualenvs/seagull/lib/python3.6/site-packages/

mov_range = collections.namedtuple('mov_range', ['min', 'max'])

# r_shoulder_frontal_ext = mov_range(95, 145)
# r_shoulder_lateral_ext = mov_range(50, 99)
# r_biceps_rot = mov_range(50, 90)
# r_elbow_flex = mov_range(45, 96)

th = 5;

l_shoulder_frontal_ext = mov_range(20+th, 110-th)
l_shoulder_lateral_ext = mov_range(95+th, 150-th)
l_biceps_rot = mov_range(45+th, 105-th)
l_elbow_flex = mov_range(17+th, 90-th)


def toEulerianAngle(q):
    # normalization
    quat = np.array(q)
    quat = quat / np.sqrt(np.dot(quat, quat))

    w = quat.item(0)
    x = quat.item(1)
    y = quat.item(2)
    z = quat.item(3)

    roll = math.atan2(2.0 * (w * x + y * z),
                       1.0 - 2.0 * (x * x + y * y)) * (180 / 3.1415)

    pitch = math.asin(max(-1.0, min(1.0, 2.0 * (-w * y + z * x)))) * (180 / 3.1415)

    yaw = math.atan2(2.0 * (w * z + x * y),
                    1.0 - 2.0 * (y * y + z * z)) * (180 / 3.1415)

    euler_angles = collections.namedtuple('euler_angles', ['roll', 'pitch', 'yaw'])
    return euler_angles(int(roll), int(pitch), int(yaw))

def pitch_to_servo(joint, rawValue):
    p_min = 90
    p_max = -90
    position = 0

    if (joint==Joint.SHOULDER_FRONT.value):
        position = (((-rawValue - p_min) * (l_shoulder_frontal_ext.max - l_shoulder_frontal_ext.min)) / (p_max - p_min)) + l_shoulder_frontal_ext.min
    elif (joint==Joint.SHOULDER_LAT.value):
        position = (((rawValue - p_min) * (l_shoulder_lateral_ext.max - l_shoulder_lateral_ext.min)) / (p_max - p_min)) + l_shoulder_lateral_ext.min
    elif (joint==Joint.BICEPS.value):
        position = (((rawValue - p_min) * (l_biceps_rot.max - l_biceps_rot.min)) / (p_max - p_min)) + l_biceps_rot.min
    elif (joint==Joint.ELBOW.value):
        position = (((-rawValue - p_min) * (l_elbow_flex.max - l_elbow_flex.min)) / (p_max - p_min)) + l_elbow_flex.min
    return position

class MyoThread(QtCore.QThread):

    myo_stop_signal = False

    pose = []
    quat = []
    acc = []
    gyro = []
    joint = 0
    angles = []
    servo_position = 0

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.m = []

    def set_myo_stop_signal(self, bool):
        self.myo_stop_signal = bool

    def save_pose(self, p):
        self.pose = p
        self.emit(QtCore.SIGNAL("pose_px(QString)"),str(p.value))
        if p.value==myo.Pose.THUMB_TO_PINKY.value:
            self.joint+=1
            if self.joint>4:
                self.joint=0
            print(self.joint)

    def save_imu(self, quat, acc, gyro):
        self.quat = quat
        self.acc = acc
        self.gyro = gyro
        # print(quat)

    def connect(self):
        self.m = myo.MyoRaw()
        #self.m.add_arm_handler(lambda arm, xdir: print('arm', arm, 'xdir', xdir))
        self.m.add_pose_handler(lambda p: self.save_pose(p))
        self.m.add_imu_handler(lambda quat, acc, gyro: self.save_imu(quat, acc, gyro))
        self.m.connect()

    def run(self):
        self.set_myo_stop_signal(False)

        t = time.time()
        try:
            while self.myo_stop_signal==False:
                self.m.run(1)
                t2 = time.time()
                if t2-t>0.3:
                    self.angles = toEulerianAngle(self.quat)
                    self.servo_position = self.pitch_to_servo()
                    self.emit(QtCore.SIGNAL("imu()"))
                    t = t2;
        except Exception as e:
            print(str(e))
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

    def pitch_to_servo(self):
        p_min = 90
        p_max = -90
        position = 0

        if (self.joint==Joint.SHOULDER_FRONT.value):
            position = (((-self.angles.pitch - p_min) * (l_shoulder_frontal_ext.max - l_shoulder_frontal_ext.min)) / (p_max - p_min)) + l_shoulder_frontal_ext.min
        elif (self.joint==Joint.SHOULDER_LAT.value):
            position = (((self.angles.pitch - p_min) * (l_shoulder_lateral_ext.max - l_shoulder_lateral_ext.min)) / (p_max - p_min)) + l_shoulder_lateral_ext.min
        elif (self.joint==Joint.BICEPS.value):
            position = (((self.angles.pitch - p_min) * (l_biceps_rot.max - l_biceps_rot.min)) / (p_max - p_min)) + l_biceps_rot.min
        elif (self.joint==Joint.ELBOW.value):
            position = (((-self.angles.pitch - p_min) * (l_elbow_flex.max - l_elbow_flex.min)) / (p_max - p_min)) + l_elbow_flex.min

        return position

class Joint(enum.Enum) :
    SHOULDER_FRONT = 1
    BICEPS = 2
    SHOULDER_LAT = 3
    ELBOW = 4

class MyForm(QtGui.QMainWindow):

    x = 0
    arduino_connected = False

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
        QtCore.QObject.connect(self.ui.btn_connectArduino,QtCore.SIGNAL("clicked()"), self.arduino_serial_connect)
        QtCore.QObject.connect(self.ui.btn_send,QtCore.SIGNAL("clicked()"), self.serial_send)
        QtCore.QObject.connect(self.ui.cb_myo2,QtCore.SIGNAL("clicked()"), self.enable_myo)


        self.connect(self.thread, QtCore.SIGNAL("pose_px(QString)"), self.set_pose_px)
        self.connect(self.thread, QtCore.SIGNAL("imu()"), self.show_angles)
        # self.connect(self.thread, QtCore.SIGNAL("imu()"), self.draw)

        self.init_buttons(False)

        self.set_pose_px('0')

        # plot
        self.figure = plt.figure()
        #plt.ion() # funciona?
        self.canvas = FigureCanvas(self.figure)
        self.ui.mplvl.addWidget(self.canvas)
        #self.ui.mplvl.setSizeConstraint
        # create an axis
        self.ax = self.figure.gca(projection='3d')
        #self.ax.patch.set_facecolor('black')

        self.serial_ports()

        self.ui.lbl_art.setText("joint 0")
        #self.draw()

        #fig = plt.figure()
        #ax = fig.gca(projection='3d')
        # plt.show()

        print("1 ")
        print(pitch_to_servo(1,0))
        print("2")
        print(pitch_to_servo(2,0))
        print("3")
        print(pitch_to_servo(3,0))
        print("4")
        print(pitch_to_servo(4,0))

    def serial_ports(self):
        for p in comports():
            if not re.search(r'PID=2458:0*1', p[2]):
                self.ui.cb_port.addItem(p[0])

    def read_serial(self):
        while True:
            if self.arduino.in_waiting:
                print(self.arduino.readline())
                time.sleep(0.3)

    def arduino_serial_connect(self):
        try:
            self.arduino = serial.Serial(self.ui.cb_port.currentText(), 9600)
            self.arduino_connected = True
            self.serialThread = threading.Thread(target=self.read_serial)
            self.serialThread.daemon = True
            self.serialThread.start()
            print("Arduino connected")
        except Exception as e:
            print("Error de conexión con Arduino: " + str(e))
        finally:
            pass

    def arduino_serial_disconnect(self):
        self.arduino_connected = False
        self.arduino.close()

    def serial_send(self):
        self.send(0, 0)

    def send(self, joint, position):
        pos_1 = (position >> 8) & 0xFF
        pos_2 = (position) & 0xFF
        self.arduino.write(bytes([253]))
        self.arduino.write(bytes([joint]))
        self.arduino.write(bytes([pos_1]))
        self.arduino.write(bytes([pos_2]))
        self.arduino.write(bytes([((joint + pos_1 + pos_2) & 0xFF)]))
        self.arduino.write(bytes([254]))

    def show_angles(self):

        if (self.arduino_connected):
            self.send(int(self.thread.joint), int(self.thread.servo_position))

        # print("pos= " + str(int(self.thread.servo_position)))
        print("joint= " + str(int(self.thread.joint)))

        self.ui.lbl_art.setText("joint " + str(self.thread.joint))
        self.ui.lbl_mov.setText("roll = " + str(self.thread.angles.roll) + "\npitch = " + str(self.thread.angles.pitch) + "\nyaw = " + str(self.thread.angles.yaw))

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

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    #myapp.setFixedSize(500,300)
    myapp.show()
    sys.exit(app.exec_())
