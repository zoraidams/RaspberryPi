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

# Modo test #
test = 1 # 0 si el modo test esta desactivado, 1 si esta activado

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
# Inicializamos las variables globales a los dos threads
motor_izquierdo = False # Motor izquierdo activado
motor_derecho = False # Motor derecho activado
movimiento = 0 # 0 hacia delante, 1 marcha atras
parado = 1 # 1 si esta parado, en caso contrario en movimiento
escribiendo = 0 # 0 si no esta escribiendo, 1 en caso contrario


# -------------------------------------------------- #
# Funciones motores                                  #
# -------------------------------------------------- #

def forward():
    # Definicion de variables globales que controlan el movimiento
    global motor_izquierdo
    global motor_derecho
    global movimiento
    global parado
    
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    if escribiendo==0:
        if test==1:
           print('--------------------------------------')
           print('Modificando datos en forward')
           print('--------------------------------------')
        motor_izquierdo = True
        print('----------', motor_izquierdo, '-----------')
        motor_derecho = True
        movimiento = 0
        parado = 0

def backward():
    # Definicion de variables globales que controlan el movimiento
    global motor_izquierdo
    global motor_derecho
    global movimiento
    global parado

    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    if escribiendo==0:
        if test==1:
            print('--------------------------------------')
            print('Modificando datos en backward')
            print('--------------------------------------')
        motor_izquierdo = True
        motor_derecho = True
        movimiento = 1
        parado = 0

def left():
    # Definicion de variables globales que controlan el movimiento
    global motor_izquierdo
    global motor_derecho
    global movimiento
    global parado

    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)
    if escribiendo==0:
        if test==1:
            print('--------------------------------------')
            print('Modificando datos en left')
            print('--------------------------------------')
        motor_derecho = True
        parado = 0

def right():
    # Definicion de variables globales que controlan el movimiento
    global motor_izquierdo
    global motor_derecho
    global movimiento
    global parado

    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    if escribiendo==0:
        if test==1:
            print('--------------------------------------')
            print('Modificando datos en right')
            print('--------------------------------------')
        motor_izquierdo = True
        parado = 0

def stop():
    # Definicion de variables globales que controlan el movimiento
    global motor_izquierdo
    global motor_derecho
    global movimiento
    global parado

    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    if escribiendo==0:
        if test==1:
            print('--------------------------------------')
            print('Modificando datos en stop')
            print('--------------------------------------')
        motor_izquierdo = False
        motor_derecho = False
        parado = 1


# -------------------------------------------------- #
# Daemon que guarda los datos                        #
# -------------------------------------------------- #

def daemon():
    # Definicion de variable global para controlar la escritura de datos
    global escribiendo
    while True:
        # Abrimos fichero para incluir los datos al final
        fil = open('/var/www/webiopi/data.txt', 'w')
        # Bloqueamos las variables de movimiento para que sean consistentes
        escribiendo = 1
        print('--------- motor izquierdo en daemon: ', motor_izquierdo, '----')
        # Capturamos imagen
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()

        # Comprobamos la distancia
        GPIO.output(TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(TRIGGER, False)
        while GPIO.input(ECHO)==0:
            start = time.time()
    
        while GPIO.input(ECHO)==1:
            stop = time.time()
     
            elapsed = stop - start
            distance = elapsed * 34000
            distance = distance / 2

        if test==1:
            print('--------------------------------------')
            print('Comienza la escritura de datos')
            print('--------------------------------------')

        st = time.time()
        # Escribimos los datos en el fichero
        fil.write('{'+str(img.tolist())+', '+str(distance)+', '+str(motor_izquierdo)+', '+str(motor_derecho)+', '+str(movimiento)+', '+str(parado)+'}')
        fil.write(img)
        sp = time.time()
        el = sp - st
        print(el)

        if test==1:
            print('--------------------------------------')
            print('Acaba la escritura de datos')
            print('--------------------------------------')
        # Cerramos el fichero
        fil.close()
        # Liberamos la captura
        cap.release()
        escribiendo = 0
        # Esperamos un tiempo para poder captar datos otra vez
        time.sleep(10)    


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
