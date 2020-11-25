from fpioa_manager import *
from fpioa_manager import fm
from machine import UART
from Maix import GPIO
import sensor, image,lcd,time,math,pyb,machine
# 为了使色彩追踪效果真的很好，你应该在一个非常受控制的照明环境中。
# 设置各个颜色的阈值，括号里面的数值分别是L A B 的最大值和最小值（minL, maxL, minA,
# maxA, minB, maxB），LAB的值在图像左侧三个坐标图中选取。
pink_threshold =                                          //粉色障碍物
purple_threshold =                                        //紫色停车区
red_threshold =                                           //红灯
yellow_threshold =                                        //黄灯
green_threshold   = (21, 51, 30, 72, 6, 63)               //绿灯
brown_threshold =                                         //棕色收货区
depart_threshold =                                        //黄色出发区

# 更改此值以调整曝光。试试10.0 / 0.1 /等。
EXPOSURE_TIME_SCALE = 0.42。

sensor.reset() # 初始化sensor
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QVGA) # 使用QVGA的速度。
#设置图像像素大小

# 打印出初始曝光时间以进行比较。
print("Initial exposure == %d" % sensor.get_exposure_us())

sensor.skip_frames(30)         # 等待设置生效。
clock = time.clock()           # 创建一个时钟对象来跟踪FPS帧率。

# 您必须关闭自动增益控制和自动白平衡，否则他们将更改图像增益以撤消您放置的任何曝光设置...
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
# 需要让以上设置生效
sensor.skip_frames(time = 500)
clock = time.clock() # 跟踪FPS帧率
current_exposure_time_in_microseconds = sensor.get_exposure_us()
print("Current Exposure == %d" % current_exposure_time_in_microseconds)

# 默认情况下启用自动曝光控制（AEC）。调用以下功能可禁用传感器自动曝光控制。
# 另外“exposure_us”参数在AEC被禁用后覆盖自动曝光值。
sensor.set_auto_exposure(False, \
    exposure_us = int(current_exposure_time_in_microseconds * EXPOSURE_TIME_SCALE))

#串口初始化  注意此处是k210的串口与Openmv不同
fm.register(board_info.PIN15,fm.fpioa.UART1_TX)
fm.register(board_info.PIN17,fm.fpioa.UART1_RX)
uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

#area_threshold 面积阈值，如果色块被框起来的面积小于这个值，会被过滤掉
#pixels_threshold 像素个数阈值，如果色块像素数量小于这个值，会被过滤掉
blobs_pink = img.find_blobs([pink_threshold],pixels_threshold=50, area_threshold=50)
blobs_purple = img.find_blobs([purple_threshold],pixels_threshold=50, area_threshold=50)
blobs_red = img.find_blobs([red_threshold],pixels_threshold=50, area_threshold=50)
blobs_green = img.find_blobs([green_threshold],pixels_threshold=50, area_threshold=50)
blobs_yellow = img.find_blobs([yellow_threshold],pixels_threshold=50, area_threshold=50)
blobs_brown = img.find_blobs([brown_threshold],pixels_threshold=50, area_threshold=50)
blobs_depart = img.find_blobs([depart_threshold],pixels_threshold=50, area_threshold=50)

# QRcode识别
while(True):
    clock.tick()
    img = sensor.snapshot()
    #img.lens_corr(1.8) # 1.8的强度参数对于2.8mm镜头来说是不错的。
    for code in img.find_qrcodes():
        img.draw_rectangle(code.rect(), color = (255, 0, 0))
        message = code.payload()
        if (code.payload() == '11'):
            uart_A.write("")
            i=1
            break
        elif (code.payload() == '12'):
            uart_A.write("")
            i = 1
            break
        elif (code.payload() == '22'):
            uart_A.write("")
            i = 1
            break
        elif (code.payload() == '21'):
            uart_A.write("")
            i = 1
            break
    if (i==1):
        break

while(True):
    clock.tick() # 追踪两个snapshots()之间经过的毫秒数.
    img = sensor.snapshot() # 拍一张照片并返回图像。

    # blobs_purple = img.find_blobs([purple_threshold])
    # blobs_red = img.find_blobs([red_threshold])
    # blobs_green = img.find_blobs([green_threshold])
    # blobs_brown = img.find_blobs([brown_threshold])
    # blobs_yellow = img.find_blobs([yellow_threshold])
    # 障碍物识别
    if blobs_pink:
        # 如果找到了目标颜色
        for b in blobs_pink:
            # 找到的目标颜色区域
            img.draw_rectangle(b[0:4])  # rect
            # 用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6])  # cx, cy
            # 在目标颜色区域的中心画十字形标记
            print(b[5], b[6])
            uart_A.write(b[5], b[6])

     # 找紫色停车区
    if blobs_purple:
    #如果找到了目标颜色
        for b in blobs_purple:
            #发送停车标志位到串口
            uart_A.write('purple_stop')
            #单片机操作云台，抬升摄像机，识别红绿灯
            pyb.delay(1000) #延时1s

    for c in img.find_circles(threshold = 3500, x_margin = 10, y_margin = 10, r_margin = 10,
            r_min = 2, r_max = 100, r_step = 2):
        area = (c.x()-c.r(), c.y()-c.r(), 2*c.r(), 2*c.r())
        #area为识别到的圆的区域，即圆的外接矩形框
        statistics = img.get_statistics(roi=area)#像素颜色统计
        #如(0,100,0,120,0,120)是红色的阈值，范围在这个阈值内，就说明是红色的圆。
        #l_mode()，a_mode()，b_mode()是L通道，A通道，B通道的众数。
        if 0<statistics.l_mode()<100 and 0<statistics.a_mode()<127 and 0<statistics.b_mode()<127:#if the circle is red light
            img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))#识别到的红色圆形用红色的圆框出来
            uart_A.write('')
            #阈值待调
        elif 10<statistics.l_mode()<17 and -20<statistics.a_mode()<-12 and -10<statistics.b_mode()<13:#if the circle is yellow light
            img.draw_circle(c.x(), c.y(), c.r(), color=(255, 255, 0))  # 识别到的黄色圆形用黄色的圆框出来
            uart_A.write('')
            # 阈值待调
        elif 10<statistics.l_mode()<17 and -20<statistics.a_mode()<-12 and -10<statistics.b_mode()<13:#if the circle is green light
            img.draw_circle(c.x(), c.y(), c.r(), color=(0, 255, 0))  # 识别到的黄色圆形用黄色的圆框出来
            uart_A.write('')

    # 找棕色区域
    if  blobs_brown:
    #如果找到了目标颜色
        for b in blobs_brown:
            #发送停车标志位到串口
            uart_A.write('brown_stop')
            #单片机操作云台，抬升摄像机，识别红绿灯
            pyb.delay(1000) #延时1s

    #找最后的黄色停车区
    if blobs_depart
        for b in blobs_depart
            uart_A.write('')


    #print(clock.fps()) # 注意: 当连接电脑后，OpenMV会变成一半的速度。当不连接电脑，帧率会增加
