import webiopi
import time
from cv2.cv import *
##import cv2

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
    # Initialize the camera
    capture = CaptureFromCAM(0)  # 0 -> index of camera
    if capture:     # Camera initialized without any errors
       f = QueryFrame(capture)     # capture the frame
       if f:
           ShowImage("cam-test",f)

##    # Camera 0 is the integrated web cam on my netbook
##    camera_port = 0
##    
##    #Number of frames to throw away while the camera adjusts to light levels
##    ramp_frames = 30
## 
##    # Now we can initialize the camera capture object with the cv2.VideoCapture class.
##    # All it needs is the index to a camera port.
##    camera = cv2.VideoCapture(camera_port)
##    
##    # Captures a single image from the camera and returns it in PIL format
##    def get_image():
##        # read is the easiest way to get a full image out of a VideoCapture object.
##        retval, im = camera.read()
##        return im
##
##    # Ramp the camera - these frames will be discarded and are only used to allow v4l2
##    # to adjust light levels, if necessary
##    for i in xrange(ramp_frames):
##        temp = get_image()
##    print("Taking image...")
##    # Take the actual image we want to keep
##    camera_capture = get_image()
##    file = "/home/codeplasma/test_image.png"
##    # A nice feature of the imwrite method is that it will automatically choose the
##    # correct format based on the file extension you provide. Convenient!
##    cv2.imwrite(file, camera_capture)
##
##    # You'll want to release the camera, otherwise you won't be able to create a new
##    # capture object until your script exits
##    del(camera)

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
    picture()

@webiopi.macro
def turn_left():
    left()
    distance()
    picture()

@webiopi.macro
def turn_right():
    right()
    distance()
    picture()

@webiopi.macro
def stop_motors():
    stop()
    distance()
    picture()
    
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
    GPIO.setFunction(TRIGGER, GPIO.OUT)
    GPIO.setFunction(ECHO, GPIO.IN)

def destroy():
    # Resetea las funciones GPIO
    #GPIO.setFunction(ENA, GPIO.IN)
    GPIO.setFunction(IN1, GPIO.IN)
    GPIO.setFunction(IN2, GPIO.IN)
    #GPIO.setFunction(ENB, GPIO.IN)
    GPIO.setFunction(IN3, GPIO.IN)
    GPIO.setFunction(IN4, GPIO.IN)
    GPIO.setFunction(TRIGGER, GPIO.IN)
    GPIO.setFunction(ECHO, GPIO.OUT)
