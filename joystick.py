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

class joystick():

    UP, DOWN, LEFT, RIGHT, CENTER = 0, 1, 2, 3, 4

    def __init__(self, ):
        super().__init__()

        self.func = None
        self.args = None
        self.is_stop = True

        self.up = 5
        self.down = 6
        self.left = 16
        self.right = 20
        self.center = 21

        #, pull_up_down=GPIO.PUD_UP

        GPIO.setup(self.up, GPIO.IN)
        GPIO.setup(self.down, GPIO.IN)
        GPIO.setup(self.left, GPIO.IN)
        GPIO.setup(self.right, GPIO.IN)
        GPIO.setup(self.center, GPIO.IN)

    def __del__(self):
        super().__del__()

    def __callback(self, gpio):

        if gpio == self.up:
            self.func(Joystick.UP, *self.args)
        elif gpio == self.down:
            self.func(Joystick.DOWN, *self.args)
        elif gpio == self.left:
            self.func(Joystick.LEFT, *self.args)
        elif gpio == self.right:
            self.func(Joystick.RIGHT, *self.args)
        elif gpio == self.center:
            self.func(Joystick.CENTER, *self.args)

    def start(self, func, *args):
        if self.is_stop:
            self.func = func
            self.args = args
            self.is_stop = False

            GPIO.add_event_detect(self.up, GPIO.RISING, callback=self.__callback, bouncetime=50)
            GPIO.add_event_detect(self.down, GPIO.RISING, callback=self.__callback, bouncetime=50)
            GPIO.add_event_detect(self.left, GPIO.RISING, callback=self.__callback, bouncetime=50)
            GPIO.add_event_detect(self.right, GPIO.RISING, callback=self.__callback, bouncetime=50)
            GPIO.add_event_detect(self.center, GPIO.RISING, callback=self.__callback, bouncetime=50)

    def stop(self):
        if not self.is_stop:
            self.is_stop = True

            GPIO.remove_event_detect(self.up)
            GPIO.remove_event_detect(self.down)
            GPIO.remove_event_detect(self.left)
            GPIO.remove_event_detect(self.right)
            GPIO.remove_event_detect(self.center)

    def input(self):
        while True:
            if GPIO.input(self.up):
                return Joystick.UP
            elif GPIO.input(self.down):
                return Joystick.DOWN
            elif GPIO.input(self.left):
                return Joystick.LEFT
            elif GPIO.input(self.right):
                return Joystick.RIGHT
            elif GPIO.input(self.center):
                return Joystick.CENTER
            time.sleep(20 * MS)
