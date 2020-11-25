import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()


while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    for c in img.find_circles(threshold = 3500, x_margin = 10, y_margin = 10, r_margin = 10,
            r_min = 2, r_max = 100, r_step = 2):
        area = (c.x()-c.r(), c.y()-c.r(), 2*c.r(), 2*c.r())
        #area为识别到的圆的区域，即圆的外接矩形框
        statistics = img.get_statistics(roi=area)#像素颜色统计
        print(statistics)
        img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
        #(0,100,0,120,0,120)是红色的阈值，所以当区域内的众数（也就是最多的颜色），范围在这个阈值内，就说明是红色的圆。
        #l_mode()，a_mode()，b_mode()是L通道，A通道，B通道的众数。(90, 93, -52, -35, -15, 2)
        #if 90<statistics.l_mode()<93 and -52<statistics.a_mode()<-35 and -15<statistics.b_mode()<2:#if the circle is red
            #img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))#识别到的红色圆形用红色的圆框出来
        #else:
            #img.draw_rectangle(area, color = (255, 255, 255))
            #将非红色的圆用白色的矩形框出来
    print("FPS %f" % clock.fps())
