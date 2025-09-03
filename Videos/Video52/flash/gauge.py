# gauge.py
#
# Created: 21 August 2025
#
# Copyright (C) 2025 KW Services.
# MIT License
# Verified using:
#   MicroPython v1.20.0-2504.g9fe842956 on 2025-06-04; F429I-DISCO with STM32F429
#   STM32F4DISC (STM32)
# LVGL 9.3
#

# This is a LVGL 9.3 class to create a custom gauge on an ILI9341 display

import lvgl as lv
import time
import math

class Gauge():

    def draw_center(self,x,y):
        self.led1 = lv.led(self.scr)
        self.led1.set_color(lv.palette_main(lv.PALETTE.RED))
        self.led1.set_pos(x-self.lw,y-self.lw)
        self.led1.set_size(self.lw*2,self.lw*2)
        self.led1.off()

    def make_style(self):
        self.lstyle = lv.style_t()
        self.lstyle.init()
        self.lstyle.set_line_width(5)
        self.lstyle.set_line_color(lv.palette_main(lv.PALETTE.GREY))

    def __init__(self,screen,xpos,ypos,line_size,title):
        self.scr = screen
        self.xpos = xpos
        self.ypos = ypos
        self.lw = line_size
        self.make_style()
        self.draw_center(self.xpos,self.ypos)
        self.line1 = lv.line(self.scr)
        self.line1.add_style(self.lstyle,0)
        self.show_value = lv.label(self.scr)
        self.show_value.align_to(self.led1, lv.ALIGN.BOTTOM_MID,-20, 30)
        self.title = lv.label(self.scr)
        adj = len(title) // 2
        self.title.align_to(self.led1, lv.ALIGN.TOP_MID, -adj -22, -50)
        self.title.set_style_text_font(lv.font_montserrat_24,0)
        self.title.set_text(title)
        
    def show(self,r):
        y1 = self.ypos + int(self.lw*math.sin(r))
        y2 = self.ypos - int(self.lw*math.sin(r))
        x1 = self.xpos - int(self.lw*math.cos(r))
        x2 = self.xpos + int(self.lw*math.cos(r))
        lpoints = [{"x":x1,"y":y1},{"x":x2,"y":y2}]
        self.line1.set_points(lpoints, 2)
        msg = " %3.2f " % (r * 57.3)
        self.show_value.set_text(msg)

    