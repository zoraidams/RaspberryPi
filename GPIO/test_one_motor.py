#!/usr/bin/python
import RPi.GPIO as GPIO
import time

IN1 = 17
IN2 = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

print("Forwards")
GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)
time.sleep(3)

print("Backwards")
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.HIGH)
time.sleep(3)

GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)

GPIO.cleanup()

