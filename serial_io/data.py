import array
import collections


class DataOutput:
    def __init__(self):
        self._datas = collections.OrderedDict({"dy": 0, "dp": 0, "t": 0})

    def load_data(self, dy, dp, t):
        # dy：yaw轴角度偏移量 dp：pitch轴角度偏移量 t：时间
        self._datas["dy"] = int(dy * 10000)
        self._datas["dp"] = int(dp * 10000)
        self._datas["t"] = int(t * 10000)

    def _encode_it(self, data):
        # 将uint32的数据拆散成四个uint8数据
        res = []  # u8
        for i in range(4):
            res.append((data >> 8 * (3 - i)) & 0xff)
        return res

    def encode(self):
        encoded = [self._encode_it(x) for x in self._datas.values()]
        u8datas = array.array("B")
        for e in encoded:
            u8datas.extend(e)
        return u8datas

    def decode(self, u8datas):
        # 将uint8数据重新组合回uint32数据并还原成为浮点数
        dy = (u8datas[0] << 8 * 3) | (u8datas[1] << 8 * 2) | (u8datas[2] << 8 * 1) | (u8datas[3] << 8*0)
        dp = (u8datas[4] << 8 * 3) | (u8datas[5] << 8 * 2) | (u8datas[6] << 8 * 1) | (u8datas[7] << 8*0)
        t = (u8datas[8] << 8 * 3) | (u8datas[9] << 8 * 2) | (u8datas[10] << 8 * 1) | (u8datas[11] << 8*0)
        return float(dy) / 10000., float(dp) / 10000., float(t) / 10000.
