from machine import Pin
import time

# create output pin on GPIO0 = physical Pin 1
pump = Pin(0, Pin.OUT, Pin.PULL_UP) 

# create input pin on GPIO1 = physical Pin 2 (drag up to 3.3V with an internal resistor)
sensor = Pin(1, Pin.IN, Pin.PULL_UP)
# analog_sensor = ADC(Pin(28))

while True:
    if sensor.value() == 1:
        pump.value(1)
    elif sensor.value() == 0:
        pump.value(0)
        print(sensor.value())