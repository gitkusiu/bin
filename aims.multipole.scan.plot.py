#!/usr/bin/python
import sys
from numpy.random import uniform, seed
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np

from ase.io.aims import read_aims



# make up data.
#npts = int(raw_input('enter # of random points to plot:'))
seed(0)
npts = 200
#x = uniform(-2, 2, npts)
#y = uniform(-2, 2, npts)
#z = x*np.exp(-x**2 - y**2)

num = len(sys.argv)
ifile = sys.argv[num-1]

xx =  []
yy =  []
zz =  []
f = open(ifile, 'r')
for i in f:
    r=i.split()
#    print r
#    rd = [r[0], r[1], r[2]]
    xx.append(float(r[0])) 
    yy.append(float(r[1])) 
    zz.append(float(r[2])) 

x = np.array(xx)
y = np.array(yy)
z = np.array(zz)


print len(x)
#print x

print len(y)
#print y

print len(z)
#print z



# define grid.
#xi = np.linspace(0.0, 30.0, 100)
#yi = np.linspace(0.0, 12.0, 200)
xmin = x.min()
xmax = x.max()

ymin = y.min()
ymax = y.max()

zmin = z.min()
zmax = z.max()

xi = np.linspace(xmin, xmax , len(x))
yi = np.linspace(ymin, ymax , len(y))
#print x
#print yi.shape

zi = griddata(x, y, z, xi, yi, interp='nn')

# contour the gridded data, plotting dots at the nonuniform data points.
print len(xi)
#print xi

print len(yi)
#print yi


print zmin, zmax
zi = np.clip(zi, 0.05, 0.27)

#CS = plt.contour(xi, yi, zi)
CS = plt.contour(xi, yi, zi, 50, linewidths=0.5, colors='k',  vmin=0.05, vmax=0.27)

#CS = plt.contourf(xi, yi, zi, 10, cmap=plt.cm.rainbow,
#                  vmax=abs(zi).max(), vmin=-abs(zi).max())

#CS = plt.contourf(xi, yi, zi, 200, cmap=plt.cm.bone,
#                  vmax=abs(zi).max(), vmin=-abs(zi).max())
#CS = plt.contourf(xi, yi, zi, 100, cmap=plt.cm.bone, vmax=0.9, )
CS = plt.contourf(xi, yi, zi, 200, cmap="PuRd", vmin=0.05, vmax=0.27)
#CS = plt.contourf(xi, yi, zi, 400, cmap="PuRd")
#CS = plt.contourf(xi, yi, zi, 400, cmap="PuRd", vmin=-1.2, vmax=3.28)
#CS = plt.contourf(xi, yi, zi, 200, cmap=plt.cm.rainbow)

plt.colorbar()  # draw colorbar
# plot data points.
#plt.scatter(x, y, marker='o', c='b', s=5, zorder=10)
#plt.xlim(-2, 2)
#plt.ylim(-2, 2)
plt.title('griddata test (%d points)' % npts)




atoms = read_aims("molecule.in")
positions = atoms.arrays['positions']

xxx=[]
yyy=[]
print len(positions)
for a in positions:
	xxx.append(a[0])
	yyy.append(a[1])


plt.plot(xxx, yyy, 'ko')

plt.savefig("en.ps")
plt.show()
