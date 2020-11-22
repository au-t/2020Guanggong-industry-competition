# 识别直线例程
#
# 这个例子展示了如何在图像中查找线条。对于在图像中找到的每个线对象，
# 都会返回一个包含线条旋转的线对象。

# 注意：线条检测是通过使用霍夫变换完成的：
# http://en.wikipedia.org/wiki/Hough_transform
# 请阅读以上关于“theta”和“rho”的更多信息。

# find_lines（）找到无限长度的线。使用find_line_segments（）
# 来查找非无限线。

enable_lens_corr = False # turn on for straighter lines...打开以获得更直的线条…
import sensor, image, time,lcd

sensor.reset()
sensor.set_pixformat(sensor.RGB565) #灰度更快
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(30)
clock = time.clock()

# 所有的线对象都有一个`theta（）`方法来获取它们的旋转角度。
# 您可以根据旋转角度来过滤线条。
black_threshold = ((3, 27, -13, 9, -9, 35))


# 所有线段都有 `x1()`, `y1()`, `x2()`, and `y2()` 方法来获得他们的终点
# 一个 `line()` 方法来获得所有上述的四个元组值，可用于 `draw_line()`.
i = 1
while(True):
    clock.tick()
    img = sensor.snapshot()
    img.lens_corr(1.8) # 1.8的强度参数对于2.8mm镜头来说是不错的。
    blobs1 =  img.find_blobs([black_threshold])
    if blobs1:
        for b in blobs1:
            tmp=img.draw_rectangle(b[0:4])
            tmp=img.draw_cross(b[5], b[6])
            c=img.get_pixel(b[5], b[6])



            #if i%2==1:
               #rx=b.cx()
               #ry=b.cy()
            #else:
               #lx=b.cx()
               #ly=b.cy()
               #qx=(rx+lx)/2
               #qy=(ly+ry)/2
               #print(qx,qy)

            #i=i+1
            print(b.cx(),b.cy())



