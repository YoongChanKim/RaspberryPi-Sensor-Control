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

class Piezo():
    NOTE = {"DO":0, "DO#":1, "RE":2, "RE#":3, "MI":4, "FA":5, "FA#":6, "SOL":7, "SOL#":8, "RA":9, "RA#":10, "SI":11}
    NOTE2STR = {0:"DO", 1:"DO#", 2:"RE", 3:"RE#", 4:"MI", 5:"FA", 6:"FA#", 7:"SOL", 8:"SOL#", 9:"RA", 10:"RA#", 11:"SI"}

    NOTE2 = {"C":0, "C#":1, "D":2, "D#":3, "E":4, "F":5, "F#":6, "G":7, "G#":8, "A":9, "A#":10, "B":11 }
    NOTE2STR2 = {0:"C", 1:"C#", 2:"D", 3:"D#", 4:"E", 5:"F", 6:"F#", 7:"G", 8:"G#", 9:"A", 10:"A#", 11:"B"}

    def __init__(self):
        self.piezo = 13
        self.tempo = 0
        self.note_type = 0

        GPIO.setup(self.piezo, GPIO.OUT)
        GPIO.output(self.piezo, LOW)

    def get_tempo(self):
        return self.__tempo

    def set_tempo(self, t = 100):
        self.__tempo = t

    def tone(self, octive, note, dulation):
        hz = [32.7032, 34.6478, 36.7081, 38.8909, 41.2034, 43.6545, 46.2493, 48.9994, 51.9130, 55.0000, 58.2705, 61.7354]

        sound = 1 / (hz[note] * (2 ** (octive - 1))) * 1000000

        loop = ((1000000 - sound) / sound) * (60.0 / self.__tempo) * (4 * dulation)
        delay = (sound/2)/1000000.0

        while loop >= 0:
            GPIO.output(self.piezo, True)
            time.sleep(delay)
            GPIO.output(self.piezo, False)
            time.sleep(delay)
            loop -= 1

        time.sleep(3/100.0)

    def rest(self, dulation):
        sound = 1 / (55.0000 * (2 ** (4 - 1))) * 1000000
        loop = ((1000000 - sound) / sound) * (60.0 / self.__tempo) * (4 * dulation)
        delay = sound/1000000.0

        while loop >= 0:
            time.sleep(delay)
            loop -= 1

    def play(self, sheet, note_type=1):
        for item in sheet:
            if note_type == 1:
                self.tone(item[0], Piezo.NOTE[item[1]], item[2])
            else:
                self.tone(item[0], Piezo.NOTE2[item[1]], item[2])

if __name__ == "__main__":
    piezo = Piezo()
    piezo.set_tempo(140)

    humoresque = (
    (4, "DO", 3/16),
    (4, "RE", 1/16),
    (4, "DO", 3/16),
    (4, "RE", 1/16),
    (4, "MI", 3/16),
    (4, "SOL", 1/16),
    (4, "RA", 3/16),
    (4, "SOL", 1/16),
    (5, "DO", 3/16),
    (4, "SI", 1/16),
    (5, "RE", 3/16),
    (5, "DO", 1/16),
    (4, "SI", 3/16),
    (5, "RE", 1/16),
    (5, "DO", 3/16),
    (4, "RA", 1/16),
    (4, "SOL", 3/16),
    (4, "SOL", 1/16),
    (4, "RA", 3/16),
    (4, "SOL", 1/16),
    (5, "DO", 3/16),
    (4, "RA", 1/16),
    (4, "SOL", 3/16),
    (4, "MI", 1/16),
    (4, "RE", 1/4),
    (3, "RA", 1/4),
    (3, "SOL", 1/4),
    (4, "FA", 1/4),
    (4, "DO", 3/16),
    (4, "RE", 1/16),
    (4, "DO", 3/16),
    (4, "RE", 1/16),
    (4, "MI", 3/16),
    (4, "SOL", 1/16),
    (4, "RA", 3/16),
    (4, "SOL", 1/16),
    (5, "DO", 3/16),
    (4, "SI", 1/16),
    (5, "RE", 3/16),
    (5, "DO", 1/16),
    (4, "SI", 3/16),
    (5, "RE", 1/16),
    (5, "DO", 3/16),
    (4, "RA", 1/16),
    (4, "SOL", 3/16),
    (4, "SOL", 1/16),
    (5, "DO", 3/16),
    (4, "DO", 1/16),
    (4, "RE", 1/4),
    (4, "SOL", 1/4),
    (4, "DO", 1))

    print("humoresque")
    piezo.play(humoresque, 1)
