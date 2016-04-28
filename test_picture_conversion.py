#!/usr/bin/python
import cv2
import numpy
import base64

########################################################
## Encode the picture
########################################################
file = open("/var/www/webiopi/data.txt", "w")
cap = cv2.VideoCapture(0)
ret, img = cap.read()
cv2.imwrite("/var/www/pic.jpg", img)
file.write(base64.b64encode(img))
file.close()
cap.release()

########################################################
## Decode the picture
########################################################
file = open("/var/www/webiopi/data.txt", "r")
elements = file.read().split('|')
elements[0] = elements[0].replace('{', '').strip()
img = numpy.frombuffer(base64.b64decode(elements[0]), dtype=numpy.uint8)
img = img.reshape(232,320,3)
cv2.imwrite("/var/www/pic64.jpg", img)
file.close()
