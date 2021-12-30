import cv2
import numpy as np

from detection.utils import multiclass_nms
from .detection_base import DetectionBase
from pathlib import Path
import multiprocessing as mp
from openvino.inference_engine import IECore
import IPC


class YOLOXDetection(DetectionBase):
    def __init__(self, ipc, model_bin, model_xml, dev):
        super(YOLOXDetection, self).__init__(ipc=ipc)

        model_bin = Path(model_bin)
        model_xml = Path(model_xml)

        ie = IECore()
        net = ie.read_network(model=model_xml, weights=model_bin)
        self.input_blob = next(iter(net.input_info))
        self.out_blob = next(iter(net.outputs))
        net.input_info[self.input_blob].precision = 'FP32'
        net.outputs[self.out_blob].precision = 'FP16'
        _, _, self.h, self.w = net.input_info[self.input_blob].input_data.shape

        self.exec_net = ie.load_network(network=net, device_name=dev)

    def _preprocess(self, img, swap=(2, 0, 1)):
        if len(img.shape) == 3:
            padded_img = np.ones((self.h, self.w, 3), dtype=np.uint8) * 114
        else:
            padded_img = np.ones((self.h, self.w), dtype=np.uint8) * 114

        r = min(self.h / img.shape[0], self.w / img.shape[1])
        resized_img = cv2.resize(
            img,
            (int(img.shape[1] * r), int(img.shape[0] * r)),
            interpolation=cv2.INTER_LINEAR,
        ).astype(np.uint8)
        padded_img[: int(img.shape[0] * r), : int(img.shape[1] * r)] = resized_img
        padded_img = padded_img.transpose(swap)
        padded_img = np.ascontiguousarray(padded_img, dtype=np.float32)
        return padded_img, r

    def _infrence(self, img):
        image, ratio = self._preprocess(img)
        res = self.exec_net.infer(inputs={self.input_blob: image})
        res = res[self.out_blob]
        predictions = self._postprocess(res, p6=False)[0]

        boxes = predictions[:, :4]
        scores = predictions[:, 4, None] * predictions[:, 5:]

        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2.
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2.
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2.
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2.
        boxes_xyxy /= ratio
        dets = multiclass_nms(boxes_xyxy, scores, nms_thr=0.45, score_thr=0.1)
        final_boxes = None
        final_scores = None
        final_cls_inds = None
        if dets is not None:
            final_boxes = dets[:, :4]
            final_scores, final_cls_inds = dets[:, 4], dets[:, 5]

        return final_boxes, final_scores, final_cls_inds

    def _postprocess(self, outputs, p6=False):
        grids = list()
        expanded_strides = list()

        if not p6:
            strides = [8, 16, 32]
        else:
            strides = [8, 16, 32, 64]

        hsizes = [self.h // stride for stride in strides]
        wsizes = [self.w // stride for stride in strides]

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
        pass
