import numpy as np

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


def stream(src):
    cap = cv2.VideoCapture(src)
    ret, fr = cap.read()
    while ret and fr is not None:
        yield fr
        ret, fr = cap.read()


if __name__ == "__main__":
    model = detection.YOLOXDetection(
        ipc=IPC.Queue(),
        model_bin="detection/nn_network/yolox_nano_416/yolox_nano.bin",
        model_xml="detection/nn_network/yolox_nano_416/yolox_nano.xml",
        dev="CPU"
    )

    cap = stream(0)

    while True:
        fr = next(cap)
        pred = model._infrence(fr)
        # print("debug")
        for box in pred[0]:
            x1, y1, x2, y2 = box.astype(np.int)
            cv2.rectangle(fr, (x1, y1), (x2, y2), color=(255, 0, 255), thickness=3)

        cv2.imshow("video", fr)
        cv2.waitKey(2)
