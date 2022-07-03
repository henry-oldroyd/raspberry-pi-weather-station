import Ann15 as Ann
import BME8 as BME
import Rain15 as Rain
import Wind14 as Wind

#Takes readings
rainVol = Rain.main()
windSpeed = Ann.main()
temp, press, humid = BME.main()
windD = Wind.get_value()

#Prints out values - in future will send to backend
print(rainVol)
print(windSpeed)
print(temp, press, humid)
print(windD)
