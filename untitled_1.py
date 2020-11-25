# 感光元件曝光控制
#
# 此示例显示如何手动控制相机传感器的曝光，而不是让自动曝光控制运行。
# 增益和曝光控制之间有什么区别？
#
# 通过增加图像的曝光时间，您可以在相机上获得更多光线。这为您提供了最佳的信噪比。
# 您通常总是希望增加曝光时间...除非，当您增加曝光时间时，您会降低最大可能的帧速率，
# 如果图像中有任何移动，它将在更长的曝光时间内开始模糊。
# 增益控制允许您使用模拟和数字乘法器增加每像素的输出......但是，它也会放大噪声。
# 因此，最好尽可能让曝光增加，然后使用增益控制来弥补任何剩余的地画面。

# 我们可以通过在自动增益控制算法上设置增益上限来实现上述目的。
# 一旦设置完毕，算法将不得不增加曝光时间以满足任何增益需求，而不是使用增益。
# 然而，当照明变化相对于曝光恒定且增益变化时，这是以曝光时间的变化为代价的。

#o make up any remaining ground.

import sensor, image, time, lcd

# 更改此值以调整曝光。试试10.0 / 0.1 /等。
EXPOSURE_TIME_SCALE = 3.0

lcd.init()
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)(89, 97, -30, -3, 53, 65)
sensor.set_hmirror(1)#摄像头镜像
sensor.set_vflip(1)
sensor.run(1)
# 打印出初始曝光时间以进行比较。
print("Initial exposure == %d" % sensor.get_exposure_us())

sensor.skip_frames(30)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

# 您必须关闭自动增益控制和自动白平衡，否则他们将更改图像增益以撤消您放置的任何曝光设置...
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
# 需要让以上设置生效
sensor.skip_frames(30)

current_exposure_time_in_microseconds = sensor.get_exposure_us()
print("Current Exposure == %d" % current_exposure_time_in_microseconds)

# 默认情况下启用自动曝光控制（AEC）。调用以下功能可禁用传感器自动曝光控制。
# 另外“exposure_us”参数在AEC被禁用后覆盖自动曝光值。
sensor.set_auto_exposure(False, \
    exposure_us = int(current_exposure_time_in_microseconds * EXPOSURE_TIME_SCALE))

print("New exposure == %d" % sensor.get_exposure_us())
# sensor.get_exposure_us()以微秒为单位返回精确的相机传感器曝光时间。
# 然而，这可能与命令的数量不同，因为传感器代码将曝光时间以微秒转换为行/像素/时钟时间，这与微秒不完全匹配...

# 如果要重新打开自动曝光，请执行以下操作：sensor.set_auto_exposure(True)
# 请注意，相机传感器将根据需要更改曝光时间。

# 执行：sensor.set_auto_exposure(False)，只是禁用曝光值更新，但不会更改相机传感器确定的曝光值。

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()
    # Take a picture and return the image.

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

    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                   # to the IDE. The FPS should increase once disconnected.
