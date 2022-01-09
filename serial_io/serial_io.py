import serial


class SerialIO:
    def __init__(self, dev):
        self._io = serial.Serial(
            port=dev,
            parity=serial.PARITY_EVEN,
        )

    def send(self, data):
        self._io.write(data)
        self._io.flush()

    def recv(self):
        pass
