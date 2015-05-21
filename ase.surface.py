#!/usr/bin/python

import sys
import os
from ase.io.aims import write_aims
#from ase.io.cube import write_cube
#from ase.io.vasp import write_vasp
#from ase.io.xsf  import write_xsf
#from ase.io.xyz  import write_xyz

from ase.lattice.surface import fcc111
import math
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-a", "--lattice",    action="store", type="float", default=1.0)
parser.add_option("-p", "--periods",    action="store", type="int",    default=[1,1,1],       help="repetition of the unit cell", nargs=3)
parser.add_option("-v", "--vaccuum",    action="store", type="float", default=1.0)
parser.add_option("-e", "--element",    action="store", type="string", default='H')
(options, args) = parser.parse_args()


num = len(sys.argv)
if(num < 2):
    parser.print_help()
    sys.exit()


l=options.lattice
p=options.periods
v=options.vaccuum
e=options.element

#atoms = fcc111(e, size=p,a=l, vacuum=v, orthogonal=True)
atoms = fcc111(e, size=p,a=l, vacuum=v)

#c=atoms.get_cell()
#c[1][0] += l*math.sqrt(2)*0.5
#atoms.set_cell(c)

#atoms.translate([0.0,0.0,-14.9999999999999982])

tmpname="geometry.in.tmp"
write_aims(tmpname, atoms)
f = open(tmpname, 'r')
print f.read()
f.close()
os.remove(tmpname)
#write_aims("geometry.in", atoms)
