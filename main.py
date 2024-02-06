"""
ESP32-S3-DevKitC V4/MicroPython
sh1106 oled
VL53LOX
Display the distance to an object above the VL5310. Up to 50cm

06.10.23
Riko Pals

"""


# ----- LIBRARIES

from machine import Pin, SoftI2C, SPI
from utime import ticks_ms, ticks_diff

from vl53l0x import VL53L0X
import sh1106


# ----- PINOUT
pin_SDA = 41
pin_SCL = 42

st7789_res = 5
st7789_dc  = 4
st7789_sck = 6
st7789_mosi  = 7


# ----- VARS
passed = 0
distance = 0

# ----- I2C setup
i2c = SoftI2C(scl=Pin(pin_SCL), sda=Pin(pin_SDA), freq=100000)

def average(values):
    if len(values) > 0:
        return sum(values) / len(values)
    else:
        return 0

        
def sensor():
    global distance
    dist = []
    dist.append(float(tof.read()))
    if len(dist) >= 5:
        dist.pop(0)
    distance = round(average(dist)*0.1,1)
    if distance > 50:
        distance = 'no object in range'
    else:
        distance = "%0.0f cm" % distance

def display():
    oled.fill(0)
    oled.text("Entfernung:", 0, 16, 1)
    oled.text(distance, 0, 32, 1)
    oled.show()

print(i2c)

tof = VL53L0X(i2c)
tof.set_measurement_timing_budget(10000)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)

oled = sh1106.SH1106_I2C(128, 64, i2c, Pin(0), 0x3c)
oled.sleep(False)
oled.flip()
oled.fill(0)

while True:
    time = ticks_ms()
    if (ticks_diff(time, passed) > 500):
        for i in range (5):
            sensor()
        try:
            print("%0.0f cm" % distance)
        except:
            print(distance)
        display()
        passed = time

    
    
    
    