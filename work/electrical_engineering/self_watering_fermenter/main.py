from machine import Pin

# create output pin on GPIO0 = physical Pin 1
pump = Pin(0, Pin.OUT) 

# create input pin on GPIO1 = physical Pin 2
# depending on Pin.PULL_UP resistors has been spotty at best, used external
sensor = Pin(1, Pin.IN)

while True:
     # Liquid level sensor high == 1/logic level high in air
    if sensor.value() == 1: 
        # Gate of N-channel MOSFET switching Drain->Source to ground from float to 5V
        pump.value(1)    