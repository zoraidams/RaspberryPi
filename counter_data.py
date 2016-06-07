#!/usr/bin/python
file_read = open("../data_final_full.txt", "r")

stop = 0
left = 0
right = 0
forwards = 0
backwards = 0
other = 0
counter = 0

for line in file_read:
    elements = line.split('\t')

    if elements[-1].replace('\n', '')=='0' and elements[-2]=='00':
        stop += 1
    elif elements[-1].replace('\n', '')=='1' and elements[-2]=='11':
        forwards += 1
    elif elements[-1].replace('\n', '')=='2' and elements[-2]=='11':
        backwards += 1
    elif elements[-2]=='01' and elements[-1].replace('\n', '')=='1':
        left += 1
    elif elements[-2]=='10' and elements[-1].replace('\n', '')=='1':
        right += 1

    counter += 1

print "Stop: ", stop
print "Forwards: ", forwards
print "Backwards: ", backwards
print "Left: ", left
print "Right: ", right
print "TOTAL: ", stop+left+right+forwards+backwards
print "Counter: ", counter
    
file_read.close()
