import serial


class SerialIO:
    def __init__(self, dev):
        self._io = serial.Serial(
            port=dev,
            parity=serial.PARITY_EVEN,
            baudrate=115200,
            stopbits=1
        )
        self._io.close()
        self._io.open()

    def __del__(self):
        pass
        self._io.close()

    def send(self, data):
        self._io.write(data)
        self._io.flush()

    def recv(self):
        pass
