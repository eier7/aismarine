#!/usr/bin/python
import serial
import socket
from time import sleep
import re

UDP_IP   = '5.9.207.224' 
UDP_PORT = 7607
port = '/dev/ttyUSB0'
ser = serial.Serial(port, 38400)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    try:
        data = ser.readline()
        if(re.match("^\!AIVD", data)):
            sock.sendto(data, (UDP_IP, UDP_PORT))
    except:
        sleep(.5)

ser.close()

