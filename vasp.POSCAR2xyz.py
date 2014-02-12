#!/usr/bin/python

import sys
import numpy as np 

from ase.io.vasp import read_vasp
from ase.io.xyz import write_xyz
from optparse import OptionParser
import re

parser = OptionParser()
parser.add_option("-c", "--comment", action="store", type="string")
parser.add_option("-r", "--repeat", action="store", type="string")
(options, args) = parser.parse_args()

n = len(sys.argv)

if(n < 2):
    parser.print_help()
else:

    poscar_tmp = read_vasp(sys.argv[n-1])

    if(options.repeat != None):
        net      = map(int, re.findall(r'\d+', options.repeat) )
        poscar   = poscar_tmp*net
        filename = "poscar."+str(net[0])+"x"+str(net[1])+"x"+str(net[2])+".xyz"
    else:
        poscar   = poscar_tmp
        filename = "poscar.xyz"

    write_xyz(filename, poscar, comment=options.comment)
