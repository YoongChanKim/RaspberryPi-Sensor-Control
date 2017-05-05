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

class CharLcd():
    CMD_MODE = LOW
    CHR_MODE = HIGH

    def __init__(self, data_line = 4):
        self.rs = 23
        self.en = 26
        self.data = [17, 18, 27, 22]
        self.data_line = data_line

        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.en, GPIO.OUT)
        for pin in self.data:
            GPIO.setup(pin, GPIO.OUT)

        GPIO.output(self.rs, LOW)
        GPIO.output(self.en, LOW)

        self._write(0x33)
        self._write(0x32)

    def __write(self, bits, mode):
        for i in range(self.data_line):
            GPIO.output(self.data[i], (bits & (0x01 << i)) != 0)

        GPIO.output(self.en, LOW)
        time.sleep(1 * US)              #Min 230ns
        GPIO.output(self.en, HIGH)
        time.sleep(1 * US)              #Min 230ns (E cycle Wdith Min 500ns))
        GPIO.output(self.en, LOW)
        if mode == CharLcd.CMD_MODE:
            time.sleep(100 * US)        #commnads need > 37us to settle

    def _write(self, bits, mode=CMD_MODE):
        GPIO.output(self.rs, mode)

        if self.data_line == 4:
            self.__write((bits >> 4) & 0x0F, mode)  #High bits
            self.__write(bits & 0x0F, mode)         #Low bits
        else:
            self.__write(bits, mode)

    def __set_function(self, line2, dot10):
        """
        001<DL> <N><F>**
        DL(Data Line) : 0(4bit), 1(8bit)
        N(Line Number) : 0(1line), 1(2line)
        F(Font Size) : 0(5x7dot), 1(5x10dot)
        """

        cmd = 0x20  #0010 0000

        cmd = (cmd | 0x10) if self.data_line == 8 else cmd
        cmd = (cmd | 0x08) if line2 else cmd
        cmd = (cmd | 0x04) if dot10 else cmd

        self._write(cmd)

    def __set_entry_mode(self, increment, accompanies_shift):
        """
        0000 01<I/D><S>
        I/D(Decrement/Increment) : 0(decrement), 1(increment)
        S(Display Shift) : 0(off), 1(on)
        """

        cmd = 0x04

        cmd = (cmd | 0x02) if increment else cmd
        cmd = (cmd | 0x01) if accompanies_shift else cmd

        self._write(cmd)

    def clear(self, line=None):
        """
        line = 0(only Line0 clear), 1(only Line2 clear), None(all cleanr)
        """

        cmd = 0x01              #Clear Screen

        if line == None:
            self._write(cmd)
            time.sleep(2 * MS)  #Max 1.53ms
        else:
            space = " " * 40    #Max Width 40 char
            self.puts_p(space, line)

    def home(self):
        self._write(0x02)
        time.sleep(2 * MS)  #Max 1.53ms

    def set_pos(self, row, column):
        """
        row : 0 ~ 1
            Line0 row addr offset : 0x00
            Line1 row addr offset : 0x40
        column : 0 ~ 39 (max 40byte, visible 16byte)
        """

        cmd = 0x80; #set DDRAM addr
        row_offset = [0x00, 0x40]

        cmd = cmd | (row_offset[row] + column)

        #cmd = (cmd | column) if (row == 0) else (cmd | 0x40 | column)

        self._write(cmd)


    def set_display(self, cursor=False, blink=False, display=True):
        """
        0000 1<D><C><B>
        D(Display) : 0(off), 1(on)
        C(Cursor) : 0(off), 1(on)
        B(Blink) : 0(off), 1(on)
        """

        cmd = 0x08  #0000 1000

        cmd = (cmd | 0x04) if display else cmd
        cmd = (cmd | 0x02) if cursor else cmd
        cmd = (cmd | 0x01) if blink else cmd

        self._write(cmd)

    def shift_display(self, right=True):
        """
        0001 <M><L|R>00
        M(Move) : 0(Cursor), 1(Display)
        L|R(Left | Right) : 0(left), 1(right)
        """

        cmd = 0x10

        cmd = (cmd | 0x08) #Display Move
        cmd = (cmd | 0x04) if right else cmd

        self._write(cmd);

    def puts(self, text):
        for ch in text:
            self._write(ord(ch), CharLcd.CHR_MODE)
            #time.sleep(50 * US)  #Max 43us

    def puts_p(self, text, row, column=0):
        self.set_pos(row, column)
        self.puts(text)

    def enroll(self, code, data):
        code &= 0x7 #0 ~ 7(have 8 locations)

        cmd = 0x40 | code << 3
        self._write(cmd)

        for i in range(8):
            self._write(data[i], CharLcd.CHR_MODE)

    def write(self, code):
        self._write(code, CharLcd.CHR_MODE)

    def write_p(self, code, row, column=0):
        self.set_pos(row, column)
        self._write(code, CharLcd.CHR_MODE)

def charlcd_unit_test():
    clcd = CharLcd()

    clcd.puts("Enroll Testing.")
    for i in range(3, -1, -1):
        clcd.puts_p("Wait %dsec"%i, 1)
        time.sleep(1)

    clcd.clear()

    font = [
        [
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01110
        ],
        [
        0b11111,
        0b00001,
        0b00001,
        0b00001,
        0b01111,
        0b00001,
        0b00001,
        0b00001
        ],
        [
        0b01000,
        0b01000,
        0b01000,
        0b01111,
        0b01000,
        0b01000,
        0b01000,
        0b01000
        ],
        [
        0b00010,
        0b00010,
        0b00010,
        0b11110,
        0b00010,
        0b00010,
        0b00010,
        0b00010
        ],
        [
        0b00100,
        0b00100,
        0b11111,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000
        ],
        [
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100
        ]
    ]

    clcd.enroll(0x0, font[0])
    clcd.enroll(0x1, font[1])
    clcd.enroll(0x2, font[2])
    clcd.enroll(0x3, font[3])
    clcd.enroll(0x4, font[4])
    clcd.enroll(0x5, font[5])

    try:
        clcd.set_display(False, False)
        clcd.set_pos(0, 0)
        clcd.puts(">>>")
        clcd.write(0x0)
        clcd.write(0x2)
        clcd.write(0x0)
        clcd.write(0x5)
        clcd.write(0x1)
        clcd.write_p(0x4, 1, 7)
        clcd.write_p(0x0, 0, 8)
        clcd.write(0x3)

        clcd.set_pos(0, 11)
        clcd.puts("E&C")
        time.sleep(2)

        for i in range(16):
            clcd.shift_display(False)
            time.sleep(0.2)
        time.sleep(0.5)

        clcd.home()
        clcd.puts_p("Peri0", 1)
        time.sleep(2)

        for i in range(16):
            clcd.shift_display()
            time.sleep(0.2)
        time.sleep(0.5)

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':
    charlcd_unit_test()
