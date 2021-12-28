from pathlib import Path
import multiprocessing as mp
from openvino.inference_engine import IECore


class DetectionBase(mp.Process):
    def __init__(self, model_bin, model_xml, dev, ipc):
        super(DetectionBase, self).__init__()

        model_bin = Path(model_bin)
        model_xml = Path(model_xml)

        self._ipc = ipc

        ie = IECore()
        net = ie.read_network(model=model_xml, weights=model_bin)

        input_blob = next(iter(net.input_info))
        out_blob = next(iter(net.outputs))

        net.input_info[input_blob].precision = 'FP32'
        net.outputs[out_blob].precision = 'FP16'

        self.exec_net = ie.load_network(network=net, device_name=dev)

    def _infrence(self, *args, **kwargs):
        raise NotImplementedError()

    def run(self, *args, **kwargs):
        raise NotImplementedError()
