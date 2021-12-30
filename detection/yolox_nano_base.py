from detection_base import DetectionBase
from pathlib import Path
import multiprocessing as mp
from openvino.inference_engine import IECore
import IPC


class YOLOXNanoDetection(DetectionBase):
    def __init__(self):
        super(YOLOXNanoDetection, self).__init__()

    def _preprocess(self, *args, **kwargs):
        pass

    def _infrence(self, *args, **kwargs):
        pass

    def _postprocess(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass


