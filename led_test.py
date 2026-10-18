
import serial
import time

arduino = serial.Serial("COM7", 9600)
time.sleep(2)

patterns = [
    "10000",
    "01000",
    "00100",
    "00010",
    "00001",
    "11111",
    "00000"
]

for pattern in patterns:
    print("Sending:", pattern)
    arduino.write((pattern + "\n").encode())
    time.sleep(1)

arduino.close()