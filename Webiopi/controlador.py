#!/usr/bin/env python
import webiopi
import time
import cv2

# Libreria GPIO
GPIO = webiopi.GPIO

# -------------------------------------------------- #
# Definicion constantes                              #
# -------------------------------------------------- #

# Pines motor derecho
ENA = 27
IN1 = 17
IN2 = 22
# Pines motor izquierdo
ENB = 18
IN3 = 23
IN4 = 24
# Pines sensor distancia
TRIGGER = 5
ECHO = 6

# -------------------------------------------------- #
# Funciones motores                                  #
# -------------------------------------------------- #

def forward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def backward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def left():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def right():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def distance():
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

def picture():
    pass
   # cap = cv2.VideoCapture(0)
   # ret, img = cap.read()
   # cv2.imwrite('pic.jpg', img)

# -------------------------------------------------- #
# Definicion macros                                  #
# -------------------------------------------------- #

@webiopi.macro
def go_forward():
    forward()
    distance()
    picture()

@webiopi.macro
def go_backward():
    backward()
    distance()
#    picture()

@webiopi.macro
def turn_left():
    left()
    distance()
#    picture()

@webiopi.macro
def turn_right():
    right()
    distance()
#    picture()

@webiopi.macro
def stop_motors():
    stop()
    distance()
#    picture()
    
# -------------------------------------------------- #
# Iniciacializacion                                  #
# -------------------------------------------------- #

def setup():
    # Instalacion GPIOs
    # Motor derecho
    #GPIO.setFunction(ENA, GPIO.OUT)
    GPIO.setFunction(IN1, GPIO.OUT)
    GPIO.setFunction(IN2, GPIO.OUT)
    # Motor izquierdo
    #GPIO.setFunction(ENB, GPIO.OUT)
    GPIO.setFunction(IN3, GPIO.OUT)
    GPIO.setFunction(IN4, GPIO.OUT)
    # Sensor distancia
    GPIO.setFunction(TRIGGER, GPIO.OUT)
    GPIO.setFunction(ECHO, GPIO.IN)

def destroy():
    # Resetea las funciones GPIO
    # Motor derecho
    #GPIO.setFunction(ENA, GPIO.IN)
    GPIO.setFunction(IN1, GPIO.IN)
    GPIO.setFunction(IN2, GPIO.IN)
    # Motor izquierdo
    #GPIO.setFunction(ENB, GPIO.IN)
    GPIO.setFunction(IN3, GPIO.IN)
    GPIO.setFunction(IN4, GPIO.IN)
    # Sensor distancia
    GPIO.setFunction(TRIGGER, GPIO.IN)
    GPIO.setFunction(ECHO, GPIO.OUT)
