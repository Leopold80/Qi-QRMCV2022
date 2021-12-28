# 尝试一下共享内存的通信方式？ 参考：https://docs.python.org/zh-cn/3/library/multiprocessing.shared_memory.html
from .ipc_abstract import IPCAbstract
from .rtqueue import Queue

IPC = Queue
