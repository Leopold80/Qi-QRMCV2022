import multiprocessing as mp
import time

import cv2

import IPC


class CameraStream(mp.Process):
    def __init__(self, ipc: IPC.IPCAbstract, src):
        super(CameraStream, self).__init__()
        self._ipc = ipc
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
