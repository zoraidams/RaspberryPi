import base64
import numpy
import cv2

file_read = open("data.txt", "r")
file_write = open("data_conversion_v4.txt", "w")

for line in file_read:
    elements = line.split('\t')

    numpy.set_printoptions(threshold='nan')
    # Decode base64
    img = numpy.frombuffer(base64.b64decode(elements[0]), dtype=numpy.uint8)
    img = img.reshape(232,320,3)
    # Change the picture to black and white
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Delete the edges of the picture
    gray = numpy.delete(gray, 0, axis=0)
    gray = numpy.delete(gray, 230, axis=0)
    gray = numpy.delete(gray, 0, axis=1)
    gray = numpy.delete(gray, 318, axis=1)
    
    # Change the type to write in the txt file
    string_img = str(gray)
    string_img = string_img.replace('[', '')
    string_img = string_img.replace(']', '')
    string_img = string_img.split(' ')
    string_img = [i.strip() for i in string_img if i!='']
    string_img = ", ".join(string_img)
    file_write.write(string_img+', '+elements[1]+', '+elements[2]+', '+elements[3])
    
print("END")

file_read.close()
file_write.close()
