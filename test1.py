#!/usr/bin/env python
import Adafruit_GPIO.MCP230xx as MCP230XX
import RPi.GPIO as GPIO
import time
from MCP342x import MCP342x
import glob
import smbus

in1 = 4
in2 = 17
in3 = 27
in4 = 23
in5 = 22
in6 = 24
in7 = 11
in8 = 7
in9 = 8
in10 = 9
in11 = 25
in12 = 10
out1 = 18
inputlist = [in1, in2, in3, in4, in5, in6, in7, in8, in9, in10,  in11, in12]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

def get_smbus():
    candidates = []
    prefix = '/dev/i2c-'
    for bus in glob.glob(prefix + '*'):
        try:
            n = int(bus.replace(prefix, ''))
            candidates.append(n)
        except:
            pass
        
    if len(candidates) == 1:
        return smbus.SMBus(candidates[0])
    elif len(candidates) == 0:
        raise Exception("Could not find an I2C bus")
    else:
        raise Exception("Multiple I2C busses found")



def initializeIO():
    for i in inputlist:
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(out1, GPIO.OUT)
    return

def take_measurements():
    try:
        initializeIO()
        print ("Inputs 1-12: ",
                GPIO.input(in1),GPIO.input(in2),GPIO.input(in3),
                GPIO.input(in4),GPIO.input(in5),GPIO.input(in6),
                GPIO.input(in7),GPIO.input(in8),GPIO.input(in9),
                GPIO.input(in10),GPIO.input(in11),GPIO.input(in12))
    except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
        GPIO.cleanup()  # resets all GPIO ports used by this program

def main():
    io = MCP230XX.MCP23008(busnum=1, address=0x20)
    io.output(0, 1)
    io.output(7, 1)
    time.sleep(0.2)
    take_measurements()
    time.sleep(0.2)
    io.output(0,0)
    io.output(7,0)

    pwm = GPIO.PWM(out1, 400)
    pwm.start(0)

    try:
        while True:
            dutycycle = input('Enter a duty cycle percentage from 0-100 : ')
            print("Duty Cycle is : {0}%".format(dutycycle))
            pwm.ChangeDutyCycle(dutycycle)
            time.sleep(2)
            bus = get_smbus()
            addr68ch0 = MCP342x(bus, 0x68, channel=0, resolution=16)
            print(addr68ch0.convert_and_read()*5.5865)

    except (KeyboardInterrupt, ValueError, Exception) as e:
        print(e)
        pwm.stop()  # stop the PWM output
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit

if __name__ == "__main__":
    main()
