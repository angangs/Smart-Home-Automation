#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from homeoperations import Home

def main():
    port = 8080
    relay1 = 7
    relay2 = 6
    relay3 = 5
    relay4 = 4
    relay5 = 3
    relay6 = 2
    relay7 = 1
    relay8 = 0
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
    inputlist = [in1, in2, in3, in4, in5, in6, in7, in8, in9, in10, in11, in12]
    outputlist = [out1]
    relaylist = [relay1, relay2, relay3, relay4, relay5, relay6, relay7, relay8]

    sitakis = Home(inputlist, outputlist, relaylist, port, None, None)
    sitakis.turnrelayon(sitakis.io, relay3)

    time.sleep(0.2)
    print "Relay 3 is on: " + str(sitakis.readrelay(sitakis.io, relay3))
    print "Relay 4 is on: " + str(sitakis.readrelay(sitakis.io, relay4))
    print "Digital input: "+str(sitakis.readdigitalinput())
    time.sleep(1)
    sitakis.turnrelayoff(sitakis.io, relay3)
    print "Relay 3 is on: " + str(sitakis.readrelay(sitakis.io, relay3))

    try:
        while True:
            voltage = input('Enter voltage 0-10 : ')
            sitakis.changepwm(voltage, sitakis.pwm)
            time.sleep(1)
            print "GPIO analog 2: " + str(GPIO.input(out1))
            print "Analog input 1: " + str(sitakis.readanaloginput(int(0)))
            print "Analog input 2: " + str(sitakis.readanaloginput(int(1)))
    except (KeyboardInterrupt, ValueError, Exception) as e:
        print(e)
        sitakis.pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()