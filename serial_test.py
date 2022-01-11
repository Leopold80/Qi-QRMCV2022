from serial_io import DataOutput, SerialIO
from time import time
from loguru import logger

if __name__ == "__main__":
    data = DataOutput()
    io = SerialIO(dev="")  # 写上你的发送串口

    data.load_data(dy=3.14, dp=4.13, has_target=True)
    t1 = time() * 1000
    msg = data.encode().tostring()
    t2 = time() * 1000
    io.send(msg)
    t3 = time() * 1000

    logger.debug("encoding cost time {} ms, send data cost time {} ms".format(t2 - t1, t3 - t2))

    data.load_data(dy=0., dp=0., has_target=False)
    t1 = time() * 1000
    msg = data.encode().tostring()
    t2 = time() * 1000
    io.send(msg)
    t3 = time() * 1000

    logger.debug("encoding cost time {} ms, send data cost time {} ms".format(t2 - t1, t3 - t2))
