from machine import Pin, ADC
import time
# import os

pump = Pin(0, Pin.OUT, Pin.PULL_UP)    # create output pin on GPIO0 = Pin 1 (drag up to 3.3V with an internal resistor)
sensor = Pin(1, Pin.IN, Pin.PULL_UP) # create input pin on GPIO1 = Pin 2

pump.value(1)

time.sleep(15)

while True:
    if sensor.value() == 1:
        pump.value(1)
    elif sensor.value() == 0:
        pump.value(0)

## Sensor ouput = digital high output in air = dry = high > 30000 
# analog_water_level_sensor = ADC(Pin(26))
# analog_water_level_sensor = ADC(Pin(27))
# analog_water_level_sensor.read_u16()
#low @ 0V = 224, high @ 3.3V = 65535
#     print(analog_water_level_sensor.read_u16()) #low @ 0V = 224, high @ 3.3V = 65535

# # logging stub #
# file = open('data.csv', 'w')
# row_count = 0

# 24 hours = 86,400 seconds.  1 byte per char, 2 byes per int, 3 bytes per entry  2 megabytes of flash
# factor of 10 -> 0.2 MB = 50,000 entries or once every 2nd second 
# rows = 10000


# while True:
#     
#     
#     
#     if sensor.value() == 1: # high in air
#         pump.high()
#     else:
#         pump.low()
#         pass
    
    
#     time.sleep(2)
#     print(digital_water_level_sensor.value())
#     print(analog_water_level_sensor.read_u16()) #low @ 0V = 224, high @ 3.3V = 65535
#     analog_water_level_sensor_decimal_value = analog_water_level_sensor.read_u16()
#     if analog_water_level_sensor_decimal_value > 30000:
#         print("sensor dry ~= low water -> pumping")
#     else:
#         print("sensor wet ~= water level acceptable -> pump off")
#         
#     print("	",analog_water_level_sensor_decimal_value)
#     
#     if row_count < rows:
#         file.write(str(analog_water_level_sensor_decimal_value)+',')
#         row_count = row_count + 1
#     else:
#         file.close()
#         os.remove('data.csv') # 

#         print(sensor =)
#         pump.high()
#     else:
#         pump.low()



# This pump has a flow rate of 100 mL/min and the fermenter water moat is 50 mL capacity so super slow no need to settle the pump
# print(pump_pin.value(0))


# while True:
# 
# 
# 	# TODO = and add if pump_timer < 30 basically 
#    if water_level_sensor_pin == 1:  # sensor high in air means low water level
#       # TODO = reset  pump timer to 0
# pump_pin.value(1)  # Turn on pump
# 
# 
#    else: # sensor low in water = water level fine
# 	# TODO = start a timer and if the pump_pin has been on for 
#        pump_pin.value(0)  # Turn off pump