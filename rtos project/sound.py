import RPi.GPIO as GPIO
import smbus
import spidev
import lirc
import time
import ctypes

from SpiAdc import SpiAdc

GPIO.setmode(GPIO.BCM)

LOW = False
HIGH = True

MS = 0.001
US_100 = 0.0001
US = 0.000001

class Sound(SpiAdc):
    CAL = 2062

    def __init__(self):
        super().__init__()
        self.set_channel(0x02)

    def measure(self):
        """
        return 0 ~ 40 level
        """
        return abs(SpiAdc.measure(self) - Sound.CAL)

if __name__ == "__main__":
    sound = Sound()

    while True:
        ret = sound.measure()
        print("current potent = {0}".format(round(ret)))
        time.sleep(0.1)
