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
        # 模型权重文件路径
        model_bin = Path(model_bin)
        # 模型结构文件路径
        model_xml = Path(model_xml)

        # 多进程通信模块
        self._ipc = ipc

        # 加载推理引擎
        ie = IECore()
        # 读取网络
        net = ie.read_network(model=model_xml, weights=model_bin)

        # 输入输出信息
        self.input_blob = next(iter(net.input_info))
        self.out_blob = next(iter(net.outputs))

        # 设置输入输出精度
        net.input_info[self.input_blob].precision = 'FP32'
        net.outputs[self.out_blob].precision = 'FP16'

        # 加载可执行网络
        self.exec_net = ie.load_network(network=net, device_name=dev)

    # 图像预处理
    def _preprocess(self, *args, **kwargs):
        return self._ipc.pull()

    # 推理
    def _infrence(self, *args, **kwargs):
        raise NotImplementedError()

    # 推理结果后处理
    def _postprocess(self, *args, **kwargs):
        raise NotImplementedError()

    # 线程运行核心函数
    def run(self, *args, **kwargs):
        raise NotImplementedError()
