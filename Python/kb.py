'''matrix scan keyboard using GPIO in Raspberry Pi'''

import RPi.GPIO as GPIO
from time import sleep

# key map, 1d array is enough
key = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#')

scan_pins = (24, 22, 18, 16)
read_pins = (12, 10, 8)

# initialize GPIO and pins
def init():
	GPIO.setmode(GPIO.BOARD)
	for pin in scan_pins: GPIO.setup(pin, GPIO.OUT)
	for pin in read_pins: GPIO.setup(pin, GPIO.IN)

# scan input
def scan():
	# record status of every key
	key_status = []

	# scan every line in keyboard
	for i in range(4):
		# throw singals
		GPIO.output(scan_pins[i], True)

		# scan every key in line
		for j in range(3):
			# read key status
			key_status.append(1 if GPIO.input(read_pins[j]) else 0)

		GPIO.output(scan_pins[i], False)
		sleep(0.01)

	# output key when 1 key pressed only
	if key_status.count(1) == 1:
		print(key[key_status.index(1)])
		return key[key_status.index(1)]

	return 0

def close():
	GPIO.cleanup()