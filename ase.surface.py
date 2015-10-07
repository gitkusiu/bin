#!/usr/bin/python

import sys
import os
from ase.io.aims import write_aims
#from ase.io.cube import write_cube
#from ase.io.vasp import write_vasp
#from ase.io.xsf  import write_xsf
#from ase.io.xyz  import write_xyz

from ase.lattice.surface import fcc111
from ase.lattice.surface import fcc110
#from ase.lattice.surface import mx2
import math
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-a", "--lattice",    action="store", type="float", default=1.0)
parser.add_option("-p", "--periods",    action="store", type="int",    default=[1,1,1],       help="repetition of the unit cell", nargs=3)
parser.add_option("-v", "--vaccuum",    action="store", type="float", default=1.0)
parser.add_option("-e", "--element",    action="store", type="string", default='H')
parser.add_option("-o", "--ortogonal",  action="store_true", default=False)
parser.add_option("-b", "--bravais",    action="store", type="string", default='fcc')
parser.add_option(      "--hkl",        action="store", type="string", default='111')


(options, args) = parser.parse_args()


num = len(sys.argv)
if(num < 2):
    parser.print_help()
    sys.exit()


l=options.lattice
p=options.periods
v=options.vaccuum
e=options.element

atoms = []
if(options.bravais == 'fcc'):
    if(options.hkl == '111'):
        #atoms = fcc111(e, size=p,a=l, vacuum=v, orthogonal=False)
        atoms = fcc111(e, size=p,a=l, vacuum=v, orthogonal=options.ortogonal)
    elif(options.hkl == '110'):
        atoms = fcc110(e, size=p,a=l, vacuum=v)
elif(options.bravais == 'MoS2'):
    atoms = mx2(formula='MoS2', kind='2H', a=3.18, thickness=3.19, size=(1, 1, 1), vacuum=7.5)
#c=atoms.get_cell()
#c[1][0] += l*math.sqrt(2)*0.5
#atoms.set_cell(c)

#atoms.translate([0.0,0.0,-14.9999999999999982])

print atoms
tmpname="geometry.in.tmp"
write_aims(tmpname, atoms)
f = open(tmpname, 'r')
print f.read()
f.close()
os.remove(tmpname)
#write_aims("geometry.in", atoms)
