#!/usr/bin/python
file_read = open("../data_final_full.txt", "r")
file_write = open("../data_final_full_.txt", "w")

for line in file_read:
    elements = line.split('\t')

    if len(elements) == 4:
        if elements[-1].replace('\n', '')=='0' and elements[-2]=='00':
            file_write.write(elements[0]+'\t'+elements[1]+'\t'+elements[2]+'\t'+elements[3])
        elif elements[-1].replace('\n', '')=='1' and elements[-2]=='11':
            file_write.write(elements[0]+'\t'+elements[1]+'\t'+elements[2]+'\t'+elements[3])
        elif elements[-1].replace('\n', '')=='2' and elements[-2]=='11':
            file_write.write(elements[0]+'\t'+elements[1]+'\t'+elements[2]+'\t'+elements[3])
        elif elements[-2]=='01' and elements[-1].replace('\n', '')=='1':
            file_write.write(elements[0]+'\t'+elements[1]+'\t'+elements[2]+'\t'+elements[3])
        elif elements[-2]=='10' and elements[-1].replace('\n', '')=='1':
            file_write.write(elements[0]+'\t'+elements[1]+'\t'+elements[2]+'\t'+elements[3])

file_write.close()
file_read.close()
