
import serial
import time

arduino = serial.Serial("COM5", 9600)

time.sleep(2)

arduino.write(b"1")
time.sleep(2)

arduino.write(b"0")
time.sleep(2)

arduino.close()