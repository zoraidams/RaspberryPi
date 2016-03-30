#!/usr/bin/env python
import webiopi
import time
import cv2
import numpy
import threading

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
# Variables que controlan el movimiento
motor_izquierdo = False # Motor izquierdo activado
motor_derecho = False # Motor derecho activado
movimiento = 0 # 0 hacia delante, 1 marcha atras
parado = 1 # Si esta a 1 esta parado


# -------------------------------------------------- #
# Funciones motores                                  #
# -------------------------------------------------- #

def forward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    motor_izquierdo = True
    motor_derecho = True
    movimiento = 0
    parado = 0

def backward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    motor_izquierdo = True
    motor_derecho = True
    moviemiento = 1
    parado = 0

def left():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    motor_derecho = True
    parado = 0

def right():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)
    motor_izquierdo = True
    parado = 0

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    motor_izquierdo = False
    motor_derecho = False
    parado = 1


# -------------------------------------------------- #
# Daemon que guarda los datos                        #
# -------------------------------------------------- #

def daemon():
    # Abrimos fichero para incluir los datos al final
    fil = open('/var/www/webiopi/data.txt', 'a')
    # Capturamos imagen
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite('/var/www/webiopi/pic.jpg', gray)

    numpy.set_printoptions(threshold='nan')

    # Comprobamos la distancia
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
    print('Comienza la escritura de datos')
    # Escribimos los datos en el fichero
    fil.write('{'+str(img)+', '+str(distance)+', '+str(motor_izquierdo)+', '+str(motor_derecho)+str(movimiento)+str(parado)+'}')
    print('Acaba la escritura de datos')
    # Cerramos el fichero
    fil.close()


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
    # Motor derecho
    GPIO.setFunction(ENA, GPIO.PWM)
    GPIO.setFunction(IN1, GPIO.OUT)
    GPIO.setFunction(IN2, GPIO.OUT)
    # Motor izquierdo
    GPIO.setFunction(ENB, GPIO.PWM)
    GPIO.setFunction(IN3, GPIO.OUT)
    GPIO.setFunction(IN4, GPIO.OUT)
    # Sensor distancia
    GPIO.setFunction(TRIGGER, GPIO.OUT)
    GPIO.setFunction(ECHO, GPIO.IN)
    
    GPIO.pulseRatio(ENA, 0.5)
    GPIO.pulseRatio(ENB, 0.5)
    
    stop()
    # Thread daemon que guarda los datos
    d = threading.Thread(target=daemon, name='Daemon')
    d.setDaemon(True)
    d.start()


def destroy():
    # Resetea las funciones GPIO
    # Motor derecho
    GPIO.setFunction(ENA, GPIO.IN)
    GPIO.setFunction(IN1, GPIO.IN)
    GPIO.setFunction(IN2, GPIO.IN)
    # Motor izquierdo
    GPIO.setFunction(ENB, GPIO.IN)
    GPIO.setFunction(IN3, GPIO.IN)
    GPIO.setFunction(IN4, GPIO.IN)
    # Sensor distancia
    GPIO.setFunction(TRIGGER, GPIO.IN)
    GPIO.setFunction(ECHO, GPIO.OUT)
