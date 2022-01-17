import multiprocessing as mp
import time

import cv2

import IPC


class CameraBase(mp.Process):
    def __init__(self, ipc: IPC.IPCAbstract):
        super(CameraBase, self).__init__()
        self._ipc = ipc

    def set_camera(self, **camera_args):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
