#!/usr/bin/python
from os import listdir
from os.path import isfile, isdir, join
import re
import numpy as np

#read all directories
mypath="."
onlydirs = [f for f in listdir(mypath) if isdir(join(mypath, f))]

x=[]
y=[]
en=[]
xy=[]
#en=0.0
for d in onlydirs:
	for line in open(d+"/out", 'r'):
		if "  multipole" in line:
			xy = line.split()[1:3]
		if "| Total energy of the DFT" in line:
			en.append(float(line.split()[11]))
#	xy = d.split("_")
	x.append(float(xy[0]))
	y.append(float(xy[1]))
#	append([x,y,z])

enmin=np.array(en).min()
#print enmin
for i in range(len(en)):
	print '{:14.8f} {:14.8f} {:20.8f}'.format( x[i], y[i], en[i]-enmin)
#	
