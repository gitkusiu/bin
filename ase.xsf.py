#!/usr/bin/python

# Convertion form xfs to cube format is done by ase.convert.py script right now

import sys
from ase.io.xsf import read_xsf
from ase.io.cube import write_cube
#from ase        import Atoms

from optparse import OptionParser

#parser = OptionParser()
#parser.add_option("-f", "--format",   action="store", type="string", default="xsf",      help="output format")

num = len(sys.argv)
xsf = read_xsf(sys.argv[num-1],read_data=True)


grid = xsf[0]
cell = xsf[1].cell  

lx = len(grid)
ly = len(grid[0])
lz = len(grid[0][0])
dz = cell[2][2]/lz

#print lx,ly,lz, dz

summ =0.0
#print range(lz)
for k in range(lz):
    for j in range(ly):
        for i in range(lx):
            summ += grid[i][j][k]
    print dz*k, summ/(lx*ly)
    summ = 0.0



