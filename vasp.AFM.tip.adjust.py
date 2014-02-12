#!/usr/bin/python

import sys
import numpy as np 

from ase.io.vasp import read_vasp
from ase.io.vasp import write_vasp

#print sys.argv[1]
narg = len(sys.argv)

if( narg != 6 ):
	print "You have passed " + str(narg-1) + " arguments to the script"
	print "This script needs 5 parameters"
	print "Scrips exits"
	exit()

r = []
surID = int(  sys.argv[1])      # surface atom ID
tipID = int(  sys.argv[2])    # tip appex atom ID
r.append( float(sys.argv[3]) )
r.append( float(sys.argv[4]) )
r.append( float(sys.argv[5]) )

contcar = read_vasp('CONTCAR')
pos = contcar.arrays['positions']
symbols = contcar.get_chemical_symbols()

print pos
#print symbols

R     = pos[tipID-1] - pos[surID-1]
tip_z = pos[tipID-1][2]
dr = r - R

#print tipID, surID
#print symbols[tipID-1],pos[tipID-1]
#print symbols[surID-1],pos[surID-1]
#print "R", R
#print "r", r
#print "dr", dr


N=contcar.get_number_of_atoms()
write_vasp("POSCAR.old",contcar,label="Old Poscar", direct=False,sort=False,vasp5=True)
#print "tipID, N", tipID, N


for i in range(N):
	if(pos[i][2] >= tip_z):
#		print i+1, contcar.arrays['positions'][i]
		contcar.arrays['positions'][i] +=  dr 

write_vasp("POSCAR.new",contcar,label="New Poscar", direct=False,sort=False,vasp5=True)
