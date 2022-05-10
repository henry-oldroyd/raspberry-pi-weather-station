import time

import board
import busio
#from adafruit_bme280 import basic as adafruit_bme280
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#bme = adafruit_bme280.Adafruit_BME280_I2C(i2c)
ads = ADS.ADS1015(i2c)
ads.gain = 1

interval = 10 #Gap between readings

while True:

    time.sleep(interval)

    #Calculate wind direction based on ADC reading
    chan = AnalogIn(ads, ADS.P0)
    val = chan.value
    windDir = "Not Connected"
    windDeg = 999

    if 20000 <= val <= 20500:
        windDir = "N"
        windDeg = 0

    if 10000 <= val <= 10500:
        windDir = "NNE"
        windDeg = 22.5

    if 11500 <= val <= 12000:
        windDir = "NE"
        windDeg = 45

    if 2000 <= val <= 2250:
        windDir = "ENE"
        windDeg = 67.5

    if 2300 <= val <= 2500:
        windDir = "E"
        windDeg = 90

    if 1500 <= val <= 1950:
        windDir = "ESE"
        windDeg = 112.5

    if 4500 <= val <= 4900:
        windDir = "SE"
        windDeg = 135

    if 3000 <= val <= 3500:
        windDir = "SSE"
        windDeg = 157.5

    if 7000 <= val <= 7500:
        windDir = "S"
        windDeg = 180

    if 6000 <= val <= 6500:
        windDir = "SSW"
        windDeg = 202.5

    if 16000 <= val <= 16500:
        windDir = "SW"
        windDeg = 225

    if 15000 <= val <= 15500:
        windDir = "WSW"
        windDeg = 247.5

    if 24000 <= val <= 24500:
        windDir = "W"
        windDeg = 270

    if 21000 <= val <= 21500:
        windDir = "WNW"
        windDeg = 292.5

    if 22500 <= val <= 23000:
        windDir = "NW"
        windDeg = 315

    if 17500 <= val <= 18500:
        windDir = "NNW"
        windDeg = 337.5

    #Print the results
    print( "Wind Direction: " , windDir, "(", windDeg, ")")
    print( " ")

