from gpiozero import Button
import math

def spin():
    global wind_count
    wind_count = wind_count + 1
    #print("spin" + str(wind_count))

def calculateSpeed():
    radius_cm = 9.0
    wind_interval = 5 #Change me to the time between readings
    global wind_count
    
    cm_in_km = 100000
    
    secs_in_hr = 3600

    km_per_mile = 1.60934
    kmph_per_knot = 1.852

    anem_factor = 1.18 #Due to energy being lost when blades turn - differenent annemometer will have different no. 

    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0
    
    dist_cm = circumference_cm * rotations
    dist_km = (circumference_cm * rotations) / cm_in_km
    
    cm_per_sec = (dist_cm / wind_interval) * anem_factor
    km_per_sec = (dist_km / wind_interval)
    km_per_hour = (km_per_sec * secs_in_hr) * anem_factor
    miles_per_hour = km_per_hour / km_per_mile
    knots = km_per_hour / kmph_per_know

    return cm_per_sec, km_per_hour

def reset_wind():
    global wind_count
    wind_count = 0

wind_speed_sensor.when_pressed = spin
wind_speed_sensor = Button(wind_interval)
wind_count = 0
