# Qi-QRMCV2022
QI-Q RoboMaster2022 CV Algorithm
山东理工大学齐奇RoboMaster战队2022赛季自瞄算法
（搭建中）

## 文件结构
- detection -- 目标检测器  
    - detection_base.py -- 目标检测器基类
    - yolox.py          -- 生成矩形框的yolox目标检测onnx部署  
    - yolox_poly.py     -- 生成不规则四边形框的yolox_poly目标检测onnx部署  


- IPC -- 进程间通信模块  
    - ipc_abstranct.py -- 进程间通信抽象基类  
    - rtquque.py       -- 进程通信队列  
    - shared_mem.py    -- 共享内存通信  


- videostream -- 视频流  
    - camerastream.py  -- 实现了一个usb摄像头的生产者进程class  

