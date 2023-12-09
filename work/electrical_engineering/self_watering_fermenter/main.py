from machine import Pin
import time

pump = Pin(0, Pin.OUT, Pin.PULL_UP)    # create output pin on GPIO0 = Pin 1 (drag up to 3.3V with an internal resistor)
sensor = Pin(1, Pin.IN, Pin.PULL_UP) # create input pin on GPIO1 = Pin 2

pump.value(1)

time.sleep(15)

while True:
    if sensor.value() == 1:
        pump.value(1)
    elif sensor.value() == 0:
        pump.value(0)