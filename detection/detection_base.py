import multiprocessing as mp

import IPC


# 消费者进程基类，继承mp.Process实现多进程及跨进程通信
# 同时也实现了探测器的功能的函数抽象
# 现在的问题是串口通讯要不要单独做一个进程？如果不做单独的进程的话看看他的发送是否为阻塞模式。
class DetectionBase(mp.Process):
    def __init__(self, ipc: IPC.IPCAbstract, callback_fn):
        super(DetectionBase, self).__init__()
        # 多进程通信模块
        self._ipc = ipc
        # 回调函数
        self._callback_fn = callback_fn

    # 图像预处理
    def _preprocess(self, *args, **kwargs):
        return self._ipc.pull()

    # 推理
    def _inference(self, *args, **kwargs):
        raise NotImplementedError()

    # 推理结果后处理
    def _postprocess(self, *args, **kwargs):
        raise NotImplementedError()

    # 线程运行核心函数
    def run(self, *args, **kwargs):
        raise NotImplementedError()


