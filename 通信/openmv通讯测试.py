# Blob Detection Example
#
# 这个例子展示了如何使用find_blobs函数来查找图像中的颜色色块。这个例子特别寻找深绿色的物体。

import sensor, image, time
from pyb import UART
from pyb import LED
import json

# 为了使色彩追踪效果真的很好，你应该在一个非常受控制的照明环境中。
green_threshold   = (25, 36, -13, 3, -2, 19)
# 设置绿色的阈值，括号里面的数值分别是L A B 的最大值和最小值（minL, maxL, minA,
# maxA, minB, maxB），LAB的值在图像左侧三个坐标图中选取。如果是灰度图，则只需
# 设置（min, max）两个数字即可。

# 你可能需要调整上面的阈值来跟踪绿色的东西…
# 在Framebuffer中选择一个区域来复制颜色设置。

sensor.reset() # 初始化sensor

sensor.set_pixformat(sensor.RGB565) # use RGB565.
#设置图像色彩格式，有RGB565色彩图和GRAYSCALE灰度图两种

sensor.set_framesize(sensor.QQVGA) # 使用QQVGA的速度。
#设置图像像素大小

sensor.skip_frames(10) # 让新的设置生效。
sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock() # 跟踪FPS帧率
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
