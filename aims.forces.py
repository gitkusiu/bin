#!/usr/bin/python

######################################
#
#   Script which calculate average
#   efective potential basing on the
#   v_eff.dat file 
#
######################################
import sys
import numpy as np

from ase.io.aims import read_aims_output
from ase.io.xyz import write_xyz

from optparse import OptionParser

parser = OptionParser()
parser.add_option('-a', '--atoms',            action="store",       type="int",    help="specify the atoms range", nargs=2)
(options, args) = parser.parse_args()


a_range = options.atoms

num = len(sys.argv)
f  = open(sys.argv[num-1], "r")
lines = f.read().splitlines()

f_tot = [0.,0.,0.]
natom = a_range[0]
#print a_range
for i, line in enumerate(lines):    
    if line.find("Total forces({0:{width}})".format(natom,width=4))  != -1:
        f = np.array(line.split()[4:7]).astype(np.float)
        f_tot += f
        natom += 1
        if (natom > a_range[1]):
            natom = a_range[0]
            print  float(f_tot[0]), float(f_tot[1]), float(f_tot[2])
            f_tot = [0.,0.,0.]
