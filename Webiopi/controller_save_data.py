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
debug = 1 # 0 disable, 1 enable
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
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    if writing:
        motors = '11'
        movement = 1

def backward():
    # Global variables
    global motors
    global movement

    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
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
    global left_motor
    global right_motor
    global movement

    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
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
    while True:
        # Open the file to include data at the end
        file = open('/var/www/webiopi/data.txt', 'a')
        # Lock the variables to make the data consistent
        writing = True
        # Take a picture
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()

        # Check the distance with the objects in front of it
        GPIO.output(TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(TRIGGER, False)
        start = time.time()
        while GPIO.input(ECHO)==0:
            start = time.time()
        distance = -1
        while GPIO.input(ECHO)==1:
            stop = time.time()

            elapsed = stop - start
            distance = elapsed * 34000
            distance = distance / 2

        st = time.time()
        # Write the data in the file
        file.write(base64.b64encode(img)+'\t'+str(distance)+'\t'+str(motors)+'\t'+str(movement)+'\n')
        sp = time.time()
        el = sp - st
        if debug==1:
            print("It needed "+str(el)+" seconds to save the data")

        # Close the file
        file.close()
        # Release the camera
        cap.release()
        writing = False
        # Wait to the next capture of data
        time.sleep(1)
        if debug==1:
            print("----------------- END -----------------")
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
    
    GPIO.pulseRatio(ENA, 0.5)
    GPIO.pulseRatio(ENB, 0.5)
    
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
