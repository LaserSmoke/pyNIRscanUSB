#Read Interpreted data from NIRScan Nano
#1. Currently NNO_InterpretScan 0x02 0x39 does not seem to work
#1a so instate just trying to grab byte array from NNO_PerformScan
#2. NN0_GetFileSizetoRead(NN0_FILE_INTERPRET_DATA) )0x00 0x2D
#2a Getting the file size of ScanData works, but dont seem to be able to get the file size of InterpretScanData
#    NNO_FILE_INTERPRET_DATA is an enum 8
#3. NNO_GetFile uses NNO_GetFileData which reads in a packet at a time. Appears nine packets (512bytes?) sent
#  for each GetFileData Command. Must sen this command several times


import hid
import time
import struct
import math

NNO_FILE_INTERPRET_DATA=8
NNO_FILE_SCAN_DATA=0

class NNO_ScanInterpret:
    def __init__(self):
        ReportIDByte = int(0x00)
        WriteFlagByte = int(0x40)
        SeqByte = int(0x00)
        LengthByteLSB = int(0x02)
        LengthByteMSB = int(0x00)
        CmdByte1 = int(0x39)
        CmdByte2 = int(0x02)
        self.cmd = [ReportIDByte, WriteFlagByte, SeqByte, LengthByteLSB, LengthByteMSB, CmdByte1, CmdByte2]

class NNO_PerformScan:
    def __init__(self):
        ReportIDByte = int(0x00)
        WriteFlagByte = int(0x40)
        SeqByte = int(0x00)
        LengthByteLSB = int(0x03)
        LengthByteMSB = int(0x00)
        CmdByte1 = int(0x18)
        CmdByte2 = int(0x02)
        DataByte0=int(0x00)
        self.cmd = [ReportIDByte, WriteFlagByte, SeqByte, LengthByteLSB, LengthByteMSB, CmdByte1, CmdByte2,DataByte0]

class NNO_GetFileSize:
    def __init__(self):
        ReportIDByte = int(0x00)
        WriteFlagByte = int(0xC0)
        SeqByte = int(0x00)
        LengthByteLSB = int(0x03)
        LengthByteMSB = int(0x00)
        CmdByte1 = int(0x2D)
        CmdByte2 = int(0x00)
        DataByte0 = int(0x00)
        self.cmd = [ReportIDByte, WriteFlagByte, SeqByte, LengthByteLSB, LengthByteMSB, CmdByte1, CmdByte2, DataByte0]

class NNO_GetFileData:
    def __init__(self):
        ReportIDByte = int(0x00)
        WriteFlagByte = int(0xC0)
        SeqByte = int(0x00)
        LengthByteLSB = int(0x02)
        LengthByteMSB = int(0x00)
        CmdByte1 = int(0x2E)
        CmdByte2 = int(0x00)
        self.cmd = [ReportIDByte, WriteFlagByte, SeqByte, LengthByteLSB, LengthByteMSB, CmdByte1, CmdByte2]

vendor_id=0x0451
product_id=0x4200

hex_string=""

scanInterpret=NNO_ScanInterpret()
performScan=NNO_PerformScan()
getfilesize=NNO_GetFileSize()
getfiledata=NNO_GetFileData()

device_list=hid.enumerate(vendor_id,product_id)
scanner=hid.device(vendor_id,product_id)
scanner.open(vendor_id,product_id)
scanner.set_nonblocking(0)

#Perform scan 0x02 0x18
ack=scanner.write(performScan.cmd)
scanner.read(65)
time.sleep(6)

#ack=scanner.write(scanInterpret.cmd)
#time.sleep(5)

#get file size of Scan Data
ack=scanner.write(getfilesize.cmd)
res=scanner.read(8)
file_size=int(struct.unpack('<h',struct.pack('B'*2,res[4],res[5]))[0])
print "filesize= {} bytes".format(file_size)
time.sleep(5)

#get scan data file is 3822 , which is 7 512byte files + a 238 bute file
#Reading the file requires nine USB packets (64 bytes) because there is a 6 byte header

resp_pkt = []
#calculate the number of 512 byte NIRfiles (which ends up being 518 bytes because of header
# can only read data in 64 byte chuncks, need to get rid of padding in the nineth packet

num_NIRpkts=int(math.ceil(file_size/512))
num_HEADbytes=6

#Read in Scan Data File from USB HID packets
for data_packet in range(0,7):
    ack=scanner.write(getfiledata.cmd)
    #number of 64 byte USB packets
    num_USBpkts =9
    for usb_packet in range(0,num_USBpkts-1):
            resp_pkt+=(scanner.read(64))
    #read last packet (partial) 6 bytes pushed over from Header & strip padding)
    partial = scanner.read(64)
    for data_byte in  range(0,8):
        resp_pkt.append(partial[data_byte])

#If there are still bytes left, get remaining NIRpkt
if 1==1:
    ack=scanner.write(getfiledata.cmd)
    # calculate remaining USB_pkts from remaining NIRfile bytes
    num_USBpkts=math.ceil(((file_size-(num_USBpkts-1)*512+num_HEADbytes)/64)+1)
    for data_packet in range (0,4):
        resp_pkt+=(scanner.read(64))


bvariable=bytearray()
for i in resp_pkt:
    bvariable+=struct.pack('<B',i)
    hex_string+=''.join([hex(i),','])

with open('response.txt','wb') as data_file:
    data_file.write(bvariable)

with open('hex_response.txt','w') as hex_file:
    hex_file.write(hex_string)

print("length of file={:d}".format(len(resp_pkt)))
scanner.close()