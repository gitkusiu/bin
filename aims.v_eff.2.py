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


points_tmp = []
values_tmp = []
for l in lines:
    r = l.split()
    row = [float(r[0]), float(r[1]), float(r[2]),  float(r[3])]
    points_tmp.append(row[0:3])
    values_tmp.append(row[3])

points3D = np.array(points_tmp)
values3D = np.array(values_tmp)



max_x = max(points3D[:,0])
max_y = max(points3D[:,1])
max_z = max(points3D[:,2])
min_x = min(points3D[:,0])
min_y = min(points3D[:,1])
min_z = min(points3D[:,2])

dd=int(sys.argv[num-2])
density=complex(0.0,dd)
npoints = density.imag


z0  = min_z + (max_z-min_z)*0.48 
dz  = ((max_z-min_z)/npoints)

grid_x, grid_y = np.mgrid[min_x:max_x:2*density, min_y:max_y:density]

interpolation = np.empty([npoints*2,npoints])
#print "len(interpolation)", len(interpolation)
#print interpolation
#for z0 in np.arange(min_z,max_z,dz):
for z0 in np.arange(z0-10*dz,z0+10*dz,dz):
#    print z0
    condition = (points3D[:,2] > z0-dz) & (points3D[:,2] < z0+dz)
    p2D = points3D[condition]
    points2D = p2D[:,0:2]
    values2D = values3D[condition]
#    print "p" ,len(points2D), points2D
#    print "v" ,len(values2D), values2D
#grid_x, grid_y , grid_z = np.mgrid[min_x:max_x:2*density, min_y:max_y:density, min_z:max_z:density]
#interpolation = griddata(points3D, values3D, (grid_x, grid_y , grid_z), method='nearest')
#interpolation = interpolation[:,:,npoints*0.47]
    tmp = griddata(points2D, values2D, (grid_x, grid_y), method='linear')

    plt.imshow(tmp, interpolation='nearest')
    plt.grid()
    plt.axis([0.4*npoints,0.6*npoints,0.5*npoints,npoints])
    plt.savefig('v_eff_'+str((z0-min_z)/dz)+'j.png')
#    plt.show()
#    print tmp

#    np.append(interpolation, tmp)
#print interpolation
#print len(interpolation)


#plt.imshow(interpolation, interpolation='nearest')
#plt.grid()
#plt.axis([0.4*npoints,0.6*npoints,0.5*npoints,npoints])
##plt.savefig('v_eff_'+str(npoints)+'j.png')
#plt.show()




#atoms = read_aims("geometry.in")
#cell = np.array(    [[max_x-min_x, 0.         ,0.         ],\
#                     [0.0        , max_y-min_y,0.         ],\
#                     [0.         , 0.         ,max_z-min_z]]    )
#print cell

#atoms.set_cell(cell*0.5)
#shift = np.array([min_x,min_y,min_z])
#atoms.translate(-0.5*shift)
#write_cube("v_eff.cube",atoms,interpolation)




