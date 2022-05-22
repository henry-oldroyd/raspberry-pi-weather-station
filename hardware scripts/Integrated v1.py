from gpiozero import Button
import math
import time

try:
	from smbus2 import SMBus
except ImportError:
	from smbus import SMBus
from bme280 import BME280

#Set up anemometer
wind_speed_sensor = Button(14) #GPIO Pin Anemometer connected to
wind_count = 0

#Initalise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

#Set up rain gauge
rain_sensor = Button(6) #Change value to GPIO pin the guage is connected to
bucket_size = 0.2794 #Again change as needed to volume of water needed to tip rain gague
rain_count = 0

def spin():
    global wind_count
    wind_count = wind_count + 1

def calculateSpeed(wind_interval):
    radius_cm = 9.0
    global wind_count
    
    cm_in_km = 100000
    secs_in_hr = 3600
    km_per_mile = 1.60934

    anem_factor = 1.18 #Due to energy being lost when blades turn - differenent annemometer will have different no. 

    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0
    
    dist_cm = circumference_cm * rotations
    dist_km = (circumference_cm * rotations) / cm_in_km
    
    km_per_sec = (dist_km / wind_interval)
    km_per_hour = (km_per_sec * secs_in_hr) * anem_factor
    miles_per_hour = km_per_hour / km_per_mile

    #CHANGE BELOW LINE TO SEND DATA TO BACKEND
    print(miles_per_hour)

def reset_wind():
    global wind_count
    wind_count = 0

def bucket_tipped():
    global rain_count
    count = count + 1
    print(count * bucket_size)

def reset_rainfall():
    global rain_count
    count = 0

wind_gap = 5 #Gap between calculating speeds
startTime = time.time()
rainfallStart = time.time()

while True:
	while time.time() - startTime < wind_gap:
		wind_speed_sensor.when_pressed = spin
	reset_wind()

        #Take Rain Gauge Reading
        rain_sensor.when_pressed = bucket_tipped #Not sure where I put this to ensure measurements are still taken for other sensors but also for rain gauge (which will be triggered less often)

        if time.time() - rainfallStart >= (60 * 60 * 24):
            reset_rainfall()
            rainfallStart = time.time()

        #Take  BME reading
        temperature = bme280.get_temperature()
	pressure = bme280.get_pressure() + 12
	humidity = bme280.get_humidity() + 4
	
	#CHANGE BELOW LINE TO SEND DATA TO BACKEND
	print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperature, pressure, humidity))

	
	startTime = time.time()
