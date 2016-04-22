#!/usr/bin/python
import RPi.GPIO as GPIO
import time

ENA = 27
IN1 = 17
IN2 = 22
ENB = 18
IN3 = 23
IN4 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

pA = GPIO.PWM(ENA, 100)
pB = GPIO.PWM(ENB, 100)

pA.start(100)
pB.start(100)

# Ponemos la velocidad a la mitad
pA.ChangeDutyCycle(90)
GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)
# Ponemos la velocidad a la mitad
pB.ChangeDutyCycle(95)
GPIO.output(IN3, GPIO.HIGH)
GPIO.output(IN4, GPIO.LOW)

time.sleep(2)

pA.stop()
pB.stop()

GPIO.cleanup()
