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
https://github.com/kwinter745321/STM32LVGL/tree/main/Videos/Video52

# Files

| Directory | File Name  |  Comment |
|-----------|-------------------------------|----------|
|           |                               |          |
| Datasheets |                              |          |
|           | Test_scan_i2c.py      | ST User Manual  |
|           |  stmpe811.pdf                 | ST User Manual  |
|           |                               |          |
| Desktop   |                               |          |
|           | test_gauge_mpu6050.py    | The main demonstration program with the gauges. |
|           | test_mpu6050.py    | A programby Warayut Poomiwatracanont to test mpu6050. |
|           | test_scan_I2c.py    | Tests I2C channel and returns address of any devices. |
|           |                               |          |
| PYBflash  |                               |          |
|           | display_driver.py    |  Edit this with your Pin Names.        |
|           | ili9xxx.py    |  Display classes.        |
|           | gauge.py    | The gauge class program. |
|           | lv_utils.py    |  Utility used by lvgl.        |
|           | MPU6060.py   | Warayut Poomiwatracanont driver. |
|           | st77xx.py    |  Base display classes.        |
|           | stmpe811.py    |  Touch class.        |
|           |                               |          |