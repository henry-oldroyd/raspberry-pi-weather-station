import Ann15 as Ann
import BME8 as BME
import Rain14 as Rain
rainVol = Rain.main()
windSpeed = Ann.main()
temp, press, humid = BME.main()
print(rainVol)
print(windSpeed)
print(temp, press, humid)
