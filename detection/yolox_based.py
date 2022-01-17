from pathlib import Path

import cv2
import numpy as np
from openvino.inference_engine import IECore

from detection.utils import multiclass_nms
from serial_io import SerialIO
from .detection_base import DetectionBase


def drawbox(img, boxes, conf, classes):
    # 画图
    if boxes is None:
        return
    for box in boxes:
        x1, y1, x2, y2 = box.astype(np.int)
        cv2.rectangle(img, (x1, y1), (x2, y2), color=(255, 0, 255), thickness=3)
    cv2.imshow("video", img)
    cv2.waitKey(2)


class YOLOXDetection(DetectionBase):
    def __init__(
            self,
            ipc,
            dev,
            serial_dev="/dev/ttyUSB0",
            callback_fn=drawbox,
            model_bin="detection/nn_network/yolox_nano_416/yolox_nano.bin",
            model_xml="detection/nn_network/yolox_nano_416/yolox_nano.xml"
    ):
        super(YOLOXDetection, self).__init__(ipc=ipc, callback_fn=callback_fn)

        self.model_bin = Path(model_bin)
        self.model_xml = Path(model_xml)
        self.dev = dev
        self.serial_dev = serial_dev

    # 图像预处理
    def _preprocess(self, img, size, swap=(2, 0, 1)):
        h, w = size
        if len(img.shape) == 3:
            padded_img = np.ones((h, w, 3), dtype=np.uint8) * 114
        else:
            padded_img = np.ones((h, w), dtype=np.uint8) * 114

        r = min(h / img.shape[0], w / img.shape[1])
        resized_img = cv2.resize(
            img,
            (int(img.shape[1] * r), int(img.shape[0] * r)),
            interpolation=cv2.INTER_LINEAR,
        ).astype(np.uint8)
        padded_img[: int(img.shape[0] * r), : int(img.shape[1] * r)] = resized_img
        padded_img = padded_img.transpose(swap)
        padded_img = np.ascontiguousarray(padded_img, dtype=np.float32)
        return padded_img, r

    def _inference(self, exec_net, out_blob, size, img):
        pass

    def _postprocess(self, outputs, size, p6=False):
        h, w = size
        grids = list()
        expanded_strides = list()

        if not p6:
            strides = [8, 16, 32]
        else:
            strides = [8, 16, 32, 64]

        hsizes = [h // stride for stride in strides]
        wsizes = [w // stride for stride in strides]

        for hsize, wsize, stride in zip(hsizes, wsizes, strides):
            xv, yv = np.meshgrid(np.arange(wsize), np.arange(hsize))
            grid = np.stack((xv, yv), 2).reshape(1, -1, 2)
            grids.append(grid)
            shape = grid.shape[:2]
            expanded_strides.append(np.full((*shape, 1), stride))

        grids = np.concatenate(grids, 1)
        expanded_strides = np.concatenate(expanded_strides, 1)
        outputs[..., :2] = (outputs[..., :2] + grids) * expanded_strides
        outputs[..., 2:4] = np.exp(outputs[..., 2:4]) * expanded_strides

        return outputs

    def run(self, *args, **kwargs):
        # init infrence modules
        ie = IECore()
        net = ie.read_network(model=self.model_xml, weights=self.model_bin)
        input_blob = next(iter(net.input_info))
        out_blob = next(iter(net.outputs))
        net.input_info[input_blob].precision = 'FP32'
        net.outputs[out_blob].precision = 'FP16'
        _, _, h, w = net.input_info[input_blob].input_data.shape
        exec_net = ie.load_network(network=net, device_name=self.dev)

        # init serial io
        _io = SerialIO(dev=self.serial_dev)

        while True:
            # 从生产者线程读取图像
            t, img = self._ipc.pull()
            # 图像预处理
            image, ratio = self._preprocess(img, (h, w))
            # 前向推理
            res = exec_net.infer(inputs={input_blob: image})[out_blob]
            # 后处理
            predictions = self._postprocess(res, (h, w), p6=False)[0]

            # 预测框
            boxes = predictions[:, :4]
            # 预测框置信度
            scores = predictions[:, 4, None] * predictions[:, 5:]
            # 左上右下格式的预测框
            boxes_xyxy = np.ones_like(boxes)
            boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2.
            boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2.
            boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2.
            boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2.
            boxes_xyxy /= ratio
            # 非极大值抑制
            dets = multiclass_nms(boxes_xyxy, scores, nms_thr=0.45, score_thr=0.1)
            final_boxes = None
            final_scores = None
            final_cls_inds = None
            if dets is not None:
                final_boxes = dets[:, :4]
                final_scores, final_cls_inds = dets[:, 4], dets[:, 5]

            # final_boxes = np.ascontiguousarray(final_boxes)
            # final_scores = np.ascontiguousarray(final_scores)
            # final_cls_inds = np.ascontiguousarray(final_cls_inds)

            msg = self._callback_fn(img, final_boxes, final_scores, final_cls_inds)
            if msg is not None:
                _io.send(msg)
