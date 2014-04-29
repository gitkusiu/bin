#! /usr/bin/env python

import sys
from math import sqrt
from math import pi


if(len(sys.argv) > 1):
    print float(sys.argv[1])
    shift=float(sys.argv[1])
else:
    shift=0.0

# looking for BZ lattice vectors in OUTCAR
outcar = open("OUTCAR", 'r')
outcar_lines = outcar.readlines()
i = 0
for line in outcar_lines:
    i = i + 1
    l = line.split()
    if(len(l) == 6 and str(l[4]) == "lattice" and str(l[5]) == "vectors"):
        break

#print "i=", i
#print outcar_lines[i]
BZ_cell=[ [ 0.0 for k in range(3) ] for l in range(3) ]
cell_r1 = outcar_lines[i  ].split()
cell_r2 = outcar_lines[i+1].split()
cell_r3 = outcar_lines[i+2].split()
BZ_cell[0] = [ float(cell_r1[3]), float(cell_r1[4]), float(cell_r1[5]) ]
BZ_cell[1] = [ float(cell_r2[3]), float(cell_r2[4]), float(cell_r2[5]) ]
BZ_cell[2] = [ float(cell_r3[3]), float(cell_r3[4]), float(cell_r3[5]) ]

#print BZ_cell[0]
#print BZ_cell[1]
#print BZ_cell[2]


f = open("EIGENVAL", 'r')
l = f.readline()
is_spin_poralized = bool(l.split()[3])


l = f.readline()
l = f.readline()
l = f.readline()
l = f.readline()
l = f.readline() 

nkpoints = int(l.split()[1])
nbands   = int(l.split()[2])

kpoints=[ [ 0.0 for i in range(3) ] for j in range(nkpoints) ]
bands=[ [ 0.0 for i in range(nbands) ] for j in range(nkpoints) ]


for k in range(nkpoints):
    l = f.readline()
    l = f.readline().split()
    kx = float(l[0])*BZ_cell[0][0] + float(l[1])*BZ_cell[1][0] + float(l[2])*BZ_cell[2][0]
    ky = float(l[0])*BZ_cell[0][1] + float(l[1])*BZ_cell[1][1] + float(l[2])*BZ_cell[2][1]
    kz = float(l[0])*BZ_cell[0][2] + float(l[1])*BZ_cell[1][2] + float(l[2])*BZ_cell[2][2]
#    kpoints[k] = [ float(l[0]), float(l[1]), float(l[2]) ]
#    kpoints[k][0] = float(l[0])
#    kpoints[k][1] = float(l[1])
#    kpoints[k][2] = float(l[2])
    kpoints[k] = [2.0*pi*kx,2.0*pi*ky,2.0*pi*kz]
#    print  kpoints[k]
    for b in range(nbands):
        l = f.readline()
        if(int(l.split()[0]) == b+1):
            bands[k][b] = float(l.split()[1]) + shift
#            bands[k][b] = float(l.split()[1])
        else :
            print "error:"

#kx=-1.344082455
#kx=-0.855669466543
#kx=1.024882333
#kx=-0.527
kx=0.0

print kx, ' '.join(map(str, bands[0]))
for k in range(1,nkpoints):
    dk = (kpoints[k][0] - kpoints[k-1][0])**2 + (kpoints[k][1] - kpoints[k-1][1])**2  + (kpoints[k][2] - kpoints[k-1][2])**2
    kx = kx + sqrt(dk)
    print kx, ' '.join(map(str, bands[k]))

f.close()

