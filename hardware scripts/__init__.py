import Ann14 as Ann
import BME8 as BME
windSpeed = Ann.main()
temp, press, humid = BME.main()
print(windSpeed)
print(temp, press, humid)
