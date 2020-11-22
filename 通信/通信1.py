from fpioa_manager import *
from fpioa_manager import fm
from machine import UART
from Maix import GPIO
import sensor
import image
import lcd
import time
import math
#import KPU as kpu
#LCD初始化


green_threshold   = (27, 60, -38, 0, 2, 20)#(21, 51, 30, 72, 6, 63)

lcd.init()
#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)
sensor.set_vflip(1)
sensor.skip_frames(10) # 让新的设置生效。
#sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock()


#串口初始化
fm.register(15,fm.fpioa.UART1_TX)
fm.register(7,fm.fpioa.UART1_RX)
uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob

while(True):
    img = sensor.snapshot() # Take a picture and return the image.

    blobs = img.find_blobs([green_threshold])
    if blobs:
        max_blob=find_max(blobs)
        print('sum :', len(blobs))
        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())

        output_str="[%d,%d]" % (max_blob.cx(),max_blob.cy()) #方式1
        #output_str=json.dumps([max_blob.cx(),max_blob.cy()]) #方式2
        print('you send:',output_str)
        uart_A.write(output_str+'\r\n')
    else:
        print('not found!')
uart_A.deinit()
del uart_A



