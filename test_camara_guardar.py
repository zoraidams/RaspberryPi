import cv2
import time
import numpy

# Abrimos fichero para guardar la captura
fichero = open("captura.txt", "w")

# Realizamos la captura
cap = cv2.VideoCapture(0)
ret, img = cap.read()

# Escribimos la captura en el fichero
fichero.write(str(img.tolist()))

# Cerramos el fichero
fichero.close()

# Liberamos la camara
cap.release()
