import numpy as np

import IPC
import videostream

import multiprocessing as mp
import cv2
from time import time
from loguru import logger
import detection


if __name__ == "__main__":
    ipc = IPC.Queue()
    producer = videostream.Producer(ipc=ipc, src=0)
    consumer = detection.YOLOXDetection(ipc=ipc, dev="CPU")

    producer.start()
    consumer.start()

    producer.join()
    consumer.start()
