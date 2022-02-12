from pathlib import Path

import cv2
import numpy as np
import yaml

import IPC
import angle_solver
import camera
import detection
from serial_io import DataOutput


class SinglePointDetectCall:
    def __init__(self, armorinfo):
        self._anglesolver = angle_solver.SinglePointSolver()
        self._iodata = DataOutput()
        self._armorinfo = armorinfo

    def __call__(self, img, dets):
        if dets is None:
            self._iodata.load_data(0., 0., 0., False)
            msg = self._iodata.encode().tostring()
        else:
            # 根据评分给装甲板候选框排序
            dets = self._score_boxes(dets)
            armor = dets[0]
            # 求解矩形框中心点
            c = np.zeros([2], dtype=armor.dtype)
            c[0] = .5 * (armor[0] + armor[2])
            c[1] = .5 * (armor[1] + armor[3])
            # 角度解算
            ax, ay, _ = self._anglesolver.get_angle(c)
            # 数据编码
            self._iodata.load_data(ax[0], ay[0], 0., True)
            msg = self._iodata.encode().tostring()

        # 画图
        if dets is not None:
            x1, y1, x2, y2 = armor[:4].astype(np.int32)
            cv2.rectangle(img, (x1, y1), (x2, y2), color=(255, 0, 255), thickness=3)
            cv2.putText(img, "ax:{:.2f}, ay:{:.2f}".format(ax[0], ay[0]),
                        (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), thickness=2)
        cv2.imshow("vis", img)
        cv2.waitKey(1)
        return msg

    def _score_boxes(self, dets):
        """
        给每个检测出来的装甲板候选框评分 并排序
        """
        sorted(dets, key=self.sorted_key, reverse=True)
        return dets

    def sorted_key(self, x):
        conf = x[4]
        x1, y1, x2, y2 = x[:4]
        s = (x2 - x1) * (y2 - y1)
        r = abs(self._armorinfo["r"] - (x2 - x1) / (y2 - y1))
        return conf * 0.2 + s * 0.3 + r * 0.3


if __name__ == '__main__':
    ipc = IPC.IPC()
    producer = camera.UVCCamera(ipc=ipc, src=1)
    consumer = detection.YOLOXDetection(
        ipc=ipc,
        dev="CPU",
        serial_dev="/dev/ttyUSB0",
        callback_fn=SinglePointDetectCall(armorinfo={"r": 135.8 / 55.11}),
        model_dir="detection/nn_network/nano_tr.onnx"
    )

    producer.start()
    consumer.start()
    producer.join()
    consumer.join()
