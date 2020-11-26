import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

test_threshold   = (92, 100, -28, 1, -8, 1)

while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    blobs_test = img.find_blobs([test_threshold],pixels_threshold=50, area_threshold=50)
    for c in img.find_circles(threshold = 4000, x_margin = 10, y_margin = 10, r_margin = 10,
            r_min = 2, r_max = 50, r_step = 2):
        area = (c.x()-c.r(), c.y()-c.r(), 2*c.r(), 2*c.r())
        #area为识别到的圆的区域，即圆的外接矩形框
        statistics = img.get_statistics(roi=area)#像素颜色统计
        print(statistics)
        img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
        if blobs_test:
            for b in blobs_test:
                img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))  #测试（可注释）
                print("test")
                data0=0x04
                data1=0x00
                data2=0x00
                checkout=(data1+data2)   #取其低八位
                data = bytearray([0xAA,data0,0x00,0x00,checkout,0x54])
                #uart.write(data)
    #print("FPS %f" % clock.fps())
