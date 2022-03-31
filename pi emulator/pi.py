import requests
import json
import random
import logging
import os

# local
import logger as logger_module

PORT = 443

# setup logger
logger_module.setup_logger(os.path.basename(__file__))
logger = logging.getLogger(os.path.basename(__file__))

# will be sotred in an environmental variable in PI
with open("secret_key.key", "r") as file:
    SECRET_KEY = file.read()
SERVER_URL = f'http://127.0.0.1:{PORT}/data'
# SERVER_URL = 'https://cbcb-2-218-255-35.ngrok.io/data'


output_safe_secret_key = SECRET_KEY[:4] + "*"*(len(SECRET_KEY)-8) + SECRET_KEY[-4:]
logger.info(f"using secret key:   {output_safe_secret_key}")
logger.info(f"using server url:   {SERVER_URL}")

example_data = {
    "light": random.randint(0, 100),
    "rain": random.randint(0, 100)
}
logger.info(f"using sample data:   {example_data}")


data_to_send = {"secret_key": SECRET_KEY, "new_data_item": example_data}
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
        # logger.critical("status code was not 200")
        # match request.status_code:
        #     case 404:
        #         logger.critical('404 page not found')
        #     case 401:
        #         logger.critical('401 authentication failed, check key')
        #     case 500:
        #         logger.critical('500 internal server error, perhaps flask server has crashed')
        # raise
        pass
    else:
        logger.info("Post request successfull")
        logger.info(f"request status code:   {request.status_code}")
        json = json.loads(request.text)
        logger.info(f"""returned json data:   {json}""")

except Exception as e:
    logger.exception(e)
    raise
