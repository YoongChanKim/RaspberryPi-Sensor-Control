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

class pir():

    def __init__(self):
        super().__init__()

        self.pir = 24

        self.func = None
        self.args = None
        self.is_stop = True

        self.real = False
        self.start_clock = 0

        GPIO.setup(self.pir, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Active Low

    def __del__(self):
        super().__del__()

    def __callback(self, gpio):
        if GPIO.input(self.pir):
            self.__rising()
        else:
            self.__falling()

    def __rising(self):
        if self.real:
            self.func(*self.args)
        else:
            end = (time.clock() - self.start_clock) * 1000000
            if(end >= 60):
                self.func(*self.args)
                time.sleep(1)

    def __falling(self):
        self.start_clock = time.clock()

    def start(self, func, *args, real = False):
        if self.is_stop:
            self.func = func
            self.args = args
            self.is_stop = False

        self.real = real
        GPIO.add_event_detect(self.pir, GPIO.BOTH, callback=self.__callback, bouncetime=1)

    def stop(self):
        if not self.is_stop:
            self.is_stop = True
            GPIO.remove_event_detect(self.pir)
