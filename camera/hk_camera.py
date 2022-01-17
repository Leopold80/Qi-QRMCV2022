from .camera_base import CameraBase

from .hkdriver import HKDriver

import numpy as np
import IPC
import time


class HKCam(CameraBase):
    def __init__(self, ipc: IPC.IPCAbstract):
        super().__init__(ipc)

    def run(self):
        driver = HKDriver()
        flag = driver.init()
        while not flag:
            flag = driver.init()
        np.array(driver)
        w, h = driver.width, driver.height

        while True:
            img = np.array(driver).reshape(h, w, 3)
            self._ipc.push((time.time(), img))

    def set_camera(self, **camera_args):
        pass
