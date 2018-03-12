# -*- coding: utf-8 -*-
"""
Created on Wed May  3 09:25:32 2017

@author: jstafford
"""

import hid
import time


class Battery:
    def __init__(self):
        ReportIDByte = int(0x00)
        WriteFlagByte = int(0xC0)
        SeqByte = int(0x00)
        LengthByteLSB = int(0x02)  # this is defined as short in code so not sure of byte order
        LengthByteMSB = int(0x00)
        CmdByte1 = int(0x0A)
        CmdByte2 = int(0x03)
        DataByte0 = int(0x01)
        self.msg = [ReportIDByte, WriteFlagByte, SeqByte, LengthByteLSB, LengthByteMSB, CmdByte1, CmdByte2]


class LED:
    def __init__(self):
        ReportIDByte = int(0x00)
        WriteFlagByte = int(0x40)
        SeqByte = int(0x00)
        LengthByteLSB = int(0x03)  # this is defined as short in API c struct nnoMessageStruct
        LengthByteMSB = int(0x00)
        CmdByte1 = int(0x0B)
        CmdByte2 = int(0x01)
        DataByte0 = int(0x00)
        self.msg = [ReportIDByte, WriteFlagByte, SeqByte, LengthByteLSB, LengthByteMSB, CmdByte1, CmdByte2,0]

        # pad to 65bytes , one record id byte, 64 record bytes
        # for i in range(len(self.msg),65):
        # self.msg.append(int(0x00))

    def on(self):
        self.msg[7] = int(0x01)

    def off(self):
        self.msg[7] = int(0x00)


# Vendor ID and Product ID for TI NIRscan Nano
vendor_id = 0x0451
product_id = 0x4200

# HID set up
device_list = hid.enumerate(vendor_id, product_id)
scanner = hid.device(vendor_id, product_id)
scanner.open(vendor_id, product_id)
scanner.set_nonblocking(1)

# check if I am actually connected device
serial_number = scanner.get_serial_number_string()

# Perform LED Test
nir_led = LED()
nir_bat_voltage = Battery()
nir_led.on()
msg = nir_led.msg
hid_buff = ''.join(map(chr, msg))
test_buff = bytes(msg)

# hid.write accepts a list of integers and sends them to the device
# converted to bytes in the method


# ack is the number of bytes written
ack = scanner.write(nir_led.msg)
print('number of bytes written {:d}'.format(ack))
time.sleep(5)
nir_led.off()
ack=scanner.write(nir_led.msg)
scanner.close()
