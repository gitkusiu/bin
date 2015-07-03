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

n=0

for i, line in enumerate(lines):
    if "The structure contains" in line:
        l = line.split()
        n = int(l[3])
        break

print n
f_tot = [0.,0.,0.]
for i, line in enumerate(lines):
    if 'atomic forces [eV/Ang]:' in line:
        for j in range (1,n+1):
#            print a_range
            if( j>=a_range[0] and j<=a_range[1] ):
                f_tmp = np.array(lines[i+1+j*6].split()[4:7])
                f = f_tmp.astype(np.float)
                f_tot += f
        print  float(f_tot[0]), float(f_tot[1]), float(f_tot[2])
#        print f_tot
        f_tot = [0.,0.,0.]
