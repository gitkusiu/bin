#!/usr/bin/python

import sys
import numpy as np 
import re
import os
from math import *

from ase.io.vasp import read_vasp_out
from ase.io.xyz import write_xyz

from optparse import OptionParser


parser = OptionParser()
parser.add_option("-g", "--get",     action="store", type="string", default="positions",      help="what kind of data shoud be extracted")
parser.add_option("-f", "--format",     action="store", type="string", default="xyz",           help="format of positions file: xyz ")
parser.add_option("-a", "--atoms",      action="store", type="int",    default=[-1,-1],         help="specify range of atoms", nargs=2)
parser.add_option("-s", "--steps",      action="store", type="int",    default=[-1,-1],         help="specify range of steps", nargs=2)
parser.add_option("-p", "--periods",    action="store", type="int",    default=[1,1,1],       help="repetition of the unit cell", nargs=3)
(options, args) = parser.parse_args()

num = len(sys.argv)


if(num < 2):
    parser.print_help()
else:
    if(options.get == "conv"):
        ediffg = 0.0
        for line in open(sys.argv[num-1]):
            if "EDIFFG" in line:
                ediffg = float(line.split()[2])
                print "EDIFFG = ", ediffg, ":       "
            if "reached required accuracy" in line:
                print line
                exit()
        print "Error: VASP did not reached required accuracy. Maximal force is "
        options.get   = "max_force"
        options.steps = [-1,1]

    elif(options.get == "energy"):
        toten = 0.0
        for line in open(sys.argv[num-1]):
            if "TOTEN" in line:
                toten = float(line.split()[4])
        print toten
        exit()

    outcar = read_vasp_out(sys.argv[num-1], slice(0,None,1))

    n = len(outcar)
    if(n > 0):

        # --------------- step index range ------------------------
        s = options.steps
        if(s[0] == -1): # deafult case: all steps
            if( s[1] == -1):
                s = (1, n)
            else:
                s = (n,n)
        elif( s[0] > n or s[1] > n ):
            print "ERROR: Step range is larger than number of steps in OUTCAR"
            exit()
        elif( s[0] > s[1] ):
            print "ERROR: Max step is smaler that Min step"
            exit()

        # --------------- atoms index range ------------------------
        natoms = outcar[0].get_number_of_atoms()
        a = options.atoms
        if( a[0] > natoms or a[1] > natoms ):
            print "ERROR: Atoms range is larger than number of steps in OUTCAR"
            exit()
        elif( a[0] > a[1] ):
            print "ERROR: Max step is smaler that Min step"
            exit()
        elif(a[0] == -1): # deafult case: we change all atoms
            a[0] = 1
            a[1] = natoms
    
        p = options.periods
        if( p[0] <= 0 and p[1] <= 0 and p[2] <= 0 ):
            print "ERROR: At least one of period is not positive"
            exit()

        for i in range(s[0],s[1]+1):
            step = outcar[i-1]


            if(options.get == "positions" or options.get == "pos"):
                comm = "step no. " + str(i) + " TOTEN = " + str(step.get_total_energy())
                if(p == [1,1,1]):
                    write_xyz(sys.stdout,step,comment=comm)
                else:
                    step_period = step*p
                    write_xyz(sys.stdout,step_period,comment=comm)


            if(options.get == "forces"):
                forces = step.get_forces()
                for j in range(a[0],a[1]+1):
                    print j , forces[j-1][0], forces[j-1][1], forces[j-1][2]
                print " "


            if(options.get == "force"):
                forces = step.get_forces()
                print len(outcar), i, len(forces)
                tip_force = [0.0,0.0,0.0]
                for j in range(a[0],a[1]+1):
#                    print "%0.24f" % forces[j-1][0]
                    print j, forces[j-1]
                    tip_force += forces[j-1]
                print tip_force[0],tip_force[1],tip_force[2]


            if(options.get == "max_force"):
                forces    = np.array(step.get_forces())
                fix_atoms = step.constraints[0].index
                max_force = 0.0
                for j in range(a[0],a[1]+1):
                    if((j in fix_atoms) != True):
                        f = forces[j-1]
                        norm = sqrt(f[0]**2 + f[1]**2 + f[2]**2)
                        if ( norm > max_force):
                            max_force = norm
                print "\t",max_force
    else:
        print "Error: OUTCAR does not contain sufficient amount of information. Number of ionic steps = 0."
