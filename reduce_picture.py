import base64
import numpy
import cv2

file_read = open("../data_final_full.txt", "r")
file_write = open("../datax4.txt", "w")

dim = 4

for line in file_read:
    elements = line.split('\t')
    
    numpy.set_printoptions(threshold='nan')
    # Decode base64
    img = numpy.frombuffer(base64.b64decode(elements[0]), dtype=numpy.uint8)
    img = img.reshape(232,320,3)
    # Change the picture to black and white
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    pic = []
    for x in range(0,gray.shape[0]-1, dim):
        for y in range(0, gray.shape[1]-1, dim):
            n = 0
            for dx in range(dim-1):
                for dy in range(dim-1):
                    n += gray[x+dx][y+dy]
            n = int(round(n/(dim*dim), 0))
            pic.append(n)
    file_write.write(', '.join(str(p) for p in pic)+', '+elements[1]+', '+elements[2]+', '+elements[3])

print ("END")

file_write.close()
file_read.close()
