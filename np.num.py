#!/usr/bin/python

######################################
#
#   
#
######################################
import sys
import numpy as np


from optparse import OptionParser

parser = OptionParser()
parser.add_option("--get",           action="store", type="string", help="What to calculate"), 
parser.add_option("-x",           action="store", type="float", help="Rnge of x", nargs=2), 
(options, args) = parser.parse_args()

x_range=options.x
#print x_range
num = len(sys.argv)
f  = open(sys.argv[num-1], "r")


lines = f.read().splitlines()

x=np.empty(0, dtype=float)
y=np.empty(0, dtype=float)
for ll in lines:
    l = ll.split()[0:2]
    xxx = l[0]
    if xxx.replace(".", "").replace("-", "").isdigit():
        xx = float(xxx)
        if x_range == None or ( xx >= x_range[0] and  xx <= x_range[1]):
            x =  np.append(x, float(xxx))
            yyy = l[1]
            if yyy.replace(".", "").replace("-", "").replace("e", "").isdigit():
                y = np.append(y, float(yyy))



if(options.get == 'integral'):
#    print x
#    print y
    print np.trapz(y, x=x)
elif(options.get == 'diff'):
#    dx_p = np.diff(x)
#    dx_m = np.roll(dx_p,-1)
#    dx   = dx_p + dx_m
#    dy_p = np.diff(y)
#    dy_m = np.roll(dy_p,-1)
#    dy   = dy_p + dy_m
    dx=np.diff(x)
    dy=np.diff(y)
    dd=np.divide(dy,dx)
    for i, d in enumerate(dd):
        print x[i], d

