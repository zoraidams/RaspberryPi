#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_TRIGGER = 27
GPIO_ECHO = 17
GPIO_LED = 21

GPIO.setup(GPIO_TRIGGER, GPIO.OUT) #Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN) #Echo
GPIO.setup(GPIO_LED, GPIO.OUT) #Led

try:
  while True:
    GPIO.output(GPIO_LED, GPIO.HIGH)
    
    GPIO.output(GPIO_TRIGGER, False)
    
    time.sleep(0.5)
    
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    star = time.time()
    while GPIO.input(GPIO_ECHO)==0:
      start = time.time()
    
    while GPIO.input(GPIO_ECHO)==1:
      stop = time.time()
     
      elapsed = stop-start
      
      distance = elapsed * 34000
      
      distance = distance / 2
      
      if distance>10:
        GPIO.output(GPIO_LED, GPIO.LOW)
      
      print "Distance: %.1f"% distance
    
except KeyboardInterrupt:
  GPIO.cleanup()
