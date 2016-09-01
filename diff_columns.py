#!/usr/bin/python


#TODO this is supposed to be a quite large converter scirpt 
# ase.convert.py -i inport_format -o output_format
import sys
import os.path
import numpy as np
import math


from optparse import OptionParser

import asekk

num = len(sys.argv)
file1 = sys.argv[num-2]
file2 = sys.argv[num-1]

#parser = OptionParser()
#parser.add_option("-i", "--input",            action="store",       type="string", help="input file format")
#parser.add_option("-o", "--output",           action="store",       type="string", help="output file format")

#(options, args) = parser.parse_args()


f1 = open(file1, 'r')
f2 = open(file1, 'r')

data1 = []
data2 = []
#outcar_lines = outcar.readlines()
for line in f1:
    print line.split()
    x = float(line.split()[0])
    y = float(line.split()[1])
    z = float(line.split()[2])
    data1.append([x,y,z])
    
    
for line in f2:
    print line.split()
    x = float(line.split()[0])
    y = float(line.split()[1])
    z = float(line.split()[2])
    data2.append([x,y,z])
    
print data1
print data2

for i, x in enumerate(data1):
#    print x[0], data2[i][1] - x[1], data2[i][2] - x[2]
    print '{:34.24f} {:34.24f} {:34.24f}'.format( x[0], data2[i][1] - x[1], data2[i][2] - x[2])
#    print x[0], data2[i][1] - x[1], data2[i][2] - x[2]

#     if(len(l) == 6 and str(l[4]) == "lattice" and str(l[5]) == "vectors"):
#         break

