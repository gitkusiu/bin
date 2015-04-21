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

dd=int(sys.argv[num-2])

density=complex(0.0,dd)
grid_x, grid_y , grid_z = np.mgrid[min_x:max_x:2*density, min_y:max_y:density, min_z:max_z:density]
interpolation = griddata(points, values, (grid_x, grid_y , grid_z), method='nearest')
print interpolation.shape

#plt.subplot(221)

#plt.gcf().set_size_inches(10, 10)
npoints = density.imag
print 
plt.imshow(interpolation[:,:,npoints*0.47], interpolation='nearest')
plt.grid()
plt.axis([0.4*npoints,0.6*npoints,0.5*npoints,npoints])

plt.savefig('v_eff_'+str(npoints)+'j.png')
#plt.show()

#s = len(interpolation[0,0,:])
#for i in range(s):
#    plt.imshow(interpolation[:,:,i])
#    plt.savefig('v_eff'+str(i)+'.png')



atoms = read_aims("geometry.in")
cell = np.array(    [[max_x-min_x, 0.         ,0.         ],\
                     [0.0        , max_y-min_y,0.         ],\
                     [0.         , 0.         ,max_z-min_z]]    )
print cell

#atoms.set_cell(cell*0.5)
#shift = np.array([min_x,min_y,min_z])
#atoms.translate(-0.5*shift)

#write_cube("v_eff.cube",atoms,interpolation)




