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

class Cds(SpiAdc):
    CAL = 4.2

    def __init__(self):
        super().__init__()
        self.set_channel(0x0)

    def measure(self):
        cds = SpiAdc.measure(self)

        volt = cds * (3.3 / 2 ** 12) + 0.1
        r = (10 * 3.3) / volt - 10
        lx = 255.84 * r ** (-10/9) * Cds.CAL

        return cds, round(volt, 2), round(lx, 2)

    def measure_average(self, count=5, delay = 220 * MS):
        delay = delay - 200 * MS
        sum_cds, sum_volt, sum_lx = 0, 0, 0

        for i in range(count):
            tmp = self.measure()
            sum_cds += tmp[0]
            sum_volt += tmp[1]
            sum_lx += tmp[2]
            time.sleep(delay)

        return sum_cds / count, sum_volt / count, sum_lx / count


#def cds_read(dummy, cds, volt, lx, light = Light()):
#    light_ret = light.measure_average()
#    print("cds = %d Level, %.2f Volt, %.2f Lux, light = %.2f Lux"%(cds, volt, lx, light_ret))

if __name__ == "__main__":
    cds = Cds()

    while True:
        ret = cds.measure_average()
        print("current cds = {0}".format(ret))
        time.sleep(1)
