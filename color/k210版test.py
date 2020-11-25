#k210阈值测试codes
import sensor
import image
import lcd
import time
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)#摄像头镜像
sensor.set_vflip(1)
sensor.run(1)
sensor.skip_frames(30) #跳过指定帧数或者跳过指定时间内的图像，让相机图像稳定
test_threshold  = (87, 100, -8, 14, -1, 11)
while True:
    img=sensor.snapshot()
    blobs = img.find_blobs([test_threshold])
    if blobs:
        for b in blobs:
            tmp=img.draw_rectangle(b[0:4]) #画矩阵
            tmp=img.draw_cross(b[5], b[6]) #画中心交叉点
            c=img.get_pixel(b[5], b[6])
            print('find it')
        lcd.display(img)
