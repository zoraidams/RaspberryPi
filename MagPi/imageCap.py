#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  imageCap.py
#  
#  Copyright 2014  <guzunty@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 
import cv2

cap = cv2.VideoCapture(-1)

if (not cap.isOpened()):
  print("Cannot open camera")
else:
  cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
  cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
  while True:
    success, frame = cap.read()
    cv2.imshow("Captured:", frame)
    if (cv2.waitKey(1) == 27):
      break
  cap.release
  cv2.destroyAllWindows()
