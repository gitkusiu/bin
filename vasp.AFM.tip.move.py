#!/usr/bin/python

import sys
import numpy as np 

from ase.io.vasp import read_vasp
from ase.io.vasp import write_vasp

#print sys.argv[1]
narg = len(sys.argv)

if( narg < 5 ):
	print "You have passed " + str(narg-1) + " arguments to the script"
	print "This script needs 5 parameters"
	print "Scrips exits"
	exit()


contcar = read_vasp('CONTCAR')

r = []
n = int(  sys.argv[1])
m = int(  sys.argv[2])


if( narg==6 ):
	r.append( float(sys.argv[3]) )
	r.append( float(sys.argv[4]) )
	r.append( float(sys.argv[5]) )


if( narg==5 ):
	a1 = int(sys.argv[3])
	a2 = int(sys.argv[4])
	r1 = contcar.arrays['positions'][a1-1]
	r2 = contcar.arrays['positions'][a2-1]
	r = r2-r1
	print r

write_vasp("POSCAR.old",contcar,label="Old Poscar", direct=False,sort=False,vasp5=True)
for i in range(n-1, m):
	contcar.arrays['positions'][i] +=  r 

write_vasp("POSCAR.new",contcar,label="New Poscar", direct=False,sort=False,vasp5=True)
