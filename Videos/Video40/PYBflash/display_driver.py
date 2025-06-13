# display_driver.py
#
# Copyright (C) 2025 KW Services.
# MIT License
# MicroPython v1.20.0-724-gbf1107420 on 2025-02-19; Raspberry Pi Pico with RP2040
# Raspberry Pi Pico (RP2040)
# LVGL 9.1                    https://docs.lvgl.io/9.1/
#
# 
import lvgl as lv
import st77xx
import ili9xxx
import stmpe811
import machine
from machine import reset
from machine import Pin, SPI, SoftSPI
import time

# Information Sources
# https://stm32f4-discovery.net/2014/04/library-08-ili9341-lcd-on-stm32f429-discovery-board/
# https://blog.embeddedexpert.io/?p=2085

# Initialize LVGL
lv.init()
print("Running LVGL %d.%d" % (lv.version_major(), lv.version_minor() )  )

mycs =  Pin("PC2", Pin.OUT)
mytcs = Pin("PB12", Pin.OUT)
myrst = Pin("PD12", Pin.OUT)
mydc =  Pin("PD13", Pin.OUT)
mymiso = Pin("PF8", Pin.IN)
myint = Pin("PA15", Pin.IN)
mycs.on()
mytcs.on()
myrst.on()
mydc.on()

spi = SoftSPI(baudrate=60_000_000, sck=Pin("PF7"), mosi=Pin("PF9"), miso=Pin("PF8"))
mycs.off()
disp = ili9xxx.Ili9341(spi=spi, dc=Pin("PD13"), cs=Pin("PC2"), rst=Pin("PD12"), rot=1)

# touch screen
touch = stmpe811.STMPE811(i2c_dev=3, sda=Pin("PC9"), scl=Pin("PA8"), swap_xy=True)
print("Using Touch STMPE811 setup")
  
coords = None
touch.touch_enable()
#touch.first()

def scale_value(value, in_min, in_max, out_min, out_max):
  scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  return scaled_value

def tsread(indev_drv, data) -> int:
    global coords, pressed
    if touch.isTouched():
        pt = touch.point
        coords = (pt.x, pt.y)
        x, y = coords
        # only calibrated for LANDSCAPE
        x = int(scale_value( x, 300, 3800, 240, 1)) 
        y = int(scale_value( y, 300, 3800, 320, 1))  
        coords = (y,x)
        #print("touch at:",coords)
        data.point.x, data.point.y = coords
        data.state = lv.INDEV_STATE.PRESSED
        time.sleep_ms(50)
        return True  
    else:
        data.state = lv.INDEV_STATE.RELEASED
        return False

# #indev for touch screen
indev_drv = lv.indev_create()
indev_drv.set_type(lv.INDEV_TYPE.POINTER)
indev_drv.set_read_cb(tsread)
###############################################
# UI
###############################################
