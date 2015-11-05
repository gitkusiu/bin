#!/usr/bin/python

import sys
from ase.io.xsf import read_xsf
from ase.io.cube import write_cube
#from ase        import Atoms

num = len(sys.argv)
xsf = read_xsf(sys.argv[num-1],read_data=True)

print xsf[0]
#write_cube(sys.stdout,xsf[1],xsf[0])
#write_cube("tmp.cube",xsf[1],xsf[0])


