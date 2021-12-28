import multiprocessing as mp
from .ipc_abstract import IPCAbstract


class SHM(IPCAbstract):
    def push(self, *args, **kwargs):
        pass

    def pull(self, *args, **kwargs):
        pass

    def __init__(self):
        pass
