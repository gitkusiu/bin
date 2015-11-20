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

import asekk

num = len(sys.argv)
ifile = sys.argv[num-1]
xyzCellFile = os.path.splitext(ifile)[0]+".lvs"

parser = OptionParser()
parser.add_option("-i", "--input",            action="store",       type="string", help="input file format")
#parser.add_option("-o", "--output",           action="store",       type="string", help="output file format")
#parser.add_option("-t", "--trans",            action="store",       type="string", help="Transformation to be done")
parser.add_option("-a",  "--atoms",            action="store",        type="int",    help="specify the atoms to whcih changes (translation rotation etc. will be made)", nargs=2)
parser.add_option("-d",  "--distance",         action="store_true",   help="Get distance between two atoms")
parser.add_option("-v",  "--vector",           action="store_true",   help="Get distance vector between two atoms")
parser.add_option("-n",  "--no_atoms",         action="store_true",   help="Get number of atoms")
parser.add_option(       "--enumerate",         action="store_true",  help="Enumerate an atoms")
parser.add_option(       "--lc1",              action="store_true",   help="Get Lenght of cell1")
parser.add_option(       "--lc2",              action="store_true",   help="Get Lenght of cell2")
parser.add_option(       "--lc3",              action="store_true",   help="Get Lenght of cell3")
#parser.add_option(      "--translate_vector", action="store",       type="float",  help="Vector of translation", default=[0.,0.,0.], nargs=3)
#parser.add_option(      "--rotate_angle",     action="store",       type="float",  help="Angle  of rotation",    default=0.0)
#parser.add_option(      "--rotate_around",    action="store",       type="int",    help="Number of atom around which rotation should be performed")
#parser.add_option(      "--rotate_axis",      action="store",       type="string", help="Rotation axis",  default='z')
#parser.add_option(      "--cellExtend",       action="store",       type="string", help="Vector of Cell_1 extention", nargs=3)
##parser.add_option(      "--cell_2_extend",    action="store",       type="string", help="Vector of Cell_2 extention", default=[0.,0.,0.], nargs=3)
##parser.add_option(      "--cell_3_extend",    action="store",       type="string", help="Vector of Cell_3 extention", default=[0.,0.,0.], nargs=3)
#parser.add_option(      "--cellSet",          action="store",       type="string", help="Vector of Cell_1", nargs=3)
##parser.add_option(      "--cellSet",       action="store",       type="string", help="Vector of Cell_2", nargs=3)
##parser.add_option(      "--cell_3_set",       action="store",       type="string", help="Vector of Cell_3", nargs=3)
#parser.add_option(      "--repeat_dim",       action="store",       type="int", help="simension of repeation", default=[1,1,1], nargs=3)
#parser.add_option(      "--comment",          action="store",       type="string", help="his file was created by ase.convert.py script",     default='z')
#parser.add_option(      "--vaspold",          action="store_false",                help="comment line",     default=True)
#parser.add_option(      "--vaspsort",         action="store_true",                 help="comment line",     default=False)
parser.add_option(      "--xyzcell",          action="store",       type="string", help="file of xyz cell", default=xyzCellFile)
(options, args) = parser.parse_args()

##TODO use this four lines to eliminate --trans variable
#do_we_translate = (options.translate_vector != [0.,0.,0.]) 
#do_we_rotate    = (options.rotate_angle     != 0.0) and \
#                  (options.rotate_around    != None) and \
#                  (options.rotate_axis      != None)

iformat = options.input
#trans   = options.trans
#trange  = options.atoms
#ostream = sys.stdout


atoms=[]
natoms = 0

if(num < 2):
    parser.print_help()
else:
    # >>>>>>>>>>>>>>>>>>>>> READ GEOMETRY <<<<<<<<<<<<<<<<<<<<
    if(iformat == "geometry.in"):
        atoms = read_aims(ifile)
#    elif(iformat == "cube"):
#        atoms = read_cube(sys.argv[num-1])
#    elif(iformat == "xsf"):
#        atoms = read_xsf(sys.argv[num-1],read_data=True)
    elif(iformat == "POSCAR"):
        atoms = read_vasp(ifile)
    elif(iformat == "xyz"):
        atoms           = read_xyz(ifile)
        cfile           = options.xyzcell
        ThereIsCellFile = os.path.isfile(cfile)
        if(ThereIsCellFile):
            cell = [[],[],[]]
            f    = open(cfile, "r")
            ls   = f.read().splitlines()
            for i in range(3):
                l = ls[i].split()
                cell[i] = [float(l[0]), float(l[1]), float(l[2])]
            atoms.set_cell(cell)
            atoms.set_pbc([True,True,True])


    if(options.vector == True):
        a = options.atoms
        r1 = atoms.arrays['positions'][a[0]-1] 
        r2 = atoms.arrays['positions'][a[1]-1] 
#        print a[0],r1
#        print a[1],r2
        dr = r2-r1
        print dr[0], dr[1], dr[2]

    if(options.distance == True):
        a = options.atoms
        print atoms.get_distance(a[0],a[1])

    if(options.enumerate == True):
        chem = atoms.get_chemical_symbols()
        for i, r in enumerate(atoms.arrays['positions']):
            print i+1, chem[i], r

    if(options.no_atoms == True):
        print atoms.get_number_of_atoms()

    c        = atoms.get_cell()
    if(options.lc1 == True): print np.linalg.norm(c[0])
    if(options.lc2 == True): print np.linalg.norm(c[1])
    if(options.lc3 == True): print np.linalg.norm(c[2])



