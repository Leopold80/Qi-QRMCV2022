from time import time

from loguru import logger

from serial_io import DataOutput, SerialIO

if __name__ == "__main__":
    data = DataOutput()
    s = SerialIO(dev="COM8")

    # msg = array.array("B", range(10)).tostring()
    t1 = time() * 1000.
    # s.send(msg)
    t2 = time() * 1000.

    logger.debug(t2 - t1)

    data.load_data(dy=3., dp=4., t=0., has_target=True)
    msg = data.encode().tostring()
    s.send(msg)
