#!/usr/bin/env python
import Adafruit_GPIO.MCP230xx as MCP230XX
import RPi.GPIO as GPIO
from MCP342x import MCP342x
import glob
import smbus

class Home(object):
    def __init__(self, input, output, relays, port, io, pwm):
        self.input = input
        self.output = output
        self.port = port
        self.relays = relays
        self.initializegpio()
        self.io = self.initializerelays(relays)
        self.pwm = GPIO.PWM(output[0], 400)
        self.pwm.start(0)

    @staticmethod
    def readvo():
        f = open('status.txt', 'rb')
        st = str(f.readline())
        f.close()
        return st

    # @staticmethod
    # def readtxtdin():
    #     dinlist = []
    #     f = open('statusdin.txt', 'rb')
    #     stlist = str(f.readline()).split(',')
    #     for word in stlist:
    #         dinlist.append(int(word))
    #     f.close()
    #     return dinlist
    #
    # @staticmethod
    # def writetxtdin(din):
    #     f = open('statusdin.txt', 'wb')
    #     f.write(str(din).replace("[","").replace("]",""))
    #     f.close()

    @staticmethod
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

    def initializegpio(self):
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        for i in self.input:
            GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for i in self.output:
            GPIO.setup(i, GPIO.OUT)
        return

    def readdigitalinput(self):
        inputlistgpio = []
        for i in self.input:
            inputlistgpio.append(GPIO.input(i))
        return inputlistgpio

    def readanaloginput(self, ch):
        bus = self.get_smbus()
        addr68 = MCP342x(bus, 0x68, channel=ch, resolution=12)
        return "{0:.1f}".format(round(addr68.convert_and_read() * 5.5865, 2))

    def initializerelays(self,relaylist):
        io = MCP230XX.MCP23008(busnum=1, address=0x20)
        for r in relaylist:
            self.turnrelayoff(io, r)
        return io

    @staticmethod
    def readrelay(io, relay):
        return io.input(relay)

    @staticmethod
    def turnrelayon(io, relay):
        io.output(relay, 1)
        return

    @staticmethod
    def turnrelayoff(io, relay):
        io.output(relay, 0)
        return

    @staticmethod
    def changepwm(volt, pwm):
        dutycycle = int(volt)*10
        f = open('status.txt', 'wb')
        f.write(str(volt))
        f.close()
        print "Change Duty Cycle to: "+str(dutycycle)
        pwm.ChangeDutyCycle(dutycycle)
