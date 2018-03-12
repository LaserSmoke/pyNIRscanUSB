from usb import core
import usb.util
import usb.backend.libusb1

import os
import sys

core.find(find_all=True)


#setup backend
libusb_backend = usb.backend.libusb1.get_backend(find_library=lambda x: 'C:\Windows\System32\libusb-1.0.dll')


dev = usb.core.find(idVendor=0x0451, idProduct=0x4200)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

print'Length = {}'.format(dev.bLength)
print'Class= {}'.format(dev.bDeviceClass)
print 'Number configurations ={}'.format(dev.bNumConfigurations)
print'Descriptor Type= {}'.format(dev.bDescriptorType)
print 'Device Subclass = {}'.format(dev.bDeviceSubClass)
print 'Device Protocol = {}'.format(dev.bDeviceProtocol)

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

# write the data
ep.write('test')
