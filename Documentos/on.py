#!/usr/bin/python
import RPi.GPIO as GPIO

GPIO_LED = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setup(GPIO_LED, GPIO.OUT)

GPIO.output(GPIO_LED, GPIO.HIGH)
