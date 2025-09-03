import machine
import time
from MPU6050 import MPU6050

# Set up the I2C interface
#i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
i2c = machine.SoftI2C(sda=machine.Pin("PB9"), scl=machine.Pin("PB8"), freq=100000)
# Set up the MPU6050 class 
mpu = MPU6050(bus=i2c)
time.sleep(1)
# wake up the MPU6050 from sleep
#mpu.wake()

# continuously print the data
while True:
    gyro = mpu.read_gyro_data()
    accel = mpu.read_accel_data()
    temp = mpu.read_temperature()
    print("temp:",str(temp),"Gyro: " + str(gyro) + ", Accel: " + str(accel))
    time.sleep(1)