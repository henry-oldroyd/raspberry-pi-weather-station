from gpiozero import Button
import time

rain_sensor = Button(6) #Change value to GPIO pin the guage is connected to
bucket_size = 0.2794 #Again change as needed to volume of water needed to tip rain gague
count = 0

def bucket_tipped():
    global count
    count = count + 1
    print(count * bucket_size)

def reset_rainfall():
    global count
    count = 0

startTime = time.time()

while True:
	while time.time() - startTime < (60 * 60 * 24):
		rain_sensor.when_pressed = bucket_tipped
        reset_rainfall()
	startTime = time.time()
