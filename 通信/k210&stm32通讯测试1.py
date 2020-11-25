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
lcd.init()
#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_hmirror(0)
sensor.run(1)
clock = time.clock()
#串口初始化
fm.register(board_info.PIN15,fm.fpioa.UART1_TX)
fm.register(board_info.PIN17,fm.fpioa.UART1_RX)
uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

while(True):
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())
    uart_A.write('011/112\n')
                ##判断坐标是否为3位十进制，若不是，则在数字前填充0直至3位十进制
                #if center_x_1<1:
                    #uart_A.write('0{}/'.format(center_x))
                #else:
                    #uart_A.write('{}/'.format(center_x))
                #if center_y_1<1:
                    #uart_A.write('0{}\n'.format(center_y))
                #else:
                    #uart_A.write('{}\n'.format(center_y))
  #   a = lcd.display(img)
uart_A.deinit()

