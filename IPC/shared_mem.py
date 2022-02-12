from .ipc_abstract import IPCAbstract


"""
参考资料
https://docs.python.org/zh-cn/3/library/multiprocessing.shared_memory.html

python3.7尚不支持SharedMemory 先搁起来吧 以后把python升级到3.8就可以了
"""


class SHM(IPCAbstract):
    def __init__(self, ipc):
        super().__init__(ipc)

    def push(self, data):
        pass

    def pull(self):
        pass
