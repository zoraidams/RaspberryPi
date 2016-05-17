import base64
import numpy

file_read = open("data_final_v1.txt", "r")

stop = 0
left = 0
right = 0
forwards = 0
backwards = 0

for line in file_read:
    elementos = line.split('\t')

    if elementos[-1].replace('\n', '')=='0':
        stop += 1
    if elementos[-1].replace('\n', '')=='1':
        forwards += 1
    if elementos[-1].replace('\n', '')=='2':
        backwards += 1
    if elementos[-2]=='01':
        left += 1
    if elementos[-2]=='10':
        right += 1

print "Stop: ", stop
print "Forwards: ", forwards
print "Backwards: ", backwards
print "Left: ", left
print "Right: ", right

file_read.close()
