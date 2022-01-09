from serial_io import DataOutput

d = DataOutput()

d.load_data(3., 4., 5.)
res = d.encode()
print(res)
