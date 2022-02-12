import multiprocessing as mp


class CameraBase(mp.Process):
    def __init__(self, ipc):
        super(CameraBase, self).__init__()
        self._ipc = ipc

    def set_camera(self, **camera_args):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
