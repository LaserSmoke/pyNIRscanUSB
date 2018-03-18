# pyNIRscanUSB
This is a group of python scripts that query the TI NIRScan Nano using the USB HID interface

Communication is based on the Cython wrapper of the HID library ...put link here.. 
   I had to include  libusb-1.0.dll into the project root because the python extension could not find it in Win32 (was added to PATH)
The commands used are built based upon on TI documentation  for USB in literature  DLPU030G.
 There are a couple different scripts
 -HID_LEDtest.py will turnon all the LEDs for 5 seconds. Good for checking communications
 -HID_BatVoltage.py reads the Battery Voltage
 -GUItest provides a simple GUI to perfor the two previous functions. The GUI is based upon pyQT4

The point of this exercise was to read a spectrum from the NIRScan Nano.
In order to do this it was necessary to read the entire ScanData packet and then find the ADC values based upon the tpl serialization
formatting. Basically the interger array for the ADC values is always 864 integer values not matter the length of the spectrum. 
The ADC values are 4 byte ints (carefully of the endian).

NIR_ReadSpectrum.py  reads in the entire ScanData file and strips out the 0 padding at the end of the 512 byte NIR packets. 
The seririalized data requires multiple reads in order to consume the entiner ScanData file. The maximum data load of a HID packet
64 bytes, so it takes 9 USB packets to load in one NIR packet of 512 bytess(because of header, cant get it all into 8 packets) 
I have calcualted how many file reads are necessary for the scan data packet a always read this amount instead of basing this on FILESIZE,
although thate would be a good TODO. NIR_ReadSpectrum then saves the data from the UDB packets into **response.txt**

NIR getADCvalues.py reads response.txt and slices the data based upon the tpl formatting for an integer array *#i* .TODO add to the slicer the length of the array which is always 864 (in case an array is add somewhere down the line?. Atfer slicing the **response,.txt.=** to get the integer array, is sequentially reads in 4 bytes at a time to grab integers. However, there are two issues
  - There is abackscatter reading taken every 25th reading. These are filter out into a different list to calculate an offset correction
  -There is a problem with the last integer of the 512 byte NIR file packet, two most significant bytes are missing. 
    -The value before this integer and after the integer are averaged and used for this value. Since we have only 228 values, I only do         this at values 45 and 175. 
    
 NIR_getADCvalues uses two other files that are also located in project root.
 1. wavelengths.csv which contains the wavelengths of the device which is fix based upon the devices configuration. 
 2. reference.csv which contains the reference values from the device which is also fixed during usage. 
 
 However, these files are unique to a specific device and therefore, there would be a requirement when using this script with multiple devices to have wavelength and reference files for each device. and one would have to read the device serial number from ScanData in order to pick correct files. this is currently not included , but serial number could be grabbed from the ScanData file by appropriate slice,
