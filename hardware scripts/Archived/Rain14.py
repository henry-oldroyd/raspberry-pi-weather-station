from gpiozero import Button
import time

#Record Bucket Tip
def bucketTipped():
	rainFile = open("rainTimesAll.txt", "a")
	rainFile.write(str(time.time()) + "\n")
	rainFile.close()

#Removes bucket tips from a given period of time ago
def cleanRainfall(timeNow, timeToKeep): #timeToKeep = discard all records from more than this time ago
	rainFile = open("rainTimesAll.txt", "r")
	rainTimes = rainFile.readlines()
	rainFile.close()
	if len(rainTimes) > 0:
		while timeNow - float((rainTimes[0]).strip()) > timeToKeep:
			rainTimes.remove(rainTimes[0])
		newFileName = "rainTimes" + str(timeToKeep) + ".txt"
                
		recentRainFile = open(newFileName, "w")
		for times in rainTimes:
			recentRainFile.write(times)
		recentRainFile.close()
	return len(rainTimes)

#Returns volume of rain in given period of time
def returnTips():
	bucketTips = cleanRainfall(time.time(), (60 * 15)) #Change second argument to time beyond which records of tips are discarded
	bucket_size = 0.2794 #Volume of water needed to tip rain gague

	return bucketTips * bucket_size #Returns volume of rain collected in given period

#Wait for and record bucket tips
def main():
	rain_sensor = Button(6) #GPIO pin guage is connected to
	startTime = time.time()
 
	while time.time() - startTime < (60 * 15): #Change RHS for time between readings
		rain_sensor.when_pressed = bucketTipped
	volumeCollected = returnTips()
	return volumeCollected
