import multiprocessing as mp
import time

import cv2
from .camera_base import CameraBase

import IPC


class UVCCamera(CameraBase):
    def __init__(self, ipc: IPC.IPCAbstract, src):
        super(UVCCamera, self).__init__(ipc)
        self.src = src

    def set_camera(self, **camera_args):
        pass

    def run(self):
        cap = cv2.VideoCapture(self.src)
        while True:
            ret, fr = cap.read()
            if not ret or fr is None:
                break
            self._ipc.push((time.time(), fr))
