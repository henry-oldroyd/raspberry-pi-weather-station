#Import modules
import requests

#Import files to use
import Ann15 as Ann
import BME8 as BME
import Rain15 as Rain
import Wind14 as Wind

#Setting up server
SERVER_URL = 'http://127.0.0.1:5000/data'

#Will be stored in an environmental variable in PI
with open("secret_key.key", "r") as file:
    SECRET_KEY = file.read()

def send_reading(pressure, temperature, humidity, wind_speed, wind_direction, precipitation):
    readingData = {
        'pressure': pressure,
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'precipitation': precipitation
    }

    payload = {"secret_key": SECRET_KEY, "new_data_item": readingData}

    try:
        request = requests.post(SERVER_URL, json=payload)
        # request = requests.post('https://stackoverflow.com/', json=data_to_send)
        assert request.status_code == 200, f"Status code was not 200 success but was  {request.status_code}"
    except Exception as e:
        print("ERROR:")
        print(e)

#Defaults all values to 0
rainVol = 0
windSpeed = 0
temp = 0
press = 0
humid = 0
windD = 0

#Takes readings
rainVol = Rain.main()
windSpeed = Ann.main()
temp, press, humid = BME.main()
windD = Wind.get_value()

#Send values to store in server
send_reading(press, temp, humid, windSpeed, windD, rainVol)

#Prints out values - for testing
#print(rainVol)
#print(windSpeed)
#print(temp, press, humid)
#print(windD)
