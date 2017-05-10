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

class SpiAdc():
    def __init__(self):
        self.delay = 0      #Minimization 20ms

        self.channel = 0

        self.spi = spidev.SpiDev()
        self.spi.open(0, 1)             #port 0, device(cs) 1(ADC)
        self.spi.max_speed_hz = 1000000 #1MHz

    def set_channel(self, channel):
        self.channel = channel

    def measure(self):
        data = self.spi.xfer2([0x6 | (self.channel & 0x7) >> 2, ((self.channel & 0x7) << 6), 0 ])
        return ((data[1] & 0x0F) << 8) + data[2]   #12bit access

    def measure_average(self, count=5, delay = 220 * MS):
        delay = delay - 200 * MS
        sum_measure = 0

        for i in range(count):
            sum_measure += self.measure()
            time.sleep(delay)

        return sum_measure / count
