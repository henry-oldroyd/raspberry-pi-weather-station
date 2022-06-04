import Ann15 as Ann
import BME8 as BME
import Rain15 as Rain

#Takes readings
rainVol = Rain.main()
windSpeed = Ann.main()
temp, press, humid = BME.main()

#Prints out values - in future will send to backend
print(rainVol)
print(windSpeed)
print(temp, press, humid)
