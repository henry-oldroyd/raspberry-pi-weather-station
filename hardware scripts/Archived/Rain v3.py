import time

import board
import busio
#from adafruit_bme280 import basic as adafruit_bme280
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1015 as ADS

import RPi.GPIO as GPIO

#bme = adafruit_bme280.Adafruit_BME280_I2C(i2c)
ads = ADS.ADS1015(i2c)
ads.gain = 1

interval = 10 #How long we want to wait between loops (seconds)
rainTick = 0 #Used to count the number of times the rain input is triggered

#Set GPIO pins to use BCM pin numbers
GPIO.setmode(GPIO.BCM)

#Set digital pin 23 to an input and enable the pullup
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Event to detect rainfall tick
GPIO.add_event_detect(23, GPIO.FALLING)

def raintrig(self):
    global rainTick
    rainTick += 1

GPIO.add_event_callback(23, raintrig)

while True:

    time.sleep(interval)

    #Calculate accumulated rainfall over the last 15 seconds
    rainFall = rainTick * 0.2794
    rainTick = 0

    #Print the results
    print( "Rainfall: " , rainFall, "mm")
    print( " ")
