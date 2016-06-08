#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO_LED = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(GPIO_LED, GPIO.OUT)

try:
  while True:
    GPIO.output(GPIO_LED, GPIO.HIGH)
    time.sleep(1)
    
    GPIO.output(GPIO_LED, GPIO.LOW)
    time.sleep(1)

except KeyboardInterrupt:
  GPIO.cleanup()
