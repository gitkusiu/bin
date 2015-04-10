#!/usr/bin/python

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
(options, args) = parser.parse_args()


l=options.lattice
p=options.periods
v=options.vaccuum

atoms = fcc111('Au', size=p,a=l, vacuum=v)

#c=atoms.get_cell()
#c[1][0] += l*math.sqrt(2)*0.5
#atoms.set_cell(c)

atoms.translate([0.0,0.0,-9.9999999999999982])

write_aims("geometry.in", atoms)
