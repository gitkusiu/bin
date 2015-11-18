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
parser.add_option("-g", "--get",        action="store", type="string", default="positions",     help="Type of data we want to get")
parser.add_option("-p", "--period",     action="store", type="int", help="period",   nargs=3)
(options, args) = parser.parse_args()


# count number of command line arguments
num = len(sys.argv)
if(num < 2):
    parser.print_help()
else:
    output = read_aims_output(sys.argv[num-1], slice(0,None,1))
    n = len(output)

    if(n > 0):
        i=0
        for step in output:
            i += 1
            if(options.get == "positions"):
                comm = "step no. " + str(i) + " TOTEN = " + str(step.get_total_energy())
                p=options.period
                if(p != None):
                    step = step*(p[0], p[1], p[2])
                write_xyz(sys.stdout,[step],comment=comm)
#                print step.
