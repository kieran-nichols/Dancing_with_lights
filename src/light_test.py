# Inititalize packages
from govee_api_ble import GoveeDevice
import time

# Device setup
my_device = GoveeDevice('A4:C1:38:59:43:27')#('A4:C1:38:59:43:27') D4:AD:FC:C1:2C:43
# If I wait too long (more than 1 sec) then the bluetooth connection could fail
#time.sleep(5) # need extra time to setup the connection

# Ensure that the device starts as turned off
my_device.setPower(False) # Turns device off
time.sleep(0.1)

# Turn on device
my_device.setPower(True) # Turns device on
my_device.setBrightness(1)
time.sleep(1)

#Change color to red, then blue, then green
white = [255,255,255]
red = [0,255,0]
blue = [0,0,255]
green = [255,0,0]
colors = [red, blue, green]
brightnesses = [x for x in range(10,100,25)]
# brightness less than 10 seems hard to achieve

for color in colors:
	my_device.setBrightness(10)
	#time.sleep(0.5) # need sleep to have enough time to change brightness
	my_device.setColor(color) # Sets entire light strip to new color
	# for color, increase brightness from 0 to 100 in increments of 20
	for brightness in brightnesses:
		my_device.setBrightness(brightness)
		time.sleep(0.5)
	

my_device.setColor(white)	
time.sleep(1)
#Turn off device
my_device.setPower(False) # Turns device off
