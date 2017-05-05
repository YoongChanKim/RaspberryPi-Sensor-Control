import RPi.GPIO as GPIO
import smbus
import spidev
import lirc
import time
import ctypes

from multiprocessing import Process, Manager, Value, Lock
GPIO.setmode(GPIO.BCM)

LOW = False
HIGH = True

MS = 0.001
US_100 = 0.0001
US = 0.000001

class ManageMotor():
    def __init__(self):
        self.pin_cw = 4
        self.pin_ccw = 25
        self.pin_power = 12

        self.on = Value(ctypes.c_float, 0.0)
        self.off = Value(ctypes.c_float, 0.0)

        GPIO.setup(self.pin_cw, GPIO.OUT)
        GPIO.setup(self.pin_ccw, GPIO.OUT)
        GPIO.setup(self.pin_power, GPIO.OUT)
        self.__power_on()

    def __power_on(self, on=True):
        GPIO.output(self.pin_power, on)

    def set_speed(self, speed):
        assert(speed > 0 and speed < 11)

        self.on.value = US_100 * (speed * 0.1)
        self.off.value = US_100 - self.on.value

    def forward(self, speed = 5):
        GPIO.output(self.pin_cw, True)
        GPIO.output(self.pin_ccw, False)
        self.set_speed(speed)

    def backward(self, speed = 5):
        GPIO.output(self.pin_cw, False)
        GPIO.output(self.pin_ccw, True)
        self.set_speed(speed)

    # speed 1 ~ 10
    # direction cw or ccw
    def rotate(self, dir, speed):
        if dir.lower() == "cw":
            self.forward(speed)
        elif dir.lower() == "ccw":
            self.backward(speed)

def motor_unit_test():
    motor = ManageMotor()

    motor.rotate("CW", 5)
    time.sleep(2)

    motor.rotate("CCW", 7)
    time.sleep(2)

if __name__ == '__main__':
    motor_unit_test()
    GPIO.cleanup()
