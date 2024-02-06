"""
ESP32-S3-DevKitC V4/MicroPython
240x280 ST7789 SPI LCD
VL53LO
Display distance to object above VL53 up to 50cm

06.10.23
Riko Pals

"""


# ----- LIBRARIES

from machine import Pin, SoftI2C, SPI
from utime import ticks_ms, ticks_diff

from vl53l0x import VL53L0X
import st7789py as st7789
import vga1_16x32 as font


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
disp_width = 240
disp_height = 280
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)

# ----- I2C setup
i2c = SoftI2C(scl=Pin(pin_SCL), sda=Pin(pin_SDA), freq=100000)
# ----- SPI setup
pin_spi_sck = Pin(6, Pin.OUT)
pin_spi_mosi = Pin(7, Pin.OUT)
pin_spi_miso = Pin(15, Pin.IN)
pin_st7789_res = Pin(st7789_res, Pin.OUT)
pin_st7789_dc = Pin(st7789_dc, Pin.OUT)
spi = SPI(2, sck=pin_spi_sck, mosi=pin_spi_mosi, miso=pin_spi_miso,
                   baudrate=40000000, polarity=1, phase=0, bits=8)

display = st7789.ST7789(spi, disp_width, disp_width,
                          reset=pin_st7789_res,
                          dc=pin_st7789_dc,
                          xstart=0, ystart=0, rotation=0)
        
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
    if distance > 500:
        distance = 'no object in Range'
    
    
def display_setup():
    try:
        display.fill(st7789.BLACK)
        display.text(font, "Entfernung:", 10, 50)
    except:
        pass


def display():
    try:
        display.text(font, "%0.0f cm" % distance, 10, 80)
    except:
        display.text(font, distance, 10, 80)

print(i2c)
print(spi)

tof = VL53L0X(i2c)
tof.set_measurement_timing_budget(10000)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)

    
display_setup()

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

    
    
    
    