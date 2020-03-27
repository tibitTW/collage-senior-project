import RPi.GPIO as GPIO
from time import sleep

# key map, 1d array is enough
key = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#')

# define pins
scan_pins = (25, 8, 7, 1)
read_pins = (4, 3, 2)


def init():  # initialize GPIO and pins
    GPIO.setmode(GPIO.BCM)
    for pin in scan_pins:
        GPIO.setup(pin, GPIO.OUT)
    for pin in read_pins:
        GPIO.setup(pin, GPIO.IN)


def scan():  # scan input
    key_status = []  # record status of every key

    for i in range(4):  # scan every line in keyboard
        GPIO.output(scan_pins[i], False)  # throw singals

        for j in range(3):  # scan every key in line and read key status
            key_status.append(1 if GPIO.input(read_pins[j]) else 0)

        GPIO.output(scan_pins[i], True)
        sleep(0.01)

    if key_status.count(0) == 1:  # output key when 1 key pressed only
        return key[key_status.index(0)]

    return 0


def close():
    GPIO.cleanup()
