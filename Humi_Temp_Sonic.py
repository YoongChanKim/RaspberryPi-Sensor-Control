try:
    import time
    import smbus
    import RPi.GPIO as GPIO

except RuntimeError:
    print("Error. his is probably because you need sureruser privlegas")

trig = 0
echo = 1

addr = 0x40
temperature = 0xf3
humidity = 0xf5
reset = 0xfe

Humi = 0
C_Temp = 0
F_Temp = 0
test_t = 0
test_h = 0

dataA = 0
dataB = 0
dataC = 0
dataD = 0


def sonic():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    GPIO.add_event_detect(echo, GPIO.RISING, callback=prints)

def sonic_output():
    GPIO.output(trig, False)
    time.sleep(0.5)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

def prints(gpio):
    stop = time.time()

    dist = stop-start
    dist = dist * 17150 - 2.7
    dist = round(dist, 2)

    print "    dist :  %3.2f cm" %dist
    print "    Humi : %.2f %%    " %Humi
    print "   Temp(C) : %.2f C  " %C_Temp
    print "   Temp(F) : %.2f F  " %F_Temp
    print "------------------------"

sonic()
bus = smbus.SMBus(1)

while 1:
    bus.write_byte(addr, reset)
    time.sleep(0.08)

    bus.write_byte(addr, temperature)
    time.sleep(0.08)

    dataA = bus.read_byte(addr)
    dataB = bus.read_byte(addr)

    test_t = dataA * 256 + dataB
    C_Temp = -46.85 + ((test_t * 175.72) / 65536.0)  #Celcius
    F_Temp = C_Temp * 1.8 + 32                      #Fahrenheit / Celcius X 1.8 + 32

    bus.write_byte(addr, reset)
    time.sleep(0.08)

    bus.write_byte(addr, humidity)
    time.sleep(0.08)

    dataC = bus.read_byte(addr)
    dataD = bus.read_byte(addr)

    test_h = dataC * 256 + dataD
    Humi = -6.0 + ((test_h * 125.0) / 65536.0)

    sonic_output()

    while GPIO.input(echo) == 0 :
        start = time.time()

    while GPIO.input(echo) == 1 :
        a = 10*10


GPIO.cleanup()
