#!/usr/bin/python

import os
import sys
#import re
import numpy as np 
import subprocess

def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True



arg2 = sys.argv[2]


######## get all directory with number names
list=os.listdir("./")
d = []
dirs= []
for i in range(len(list)):
    tmp = list[i]
    if(isfloat(tmp) == True):
        d.append(float(tmp))
        dirs.append(tmp)
d.sort()
dirs.sort()
print d
print dirs

######## read TOTENs from corresponding OUTCARS
toten = []
f = []
for i in range(len(d)):

    outcar=dirs[i]+"/OUTCAR"
    cmd = "vasp.OUTCAR.py --get energy "+outcar
    fin, fout = os.popen4(cmd)
    toten.append(float(fout.read()) )

    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    cmd = "vasp.OUTCAR.py --get force --atoms " + arg1 + " " + arg2 + " --steps -1 1 " + outcar
    fin, fout = os.popen4(cmd)
    ff = fout.read().split()
    f.append( [float(ff[0]), float(ff[1]),float(ff[2])]   )


f_diff = np.zeros(len(d))
for i in range(1,len(d)-1):
    f_diff[i] = (toten[i+1]-toten[i-1])/(d[i+1]-d[i-1])


for i in range(1,len(d)-1):
    print d[i], f[i][0], f[i][1], f[i][2], f_diff[i]

