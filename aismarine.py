#!/usr/bin/python
import serial
import socket
from time import sleep
import re
import sys
import RPi.GPIO as GPIO
from queue import Queue
from threading import Thread

led = 4 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT)

activityqueue = Queue(maxsize=0)
def mainthread():
    IP   = '5.9.207.224'#Marinetraffic 
    PORT = 7607
    port = '/dev/ttyUSB0'
    ser = serial.Serial(port, 38400)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        data = ser.readline().decode('iso-8859-1', errors="ignore")
        if(re.match("^\!AIVD", data)):
            sock.sendto(bytes(data, "iso-8859-1"), (IP, PORT))
            activityqueue.put(1)

    ser.close()

def ledthread():
    led = 4
    while(True):
        while not activityqueue.empty():
            activityqueue.get()
            GPIO.output(led, GPIO.HIGH)
            sleep(.1)
            GPIO.output(led, GPIO.LOW)
        sleep(.2)

main = Thread(target=mainthread)
led = Thread(target=ledthread)
main.start()
led.start()
