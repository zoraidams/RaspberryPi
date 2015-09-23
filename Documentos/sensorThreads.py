#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import threading as th

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_TRIGGER = 27
GPIO_ECHO = 17
GPIO_LED = 21

class sensor(th.Thread):
  def __init__(self):
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT) #Trigger
    GPIO.setup(GPIO_ECHO, GPIO.IN) #Echo
    th.Thread.__init__(self)
  
  def run(self):
    tl = led()
    tl.start()
    
    while True:
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
      dist = elapsed * 34000
      lock.acquire()
      try:
        distance = dist / 2
      finally:
        lock.release()
      
      print "Distance: %.1f"% distance

  def close(self):
    print ('Servicio del sensor finalizado')
    
class led(th.Thread):
  def __init__(self):
    GPIO.setup(GPIO_LED, GPIO.OUT) #Led
    th.Thread.__init__(self)
  
  def run(self):
    while True:
      GPIO.output(GPIO_LED, GPIO.HIGH)
      time.sleep(1)
      print distance
      if distance>10:
        GPIO.output(GPIO_LED, GPIO.LOW)
        time.sleep(1) 

  def close(self):
    self.led.close()

if __name__ == '__main__':
  try:
    distance = 5000
    lock = th.Lock()
    ts = sensor()
    ts.daemon = True
    ts.start()
    
    while True:
      time.sleep(100)
  except KeyboardInterrupt:
    GPIO.cleanup()
    ts.close()
