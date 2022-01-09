import array
import collections


class DataOutput:
    def __init__(self):
        self._datas = collections.OrderedDict({"dy": 0, "dp": 0, "t": 0})

    def load_data(self, dy, dp, t):
        self._datas["dy"] = int(dy * 10000)
        self._datas["dp"] = int(dp * 10000)
        self._datas["t"] = int(t * 10000)

    def _encode_it(self, data):
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

    def _decode(self):
        dy = 0
        dp = 0
        t = 0
