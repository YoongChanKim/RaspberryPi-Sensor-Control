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

class Led():
    def __init__(self, led):
        if led == 1:
            self.led = 14
        elif led == 2:
            self.led = 15

        GPIO.setup(self.led, GPIO.OUT)

    def on(self):
        GPIO.output(self.led, HIGH)

    def off(self):
        GPIO.output(self.led, LOW)

if __name__ == "__main__":
    led_one = Led(1)
    led_two = Led(2)

    while True:
        try:
            print("One on")
            led_one.on()
            led_two.off()
            time.sleep(0.5)

            print("Two on")
            led_one.off()
            led_two.on()
            time.sleep(0.5)
        except KeyboardInterrupt:
            GPIO.cleanup()
