#!/usr/bin/python


#TODO this is supposed to be a quite large converter scirpt 
# ase.convert.py -i inport_format -o output_format
import sys
import os.path
import numpy as np

from ase.io.aims import read_aims
from ase.io.cube import read_cube
from ase.io.vasp import read_vasp
from ase.io.xsf  import read_xsf
from ase.io.xyz  import read_xyz


from ase.io.aims import write_aims
from ase.io.cube import write_cube
from ase.io.vasp import write_vasp
from ase.io.xsf  import write_xsf
from ase.io.xyz  import write_xyz

from optparse import OptionParser

num = len(sys.argv)
ifile = sys.argv[num-1]
xyzCellFile = os.path.splitext(ifile)[0]+".lvs"

parser = OptionParser()
parser.add_option("-i", "--input",    action="store",       type="string", help="input file format")
parser.add_option("-o", "--output",   action="store",       type="string", help="output file format")
parser.add_option("-g", "--get",      action="store",       type="string", help="Type of data we want to get")
parser.add_option(      "--gradient", action="store",       type="string", help="Calculate derrivative allong x y or z direction")
parser.add_option(      "--diff",     action="store_true",                 help="Calculate difference between field 1 and field 2")
parser.add_option(      "--times",    action="store",       type="string", help="Calculate derrivative allong x y or z direction")
parser.add_option(      "--comment",  action="store",       type="string", help="comment line",     default="this file was created by ase.convert.py script")
(options, args) = parser.parse_args()

iformat = options.input
if(options.output != None): # default output format
    oformat = options.output
else:
    oformat = options.input
ostream = sys.stdout

atoms=[]
field=[]

atoms2=[]
field2=[]

if(num < 2):
    parser.print_help()
else:

    opt_diff = options.diff
    opt_grad = options.gradient

    two_files_involved = (opt_diff)

####### READING THE FILE #############
    if(iformat == "cube"):
        if( two_files_involved ):
            field,  atoms  = read_cube(sys.argv[num-2],read_data=True)
            field2, atoms2 = read_cube(sys.argv[num-1],read_data=True)
            if( atoms==atoms2 ):
                print "WARRNING: geometries of the system are not the same"
        else:
            field,  atoms  = read_cube(sys.argv[num-1],read_data=True)



####### MANIPULATE #############
    get = options.get

    # Calculate Gradient of the fild
    if( opt_grad != None ):
#    if(get == "diffx" or get == "diffy" or get == "diffz"):
        cell  = np.array(atoms.get_cell())
        shape = np.array(field.shape)
        dr    = np.empty(3)
        for i in range(3):
            if(shape[i] % 2 == 1):
                shape[i] +=  1
            dcell = cell[i]/shape[i]
            dr[i] = np.linalg.norm(dcell)

        field_grad = np.gradient(field,dr[0],dr[1],dr[2])

        if  ( opt_grad == "x" ): field = field_grad[0]
        elif( opt_grad == "y" ): field = field_grad[1]
        elif( opt_grad == "z" ): field = field_grad[2]

#    print field
#    print field2
    if(opt_diff):
        field -= field2


####### WRITEING THE FILE #############
    if(oformat == "xsf"):
#        write_xsf(sys.stdout,field[1],field[0])
        write_xsf(sys.stdout,atoms,field)
    if(oformat == "cube"):
        print "Warrning: Third line should contain number of atoms together with position of the origin of the volumetric data."
        print "Warrning: Make sure it contain corrrect data."
        write_cube(sys.stdout,atoms,field)


