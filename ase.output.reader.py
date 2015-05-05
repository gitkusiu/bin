#!/usr/bin/python


#TODO this is supposed to be a quite large converter scirpt 
# ase.convert.py -i inport_format -o output_format
import sys
import os.path
import numpy as np

from ase.io.aims import read_aims_output

from ase.io.aims import write_aims
from ase.io.xyz  import write_xyz

from optparse import OptionParser

import asekk

num = len(sys.argv)
ifile = sys.argv[num-1]


parser = OptionParser()
parser.add_option("-i", "--input",            action="store",       type="string",                      help="input file format")
parser.add_option("-g", "--get",              action="store",       type="string", default="positions", help="Type of data we want to get")
parser.add_option("-o", "--output",           action="store",       type="string", default="xyz",       help="output file format")
parser.add_option(      "--step",             action="store",       type="int",    default=None,        help="Step number")
parser.add_option(      "--steps",            action="store",       type="int",    default=None,        help="Step number", nargs=2)
(options, args) = parser.parse_args()

#TODO
# 1. For larger numer of input formats make validation of other options
#    Especialy '--get' should be checket. I may have a output file which does not contain all '--get' data


num = len(sys.argv)
if(num < 2):
    parser.print_help()
    sys.exit()

if(options.input == "aims"):
    output = read_aims_output(sys.argv[num-1], slice(0,None,1))

n = len(output)

#deduce stape range
one_step   = options.step != None
more_steps = options.steps != None
step_range = [0,0]
if (one_step != more_steps): # only --step or --steps is used
    if(one_step):
        step_range = [options.step,options.step]
    else:
        step_range = options.steps
else:
    if(one_step == False and more_steps == False):
        step_range = [1,n]
    else:                   # can not have '--step' and '--steps' specified together
        print "Error: You have specified --step and --steps together. Please specifie only one of them."
        print "sys.exit()"
        sys.exit()
# check of stape range reasonability
if  (step_range[0] < 1 or step_range[1] > n):
    print "Error: specifies step range out of the [1,number of steps] range."
    print "sys.exit()"
    sys.exit()
elif(step_range[0] > step_range[1]):
    print "Error: range is negatif ('start' if larger than 'stop')."
    print "sys.exit()"
    sys.exit()


if(n > 0):
    if(options.get == "nosteps"):
        print n
    else:
        start = step_range[0]
        stop  = step_range[1]
        for i in range(start, stop+1):
            step = output[i-1]

            if(options.get == "Etot"):
                print str(i) + " " + str(step.get_total_energy())

            elif(options.get == "positions"):
                comm = "step no. " + str(i) + " TOTEN = " + str(step.get_total_energy())
                if(options.output == "xyz"):
                    write_xyz(sys.stdout,step,comment=comm)
# >>>>>>>>>>>>>>>>>>>>>>>>> TODO <<<<<<<<<<<<<<<<<<<<<<<<<
#        if(options.output == "xyz"):
#            cell = output[0].get_cell()
#            f    = open('answer.lvs', 'w')
#            print ' '.join(str(cell[0,:]))
#            f.write(str(cell[0,:]))
#            f.write(str(cell[1,:]))
#            f.write(str(cell[2,:]))
#            print cell



