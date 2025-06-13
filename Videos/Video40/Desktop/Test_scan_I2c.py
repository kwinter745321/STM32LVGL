# Test_scan_I2c.py
#
# Verified by k. winter
# MicroPython v1.20.0-2504.g9fe842956 on 2025-06-04; F429I-DISCO with STM32F429
# STM32F4DISC (STM32)
# LVGL 9.3
#
from machine import Pin, I2C, SoftI2C
import time

##### flash drive ################
#nothing extra needed

##### definitions ################
I2C_PORT = 'I2C3'
I2C_SDA_PIN = "PC8"  #GP14 I2C1
I2C_SCL_PIN = "PA8"  #GP15
I2C_FREQ = 40000

USER_BUTTON_PIN = Pin("PA0")  #GP22
#using Pin A0 for Switch

#### Init #####################
#scl = Pin(I2C_SCL_PIN, mode=Pin.OUT)
#sda = Pin(I2C_SDA_PIN, mode=Pin.OUT)
#key = Switch()
user = Pin(USER_BUTTON_PIN, Pin.IN)

# myscl = Pin("PA8", Pin.OUT)
# mysda = Pin("PC9", Pin.OUT)
# myscl.on()
# mysda.on()

#i2c=I2C(3, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_FREQ)
i2c=machine.SoftI2C(scl=Pin("PA8"),sda=Pin("PC9"),freq=100000)
#i2c=machine.SoftI2C(scl=machine.Pin('PB6'),sda=machine.Pin('PB7'),freq=400000)
#i2c=pyb.I2C(1, I2C.CONTROLLER)  #note: 1 means I2C1

#### Test Program #####################
try:
    print("----------------")
    print("Program started.")
    print("* Test scan of I2C devices.")
    print("* I2C is wired on MCU's %s port." % (I2C_PORT))
    print("*",i2c)
    print("Press User button to start test or Control-c in Shell to exit.")
    user_btn = user.value()
    #print("user button=",user_btn)
    
    while user_btn != 0:
        time.sleep(.5)
        user_btn = user.value()
        #print("user button=",user_btn)
        
    print("User button pressed.\n")
    print('Scanning I2C bus...')
    devices = i2c.scan() 
    print('Scan finished.')
    device_count = len(devices)

    if device_count == 0:
        print('No I2C device found.')
    else:
        print('I2C devices found:',device_count)
        print("| Decimal Address | Hex Address |")
        print("| --------------- | ----------- |")
        for device in devices:
            xdevice = str(hex(device))
            print("| %15s " % device,end="")
            print("| %9s " % xdevice," |")

except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    print('Finished.')
    

