# test_gauge_mpu6050.py
#
# MPU6050 code migrated from Warayut Poomiwatracanont
# Updated: 21 August 2025
#
# Copyright (C) 2025 KW Services.
# MIT License
# MicroPython v1.20.0-2504.g9fe842956 on 2025-06-04; F429I-DISCO with STM32F429
# STM32F4DISC (STM32)
# LVGL 9.3
#
from machine import Pin
from MPU6050 import MPU6050
from machine import reset
from time import sleep_ms
import time
import math

import display_driver
import lvgl as lv
from gauge import Gauge

lv.init()
scr = lv.obj()

print("scr width,height:",scr.get_width(),scr.get_height())

gauge1 = Gauge(scr, 90, 120, 50, "Roll" )
gauge2 = Gauge(scr, 230, 120, 50, "Pitch" )
lv.screen_load(scr)

mpu = MPU6050(scl=Pin("PB9"),sda=Pin("PB8"),freq=400000)

cnt = 0
sumroll = 0
sumpitch = 0

error_roll = -0.0353372
error_pitch = 0.0587947

done = False
while not done:
    angle = mpu.read_angle()
    roll = angle["x"] - error_roll
    pitch = -angle["y"] - error_pitch
    gauge1.show(roll)
    gauge2.show(pitch)
    sleep_ms(100)
    cnt += 1
    print(cnt,"Roll:",roll,"Pitch:",pitch  )
    if cnt > 200:
        print(sumroll/200,sumpitch/200)
        done = True
    sumroll = sumroll + roll
    sumpitch = sumpitch + pitch

