import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

scan_pins = (24, 22, 18, 16)
read_pins = (12, 10, 8)

for pin in scan_pins: GPIO.setup(pin, GPIO.OUT)
for pin in read_pins: GPIO.setup(pin, GPIO.IN)

try:
	while True:
		key_status = []
		for i in range(4):
			GPIO.output(scan_pins[i], True)

			tmp = []
			for j in range(3):
				tmp.append(1 if GPIO.input(read_pins[j]) else 0)

			GPIO.output(scan_pins[i], False)

			key_status.append(tmp)
			sleep(0.01)

		print(key_status)

finally:
	GPIO.cleanup()
