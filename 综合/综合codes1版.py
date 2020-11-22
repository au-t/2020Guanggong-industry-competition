from fpioa_manager import *
from fpioa_manager import fm
from machine import UART
from Maix import GPIO
import sensor, image,lcd,time,math,pyb,machine
# 为了使色彩追踪效果真的很好，你应该在一个非常受控制的照明环境中。
pink_threshold =
purple_threshold =
red_threshold =
green_threshold   = (21, 51, 30, 72, 6, 63)
brown_threshold =
yellow_threshold =

# 设置各个颜色的阈值，括号里面的数值分别是L A B 的最大值和最小值（minL, maxL, minA,
# maxA, minB, maxB），LAB的值在图像左侧三个坐标图中选取。
# 在Framebuffer中选择一个区域来复制颜色设置。

sensor.reset() # 初始化sensor
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QQVGA) # 使用QQVGA的速度。
#设置图像像素大小

sensor.skip_frames(10) # 让新的设置生效。
sensor.set_auto_whitebal(False) #关闭白平衡。
clock = time.clock() # 跟踪FPS帧率
#串口初始化  注意此处是k210的串口与Openmv不同
fm.register(board_info.PIN15,fm.fpioa.UART1_TX)
fm.register(board_info.PIN17,fm.fpioa.UART1_RX)
uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

blobs_pink = img.find_blobs([pink_threshold])
blobs_purple = img.find_blobs([purple_threshold])
blobs_red = img.find_blobs([red_threshold])
blobs_green = img.find_blobs([green_threshold])
blobs_yellow = img.find_blobs([yellow_threshold])
blobs_brown = img.find_blobs([brown_threshold])

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
    if blobs_yellow
        for b in blobs_yellow
            uart_A.write('')


    #print(clock.fps()) # 注意: 当连接电脑后，OpenMV会变成一半的速度。当不连接电脑，帧率会增加
