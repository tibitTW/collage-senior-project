import RPi.GPIO as GPIO
from time import sleep

is_locked = False

key = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#')

scan_pins = (24, 22, 18, 16)
read_pins = (12, 10, 8)

def init():
	GPIO.setmode(GPIO.BOARD)
	for pin in scan_pins: GPIO.setup(pin, GPIO.OUT)
	for pin in read_pins: GPIO.setup(pin, GPIO.IN)

def scan():
	key_status = []
	for i in range(4):
		GPIO.output(scan_pins[i], True)

		for j in range(3):
			key_status.append(1 if GPIO.input(read_pins[j]) else 0)

		GPIO.output(scan_pins[i], False)

		sleep(0.01)

	print(key_status)
	if key_status.count(1) == 1:
		print(key[key_status.index(1)])

# try:
# 	while True:
# 		kb_scan()

# finally:
# 	GPIO.cleanup()
