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

class fnd():
    #FND Data Format (Active High)
    DATA = (0xFC,   #1111 1100 (0)
            0x60,   #0110 0000 (1)
            0xDA,   #1101 1010 (2)
            0xF2,   #1111 0010 (3)
            0x66,   #0110 0110 (4)
            0xB6,   #1011 0110 (5)
            0xBE,   #1011 1110 (6)
            0xE0,   #1110 0000 (7)
            0xFE,   #1111 1110 (8)
            0xF6)   #1111 0110 (9)

    #FND Select Format (Active Low)
    SELECT = (
            0xFB,   #1111 1011 (5) --> [Digit 0]
            0xF7,   #1111 0111 (4) --> [Digit 1]
            0xEF,   #1110 1111 (3) --> [Digit 2]
            0xDF,   #1101 1111 (2) --> [Digit 3]
            0xBF,   #1011 1111 (1) --> [Digit 4]
            0x7F,   #0111 1111 (0) --> [Digit 5]
            0xFF)   #1111 1111 (All Off)

    def __init__(self, delay = 2 * MS):
        super().__init__()

        self.delay = delay
        self.task = None
        self.digits =  Manager().list([0, 0, 0, 0, 0, 0])

        self.addr = 0x20
        self.con = 0x06
        self.out = 0x02

        self.fnd = smbus.SMBus(1)
        self.fnd.write_word_data(self.addr, self.con, 0x0000)

    def __del__(self):
        super().__del__()

    def __task(self, digits):
        for pos in range(6):
            if digits[pos] != 0:
                data = digits[pos] << 8 | Fnd.SELECT[pos]
                self.fnd.write_word_data(self.addr, self.out, data)
            time.sleep(self.delay)

    def __set_task(self):
        self.task = MultiTask(self.__task, self.digits, oneshort=False)
        self.task.start()

    def set_num(self, num):
        x = []
        for n in str(num)[-1::-1]:
            x.append(Fnd.DATA[int(n)])

        pos = 0
        for value in x:
            self.digits[pos] = value
            pos += 1

        for mod_pos in range(6 - len(x)):
            self.digits[pos + mod_pos] = 0


        if self.task == None:
            self.__set_task()

    def set_data(self, value, pos):
        self.digits[pos] = value

        if self.task == None:
            self.__set_task()

    def stop(self):
        if self.task != None:
            self.task.terminate()
            self.task = None

            for i in range(6):
                self.digits[i] = 0

            self.fnd.write_word_data(self.addr, self.out, 0x0)
