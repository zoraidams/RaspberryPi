#!/usr/bin/python
import cv2

cap = cv2.VideoCapture(0)

ret, img = cap.read()

cv2.imwrite('pic.jpg', img)
