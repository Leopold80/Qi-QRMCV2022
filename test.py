import cv2
import numpy as np

import IPC
import detection
import camera
import angle_solver


class DetectionPostProc:
    def __init__(self):
        self._angle_solver = angle_solver.SinglePointSolver()

    def __call__(self, img, boxes, conf, classes):
        if boxes is None:
            return
        # 求出每个矩形框的中心点
        boxes_center = np.zeros((boxes.shape[0], 2), dtype=boxes.dtype)
        boxes_center[:, 0] = .5 * (boxes[:, 0] + boxes[:, 2])  # x
        boxes_center[:, 1] = .5 * (boxes[:, 1] + boxes[:, 3])  # y
        # 每个点的x角度，每个点的y角度，每个点去除畸变后的结果
        ax, ay, undis_pnt = self._angle_solver.get_angle(boxes_center)

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
    # TODO: 该写串口了 查一下python二进制串口通信
    ipc = IPC.Queue()
    producer = camera.Producer(ipc=ipc, src=0)
    consumer = detection.YOLOXDetection(ipc=ipc, dev="CPU", callback_fn=DetectionPostProc())

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
