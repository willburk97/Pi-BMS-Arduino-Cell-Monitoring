import RPi.GPIO as GPIO
import time
import spidev
from Adafruit_IO import Client, Feed, RequestError

ADAFRUIT_IO_USERNAME = 'yourusernamehere'
ADAFRUIT_IO_KEY = 'yourkeyhere'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
generator_id = 111 # ?? Found this in someone's code. Not sure the purpose.

battVolt1 = 0

spi2 = spidev.SpiDev()
spi2.open(0, 1)
spi2.max_speed_hz = 8000  # Was 122000 7-12
# The line above slowed it down in order to get it comms to function through an opto-isolator. This was necessary in order to connect
# multiple Arduinos to multiple cells of a series connected pack of batteries. (The ground of each arduino would be the + of the previous cell...
# ...not the ground of the Pi. I only connected the clock through an opto-isolator, but all 4 signal wires would need to be. 4 opto-isolators per arduino.

# These two lines may be unnecessary, I was controlling an LED as well through adafruit io.
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

storageTime = 60000
lastStorage = (round(time.time() * 1000))
onlineDelay = 1000
lastOnlineCheck = 0
sampleTime = 1000
lastSample = 0
averageSamples = 5
battVoltList = [0] * averageSamples

Battery1 = aio.feeds('battery')

try:
	while True :
		currentMillis = round(time.time() * 1000)

		if lastSample + sampleTime < currentMillis :
			lastSample = currentMillis
			spi2data = spi2.xfer2([1, 69])
			battVolt1 = (spi2data[0]*256 + spi2data[1])/100
			battVoltList = [battVolt1] + battVoltList[0:-1]
			battVolt1 = (int((sum(battVoltList) / averageSamples)*100)/100) # round to 2 decimal places

		if lastStorage + storageTime < currentMillis :
			lastStorage = currentMillis
			if battVolt1 > 2.0 and battVolt1 < 5.5 :  # Very, very basic error checking
				aio.send_data(Battery1.key, battVolt1)

# Chill a bit to drop cpu processing.
		time.sleep(0.1)

finally:
	
	GPIO.cleanup()
