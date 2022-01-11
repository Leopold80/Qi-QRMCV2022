import cv2
import numpy as np
from loguru import logger

import IPC
import detection
import camera
import angle_solver
from serial_io import DataOutput, SerialIO


class DetectionPostProc:
    def __init__(self):
        self._angle_solver = angle_solver.SinglePointSolver()
        self._data = DataOutput()
        # self._io = SerialIO(dev="ttyUSB0")

    def __call__(self, img, boxes, conf, classes):
        """目前测试先试着跟踪人"""
        if boxes is None:
            return

        """
        装甲板筛选：1.目标置信度
                  2.目标面积
                  3.目标凸度（参考东南大学开源）
                  4.和上一帧目标的欧氏距离或曼哈顿距离
        """

        # 只保留人的识别结果
        keep_idx = (classes == 0)
        boxes = boxes[keep_idx]
        conf = conf[keep_idx]
        classes = classes[keep_idx]

        # 找出最大的置信度
        confmax_idx = np.argmax(conf) if len(conf) != 0 else None

        if confmax_idx is not None:
            boxes = np.expand_dims(boxes[confmax_idx], axis=0)
            conf = np.expand_dims(conf[confmax_idx], axis=0)
            classes = np.expand_dims(classes[confmax_idx], axis=0)

            # 求出矩形框的中心点
            boxes_center = np.zeros((boxes.shape[0], 2), dtype=boxes.dtype)
            boxes_center[:, 0] = .5 * (boxes[:, 0] + boxes[:, 2])  # x
            boxes_center[:, 1] = .5 * (boxes[:, 1] + boxes[:, 3])  # y
            # 点的x角度，点的y角度，点去除畸变后的结果
            ax, ay, undis_pnt = self._angle_solver.get_angle(boxes_center)
        else:
            boxes_center = np.zeros((0, 2))
            ax = np.zeros((0,))
            ay = np.zeros((0,))
            undis_pnt = np.zeros((0, 2))

        # 加载数据并进行编码
        self._data.load_data(ax[0], ay[0], 0., True) if confmax_idx is not None \
            else self._data.load_data(0., 0., 0., False)
        msg = self._data.encode()

        # logger.debug(msg)
        # logger.debug(msg.tostring())
        # prev = self._data.decode(msg)
        # logger.debug(prev)

        # 发送串口数据
        # self._io.send(msg.tostring())

        # 画图
        for box, cbox, undis_cbox, anglex, angley in zip(boxes, boxes_center, undis_pnt, ax, ay):
            x1, y1, x2, y2 = box.astype(np.int)
            cx, cy = cbox.astype(np.int)
            ucx, ucy = undis_cbox.astype(np.int)
            anglex = anglex.astype(np.int)
            angley = angley.astype(np.int)

            # 画矩形框
            cv2.rectangle(img, (x1, y1), (x2, y2), color=(255, 0, 255), thickness=3)
            # 画中心点
            cv2.circle(img, (cx, cy), 3, (0, 0, 255), thickness=3)
            # 画消除畸变后中心点
            cv2.circle(img, (ucx, ucy), 3, (255, 0, 0), thickness=3)
            # 写角度
            cv2.putText(img, "ax:{}, ay:{}".format(anglex, angley),
                        (ucx, ucy + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255))

        cv2.imshow("video", img)
        cv2.waitKey(2)


if __name__ == "__main__":
    ipc = IPC.Queue()
    producer = camera.Producer(ipc=ipc, src=0)
    consumer = detection.YOLOXDetection(ipc=ipc, dev="CPU", callback_fn=DetectionPostProc())

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
