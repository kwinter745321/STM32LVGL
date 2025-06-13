# README.ms - Video 40 

# Topic
17 June 2025

This is video 40 on MicroPython and LVGL. This video introduces LVGL to STM32 via the STM32F4Discovery Board.  We briefly discuss the board and its capabilities.  We demonstrate three programs on the board.  We briefly review the STMPE811 code.

We use a STM32F4Discovery board which has a built-in ILI9341 Display and integrated touch controller (STMPE811).  Additionally, the board has user accessable LEDs and a User button that can be incorporated into programs.

In this video,
    • Discuss the STM32F4DISC and MicroPython/LVGL firmware
    • Present the setup configuration
    • Discuss and review the code for the STMPE811 touch driver which communicates via I2C
    • Finally, we demonstrate three example programs

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