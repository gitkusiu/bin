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

from ase.io.cube import write_cube
from ase.io.aims import read_aims

from scipy.interpolate import griddata  
import matplotlib.pyplot as plt

num = len(sys.argv)
f  = open(sys.argv[num-1], "r")
lines = f.read().splitlines()

# read grid
grid = []
points_x = []
points_y = []
points_z = []
values = []

points_tmp = []
values_tmp = []
for l in lines:
    r = l.split()
    row = [float(r[0]), float(r[1]), float(r[2]),  float(r[3])]
    points_tmp.append(row[0:3])
    values_tmp.append(row[3])

points = np.array(points_tmp)
values = np.array(values_tmp)

#print points
#print values

max_x = max(points[:,0])
max_y = max(points[:,1])
max_z = max(points[:,2])
min_x = min(points[:,0])
min_y = min(points[:,1])
min_z = min(points[:,2])

density=100j
grid_x, grid_y , grid_z = np.mgrid[min_x:max_x:2*density, min_y:max_y:density, min_z:max_z:density]
grid_z2 = griddata(points, values, (grid_x, grid_y , grid_z), method='nearest')

#plt.subplot(221)
#plt.imshow(grid_z2[0,:,:])
#plt.gcf().set_size_inches(10, 10)
#plt.show()



atoms = read_aims("geometry.in")
cell = np.array(    [[max_x-min_x, 0.         ,0.         ],\
                     [0.0        , max_y-min_y,0.         ],\
                     [0.         , 0.         ,max_z-min_z]]    )
atoms.set_cell(cell*0.5)
shift = np.array([min_x,min_y,min_z])
atoms.translate(-0.5*shift)

write_cube("tmp.cube",atoms,grid_z2)





##print values
##print poi
## sort grid
##grid_sorted=sorted(grid, key=lambda x: x[2])


### calculate an average along z axis
##z = grid_sorted[0][2]
##s = 0.0               # summ for average calculations
##n = 0                 # number of poiunts taken for average
##for i in grid_sorted:
##    if(i[2] == z): # still at the same height - continue summing
##        s += i[3]
##        n += 1
##    else:             # new height 
##        print z, s/n, n  # print avearage from previous height
##        z = i[2]      # begin new summing
##        s = i[3]
##        n = 1
