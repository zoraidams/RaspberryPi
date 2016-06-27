#!/usr/bin/env python
import webiopi
import time
import cv2
import numpy
import threading
import base64

# GPIO in webiopi library
GPIO = webiopi.GPIO

# -------------------------------------------------- #
# Statement of variables                             #
# -------------------------------------------------- #

# Debug mode
debug = 0 # 0 disable, 1 enable
# Right motor pinout
ENA = 27
IN1 = 17
IN2 = 22
# Left motor pinout
ENB = 18
IN3 = 23
IN4 = 24
# Distance sensor pinout
TRIGGER = 5
ECHO = 6
# Led pinout
LED = 4
# Initializate the global variables to control the movement
motors = '00' # 00 both motors disable, 01 right motor enable, 10 left motor enable, 11 both motors enable 
movement = 0 # 0 stop, 1 forwards, 2 backwards
writing = False # writing disable


# -------------------------------------------------- #
# Motor functions                                    #
# -------------------------------------------------- #

def forward():
    # Global variables
    global motors
    global movement
    
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    if writing:
        motors = '11'
        movement = 1

def backward():
    # Global variables
    global motors
    global movement

    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    if writing:
        motors = '11'
        movement = 2

def left():
    # Global variables
    global motors
    global movement

    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)
    if writing:
        motors = '01'
        movement = 1

def right():
    # Global variables
    global motors
    global movement

    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    if writing:
        motors = '10'
        movement = 1

def stop():
    # Global variables
    global motors
    global movement

    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    if writing:
        motors = '00'
        movement = 0


# -------------------------------------------------- #
# Daemon that save all the data                      #
# -------------------------------------------------- #

def save_data_daemon():
    # Global variable to control the variables of the movement
    global writing
    # Logging package seems to 
    log = open('/usr/share/nginx/www/webiopi/log.txt', 'w')

    while True:
        log.write("INFO - Abro el fichero.\n")
        # Open the file to include data at the end
        file = open('/usr/share/nginx/www/webiopi/data.txt', 'a')
        log.write("INFO - Bloqueo el flag.\n")
        # Lock the variables to make the data consistent
        writing = True
        # Put the led on
        GPIO.output(LED, True)

        log.write("INFO - Capturo la imagen.\n")
        # Take a picture
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()

        log.write("INFO - Capturo la distancia.\n")
        # Check the distance with the objects in front of it
        GPIO.output(TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(TRIGGER, False)
        start = time.time()
        while GPIO.input(ECHO)==0:
            start = time.time()
        distance = -1
        log.write("INFO - Convierto la distancia.\n")
        while GPIO.input(ECHO)==1:
            stop = time.time()
            elapsed = stop - start
            distance = elapsed * 34000
            distance = distance / 2

        log.write("INFO - Escribo en el fichero.\n")
        # Write the data in the file
        file.write(base64.b64encode(img)+'\t'+str(distance)+'\t'+str(motors)+'\t'+str(movement)+'\n')

        log.write("INFO - Cierro el fichero.\n")
        # Close the file
        file.close()
        log.write("INFO - Libero la cam y el flag.\n")
        # Release the camera
        cap.release()
        # Put the led off
        GPIO.output(LED, False)
        # Unlock the variable to make the data consistent
        writing = False

        log.write("INFO - Sleep.\n")
        # Wait to the next capture of data
        if debug==1:
            print("----------------- END -----------------")
            print("You can stop the program right now")
            time.sleep(5)
            print("Ok! You shouldn't try to stop the program now")
        else:
            time.sleep(1)


# -------------------------------------------------- #
# Macros definition                                  #
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
    # GPIOs initialization
    # Right motor
    GPIO.setFunction(ENA, GPIO.PWM)
    GPIO.setFunction(IN1, GPIO.OUT)
    GPIO.setFunction(IN2, GPIO.OUT)
    # Left motor
    GPIO.setFunction(ENB, GPIO.PWM)
    GPIO.setFunction(IN3, GPIO.OUT)
    GPIO.setFunction(IN4, GPIO.OUT)
    # Distance sensor
    GPIO.setFunction(TRIGGER, GPIO.OUT)
    GPIO.setFunction(ECHO, GPIO.IN)
    # Led
    GPIO.setFunction(LED, GPIO.OUT)
    
    GPIO.pulseRatio(ENA, 0.5)
    GPIO.pulseRatio(ENB, 0.6)
    
    stop()
    
    # Thread daemon that save all the data
    d = threading.Thread(target=save_data_daemon, name='Daemon')
    d.setDaemon(True)
    d.start()
    

def destroy():
    # Reset the GPIO functions
    # Right motor
    GPIO.setFunction(ENA, GPIO.IN)
    GPIO.setFunction(IN1, GPIO.IN)
    GPIO.setFunction(IN2, GPIO.IN)
    # Left motor
    GPIO.setFunction(ENB, GPIO.IN)
    GPIO.setFunction(IN3, GPIO.IN)
    GPIO.setFunction(IN4, GPIO.IN)
    # Distance sensor
    GPIO.setFunction(TRIGGER, GPIO.IN)
    GPIO.setFunction(ECHO, GPIO.OUT)
    # Led
    GPIO.setFunction(LED, GPIO.IN)
