import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIGGER = 5
ECHO = 6

GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

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

GPIO.cleanup()
print distance
