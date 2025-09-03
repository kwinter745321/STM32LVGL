# README.md - Video52

03 Sept 2025

# Topic
This is video 52 on creating a custom gauge. We discuss the MPU-6050, The formulas for Roll and Pitch, and the configuration
of the STM32F4Discovery board.  The STM32F4Discovery (STM32F429) board runs at 180 Mhz and has an inbuilt ILI9341 display.
Also, it has 8 MB of PSRAM that is available to programs.

The I2C configuration for the MPU6050 uses pin PB8 for SDA and PB9 for SCL. Some of the other I2C ports are unavailable because they are used by another device.

In this video, 
 - Demonstrated the custom gauge
 - Discussed the sensor and roll/pitch formulas
 - Discussed the gauge design
 - Walk-through the driver, gauge and test programs

The code for this video is available at the GitHub site:
https://github.com/kwinter745321/STM32LVGL/tree/main/Videos/video52

# Files

| Directory | File Name  |  Comment |
|-----------|-------------------------------|----------|
|           |                               |          |
| Datasheets |                              |          |
|           | stm32f4discovery-kit.pdf      | ST User Manual  |
|           |  stmpe811.pdf                 | ST User Manual  |
|           |                               |          |
| Desktop   |                               |          |
|           | test_button_display.py    | The first demonstration program. |
|           | test_matrix_display.py    | The second demonstration program. |
|           | test_keyboard_display.py    | The third demonstration program. |
|           | test_scan_I2c.py    | Tests I2C channel and returns address of any devices. |
|           |                               |          |
| PYBflash  |                               |          |
|           | display_driver.py    |  Edit this with your Pin Names.        |
|           | ili9xxx.py    |  Display classes.        |
|           | lv_utils.py    |  Utility used by lvgl.        |
|           | st77xx.py    |  Base display classes.        |
|           | stmpe811.py    |  Touch class.        |
|           |                               |          |