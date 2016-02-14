import webiopi
import time

# Libreria GPIO
GPIO = webiopi.GPIO

# -------------------------------------------------- #
# Definicion constantes                              #
# -------------------------------------------------- #

ENA = 27
IN1 = 17
IN2 = 22
ENB = 18
IN3 = 23
IN4 = 24

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

# -------------------------------------------------- #
# Definicion macros                                  #
# -------------------------------------------------- #

@webiopi.macro
def go_forward():
    forward()

@webiopi.macro
def go_backward():
    backward()

@webiopi.macro
def turn_left():
    left()

@webiopi.macro
def turn_right():
    right()

@webiopi.macro
def stop_motors():
    stop()
    
# -------------------------------------------------- #
# Iniciacializacion                                  #
# -------------------------------------------------- #

def setup():
    # Instalacion GPIOs
    #GPIO.setFunction(ENA, GPIO.OUT)
    GPIO.setFunction(IN1, GPIO.OUT)
    GPIO.setFunction(IN2, GPIO.OUT)
    #GPIO.setFunction(ENB, GPIO.OUT)
    GPIO.setFunction(IN3, GPIO.OUT)
    GPIO.setFunction(IN4, GPIO.OUT)


def destroy():
    # Resetea las funciones GPIO
    #GPIO.setFunction(ENA, GPIO.IN)
    GPIO.setFunction(IN1, GPIO.IN)
    GPIO.setFunction(IN2, GPIO.IN)
    #GPIO.setFunction(ENB, GPIO.IN)
    GPIO.setFunction(IN3, GPIO.IN)
    GPIO.setFunction(IN4, GPIO.IN)
