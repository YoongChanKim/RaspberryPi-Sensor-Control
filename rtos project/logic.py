
import character_lcd
import motor_control
import temperature
import led
import pir

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

def led_blink(led, speed):
    led.on()
    time.sleep(speed)
    led.off()
    time.sleep(speed)
    
if __name__ == "__main__":
    manager_motor = motor_control.ManageMotor()
    manager_temp = temperature.temperature()
    manager_lcd = character_lcd.CharLcd()
    manager_led = led.Led(1)
    manager_pir = pir.Pir()
    
    while True:
        temp = manager_temp.measure_temp()
        detect = manager_pir.detect_motion()
        manager_lcd.clear()
        manager_lcd.set_pos(0, 0)
        manager_lcd.puts("Temp: " + str(round(temp,2)))
        print("Temp: " + str(round(temp, 2)))
        manager_lcd.set_pos(1, 0)
        manager_lcd.puts("AirCon: ")
        
        if temp > 25 and detect:
            manager_motor.rotate("CW", 5)
            manager_lcd.puts("On")
            led_blink(manager_led, 0.01)
        else:
            manager_motor.stop()
            manager_lcd.puts("Off")
