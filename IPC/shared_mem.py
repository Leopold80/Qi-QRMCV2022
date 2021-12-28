import multiprocessing as mp
from .ipc_abstract import IPCAbstract


class SHM(IPCAbstract):
    def __init__(self, ipc):
        super().__init__(ipc)

    def push(self, data):
        pass

    def pull(self):
        pass
