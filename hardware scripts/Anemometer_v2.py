#Import GPIO and time libraries
import RPi.GPIO as GPIO
import time

#Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.IN)

#Ann. vane diameter (probably needs to be adjusted
vaneDiameter = 106

#Calculate circumferece in m
vaneCirc = (vaneDiameter / 1000) * 3.1415

#Set to count for inefficiency (just a guess)
aFactor = 2.5

#Start measuring
print("Measuring wind speed ... ")

#Defines rotaitions & triggers variables
rotations = 0
trigger = 0

#Define variable endTime
endTime = time.time() + 10

#Get initial state of sensor
sensorStart = GPIO.input(12)

#Measurement loop - runs for 10s
while time.time() < endtime:
    if GPIO.input(12) == 1 and trigger == 0:
        rotations = rotations+ 1
        trigger = 1
        #print("Recorded a trigger")
        
    if GPIO.input(12) == 0:
        trigger = 0

    #Add a little delay
    time.sleep(0.001)

#If sensor triggered at start but never again, needs to be adjusted
if (rotations == 1) and (sensorStart = 1):
    rotations = 0

#Calculations
rotsPerSec = rotations / 10
windSpeed = rotsPerSec * vaneCirc * aFactor

#Output resuts
print("{:.0f} rotations = {:.2f} rotations/second".format(rotations, rotations / 10))
print("Windspeed is {:.2f} m/s = {.2f} mph".format(windspeed, windspeed * 2.237))

#Cleanup GPIO before finishing
GPIO.cleanup()
