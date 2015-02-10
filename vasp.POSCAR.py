#!/usr/bin/python

import sys

from ase.io.vasp import read_vasp
from ase.io.vasp import write_vasp
from ase.io.xyz import write_xyz
from ase import Atoms

from math import pi

from ase.constraints import FixAtoms


from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--format",           action="store", type="string", default="POSCAR",      help="format of the output file: POSCAR, (xyz in preparation)")
parser.add_option("-a", "--atoms",            action="store", type="int",    default=[-1,-1],       help="specify the atoms to whcih changes (translation rotation etc. will be made)", nargs=2)
parser.add_option("-p", "--periods",          action="store", type="int",    default=[1,1,1],       help="repetition of the unit cell", nargs=3)
parser.add_option("-T", "--Translation",      action="store", type="float",  default=[0.0,0.0,0.0], help="ss", nargs=3)
parser.add_option("-r", "--rotation_angle",   action="store", type="float",  default=0.0,           help="rotation angle", nargs=1)
parser.add_option(      "--rotate_around",    action="store", type="int",    default=0, help="rotate around nth atom", nargs=1)
#parser.add_option(      "--rotation_vector",  action="store", type="float",  default=[0.0,0.0,0.0], help="rotation point", nargs=1)
parser.add_option("-u", "--cell_scale",       action="store", type="float",  default=[1.0,1.0,1.0],           help="unit cell scalling factor", nargs=3)
parser.add_option("-c", "--comment",          action="store", type="string", default=" ")
(options, args) = parser.parse_args()

#print parser.parse_args()

num = len(sys.argv)


if(num < 2):
    parser.print_help()
else:
    poscar = read_vasp(sys.argv[num-1])

    a = options.atoms # do not use/modify options.atoms
    natoms = poscar.get_number_of_atoms()
    if( a[0] > natoms or a[1] > natoms ):
        print "ERROR: a[0] > natoms | a[0] > natoms"
        exit()

    # atoms selection for modyfiactions
    if(a[0] == -1): # deafult case: we change all atoms
        a = (1, natoms)


    # --------------- Translations -----------------
    t = options.Translation
    is_translation_nonzero          = (t != (0.0,0.0,0.0))
    is_there_any_atoms_to_translate = (a[1]-a[0] >= 0)
    if( is_translation_nonzero and is_there_any_atoms_to_translate ):
        for i in range(a[0]-1, a[1]):
            poscar.arrays['positions'][i] +=  t


    # --------------- Rotation -----------------
    alpha  = options.rotation_angle
#    v      = options.rotation_vector

    if(alpha != 0.0):
        l_positions = poscar.get_positions()
        l_numbers   = poscar.get_atomic_numbers()
        l_cell      = poscar.get_cell()
        l_from      = a[0]-1
        l_to        = a[1]-1

        constr = poscar._get_constraints()

        l_sur1_pos            = l_positions[0      : l_from]
        l_tip_pos             = l_positions[l_from : l_to+1]
        l_sur2_pos            = l_positions[l_to+1 : natoms]

        l_sur1_atomic_numbers = l_numbers[0      : l_from]
        l_tip_atomic_numbers  = l_numbers[l_from : l_to+1]
        l_sur2_atomic_numbers = l_numbers[l_to+1 : natoms]

        l_center  = l_positions[options.rotate_around-1]

        sur2 = Atoms(positions=l_sur2_pos, numbers=l_sur2_atomic_numbers, cell=l_cell, pbc = True)
        sur1 = Atoms(positions=l_sur1_pos, numbers=l_sur1_atomic_numbers, cell=l_cell, pbc = True)
        tip  = Atoms(positions=l_tip_pos,  numbers=l_tip_atomic_numbers, cell=l_cell, pbc = True)

#        c = tip.get_cell()
#        tip.set_cell(c*(2,2,0))
#        tip.rotate(v='y',a=(alpha/180.)*pi, center=l_center,rotate_cell=True)
        tip.rotate(v='z',a=(alpha/180.)*pi, center=l_center,rotate_cell=True)
        tip.set_cell(poscar.get_cell())

        poscar = sur1+tip+sur2
        poscar.set_constraint(constr)


    # --------------- unit cell scaling facto -----------------
    u = options.cell_scale
    if( u != [1.0, 1.0, 1.0] ):
        cell = poscar.get_cell()
        poscar.set_cell(cell*u)

    # --------------- Periodic repetitions -----------------
    p = options.periods
    if( p != [1,1,1]):
        poscar = poscar*(p[0], p[1], p[2])
#        print p


    # --------------- Wirting out in proper format -----------------
    if(options.format == "POSCAR"):
        write_vasp(sys.stdout,poscar,label=options.comment, direct=False,sort=False,vasp5=True)
    elif(options.format == "xyz"):
        write_xyz(sys.stdout,poscar,options.comment)
