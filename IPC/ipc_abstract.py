class IPCAbstract:
    def __init__(self, ipc):
        self._ipc = ipc

    def push(self, *args, **kwargs):
        raise NotImplementedError()

    def pull(self, *args, **kwargs):
        raise NotImplementedError
