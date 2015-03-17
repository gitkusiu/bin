#!/usr/bin/python

######################################
#
#   Script which calculate average
#   efective potential basing on the
#   v_eff.dat file 
#
######################################
import sys
import numpy as np 

num = len(sys.argv)
f  = open(sys.argv[num-1], "r")
lines = f.read().splitlines()

# read grid
grid = []
for l in lines:
    r = l.split()
    row = [float(r[0]), float(r[1]), float(r[2]),  float(r[3])]
    grid.append(row)

# sort grid
grid_sorted=sorted(grid, key=lambda x: x[2])


# calculate an average along z axis
z = grid_sorted[0][2]
s = 0.0               # summ for average calculations
n = 0                 # number of poiunts taken for average
for i in grid_sorted:
    if(i[2] == z): # still at the same height - continue summing
        s += i[3]
        n += 1
    else:             # new height 
        print z, s/n, n  # print avearage from previous height
        z = i[2]      # begin new summing
        s = i[3]
        n = 1
