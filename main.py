import vuart
import blink
import time
from machine import Pin, I2C
import MPU6050 as mpu6050
LED = Pin(25, Pin.OUT)  # Built-in LED
vuart.send_vuart_string("Pico Ready")

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)  



vuart.send_vuart_string("Hi from Pico MicroPython")
devices = i2c.scan()
print("I2C devices found:", [hex(d) for d in devices])
MPU6050_ADDR = 0x68
ACCEL_XOUT_H = 0x3B

raw_data = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_XOUT_H, 6)  # Read 6 bytes (X, Y, Z)
print("Raw Data:", raw_data)



bme = blink.BME280(i2c=i2c)
mpu = mpu6050.MPU6050(i2c_instance=i2c)
print("Sensor init done")
while True:
    bmeres=bme.values
    temp1, press, hum = bmeres
    accel = accel = mpu.read_accel_data()
    ax,ay,az=accel['x'],accel['y'],accel['z']
    gyro = mpu.read_gyro_data()
    gx,gy,gz = gyro['x'],gyro['y'],gyro['z']
    temp2 = str(mpu.read_temperature())
    final = f"t1:{temp1};t2:{temp2};p:{press};h:{hum};ax:{ax};ay:{ay};az:{az};gx:{gx};gy:{gy};gz:{gz}"
    print(final)
    vuart.send_vuart_string(final)
    time.sleep(1)
