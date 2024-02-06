# import time
from machine import Pin, SoftI2C
from vl53l0x import VL53L0X


sda = Pin(15)
scl = Pin(16)

i2c = SoftI2C(sda=sda, scl=scl)

# Create a VL53L0X object
tof = VL53L0X(i2c)

# the measuring_timing_budget is a value in ms, the longer the budget, the more accurate the reading.
budget = tof.measurement_timing_budget_us
tof.set_measurement_timing_budget(10000)

# Sets the VCSEL (vertical cavity surface emitting laser) pulse period for the
# given period type (VL53L0X::VcselPeriodPreRange or VL53L0X::VcselPeriodFinalRange) 
# to the given value (in PCLKs). Longer periods increase the potential range of the sensor. 
# Valid values are (even numbers only):

# tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)

# tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)



while True:
    print(tof.read())