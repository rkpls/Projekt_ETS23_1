"""
ESP32-S3-DevKitC V4/MicroPython
sh1106 oled
VL53LOX
Display the distance to an object above the VL5310. Up to 50cm

06.10.23
Riko Pals
"""
# ----- LIBRARIES
from machine import Pin, SoftI2C
from utime import ticks_ms, ticks_diff

from vl53l0x import VL53L0X

# ----- PINOUT
pin_SDA = 41
pin_SCL = 42

# ----- VARS
passed = 0
distance = 0

# ----- I2C setup
i2c = SoftI2C(scl=Pin(pin_SCL), sda=Pin(pin_SDA), freq=100000)

# ----- Funktion zum mitteln 
def average(values):
    if len(values) > 0:                         # verhinderung 'devide by zero'
        return sum(values) / len(values)
    else:
        return 0

# ---- Sensor Auslesen
def sensor_read():
    global distance
    dist = []                               # zum mitteln werden die Werte in eine Liste eingetragen
    dist.append(float(tof.read()))
    if len(dist) >= 5:
        dist.pop(0)
    distance = round(average(dist)*0.1,1)   # average ist die funktion oben, wert wird wegen Ungenauigkeiten gerundet und in cm umgerechnet

print(i2c)              #i2c setup-überprüfung

# ----- Sensor setup für Bibliotheknutzung
tof = VL53L0X(i2c)
tof.set_measurement_timing_budget(10000)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)


# ----- Schleife
while True:
    time = ticks_ms()
    if (ticks_diff(time, passed) > 500):        # Programmdurchlauf nur 2x pro sekunde zur systementlastung
        for i in range (5):                     # Mehrfachabfrage zum mitteln der Werte
            sensor_read()
        print(distance)
        passed = time

