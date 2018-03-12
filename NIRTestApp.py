import hid
import struct
import sys
import time

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore


import NIRtestGui


class NIRTestApp(QtGui.QMainWindow,NIRtestGui.Ui_MainWindow):
    def __init__(self,parent=None):
            super(NIRTestApp,self).__init__(parent)
            self.setupUi(self)

            self.btnLEDtest.clicked.connect(self.LEDtest)
            self.btnReadBatVoltage.clicked.connect(self.readbatteryvoltage)

    def LEDtest(self):
        # Vendor ID and Product ID for TI NIRscan Nano
        vendor_id = 0x0451
        product_id = 0x4200

        # HID set up
        device_list = hid.enumerate(vendor_id, product_id)
        scanner = hid.device(vendor_id, product_id)
        scanner.open(vendor_id, product_id)
        scanner.set_nonblocking(1)

        msg=[int(0x00),int(0x40),int(0x00),int(0x03),int(0x00),int(0x0B),int(0x01),1]
        ack = scanner.write(msg)
        time.sleep(5)
        msg = [int(0x00), int(0x40), int(0x00), int(0x03), int(0x00), int(0x0B), int(0x01),0]
        ack = scanner.write(msg)
        scanner.close()

    def readbatteryvoltage(self):
        # Vendor ID and Product ID for TI NIRscan Nano
        vendor_id = 0x0451
        product_id = 0x4200

        # HID set up
        device_list = hid.enumerate(vendor_id, product_id)
        scanner = hid.device(vendor_id, product_id)
        scanner.open(vendor_id, product_id)
        scanner.set_nonblocking(1)

        msg = [int(0x00), int(0xC0), int(0x00), int(0x02), int(0x00), int(0x0A), int(0x03)]
        ack = scanner.write(msg)
        time.sleep(1)
        res = scanner.read(8)
        voltage = float(struct.unpack('<h', struct.pack('B' * 2, res[4], res[5]))[0]) / 100
        self.lnBatteryVoltage.setText(''.join([str(voltage),' V']))

def main():
    app=QtGui.QApplication(sys.argv)
    form=NIRTestApp()
    form.show()
    app.exec_()

if __name__=='__main__':
    main()