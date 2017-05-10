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

class temperature():
    CAL = -4.4

    def __init__(self):
            self.delay = 0      #Minimization 220ms(internal fix 200ms)

            self.addr = 0x40
            self.cmd_t = 0xf3   #templature
            self.cmd_r = 0xfe   #reset

            self.temp_humi = smbus.SMBus(1)

    def measure_temp(self):
        self.temp_humi.write_byte(self.addr, self.cmd_t)
        time.sleep(100 * MS)    #Internal minimization

        data = []
        tmp = self.temp_humi.read_byte(self.addr)
        data.append(tmp)
        tmp = self.temp_humi.read_byte(self.addr)
        data.append(tmp)

        return (-46.85 + temperature.CAL) + 175.72 / 65536 * (data[1] | data[0] << 8)


    def measure_temp_average(self, count=5, delay = 220 * MS):
        delay = delay - 200 * MS
        sum_temp = 0

        for i in range(count):
            sum_temp += self.measure_temp()
            time.sleep(delay)
        return sum_temp / count

if __name__ == "__main__":
	temp = temperature()
	print("TEMP: " + str(round(temp.measure_temp(),2)))
