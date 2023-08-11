#!/usr/bin/env python3

import re, os, time
from smbus import SMBus

adc_address1 = 0x68

adcreading = bytearray()
adcreading.append(0x00)
adcreading.append(0x00)
adcreading.append(0x00)
adcreading.append(0x00)

varDivisior = 64  # from pdf sheet on adc addresses and config

for line in open('/proc/cpuinfo').readlines():
    m = re.match('(.*?)\s*:\s*(.*)', line)
    if m:
        (name, value) = (m.group(1), m.group(2))
        if name == "Revision":
            if value[-4:] in ('0002', '0003'):
                i2c_bus = 0
            else:
                i2c_bus = 1
            break

bus = SMBus(i2c_bus)


def changechannel(address, adcConfig):
    tmp = bus.write_byte(address, adcConfig)


def getadcreading(address, adcConfig):
    adcreading = bus.read_i2c_block_data(address, adcConfig)
    h = adcreading[0]
    m = adcreading[1]
    l = adcreading[2]
    s = adcreading[3]
    # wait for new data
    while (s & 128):
        adcreading = bus.read_i2c_block_data(address, adcConfig)
        h = adcreading[0]
        m = adcreading[1]
        l = adcreading[2]
        s = adcreading[3]

    # shift bits to product result
    t = ((h & 0b00000001) << 16) | (m << 8) | l
    # check if positive or negative number and invert if needed
    if (h > 128):
        t = ~(0x020000 - t)
    return (5.5865 * 2.048 * float(t / varDivisior)) / 2048


while True:
    Adc = []
    changechannel(adc_address1, 0x9C)
    Adc.append(getadcreading(adc_address1, 0x9C))
    changechannel(adc_address1, 0xBC)
    Adc.append(getadcreading(adc_address1, 0xBC))
    # changechannel(adc_address1, 0xDC)
    # Adc.append("Channel 3  :" + str(getadcreading(adc_address1, 0xDC)))
    # changechannel(adc_address1, 0xFC)
    # Adc.append("Channel 4  :" + str(getadcreading(adc_address1, 0xFC)))
    # os.system("clear")
    for A in Adc:
        print A
    time.sleep(1)