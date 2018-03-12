import struct
import binascii
import matplotlib.pyplot as plt
import numpy as np
import csv

serial_data=bytearray()
num_pts=300
adc_values=[]
bkgnd=[]

#adc values that are not part of spectrum
bad_ints=[]
#exclude baseline readings
bkgnd_reading=[24,51,76,101,126,151,178,203,228]
bkgnd_values=[]
#exclude header bytes
bad_ints.extend([46,47,176,177])
#exclude adc values above the number of scan data points which is 228
bad_ints.extend(range(241,num_pts))
#there appears to be an issue with the last integer value of the 512 byte file.
#the last two bytes are getting dropped (two MSBs of the last digit) int 45 and 175



ar_reference=np.genfromtxt('reference.csv',delimiter=',')
ar_wavelength=np.genfromtxt('wavelengths.csv',delimiter=',')

with open('response.txt','rb') as data_file:
    serial_data=data_file.read(3822)

adc_offset=serial_data.find("i#")+7

print('adc offset in file= {}'.format(adc_offset))

serial_adc=serial_data[adc_offset:]
binary_array=bytearray(serial_adc)


cnt = 0
for i in range(0,num_pts):
    if i==45 or i==175:
        value=struct.unpack('I',struct.pack('B'*4,binary_array[cnt],binary_array[cnt+1],binary_array[cnt-2],binary_array[cnt-1]))[0]
    else:
        value = struct.unpack('I', struct.pack('B' * 4, binary_array[cnt], binary_array[cnt + 1], binary_array[cnt + 2],binary_array[cnt + 3]))[0]

    print(hex(binary_array[cnt]),hex(binary_array[cnt+1]),hex(binary_array[cnt+2]),hex(binary_array[cnt+3]))
    print (i, cnt, value)
    if i in bkgnd_reading:
        bkgnd_values.append(value)
    elif i not in bad_ints:
        adc_values.append(value)
    cnt=cnt+4

print('length of adc values= {}'.format(len(adc_values)))
bkgnd_array=np.array(bkgnd_values)
mean_offset=np.mean(bkgnd_array)

with open('hex_file.txt','w') as hex_data_file:
    hex_data_file.write(binascii.hexlify(serial_adc))

ar_adc_values=np.array(adc_values)
ar_adc_values_corrected=ar_adc_values-mean_offset
ar_absorbance=-np.log(ar_adc_values_corrected/ar_reference)

plt.subplot(2,1,1)
plt.plot(ar_wavelength,ar_adc_values)
plt.plot(ar_wavelength,ar_adc_values_corrected)
plt.title('Intensity')
plt.xlabel('wavelength (nm)')
plt.ylabel('Intensity')


plt.subplot(2,1,2)
plt.plot(ar_wavelength,ar_absorbance)
plt.title('Absorbance')
plt.xlabel('wavelength (nm)')
plt.ylabel("Absorbance")

plt.tight_layout()

plt.show()