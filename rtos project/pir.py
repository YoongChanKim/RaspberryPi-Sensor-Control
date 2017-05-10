import RPi.GPIO as GPIO
import smbus
import spidev
import lirc
import time
import ctypes

GPIO.setmode(GPIO.BCM)

LOW = False
HIGH = True

MS = 0.001
US_100 = 0.0001
US = 0.000001

class Pir():
	def __init__(self):
		self.pir = 24

		GPIO.setup(self.pir, GPIO.IN)

	def detect_motion(self):
		if GPIO.input(self.pir):
			return True

		else:
			return False
