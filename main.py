from __future__ import print_function

import myo_raw as myo
import sys

if __name__ == '__main__':

    m = myo.MyoRaw(sys.argv[1] if len(sys.argv) >= 2 else None)

    #m.add_arm_handler(lambda arm, xdir: print('arm', arm, 'xdir', xdir))
    #m.add_pose_handler(lambda p: print('pose', p))
    #m.add_imu_handler(lambda quat, acc, gyro: print('quat', quat, 'acc', acc, 'gyro', gyro))

    m.connect()

    try:
        while True:
            m.run(1)

    except KeyboardInterrupt:
        pass
    finally:
        m.deep_sleep()
        m.disconnect()
        print()
