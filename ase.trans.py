#!/usr/bin/python


#TODO this is supposed to be a quite large converter scirpt 
# ase.convert.py -i inport_format -o output_format
import sys
import os.path
import numpy as np

from ase import Atom
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
parser.add_option("-w", "--wrap",             action="store_true",  help="Wrap atoms into the unitcell")
parser.add_option("-r", "--rotate_angle",     action="store",       type="float",  help="Angle  of rotation")
parser.add_option(      "--rotate_around",    action="store",       type="int",    help="Number of atom around which rotation should be performed")
parser.add_option(      "--rotate_axis",      action="store",       type="string", help="Rotation axis",  default='z')

parser.add_option(      "--c1",               action="store",       type="float", help="Set cell_1", nargs=3)
parser.add_option(      "--c2",               action="store",       type="float", help="Set cell_2", nargs=3)
parser.add_option(      "--c3",               action="store",       type="float", help="Set cell_3", nargs=3)
parser.add_option(      "--c1+",              action="store",       type="float", help="Extend cell 1 by scalar")
parser.add_option(      "--c2+",              action="store",       type="float", help="Extend cell 2 by scalar")
parser.add_option(      "--c3+",              action="store",       type="float", help="Extend cell 3 by scalar")
parser.add_option(      "--c1*",              action="store",       type="float", help="Multiply cell 1 by scalar")
parser.add_option(      "--c2*",              action="store",       type="float", help="Multiply cell 2 by scalar")
parser.add_option(      "--c3*",              action="store",       type="float", help="Multiply cell 3 by scalar")
parser.add_option(      "--c1+v",             action="store",       type="float", help="Add to cell 1 a vector", nargs=3)
parser.add_option(      "--c2+v",             action="store",       type="float", help="Add to cell 2 a vector", nargs=3)
parser.add_option(      "--c3+v",             action="store",       type="float", help="Add to cell 3 a vector", nargs=3)
parser.add_option(      "--c1r",              action="store",       type="float", help="Rotate cell 1")
parser.add_option(      "--c2r",              action="store",       type="float", help="Rotate cell 2")
parser.add_option(      "--c3r",              action="store",       type="float", help="Rotate cell 3")


parser.add_option(      "--cutX",              action="store",       type="float", help="Cut X")
parser.add_option(      "--cutY",              action="store",       type="float", help="Cut Y")
parser.add_option(      "--cutZ",              action="store",       type="float", help="Cut Z")
#parser.add_option(      "--cellSet",       action="store",       type="string", help="Vector of Cell_2", nargs=3)
#parser.add_option(      "--cell_3_set",       action="store",       type="string", help="Vector of Cell_3", nargs=3)
parser.add_option("-p", "--period",           action="store",        type="int",    help="simension of repeation", nargs=3)
parser.add_option(      "--copy",             action="store",        type="float",  help="Angle  of rotation", nargs=3)

parser.add_option(      "--comment",          action="store",        type="string", help="his file was created by ase.convert.py script",     default='z')
parser.add_option(      "--vaspold",          action="store_false",                 help="comment line",     default=True)
parser.add_option(      "--vaspdirect",       action="store_true",                  help="comment line",     default=False)
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

    if(  options.copy != None ):
        c                          = options.copy
        is_translation_nonzero     = (c != (0.0,0.0,0.0))
        is_there_any_atoms_to_copy = (trange[1]-trange[0] >= 0)
        if( is_translation_nonzero and is_there_any_atoms_to_copy ):
            symbols   = atoms.get_chemical_symbols()
            positions = atoms.get_positions()
            for i in range(trange[0]-1, trange[1]):
                pos    = positions[i] + c
                symbol = symbols[i]
                atoms += Atom(symbol, pos)


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

    if(  options.c1 !=  None):  c[0] = options.c1
    if(  options.c2 !=  None):  c[1] = options.c2
    if(  options.c3 !=  None):  c[2] = options.c3

    # enlarging cell vectors by adding vectors
    c1 = options.__dict__['c1+v']
    c2 = options.__dict__['c2+v']
    c3 = options.__dict__['c3+v']
    if( c1 != None ):   c[0] = np.add(c[0], c1)
    if( c2 != None ):   c[1] = np.add(c[1], c2)
    if( c3 != None ):   c[2] = np.add(c[2], c3)

    # enlarging cell vectors by scalar
    c1 = options.__dict__['c1+']
    c2 = options.__dict__['c2+']
    c3 = options.__dict__['c3+']
    if( c1 != None ):
        norm   = np.linalg.norm(c[0])
        factor = (norm+c1)/norm
        c[0]   = np.multiply(c[0], factor)
    if( c2 != None ):
        norm   = np.linalg.norm(c[1])
        factor = (norm+c2)/norm
        c[1]   = np.multiply(c[1], factor)
    if( c3 != None ):
        norm   = np.linalg.norm(c[2])
        factor = (norm+c3)/norm
        c[2]   = np.multiply(c[2], factor)

    c1 = options.__dict__['c1*']
    c2 = options.__dict__['c2*']
    c3 = options.__dict__['c3*']
    if( c1 != None ):   c[0] = np.multiply(c[0], c1)
    if( c2 != None ):   c[1] = np.multiply(c[1], c2)
    if( c3 != None ):   c[2] = np.multiply(c[2], c3)



    # enlarging cell vectors rotation
    c1 = options.__dict__['c1r']
    c2 = options.__dict__['c2r']
    c3 = options.__dict__['c3r']
    if( c1 != None ): c[0] = asekk.rotate(c[0], c1, axis=options.__dict__['rotate_axis'])
    if( c2 != None ): c[1] = asekk.rotate(c[1], c2, axis=options.__dict__['rotate_axis'])
    if( c3 != None ): c[2] = asekk.rotate(c[2], c3, axis=options.__dict__['rotate_axis'])

    atoms.set_cell(c)

    if(  options.period != None ):
        is_periodic = all(atoms.get_pbc()) and atoms.get_cell().shape == (3, 3)
        if(not is_periodic):
            sys.exit("ERROR: Call for periodic extention of the system, but supercell or pbc flag setted wrongly.")
        dim = np.array( options.period)
        atoms.set_constraint() ### TODO!!!!!!!!!!!!  I can not awwoid cutting constraint. Check how to fix it
        atoms = atoms * dim


    if( options.wrap == True):
        atoms.wrap()



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
        write_vasp(ostream, atoms, label=options.comment, direct=options.vaspdirect,sort=options.vaspsort,vasp5=options.vaspold)
    if(oformat == "xyz"):
        c   = atoms.get_cell()
        pbc = atoms.get_pbc()
        fname = "answer.lvs"
        if(os.path.isfile(fname)):
            fname += ".new"
        if( c != None and pbc.all()):
            f    = open(fname, "w")
            for i in range(3):
                f.write(str(c[i][0]) + '    '+ str(c[i][1]) + '    ' +  str(c[i][2]) + '\n')
        #write_xyz(ostream, atoms, comment=options.comment)
        write_xyz(ostream, [atoms], comment=options.comment)
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
