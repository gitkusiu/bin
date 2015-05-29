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
#parser.add_option("-t", "--trans",            action="store",       type="string", help="Transformation to be done")
parser.add_option("-a", "--atoms",            action="store",       type="int",    help="specify the atoms to whcih changes (translation rotation etc. will be made)", nargs=2)
parser.add_option("-t", "--translate_vector", action="store",       type="float",  help="Vector of translation", nargs=3)
parser.add_option("-s", "--scale",            action="store",       type="float",  help="Vector of translation")
parser.add_option("-r", "--rotate_angle",     action="store",       type="float",  help="Angle  of rotation")
parser.add_option(      "--rotate_around",    action="store",       type="int",    help="Number of atom around which rotation should be performed")
parser.add_option(      "--rotate_axis",      action="store",       type="string", help="Rotation axis",  default='z')
#                       "--c1+"
parser.add_option(      "--cell1Extend",       action="store",       type="string", help="Vector of Cell_1 extention", nargs=3)
parser.add_option(      "--cell2Extend",       action="store",       type="string", help="Vector of Cell_1 extention", nargs=3)
parser.add_option(      "--cell3Extend",       action="store",       type="string", help="Vector of Cell_1 extention", nargs=3)
#parser.add_option(      "--cell_2_extend",    action="store",       type="string", help="Vector of Cell_2 extention", default=[0.,0.,0.], nargs=3)
#parser.add_option(      "--cell_3_extend",    action="store",       type="string", help="Vector of Cell_3 extention", default=[0.,0.,0.], nargs=3)
#                       "--c1"
parser.add_option(      "--cell1Set",          action="store",       type="string", help="Vector of Cell_1", nargs=3)
parser.add_option(      "--cell2Set",          action="store",       type="string", help="Vector of Cell_1", nargs=3)
parser.add_option(      "--cell3Set",          action="store",       type="string", help="Vector of Cell_1", nargs=3)
parser.add_option(      "--cutX",              action="store",       type="float", help="Cut X")
parser.add_option(      "--cutY",              action="store",       type="float", help="Cut Y")
parser.add_option(      "--cutZ",              action="store",       type="float", help="Cut Z")
#parser.add_option(      "--cellSet",       action="store",       type="string", help="Vector of Cell_2", nargs=3)
#parser.add_option(      "--cell_3_set",       action="store",       type="string", help="Vector of Cell_3", nargs=3)
parser.add_option("-p", "--period",           action="store",        type="int",    help="simension of repeation", nargs=3)
parser.add_option(      "--comment",          action="store",        type="string", help="his file was created by ase.convert.py script",     default='z')
parser.add_option(      "--vaspold",          action="store_false",                 help="comment line",     default=True)
parser.add_option(      "--vaspsort",         action="store_true",                  help="comment line",     default=False)
parser.add_option(      "--xyzcell",          action="store",        type="string", help="file of xyz cell", default=xyzCellFile)
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
#trans   = options.trans
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

    if( options.translate_vector != None ):
        v                               = options.translate_vector
        is_translation_nonzero          = (v != (0.0,0.0,0.0))
        is_there_any_atoms_to_translate = (trange[1]-trange[0] >= 0)
        if( is_translation_nonzero and is_there_any_atoms_to_translate ):
            for i in range(trange[0]-1, trange[1]):
                atoms.arrays['positions'][i] += v

    if( options.scale != None ):
        s = options.scale
        for r in atoms.arrays['positions']:
            r *= s
        if atoms.get_cell().shape == (3,3):
            for c in atoms._cell:
                c *= s

    if(options.rotate_angle != None):
        angle     = options.rotate_angle
        axis      = options.rotate_axis
        ra        = options.rotate_around
        origin = [0.,0.,0.]
        if(ra != None):
            if(ra > 0 and ra <= natoms):
                origin  = atoms.arrays['positions'][ra-1]
            else:
                print "Error"
        else:
            orgin = np.array([0.0,0.0,0.0])
        asekk.rotate_atoms(atoms, angle, fromto=trange, axis=axis, origin=origin)

    c        = atoms.get_cell()
    if(  options.cell1Set !=  None): 
        cSet = np.array(options.cell1Set).astype(np.float)
        c[0] = cSet
    if(  options.cell2Set !=  None):
        cSet = np.array(options.cell2Set).astype(np.float)
        c[1] = cSet
    if(  options.cell3Set !=  None):
        cSet = np.array(options.cell3Set).astype(np.float)
        c[2] = cSet

    if(  options.cell1Extend !=  None):
        cExtend = np.array(options.cell1Extend).astype(np.float)
        c[0]    = np.add(c[0], cExtend)
    if(  options.cell2Extend !=  None):
        cExtend = np.array(options.cell2Extend).astype(np.float)
        c[1]    = np.add(c[1], cExtend)
    if(  options.cell3Extend !=  None):
        cExtend = np.array(options.cell3Extend).astype(np.float)
        c[1]    = np.add(c[2], cExtend)
    atoms.set_cell(c)

    if(  options.period != None ):
        is_periodic = all(atoms.get_pbc()) and atoms.get_cell().shape == (3, 3)
        if(not is_periodic):
            sys.exit("ERROR: Call for periodic extention of the system, but supercell or pbc flag setted wrongly.")
        dim = np.array( options.period)
        atoms.set_constraint() ### TODO!!!!!!!!!!!!  I can not awwoid cutting constraint. Check how to fix it
        atoms = atoms * dim



    # >>>>>>>>>>>>>>>>>>>>> WRITE GEOMETRY <<<<<<<<<<<<<<<<<<<<
    if(oformat == "geometry.in"):
        tmpname="geometry.in.tmp"
        write_aims(tmpname, atoms)
        f = open(tmpname, 'r')
        print f.read()
        f.close()
        os.remove(tmpname)
#    elif(oformat == "cube"):
#        write_cube(`,xsf[1],xsf[0])
#    elif(oformat == "xsf"):
#        write_xsf(sys.stdout,xsf[1],xsf[0])
    elif(oformat == "POSCAR"):
        write_vasp(ostream, atoms, label=options.comment, direct=False,sort=options.vaspsort,vasp5=options.vaspold)
    if(oformat == "xyz"):
        write_xyz(ostream, atoms)
    if(oformat == "shtm"):
        d = {}
        f = open('species.dat', "r")
        ls = f.read().splitlines()
        n = int(ls[0])
        for ii in ls[1:n+1]:
            i = ii.split()
            d[i[3]] = int(i[0])

        n   = atoms.get_number_of_atoms()
        pos = atoms.get_positions()
        sym = atoms.get_chemical_symbols()

        print atoms.get_number_of_atoms()
        for s, p in zip(sym, pos):
            print  d[s], p[0], p[1], p[2]

##write_cube("tmp.cube",xsf[1],xsf[0])
