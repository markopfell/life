from machine import Pin
import time

# GPIO0 = physical Pin 1
pump = Pin(0, Pin.OUT) 

# GPIO1 = physical Pin 2
# depending on Pin.PULL_UP resistors has been spotty at best, used external
sensor = Pin(2, Pin.IN)

while True:
     # Liquid level sensor high = 1 = logic level high = 5V in air
     # Converted with a logic level shifter from 5V to 3.3V
    if sensor.value() == 1: 
        # Gate of N-channel MOSFET switching Drain->Source to ground from (float to 5V)
        pump.value(1)
        print('pump on')
    elif sensor.value() == 0:	
        pump.value(0)
        print('pump off')
    else:
        pass
    time.sleep(1)    
    #time.sleep_us(1)    
