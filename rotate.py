#!/usr/bin/python

import asekk
import sys
import numpy as np
from math import cos, sin, pi

from ase.io.vasp import read_vasp
from ase.io.vasp import write_vasp


num = len(sys.argv)
poscar = read_vasp(sys.argv[num-1])

p=poscar.arrays['positions']
n=len(p)
#for i in range(n):
#    print p[i]

kat=-45.0

#for i in range(n):
#    p[i] = asekk.rotate(p[i],kat,'y',origin=p[0])

asekk.rotate_atoms(poscar, kat, fromto=[1,4], axis='z', origin=[0.0,0.0,0.0])

write_vasp(sys.stdout,poscar,label="moj test", direct=False,sort=False,vasp5=True)

#v1=[2.0,0.0,0.0]
#v2=rotate(vector=v1,alpha=-90.0,axis='z',origin=[1.0,0.0,0.0])
#print v1
#print v2
