import requests
import random
import logging
import os
import marshmallow as m

# local
import logger as logger_module

# setup logger
logger_module.setup_logger(os.path.basename(__file__))
logger = logging.getLogger(os.path.basename(__file__))

# will be sotred in an environmental variable in PI
with open("secret_key.key", "r") as file:
    SECRET_KEY = file.read()
SERVER_URL = 'http://127.0.0.1:5000/add_reading'

output_safe_secret_key = SECRET_KEY[:4] + "*"*(len(SECRET_KEY)-8) + SECRET_KEY[-4:]
logger.info(f"using secret key:   {output_safe_secret_key}")
logger.info(f"using server url:   {SERVER_URL}")


logger.info("defining data readout schema")

class Data_Reading():
    def __init__(self, pressure, temperature, humidity, wind_speed, wind_direction, precipitation):
        self.pressure = pressure
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.precipitation = precipitation

class Data_Reading_Schema(m.Schema):
    pressure = m.fields.Float(required=True),
    temperature = m.fields.Float(required=True),
    humidity = m.fields.Float(required=True),
    wind_speed = m.fields.Float(required=True),
    wind_direction = m.fields.Float(required=True),
    precipitation = m.fields.Float(required=True),
    timestamp = m.fields.Float(required=True)
    
    @m.post_load
    def make_data_reading(self, data, **kwargs):
        return Data_Reading(**data)

data_reading_schema = Data_Reading_Schema()


def send_to_server(data_reading: Data_Reading):
    json_data = data_reading_schema.dump(data_reading)
    logger.info(f"using data:   {json_data}")

    data_to_send = {"secret_key": SECRET_KEY, "data_item": json_data}
    logger.info(f"data about to be sent in post request:   {data_to_send}")
    try:
        try:
            request = requests.post(SERVER_URL, json=data_to_send)
            # request = requests.post('https://stackoverflow.com/', json=data_to_send)
            assert request.status_code == 200, f"Status code was not 200 success but was  {request.status_code}"
        except requests.exceptions.ConnectionError as e:
            logger.critical(f"Post request to url  {SERVER_URL}  failed to connect, server offline?")
            raise
        except AssertionError as e:
            logger.critical("status code was not 200")
            match request.status_code:
                case 404:
                    logger.critical('404 page not found')
                case 401:
                    logger.critical('401 authentication failed, check key')
                case 500:
                    logger.critical('500 internal server error, perhaps flask server has crashed')
            raise
        else:
            logger.info("Post request successfull")
            logger.info(f"request status code:   {request.status_code}")
            text = request.text[:250].replace("\n", "")
            logger.info(f"returned text (first 250 characters):   {text}")
    except Exception as e:
        logger.exception(e)
        raise
    else:
        return True