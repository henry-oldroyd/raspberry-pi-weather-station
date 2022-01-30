from tkinter import E
import requests
import random

example_data = {
    "light": random.randint(0, 100),
    "rain": random.randint(0, 100)
}
print("pi sending data to server")
print(example_data)

request = requests.post("http://127.0.0.1:5000/data", json={"secret_key": "123abc", "new_data_item": example_data})

print("returned result")
print(request.text)

print("test get request")
request = requests.get("http://127.0.0.1:5000/data")
print(request.text)