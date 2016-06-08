#!/usr/bin/python
import cv2
import time
import numpy

# Open the file
file = open("captura.txt", "w")

# Take a picture
cap = cv2.VideoCapture(0)
ret, img = cap.read()

# Write the data in  file
file.write(str(img.tolist()))

# Close the file
file.close()

# Release the camera
cap.release()
