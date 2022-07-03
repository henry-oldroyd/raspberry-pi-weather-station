import requests
from random import uniform, randint


SERVER_URL = 'http://127.0.0.1:5000/data'


# will be stored in an environmental variable in PI
with open("secret_key.key", "r") as file:
    SECRET_KEY = file.read()


def send_reading(pressure, temperature, humidity, wind_speed, wind_direction, precipitation):
    reading_data = {
        'pressure': pressure,
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'precipitation': precipitation
    }


    payload = {"secret_key": SECRET_KEY, "new_data_item": reading_data}

    try:
        request = requests.post(SERVER_URL, json=payload)
        # request = requests.post('https://stackoverflow.com/', json=data_to_send)
        assert request.status_code == 200, f"Status code was not 200 success but was  {request.status_code}"
    except Exception as e:
        print("ERROR:")
        print(e)

if __name__ == '__main__':

    send_reading(
        pressure=uniform(0, 30),
        temperature=uniform(0, 30),
        humidity=uniform(0, 30),
        wind_speed=uniform(0, 30),
        wind_direction=randint(0, 360),
        precipitation=uniform(0, 4),
    )