import serial


def init_dict():
    return {
        "baudrate": None,

    }


class SerialIO:
    def __init__(self, dev):
        self._io = serial.Serial()


s = SerialIO(114514)
