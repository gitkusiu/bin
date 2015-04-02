#!/usr/bin/python

import sys
from ase.io.xsf import read_xsf
from ase.io.cube import write_cube

#TODO this is supposed to be a quite large converter scirpt 
# ase.convert.py -i inport_format -o output_format

num = len(sys.argv)
xsf = read_xsf(sys.argv[num-1],read_data=True)

write_cube(sys.stdout,xsf[1],xsf[0])
#write_cube("tmp.cube",xsf[1],xsf[0])
