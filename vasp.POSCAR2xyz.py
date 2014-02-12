#!/usr/bin/python

import sys
import numpy as np 

from ase.io.vasp import read_vasp
from ase.io.xyz import write_xyz

#print sys.argv[1]

poscar = read_vasp(sys.argv[1])


if( len(sys.argv) > 2):
	comm = sys.argv[2]

write_xyz("poscar.xyz", poscar, comment=comm)
