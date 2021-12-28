from pathlib import Path
import multiprocessing as mp
from openvino.inference_engine import IECore
import IPC


# 消费者进程基类，继承mp.Process实现多进程及跨进程通信
# 同时也实现了探测器的功能的函数抽象
# 现在的问题是串口通讯要不要单独做一个进程？如果不做单独的进程的话看看他的发送是否为阻塞模式。
class DetectionBase(mp.Process):
    def __init__(self, model_bin, model_xml, dev, ipc: IPC.IPCAbstract):
        super(DetectionBase, self).__init__()

        model_bin = Path(model_bin)
        model_xml = Path(model_xml)

        self._ipc = ipc

        ie = IECore()
        net = ie.read_network(model=model_xml, weights=model_bin)

        self.input_blob = next(iter(net.input_info))
        self.out_blob = next(iter(net.outputs))

        net.input_info[self.input_blob].precision = 'FP32'
        net.outputs[self.out_blob].precision = 'FP16'

        self.exec_net = ie.load_network(network=net, device_name=dev)

    def _preprocess(self, *args, **kwargs):
        return self._ipc.pull()

    def _infrence(self, *args, **kwargs):
        raise NotImplementedError()

    def _postprocess(self, *args, **kwargs):
        raise NotImplementedError()

    def run(self, *args, **kwargs):
        raise NotImplementedError()
