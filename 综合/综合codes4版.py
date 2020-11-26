import sensor, image, time, pyb
from pyb import UART
from pyb import LED
import json
# 为了使色彩追踪效果真的很好，你应该在一个非常受控制的照明环境中。
# 设置各个颜色的阈值，括号里面的数值分别是L A B 的最大值和最小值（minL, maxL, minA,
# maxA, minB, maxB），LAB的值在图像左侧三个坐标图中选取。
pink_threshold =(11, 17, 21, 30, 11, 24)                  #粉色障碍物
purple_threshold =(9, 16, -2, 12, -10, 8)                 #紫色停车区
brown_threshold =(16, 24, 19, 33, 8, 24)                  #棕色收货区
depart_threshold =(25, 31, -11, 1, 25, 34)                #黄色出发区
#红绿灯阈值
#red_threshold=(95, 98, -21, -8, 34, 61)                   #红灯
#yellow_threshold=(99, 100, -10, 5, -7, 20)                #黄灯
green_threshold= (92, 100, -28, 1, -8, 1)               #绿灯


## 更改此值以调整曝光。试试10.0 / 0.1 /等。
#EXPOSURE_TIME_SCALE = 0.49

sensor.reset() # 初始化sensor
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QQVGA) # 使用QQVGA的速度。(160*120)
#设置图像像素大小

# 打印出初始曝光时间以进行比较。
#print("Initial exposure == %d" % sensor.get_exposure_us())

sensor.skip_frames(time=200)         # 等待设置生效。
clock = time.clock()           # 创建一个时钟对象来跟踪FPS帧率。

# 您必须关闭自动增益控制和自动白平衡，否则他们将更改图像增益以撤消您放置的任何曝光设置...
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
# 需要让以上设置生效
sensor.skip_frames(time = 500)

#clock = time.clock() # 跟踪FPS帧率
#current_exposure_time_in_microseconds = sensor.get_exposure_us()
#print("Current Exposure == %d" % current_exposure_time_in_microseconds)

# 默认情况下启用自动曝光控制（AEC）。调用以下功能可禁用传感器自动曝光控制。
# 另外“exposure_us”参数在AEC被禁用后覆盖自动曝光值。
#sensor.set_auto_exposure(False, \
    #exposure_us = int(current_exposure_time_in_microseconds * EXPOSURE_TIME_SCALE))

#串口初始化Openmv
uart = UART(3, 115200)                          ##串口3，波特率115200
uart.init(115200, bits=8, parity=None, stop=1)  #8位数据位，无校验位，1位停止位

#area_threshold 面积阈值，如果色块被框起来的面积小于这个值，会被过滤掉
#pixels_threshold 像素个数阈值，如果色块像素数量小于这个值，会被过滤掉
#blobs_pink = img.find_blobs([pink_threshold],pixels_threshold=50, area_threshold=50)
#blobs_purple = img.find_blobs([purple_threshold],pixels_threshold=50, area_threshold=50)
#blobs_brown = img.find_blobs([brown_threshold],pixels_threshold=50, area_threshold=50)
#blobs_depart = img.find_blobs([depart_threshold],pixels_threshold=50, area_threshold=50)
#blobs_red = img.find_blobs([red_threshold],pixels_threshold=50, area_threshold=50, merge=True, margin=10)
#blobs_yellow = img.find_blobs([yellow_threshold],pixels_threshold=50, area_threshold=50, merge=True, margin=10)
#blobs_green = img.find_blobs([green_threshold],pixels_threshold=50, area_threshold=50, merge=True, margin=10)

#blobs = img.find_blobs([test_threshold],pixels_threshold=50, area_threshold=50)


while(True):
    clock.tick() # 追踪两个snapshots()之间经过的毫秒数.
    img = sensor.snapshot() # 拍一张照片并返回图像。
    blobs_pink = img.find_blobs([pink_threshold],pixels_threshold=25, area_threshold=25)
    blobs_purple = img.find_blobs([purple_threshold],pixels_threshold=50, area_threshold=50)
    blobs_brown = img.find_blobs([brown_threshold],pixels_threshold=50, area_threshold=50)
    blobs_depart = img.find_blobs([depart_threshold],pixels_threshold=50, area_threshold=50)
    #blobs_red = img.find_blobs([red_threshold],pixels_threshold=50, area_threshold=50, merge=True, margin=10)
    #blobs_yellow = img.find_blobs([yellow_threshold],pixels_threshold=50, area_threshold=50, merge=True, margin=10)
    blobs_green = img.find_blobs([green_threshold],pixels_threshold=50, area_threshold=50, merge=True, margin=10)
    # QRcode识别
    #img.lens_corr(1.8) # 1.8的强度参数对于2.8mm镜头来说是不错的。
    for code in img.find_qrcodes():
        img.draw_rectangle(code.rect(), color = (255, 0, 0)) #测试
        if (code.payload() == '1'):
            data1=0x01
            data2=0x00
            checkout=(data1+data2)   #取其低八位
            data = bytearray([0xAA,0x01,data1, data2,checkout,0x54])#转成16进制
            uart.write(data)#通过串口发送出去数据

        if (code.payload() == '2'):
            data1=0x02
            data2=0x00
            checkout=(data1+data2)   #取其低八位
            data = bytearray([0xAA,0x01,data1, data2,checkout,0x54])#转成16进制
            uart.write(data)#通过串口发送出去数据

        if (code.payload() == '11'):
            data1=0x03
            data2=0x00
            checkout=(data1+data2)   #取其低八位
            data = bytearray([0xAA,0x01,data1, data2,checkout,0x54])#转成16进制
            uart.write(data)#通过串口发送出去数据

        if (code.payload() == '12'):
            data1=0x04
            data2=0x00
            checkout=(data1+data2)   #取其低八位
            data = bytearray([0xAA,0x01,data1, data2,checkout,0x54])#转成16进制
            uart.write(data)#通过串口发送出去数据

        if (code.payload() == '21'):
            data1=0x05
            data2=0x00
            checkout=(data1+data2)   #取其低八位
            data = bytearray([0xAA,0x01,data1, data2,checkout,0x54])#转成16进制
            uart.write(data)#通过串口发送出去数据

        if (code.payload() == '22'):
            data1=0x06
            data2=0x00
            checkout=(data1+data2)   #取其低八位
            data = bytearray([0xAA,0x01,data1, data2,checkout,0x54])#转成16进制
            uart.write(data)#通过串口发送出去数据)




    # 粉色障碍物识别
    if blobs_pink:
        # 如果找到了目标颜色
        for b in blobs_pink:
            # 找到的目标颜色区域
            img.draw_rectangle(b[0:4])  # rect 测试（可注释）
            # 用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6])  # cx, cy 测试（可注释）
            # 在目标颜色区域的中心画十字形标记
            #print(b[5], b[6])   #输出中心坐标
            #data0=0x02
            data1=b[5]
            data2=b[6]
            checkout=(data1+data2)   #取其低八位
            #bytearray为可变序列的字节数组 返回一个新的字节数组（将数据转为16进制）
            data = bytearray([0xAA,0x02,data1, data2,checkout,0x54])#转成16进制
             #如果识别的坐标大于255，建议除以2之后再发，因为一个字节范围只有0-255
            uart.write(data)#通过串口发送出去数据
            print("pink")

     # 找紫色停车区
    if blobs_purple:
        for b in blobs_purple:
            img.draw_rectangle(b[0:4])  # rect 测试（可注释）
            # 用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6])  # cx, cy 测试（可注释）
            # 在目标颜色区域的中心画十字形标记
            #print(b[5], b[6])   #输出中心坐标
            #data0=0x03
            data1=b[5]
            data2=b[6]
            checkout=(0x03+data1+data2)   #取其低八位
            #bytearray为可变序列的字节数组 返回一个新的字节数组（将数据转为16进制）
            data = bytearray([0xAA,0x03,data1, data2,checkout,0x54])#转成16进制
            uart.write(data)#通过串口发送出去数据)
            print("puple")


    for c in img.find_circles(threshold = 3500, x_margin = 8, y_margin = 8, r_margin = 10,
            r_min = 2, r_max = 80, r_step = 2):
        area = (c.x()-c.r(), c.y()-c.r(), 2*c.r(), 2*c.r())
        #area为识别到的圆的区域，即圆的外接矩形框
        statistics = img.get_statistics(roi=area)#像素颜色统计
        #如(0,100,0,120,0,120)是红色的阈值，范围在这个阈值内，就说明是红色的圆。
        #l_mode()，a_mode()，b_mode()是L通道，A通道，B通道的众数。
        #绿灯
        if blobs_green:
            for b in blobs_green:
                img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))  #测试（可注释）
                print("green")
                data0=0x04
                data1=0x00
                data2=0x00
                checkout=(data1+data2)   #取其低八位
                data = bytearray([0xAA,data0,0x00,0x00,checkout,0x54])
                uart.write(data)



    # 找棕色收货区域
    if  blobs_brown:
    #如果找到了目标颜色
        for b in blobs_brown:
            img.draw_rectangle(b[0:4])  # rect 测试（可注释）
            # 用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6])  # cx, cy 测试（可注释）
            # 在目标颜色区域的中心画十字形标记
            #print(b[5], b[6])   #输出中心坐标
            data0=0x05
            data1=b[5]
            data2=b[6]
            checkout=(data0+data1+data2)   #取其低八位
            #bytearray为可变序列的字节数组 返回一个新的字节数组（将数据转为16进制）
            data = bytearray([0xAA,data0,data1, data2,checkout,0x54])#转成16进制
            uart.write(data)#通过串口发送出去数据)
            print("brown")


    #找最后的黄色停车区
    if blobs_depart:
        for b in blobs_depart:
            img.draw_rectangle(b[0:4])  # rect 测试（可注释）
            # 用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6])  # cx, cy 测试（可注释）
            # 在目标颜色区域的中心画十字形标记
            #print(b[5], b[6])   #输出中心坐标
            data0=0x06
            data1=b[5]
            data2=b[6]
            checkout=(data0+data1+data2)   #取其低八位
            #bytearray为可变序列的字节数组 返回一个新的字节数组（将数据转为16进制）
            data = bytearray([0xAA,data0,data1, data2,checkout,0x54])#转成16进制
            uart.write(data)#通过串口发送出去数据)
            print("depart")


    #print(clock.fps()) # 注意: 当连接电脑后，OpenMV会变成一半的速度。当不连接电脑，帧率会增加
