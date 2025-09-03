# stmpe811.py
#
# Migrated from https://blog.embeddedexpert.io/?p=2085
#
# Created: 07 June 2025
# Copyright (C) 2025 KW Services.
# MIT License
# MicroPython v1.20.0-2504.g9fe842956 on 2025-06-04; F429I-DISCO with STM32F429
#
# LVGL indev driver for the STMPE811 Resistance Touch IC
# developed on STM32F429DISC
#
#       from stmpe811 import STMPE811
#       touch = STMPE811(sda=<pin>, scl=<pin>)
#

import lvgl as lv
from machine import I2C, Pin, SoftI2C
import time

REG_SYS_CTRL2          = 0x04 #Clock control
REG_SYS_CTRL1          = 0x03 #Reset control
REG_IO_AF              = 0x17 #Alternate function register
REG_ADC_CTRL1          = 0x20 #ADC control
REG_ADC_CTRL2          = 0x21 #ADC control
REG_TSC_CFG            = 0x41 #Touch Configuration
REG_FIFO_TH            = 0x4A #FIFO threshold
REG_FIFO_STA           = 0x4B #FIFO status
REG_TSC_FRACT_XYZ      = 0x56 #Touchscreen controller FRACTION_Z
REG_TSC_I_DRIVE        = 0x58 #Touchscreen controller drive
REG_TSC_CTRL           = 0x40 #touchscreen controller control register
REG_INT_CTRL           = 0x09 #Interrupt control register
REG_INT_EN             = 0x0A #Interrupt enable register
REG_INT_STA            = 0x0B #Interrupt status register
REG_TSC_DATA_INC       = 0x57 #Touchscreen controller DATA Incremental
REG_TSC_DATA_NON_INC   = 0xD7 #Touchscreen controller DATA Non-Incremental
REG_FIFO_SIZE          = 0x4C #FIFO size
ADC_FCT                = 0x01
TS_FCT                 = 0x02
IO_FCT                 = 0x04
TEMPSENS_FCT           = 0x08
TOUCH_IO_ALL           = 0x00
TS_CTRL_ENABLE         = 0x01
TS_CTRL_STATUS         = 0x80

class STMPE811:

    def __init__(self, i2c_dev=0, sda=21, scl=22, freq=100000, addr=0x41, width=320, height=240, 
                 inv_x=False, inv_y=False, swap_xy=False):
        if not lv.is_initialized():
            lv.init()
        self.width, self.height = width, height
        self.inv_x, self.inv_y, self.swap_xy = inv_x, inv_y, swap_xy
        self.i2c = SoftI2C(sda=Pin(sda), scl=Pin(scl), freq=freq)
        self.addr = addr
        try:
            print("STMPE811 touch IC ready (id {0:d} revision {1:d})".format( \
                int.from_bytes(self.i2c.readfrom_mem(self.addr, 0x00, 2), "big"), \
                int.from_bytes(self.i2c.readfrom_mem(self.addr, 0x02, 1), "big")
            ))
        except:
            print("STMPE811 touch IC not responding")
            return
        self.point = lv.point_t( {'x': 0, 'y': 0} )
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.state = lv.INDEV_STATE.RELEASED
        self.indev_drv = lv.indev_create()
        self.indev_drv.set_type(lv.INDEV_TYPE.POINTER)
        self.indev_drv.set_read_cb(self.callback)
        
    def first(self):
        #per datasheet
        self.i2c.writeto_mem(self.addr, 0x04, b'\x0C')
        self.i2c.writeto_mem(self.addr, 0x0A, b'\x03')
        self.i2c.writeto_mem(self.addr, 0x20, b'\x49')
        self.i2c.writeto_mem(self.addr, 0x21, b'\x01')
        self.i2c.writeto_mem(self.addr, 0x17, b'\x00')
        self.i2c.writeto_mem(self.addr, 0x41, b'\x94')
        self.i2c.writeto_mem(self.addr, 0x4A, b'\x05')
        self.i2c.writeto_mem(self.addr, 0x4B, b'\x01')
        self.i2c.writeto_mem(self.addr, 0x4B, b'\x00')
        self.i2c.writeto_mem(self.addr, 0x40, b'\x01')
        self.i2c.writeto_mem(self.addr, 0x0B, b'\xFF')
        self.i2c.writeto_mem(self.addr, 0x09, b'\x01')
        
    def touch_enable(self):
        #per blog
        self.hold = REG_TSC_DATA_NON_INC
        self.i2c.writeto_mem(self.addr, REG_SYS_CTRL1, b'\x02')
        time.sleep_ms(10)
        self.i2c.writeto_mem(self.addr, REG_SYS_CTRL1, b'\x00')
        time.sleep_ms(2)
        #mode = self.i2c.readfrom_mem(self.addr, REG_SYS_CTRL2, 1 )
        #switch off GPIO clock ~(IO_FCT)
        self.i2c.writeto_mem(self.addr, REG_SYS_CTRL2, b'\x04' )
        self.i2c.writeto_mem(self.addr, REG_IO_AF, b'\x00')
        #switch on GPIO clock ~(TS_FCT | ADC_FCT)
        self.i2c.writeto_mem(self.addr, REG_SYS_CTRL2, b'\x0B' )
        self.i2c.writeto_mem(self.addr, REG_ADC_CTRL1, b'\x49')
        time.sleep_ms(2)
        self.i2c.writeto_mem(self.addr, REG_ADC_CTRL1, b'\x01')
        self.i2c.writeto_mem(self.addr, REG_TSC_CFG, b'\x9A')
        self.i2c.writeto_mem(self.addr, REG_FIFO_TH, b'\x01')
        self.refresh()
        self.i2c.writeto_mem(self.addr, REG_TSC_FRACT_XYZ , b'\x07')
        self.i2c.writeto_mem(self.addr, REG_TSC_I_DRIVE, b'\x01')
        self.i2c.writeto_mem(self.addr, REG_TSC_CTRL, b'\x01')
        self.i2c.writeto_mem(self.addr, REG_INT_STA, b'\xFF')
        time.sleep_ms(5)
        self.first()
        
    def refresh(self):
        # reset FIFO
        self.i2c.writeto_mem(self.addr, REG_FIFO_STA, b'\x01')
        self.i2c.writeto_mem(self.addr, REG_FIFO_STA, b'\x00')
        self.i2c.writeto_mem(self.addr, 0x0B, b'\xFF')
        self.i2c.writeto_mem(self.addr, 0x09, b'\x01')

    def isTouched(self):
        state = 0
        value = int.from_bytes(self.i2c.readfrom_mem(self.addr, REG_TSC_CTRL, 1),"big")
        #value &= TS_CTRL_STATUS
        #state = (value and TS_CTRL_STATUS)==0x80
        if value >= 128:
            #print("isTouched value:",value)
            value = int.from_bytes(self.i2c.readfrom_mem(self.addr, REG_FIFO_SIZE, 1),"big")
            if value > 0:
                self.point = self.getTouchValue()
                time.sleep_ms(5)
                return True
        else:
            self.refresh()
        return False
        
    def getTouchValue(self):
        dataXYZ = self.i2c.readfrom_mem(self.addr, REG_TSC_DATA_NON_INC, 4)
        uldataXYZ = (dataXYZ[0] << 24)|(dataXYZ[1] << 16)|(dataXYZ[2] << 8)|(dataXYZ[3] << 0)
        pt = lv.point_t()
        pt.x = (uldataXYZ >> 20 ) & 0x00000fff
        pt.y = (uldataXYZ >>  8 ) & 0x00000fff
        time.sleep_ms(5)
        self.refresh()
        return pt

    def callback(self, driver, data):

        def setminmax(x,y):
            # Used to get x,y Low and High values
            if self.xmin == 0:
                self.xmin = x
                self.ymin = y
                self.xmax = x
                self.ymax = y
                return
            if self.xmin > x:
                self.xmin = x 
            if self.xmax < x:
                self.xmax = x 
            if self.ymin > y:
                self.ymin = y 
            if self.ymax < y:
                self.ymax = y
            print("minmax:",self.xmin,self.xmax,self.ymin,self.ymax)
            
        def get_point():
            pt = self.point
            #print("get_point",pt.x,pt.y)
            x = pt.x
            y = pt.y
            #if (self.width != -1 and x >= self.width) or (self.height != -1 and y >= self.height):
            #    raise ValueError
            x = self.width - x - 1 if self.inv_x else x
            y = self.height - y - 1 if self.inv_y else y
            (x, y) = (y, x) if self.swap_xy else (x, y)
            return { 'x': x, 'y': y }
        
        if self.isTouched():
            data.point = get_point()
            self.state = lv.INDEV_STATE.PRESSED
            data.state = self.state
            #print("touched:",data.point.x,data.point.y)
        else:
            self.state = lv.INDEV_STATE.RELEASED
            data.state = self.state
        