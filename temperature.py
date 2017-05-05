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
    CAL = 0 #-4.4

    def __init__(self):
            super().__init__()

            self.task = None
            self.delay = 0      #Minimization 220ms(internal fix 200ms)
            self.func = None
            self.args = None

            self.addr = 0x40
            self.cmd_t = 0xf3   #templature
            self.cmd_r = 0xfe   #reset

            self.temp_humi = smbus.SMBus(1)

        def __del__(self):
            super().__del__()

        def __task(self):
            ret_temp = self.measure_temp()

            self.func(ret_temp, *self.args)
            time.sleep(self.delay)

        def start(self, func, *args, delay = 220 * MS):
            self.func = func
            self.args = args
            self.delay = delay - 200 * MS

            self.temp_humi.write_byte(self.addr, self.cmd_r)

            if self.task == None:
                self.task = MultiTask(self.__task, oneshort=False)
                self.task.start()

        def stop(self):
            if self.task != None:
                self.task.terminate()
                self.task = None

        def measure_temp(self):
            self.temp_humi.write_byte(self.addr, self.cmd_t)
            time.sleep(100 * MS)    #Internal minimization

            data = []
            tmp = self.temp_humi.read_byte(self.addr)
            data.append(tmp)
            tmp = self.temp_humi.read_byte(self.addr)
            data.append(tmp)

            return (-46.85 + TempHumi.CAL) + 175.72 / 65536 * (data[1] | data[0] << 8)


        def measure_temp_average(self, count=5, delay = 220 * MS):
            delay = delay - 200 * MS
            sum_temp = 0

            for i in range(count):
                sum_temp += self.measure_temp()
                time.sleep(delay)

            return sum_temp / count
