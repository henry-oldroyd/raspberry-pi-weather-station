import requests
import random
import logging

# local
import logger

# setup logger
logger = logging.getLogger(__name__)

# will be sotred in an environmental variable in PI
SECRET_KEY = "ABC123-this-is-a-pi-secret-key!"
logger.info(f"using secret key:   {SECRET_KEY}")
SERVER_URL = 'http://127.0.0.1:5000/data'

example_data = {
    "light": random.randint(0, 100),
    "rain": random.randint(0, 100)
}
logger.info(f"using sample data:   {example_data}")



data_to_send = {"SECRET_KEY": SECRET_KEY, "new_data_item": example_data}
logger.info(f"data about to be sent in post request:   {data_to_send}")
try:
    try:    
        request = requests.post(SERVER_URL, json=data_to_send)
        assert request.status_code == 200, f"Status code was not 200 success but was  {request.status_code}"
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Post request to url  {SERVER_URL}  failed to connect")
        raise
    except AssertionError as e:
        logger.error("status code was not 200")
        match request.status_code:
            case 404:
                logger.error('page not found')
            case 401:
                logger.error('authentication failed, check key')
            case 500:
                logger.error('internal server error, perhaps flask server has crashed')
        raise
    else:
        logger.info("Post request successfull")
        logger.info(f"request status code:   {request.status_code}")
        logger.info(f"returned text:   {request.text}")
except Exception as e:
    logger.exception(e)
    raise

