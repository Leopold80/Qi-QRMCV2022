from multiprocessing import SimpleQueue, get_context

from .ipc_abstract import IPCAbstract


class RTQueue(SimpleQueue().__class__):
    """
    继承simpleQueue，新增get_latest函数，为了获取最新的（即生产者最新返回的）数据
    """

    def __init__(self, ctx=get_context()):
        super().__init__(ctx=ctx)

    def get_latest(self):
        if self.empty():
            return self.get()
        data = None
        while not self.empty():
            data = self.get()
        return data


class Queue(IPCAbstract):
    def __init__(self):
        super().__init__(RTQueue())

    def push(self, data):
        self._ipc.put(data)

    def pull(self):
        return self._ipc.get_latest()
