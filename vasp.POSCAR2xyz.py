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
        repetitions = map(int, re.findall(r'\d+', options.repeat) )
        poscar = poscar_tmp*repetitions
    else:
        poscar = poscar_tmp

    if( len(sys.argv) > 2):
        comm = sys.argv[2]

    write_xyz("poscar.xyz", poscar, comment=options.comment)
