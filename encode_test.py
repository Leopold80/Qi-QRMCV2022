from serial_io import DataOutput

d = DataOutput()

d.load_data(3., 4., 5.)
d._encode()
print(d._u8datas)
