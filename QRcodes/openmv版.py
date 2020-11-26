import sensor
import machine
import image
import time


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # 必须关闭此功能，以防止图像冲洗…
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    #img.lens_corr(1.8) # 1.8的强度参数对于2.8mm镜头来说是不错的。
    for code in img.find_qrcodes():
        img.draw_rectangle(code.rect(), color = (160, 0, 0))
        #print(code)
        message = code.payload()
        print(message)
        #if(code.payload() == '12'):
            #print('Extracted materials')
    #print(clock.fps())



# 二维码例程
##红绿灯   颜色识别+形状识别(圆形)
