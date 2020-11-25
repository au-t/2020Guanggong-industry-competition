# Blob Detection Example
#通讯test

import sensor, image, time,pyb
from pyb import UART
from pyb import LED
import json


test_threshold   = (30, 41, 47, 67, 42, 54)

# 更改此值以调整曝光。试试10.0 / 0.1 /等。
sensor.reset()                      # 复位并初始化传感器。
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
#设置图像色彩格式，有RGB565色彩图和GRAYSCALE灰度图两种

sensor.set_framesize(sensor.QQVGA)   # 将图像大小设置为QVGA (320x240)


sensor.skip_frames(30)     # 等待设置生效。
clock = time.clock()                # 创建一个时钟对象来跟踪FPS帧率。

# 您必须关闭自动增益控制和自动白平衡，否则他们将更改图像增益以撤消您放置的任何曝光设置...
#sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
# 需要让以上设置生效
sensor.skip_frames(time = 500)



# 默认情况下启用自动曝光控制（AEC）。调用以下功能可禁用传感器自动曝光控制。
# 另外“exposure_us”参数在AEC被禁用后覆盖自动曝光值。

uart = UART(3, 115200)#串口配置

while(True):
    clock.tick() # 追踪两个snapshots()之间经过的毫秒数.
    img = sensor.snapshot() # 拍一张照片并返回图像。

    blobs = img.find_blobs([test_threshold],pixels_threshold=50, area_threshold=50)

    if blobs:
    #如果找到了目标颜色
        for b in blobs:
        #迭代找到的目标颜色区域
            print("1")
            data0=8 #校验位,为x坐标+y坐标 的低八位
            data1=254
            data2= 254
            checkout=(data1+data2)
            data = bytearray([0xAA,data0,data1, data2,checkout,0x54])#转成16进制
             #如果识别的坐标大于255，建议除以2之后再发，因为一个字节范围只有0-255
            uart.write(data)#通过串口发送出去数据
        #print(clock.fps()) # 注意: 当连接电脑后，OpenMV会变成一半的速度。当不连接电脑，帧率会增加
