import sys, time

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

from myo_ui import Ui_Dialog

import myo_raw as myo

#pyuic4 myo.ui > myo_ui.py

class MyoThread(QtCore.QThread):

    myo_stop_signal = False

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.m = []

    def set_myo_stop_signal(self, bool):
        self.myo_stop_signal = bool

    def run(self):
        self.set_myo_stop_signal(False)
        self.m = myo.MyoRaw(sys.argv[1] if len(sys.argv) >= 2 else None)
        #self.m.add_arm_handler(lambda arm, xdir: print('arm', arm, 'xdir', xdir))
        #self.m.add_pose_handler(lambda p: print('pose', p))
        self.m.add_imu_handler(lambda quat, acc, gyro: print('quat', quat, 'acc', acc, 'gyro', gyro))
        self.m.connect()
        try:
            while self.myo_stop_signal==False:
                    self.m.run(1)
        except:
            pass
        self.disconnect()

    def disconnect(self):
        self.m.disconnect()
        print('Disconnected')

    def sleep_mode(self):
        self.set_myo_stop_signal(True)
        self.m.deep_sleep()
        print('Deep Sleep activated')


class MyForm(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.btn_connect,QtCore.SIGNAL("clicked()"), self.myo_run)
        QtCore.QObject.connect(self.ui.btn_disconnect,QtCore.SIGNAL("clicked()"), self.myo_disconnect)
        QtCore.QObject.connect(self.ui.btn_sleep,QtCore.SIGNAL("clicked()"), self.myo_deep_sleep)

        self.init_buttons(False)

        self.px_tap = QtGui.QPixmap('media/double-tap.svg')
        self.px_fist = QtGui.QPixmap('media/make-fist.svg')
        self.px_pan = QtGui.QPixmap('media/pan.svg')
        self.px_rotate = QtGui.QPixmap('media/rotate.svg')
        self.px_spread = QtGui.QPixmap('media/spread-fingers.svg')
        self.px_wleft = QtGui.QPixmap('media/wave-left.svg')
        self.px_wright = QtGui.QPixmap('media/wave-right.svg')

        self.ui.lbl_pose.setScaledContents(True)

        self.ui.lbl_pose.setPixmap(self.px_fist)

        self.thread = MyoThread()

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
        self.thread.disconnect()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.setFixedSize(500,400)
    myapp.show()
    sys.exit(app.exec_())
