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
import Rain15 as Rain
import Wind14 as Wind
import logger as logger_module #For logging

def integerCheck(checkMe): #Ensures all values have been calculated as integers (i.e. all valid) - if not defaults to 0
    try:
        checkMe = int(checkMe)
    except ValueError:
        checkMe = 0
    return checkMe
        

def send_reading(pressure, temperature, humidity, wind_speed, wind_direction, precipitation):
    #Server/Logger setup
    #Local
    PORT = 5000

    #Setup logger
    logger_module.setup_logger(os.path.basename(__file__))
    logger = logging.getLogger(os.path.basename(__file__))

    #Setting up server
    SERVER_URL = 'http://127.0.0.1:5000/data'

    #Will be stored in an environmental variable in PI
    with open("secret_key.key", "r") as file:
        SECRET_KEY = file.read()

    output_safe_secret_key = SECRET_KEY[:4] + "*"*(len(SECRET_KEY)-8) + SECRET_KEY[-4:]
    logger.info(f"using secret key:   {output_safe_secret_key}")
    logger.info(f"using server url:   {SERVER_URL}")

    readingData = {
        'pressure': pressure,
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'precipitation': precipitation
    }
    logger.info(f"using data:   {example_data}")

    payload = {"secret_key": SECRET_KEY, "new_data_item": readingData}
    logger.info(f"data about to be sent in post request:   {payload}")

    try:
        try:
            request = requests.post(SERVER_URL, json=payload)
            # request = requests.post('https://stackoverflow.com/', json=payload)
            assert request.status_code == 200, f"Status code was not 200 success but was  {request.status_code}"
        except except requests.exceptions.ConnectionError as e:
            logger.critical(f"Post request to url  {SERVER_URL}  failed to connect, server offline?")
            raise
        except AssertionError as e:
            logger.critical("status code was not 200")
            if request.status_code == 404:
                    logger.critical('404 page not found')
            elif request.status_code == 401:
                    logger.critical('401 authentication failed, check key')
            elif request.status_code == 500:
                    logger.critical('500 internal server error, perhaps flask server has crashed')
        else:
            logger.info("Post request successfull")
            logger.info(f"request status code:   {request.status_code}")
            json = json.loads(request.text)
            logger.info(f"""returned json data:   {json}""")

    except Exception as e:
        logger.exception(e)
        raise

#Takes readings - ensures they are integers
rainVol = Rain.main()
rainVol = integerCheck(rainVol)

windSpeed = Ann.main()
windSpeed = integerCheck(windSpeed)

temp, press, humid = BME.main()
temp = integerCheck(temp)
press = integerCheck(press)
humid = integerCheck(humid)

windD = Wind.get_value()
windD = integerCheck(windD)

#Send values to store in server
send_reading(press, temp, humid, windSpeed, windD, rainVol)
	
#Prints out values - for testing
#print(rainVol)
#print(windSpeed)
#print(temp, press, humid)
#print(windD)
