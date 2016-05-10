#!/usr/bin/env python
import webiopi
import time
import cv2
import numpy

# GPIO in webiopi library
GPIO = webiopi.GPIO

# -------------------------------------------------- #
# Statement of variables                             #
# -------------------------------------------------- #

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

# -------------------------------------------------- #
# Motor functions                                    #
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
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)

def right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)


def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


# -------------------------------------------------- #
# Macros definitions                                 #
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
# Initialization                                  #
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
    GPIO.pulseRatio(ENB, 0.6)
    
    stop()

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
