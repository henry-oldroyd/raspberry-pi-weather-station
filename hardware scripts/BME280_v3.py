import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)


calibration_params = bme280.load_calibration_params(bus, address)#not sure what goes here

#sample method takes a single reading and return compensated_reading object

data= bme280.sample(bus, address, calibration_params)

#compensated_reading class has following attributes:
print(data.id)
print(data.timestamp)
print(data.temperature)
print(data.pressure)
print(data.humidity)

#handy string representation
print(data)
