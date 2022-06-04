from gpiozero import Button
import datetime
import time

#Record Bucket Tip
def bucketTipped():
        dtNow = datetime.datetime.now()
        appendMe = dtNow.strftime("%d/%m/%Y, %H:%M:%S") #Formats current date and time as DD/MM/YY, HH:MM:SS
        
        rainFile = open("rainTimesAll.txt", "a")
        rainFile.write(appendMe + "\n")
        rainFile.close()

#Removes bucket tips from previous day
def cleanRainfall(dateNow):
	rainFile = open("rainTimesAll.txt", "r")
	rainTimes = rainFile.readlines()
	rainFile.close()
	if len(rainTimes) > 0:
		while (rainTimes[0])[0:9] != dateNow:
			rainTimes.remove(rainTimes[0])
			
		recentRainFile = open("rainTimesAll.txt", "w")
		for times in rainTimes:
			recentRainFile.write(times)
		recentRainFile.close()
	return len(rainTimes)

#Returns volume of rain in given period of time
def returnTips():
        timeNow = datetime.datetime.now()
        dtForm = timeNow.strftime("%d/%m/%Y, %H:%M:%S") #Formats current date and time as DD/MM/YY, HH:MM:SS
        
        bucketTips = cleanRainfall(dtForm[0:9])
        bucket_size = 0.2794 #Volume of water needed to tip rain gague

        return bucketTips * bucket_size #Returns volume of rain collected in given period

#Wait for and record bucket tips
def main():
	rain_sensor = Button(6) #GPIO pin guage is connected to
	startTime = time.time()
 
	while time.time() - startTime < (15): #Change RHS for time between readings
		rain_sensor.when_pressed = bucketTipped
	volumeCollected = returnTips()
	return volumeCollected
