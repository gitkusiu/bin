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
parser.add_option("-o", "--output",           action="store",       type="string", help="output file format")
parser.add_option("-t", "--trans",            action="store",       type="string", help="Transformation to be done")
parser.add_option(      "--atoms",            action="store",       type="int",    help="specify the atoms to whcih changes (translation rotation etc. will be made)", nargs=2)
parser.add_option(      "--translate_vector", action="store",       type="float",  help="Vector of translation", default=[0.,0.,0.], nargs=3)
parser.add_option(      "--rotate_angle",     action="store",       type="float",  help="Angle  of rotation",    default=0.0)
parser.add_option(      "--rotate_around",    action="store",       type="int",    help="Number of atom around which rotation should be performed")
parser.add_option(      "--rotate_axis",      action="store",       type="string", help="Rotation axis",  default='z')
parser.add_option(      "--cellExtend",       action="store",       type="string", help="Vector of Cell_1 extention", nargs=3)
#parser.add_option(      "--cell_2_extend",    action="store",       type="string", help="Vector of Cell_2 extention", default=[0.,0.,0.], nargs=3)
#parser.add_option(      "--cell_3_extend",    action="store",       type="string", help="Vector of Cell_3 extention", default=[0.,0.,0.], nargs=3)
parser.add_option(      "--cellSet",          action="store",       type="string", help="Vector of Cell_1", nargs=3)
#parser.add_option(      "--cellSet",       action="store",       type="string", help="Vector of Cell_2", nargs=3)
#parser.add_option(      "--cell_3_set",       action="store",       type="string", help="Vector of Cell_3", nargs=3)
parser.add_option(      "--repeat_dim",       action="store",       type="int", help="simension of repeation", default=[1,1,1], nargs=3)
parser.add_option(      "--comment",          action="store",       type="string", help="his file was created by ase.convert.py script",     default='z')
parser.add_option(      "--vaspold",          action="store_false",                help="comment line",     default=True)
parser.add_option(      "--vaspsort",         action="store_true",                 help="comment line",     default=False)
parser.add_option(      "--xyzcell",          action="store",       type="string", help="file of xyz cell", default=xyzCellFile)
(options, args) = parser.parse_args()

#TODO use this four lines to eliminate --trans variable
do_we_translate = (options.translate_vector != [0.,0.,0.]) 
do_we_rotate    = (options.rotate_angle     != 0.0) and \
                  (options.rotate_around    != None) and \
                  (options.rotate_axis      != None)

iformat = options.input
if(options.output != None): # default output format
    oformat = options.output
else:
    oformat = options.input
trans   = options.trans
trange  = options.atoms
ostream = sys.stdout


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


    # >>>>>>>>>>>>>>>>>>>>> TRANSFORM GEOMETRY <<<<<<<<<<<<<<<<<<<<
    natoms = atoms.get_number_of_atoms()
    # atoms selection for modyfiactions
    if(trange == None): # # default range of atoms
        trange = (1, natoms)

    if(  trans == "T" or trans == "translation"):
        v                               = options.translate_vector
        is_translation_nonzero          = (v != (0.0,0.0,0.0))
        is_there_any_atoms_to_translate = (trange[1]-trange[0] >= 0)
        if( is_translation_nonzero and is_there_any_atoms_to_translate ):
            for i in range(trange[0]-1, trange[1]):
                atoms.arrays['positions'][i] += v

    elif(trans == "R" or trans == "rotation"   ):
        angle     = options.rotate_angle
        axis      = options.rotate_axis
        ra        = options.rotate_around
        origin = [0.,0.,0.]
        if(ra > 0 and ra <= natoms):
            origin  = atoms.arrays['positions'][ra-1]
        else:
            print "Error"
        asekk.rotate_atoms(atoms, angle, fromto=trange, axis=axis, origin=origin)

    zero     = np.zeros(3)
    cSet     = np.array(options.cellSet).astype(np.float)
    cExtend  = np.array(options.cellExtend).astype(np.float)
    c        = atoms.get_cell()
    if(  trans == "C1"  ):
        if(options.cellSet != None ):
            c[0] = cSet
        if(options.cellExtend != None ):
            c[0] = np.add(c[0], cExtend)
    if(  trans == "C2"  ):
        if(options.cellSet != None ):
            c[1] = cSet
        if(options.cellExtend != None):
            c[1] = np.add(c[1], cExtend)
    if(  trans == "C3" ):
        if(options.cellSet != None):
            c[2] = cSet
        if(options.cellExtend != None):
            c[2] = np.add(c[2], cExtend)
    atoms.set_cell(c)


    if(  trans == "repeat" ):
        dim = np.array(options.repeat_dim)
        atoms.set_constraint() ### TODO!!!!!!!!!!!!  I can not awwoid cutting constraint. Check how to fix it
        atoms = atoms * dim


    # >>>>>>>>>>>>>>>>>>>>> WRITE GEOMETRY <<<<<<<<<<<<<<<<<<<<
    if(oformat == "geometry.in"):
        write_aims("geometry.in", atoms)
#    elif(oformat == "cube"):
#        write_cube(`,xsf[1],xsf[0])
#    elif(oformat == "xsf"):
#        write_xsf(sys.stdout,xsf[1],xsf[0])
    elif(oformat == "POSCAR"):
        write_vasp(ostream, atoms, label=options.comment, direct=False,sort=options.vaspsort,vasp5=options.vaspold)
    if(oformat == "xyz"):
        write_xyz(ostream, atoms)

##write_cube("tmp.cube",xsf[1],xsf[0])
