#!/usr/bin/python
import RPi.GPIO as GPIO

GPIO_LED = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(GPIO_LED, GPIO.OUT)

while 1:
  print '''Menu:
  1. On
  2. Off
  0. Exit\n'''

  opt =  int(raw_input('Choose an option: '))

  if opt == 1:
    GPIO.output(GPIO_LED, GPIO.HIGH)
  elif opt == 2:
    GPIO.output(GPIO_LED, GPIO.LOW)
  elif opt == 0:
    break

GPIO.cleanup()