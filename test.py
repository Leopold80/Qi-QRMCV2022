import IPC
import videostream

import multiprocessing as mp
import cv2
from time import time
from loguru import logger
import detection


class Consumer(mp.Process):
    def __init__(self, ipc: IPC.IPCAbstract):
        super(Consumer, self).__init__()
        self.ipc = ipc

    def run(self):
        while True:
            time_, img = self.ipc.pull()
            cv2.imshow("video", img)
            dt = time() - time_
            logger.info("delta time {} ms".format(dt * 1000))
            cv2.waitKey(2)


if __name__ == "__main__":
    d = detection.DetectionBase(
        model_bin="detection/nn_network/yolox_nano_416/yolox_nano.bin",
        model_xml="detection/nn_network/yolox_nano_416/yolox_nano.xml",
        dev="CPU",
        ipc=None
    )
