#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
    
# Pines del sensor
TRIGGER = 5
ECHO = 6

# Pines del motor derecho
ENA = 27
IN1 = 17
IN2 = 22
   
# Pines del motor izquierdo
ENB = 18
IN3 = 23
IN4 = 24

GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

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

def medir():
    distancia = 0.0
    GPIO.output(TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)
    start = time.time()
    while GPIO.input(ECHO)==0:
        start = time.time()

    while GPIO.input(ECHO)==1:
        stop = time.time()

        elapsed = stop - start
        distance = elapsed * 34000
        distance = distance / 2
    
    return distance

def adelante():
    pA.ChangeDutyCycle(50)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pB.ChangeDutyCycle(50)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def atras():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

    pA.ChangeDutyCycle(25)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

def finalizar():
    GPIO.cleanup()

if __name__=="__main__":
    for i in range(400):
        dist = medir()
        #print(dist)
        if dist<20:
            atras()
        else:
            adelante()
    finalizar()
