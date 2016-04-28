#!/usr/bin/python

read = open("/var/www/webiopi/data.txt", "r")

counter = 0

for line in read:
    lines = line.split('\t')
    if '0' not in lines[-1]:
        counter += 1

read.close()

print("There are "+str(counter)+" correct values")
print("You need "+str(1000-counter)+" more")
