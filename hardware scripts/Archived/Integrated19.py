#Import modules
import requests
from datetime import datetime
import json
import random
import logging
import os

#Import files to use
import Ann15 as Ann
import BME8 as BME
import Rain16 as Rain
import Wind14 as Wind
import logger as logger_module #For logging

#Logger Setup
#Logger for sensor readings
logger_module.setup_logger(os.path.basename(__file__) + " - Sensor Logger")
loggerSens = logging.getLogger(os.path.basename(__file__) + " - Sensor Logger")

logger_module.setup_logger(os.path.basename(__file__) + " - Backend Logger")
loggerBack = logging.getLogger(os.path.basename(__file__) + " - Backend Logger")


def integerCheck(checkMe): #Ensures all values have been calculated as integers (i.e. all valid) - if not defaults to 0
    try:
        checkMe = float(checkMe)
    except ValueError:
        loggerSens.error('   {checkMe}   has incorrect form. ')
        checkMe = 0
    return checkMe
        

def send_reading(pressure, temperature, humidity, wind_speed, wind_direction, precipitation):
    #Server setup
    SERVER_URL = 'http://127.0.0.1:5000/data'

    with open("secret_key.key", "r") as file:
        SECRET_KEY = file.read()

    output_safe_secret_key = SECRET_KEY[:4] + "*"*(len(SECRET_KEY)-8) + SECRET_KEY[-4:]
    loggerBack.info(f"using secret key:   {output_safe_secret_key}")
    loggerBack.info(f"using server url:   {SERVER_URL}")

    readingData = {
        'pressure': pressure,
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'precipitation': precipitation
    }
    loggerBack.info(f"data about to be sent in post request:   {readingData}")

    payload = {"secret_key": SECRET_KEY, "new_data_item": readingData}

    try:
        request = requests.post(SERVER_URL, json=payload)
        assert request.status_code == 200, f"Status code was not 200 success but was  {request.status_code}"
    except Exception as e:
        print("ERROR:")
        print(e)
        try:
                if request.status_code == 404:
                        loggerBack.critical('404 page not found')
                elif request.status_code == 401:
                        loggerBack.critical('401 authentication failed, check key')
                elif request.status_code == 500:
                        loggerBack.critical('500 internal server error, perhaps flask server has crashed')
        except:
                print("Request variable not defined. Error occurred before this. ")
        else:
                logger.debug("Status code 200 - date sent successfully.")

#Takes readings - ensures they are integers
loggerSens.info(f"Taking rainfall reading...")
rainVol = Rain.main()
rainVol = integerCheck(rainVol)
loggerSens.info(f"Rainfall reading:   {rainVol}")

loggerSens.info(f"Taking wind speed reading...")
windSpeed = Ann.main()
windSpeed = integerCheck(windSpeed)
loggerSens.info(f"Wind speed reading:   {rainVol}")

loggerSens.info(f"Taking BME readings...")
temp, press, humid = BME.main()
temp = integerCheck(temp)
press = integerCheck(press)
humid = integerCheck(humid)

#Checks BME reading via pressure
if press < 900:
    loggerSens.error('Pressure value <900 - check BME')
else:
    loggerSens.info(f"Temperature reading:   {temp}")
    loggerSens.info(f"Pressure reading:   {press}")
    loggerSens.info(f"Relative Humidity reading:   {humid}")

loggerSens.info(f"Taking Wind Direction readings...")
windD = Wind.get_value()
windD = integerCheck(windD)
loggerSens.info(f"Wind Direction reading:   {humid}")

#Send values to store in server
send_reading(press, temp, humid, windSpeed, windD, rainVol)
