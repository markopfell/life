from machine import Pin, ADC
import time
import os


# digital_water_level_sensor = Pin(2, Pin.IN, Pin.PULL_UP) # just not working what the heck 12/4/23 1800
# # Need ull up pull down as otherwise input is floating???
# print(water_level_sensor_pin.value())

pump = Pin(1, Pin.OUT) # p.high turns pump off, p.low() turns pump?!? on 12/4/23 1600

pump.low()

# analog_water_level_sensor = ADC(Pin(26)) #FRIED??!?! 12/4/23 1836
analog_water_level_sensor = ADC(Pin(27)) #FRIED??!?! 12/4/23 1836
#low @ 0V = 224, high @ 3.3V = 65535

# logging stub #
file = open('data.csv', 'w')
row_count = 0
rows = 10


while True:
    time.sleep(1)
#     print(digital_water_level_sensor.value())
#     print(analog_water_level_sensor.read_u16()) #low @ 0V = 224, high @ 3.3V = 65535
    analog_water_level_sensor_decimal_value = analog_water_level_sensor.read_u16()
    if analog_water_level_sensor_decimal_value > 30000:
        print("sensor dry ~= low water -> pumping")
    else:
        print("sensor wet ~= water level acceptable -> pump off")
        
    print("	",analog_water_level_sensor_decimal_value)
    
    if row_count < rows:
        file.write(str(analog_water_level_sensor_decimal_value)+',')
        row_count = row_count + 1
    else:
        file.close()
        # os.remove('data.csv')

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