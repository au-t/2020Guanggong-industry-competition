# Blob Detection Example
#通讯test

import sensor, image, time,pyb
from pyb import UART
from pyb import LED
import json


green_threshold   = (25, 36, -13, 3, -2, 19)

# 更改此值以调整曝光。试试10.0 / 0.1 /等。
EXPOSURE_TIME_SCALE = 0.43

sensor.reset()                      # 复位并初始化传感器。
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
#设置图像色彩格式，有RGB565色彩图和GRAYSCALE灰度图两种

sensor.set_framesize(sensor.QQVGA)   # 将图像大小设置为QVGA (320x240)

# 打印出初始曝光时间以进行比较。
print("Initial exposure == %d" % sensor.get_exposure_us())

sensor.skip_frames(30)     # 等待设置生效。
clock = time.clock()                # 创建一个时钟对象来跟踪FPS帧率。

# 您必须关闭自动增益控制和自动白平衡，否则他们将更改图像增益以撤消您放置的任何曝光设置...
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
# 需要让以上设置生效
sensor.skip_frames(time = 500)

current_exposure_time_in_microseconds = sensor.get_exposure_us()
print("Current Exposure == %d" % current_exposure_time_in_microseconds)

# 默认情况下启用自动曝光控制（AEC）。调用以下功能可禁用传感器自动曝光控制。
# 另外“exposure_us”参数在AEC被禁用后覆盖自动曝光值。
sensor.set_auto_exposure(False, \
    exposure_us = int(current_exposure_time_in_microseconds * EXPOSURE_TIME_SCALE))
uart = UART(3, 115200)#串口配置

while(True):
    clock.tick() # 追踪两个snapshots()之间经过的毫秒数.
    img = sensor.snapshot() # 拍一张照片并返回图像。

    blobs = img.find_blobs([green_threshold],pixels_threshold=25, area_threshold=25)

    if blobs:
    #如果找到了目标颜色
        for b in blobs:
        #迭代找到的目标颜色区域
            # Draw a rect around the blob.
            #img.draw_rectangle(b[0:4]) # rect
            #用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6]) # cx, cy
            #在目标颜色区域的中心画十字形标记
            print(b[5], b[6])
            #输出目标物体中心坐标
            checkout=(b[5]+b[6])#校验位,为x坐标+y坐标 的低八位
            data = bytearray([0xAA,0x55,b[5], b[6],checkout,0x54])#转成16进制
             #如果识别的坐标大于255，建议除以2之后再发，因为一个字节范围只有0-255
            uart.write(data)#通过串口发送出去数据
        #print(clock.fps()) # 注意: 当连接电脑后，OpenMV会变成一半的速度。当不连接电脑，帧率会增加
