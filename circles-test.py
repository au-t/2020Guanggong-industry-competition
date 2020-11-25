import sensor, image, time

green_threshold= (25, 36, -13, 3, -2, 19)
import sensor, image, time

# 更改此值以调整曝光。试试10.0 / 0.1 /等。
EXPOSURE_TIME_SCALE = 0.48

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

print("New exposure == %d" % sensor.get_exposure_us())

while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    blobs = img.find_blobs([green_threshold], pixels_threshold=50, area_threshold=50, merge=True, margin=10)
    for c in img.find_circles(threshold = 3500, x_margin = 10, y_margin = 10, r_margin = 10,
            r_min = 2, r_max = 100, r_step = 2):
        area = (c.x()-c.r(), c.y()-c.r(), 2*c.r(), 2*c.r())
        #area为识别到的圆的区域，即圆的外接矩形框
        statistics = img.get_statistics(roi=area)#像素颜色统计
        img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
        #print(statistics)
        if blobs:
            img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))

    print("FPS %f" % clock.fps())
