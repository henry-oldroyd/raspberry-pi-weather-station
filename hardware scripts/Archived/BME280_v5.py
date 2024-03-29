import time
try:
	from smbus2 import SMBus
except ImportError:
	from smbus import SMBus
from bme280 import BME280

print("""all-values.py - Read temp, pressure & humidity

Press Ctrl+C to exit!

""")

# Initalise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

# Write pressure to text file

while True:
	temperature = bme280.get_temperature()
	pressure = bme280.get_pressure() + 12
	results = open("pressureCalibrartion.txt", "a")
	results.write(pressure)
	close(results)
	humidity = bme280.get_humidity()
	print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperature, pressure, humidity))
	time.sleep(1)
