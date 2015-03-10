#!/usr/bin/python

import sys
from ase.io.xyz  import read_xyz
from ase.io.xyz  import write_xyz
from ase.io.aims import write_aims
from ase.io.aims import read_aims
from ase         import Atoms

import asekk

from math import pi

from optparse import OptionParser


parser = OptionParser()
#parser.add_option("-f", "--format",           action="store", type="string", default="xyz",      help="format of the output file: xyz")
parser.add_option("-a", "--atoms",            action="store", type="int",    default=[-1,-1],       help="specify atoms to whcih changes (translation rotation etc. will be made)", nargs=2)
parser.add_option("-s", "--steps",            action="store", type="int",    default=None,       help="specify steps ", nargs=2)
parser.add_option("-p", "--periods",          action="store", type="int",    default=[1,1,1],       help="repetition of the unit cell", nargs=3)
parser.add_option("-T", "--Translation",      action="store", type="float",  default=[0.0,0.0,0.0], help="ss", nargs=3)
parser.add_option("-r", "--rotation_angle",   action="store", type="float",  default=0.0,           help="rotation angle", nargs=1)
parser.add_option(      "--rotate_around",    action="store", type="int",    default=0,             help="rotate around nth atom", nargs=1)
parser.add_option(      "--axis",    action="store", type="string", default="z",           help="rotation axis", nargs=1)
parser.add_option("-c", "--cell",             action="store", type="string", default="answer.lvs",  help="format of the output file: xyz")
parser.add_option("-f", "--format",           action="store", type="string", default="xyz",         help="format of the output file: POSCAR, (xyz in preparation)")

(options, args) = parser.parse_args()

num = len(sys.argv)

print_debug = False

if(num < 2):
    parser.print_help()
else:

    file_xyz = read_xyz(sys.argv[num-1], slice(0,None,1))
    natoms = file_xyz[0].get_number_of_atoms()

    # --------------- Atoms -----------------
    a = options.atoms
    if(a == [-1,-1]): # deafult case: we change all atoms
        a = [1,natoms]
    a_from = a[0]
    a_to   = a[1]
    atoms_range_negative = (a_to-a_from < 0)
    is_range_out_of_natoms  = (a_from > natoms or a_to > natoms)
    if( a_from > natoms or a_to > natoms ):
        print "ERROR: Atoms range is out of [1,number_of_atoms]"
        print a
        exit()
    elif( atoms_range_negative ):
        print "ERROR: Atoms range is negative "
        print a
        exit()


    # --------------- Translation -----------------
    t = options.Translation
    is_translation_nonzero          = (t != [0.0,0.0,0.0])
    do_we_translate = is_translation_nonzero and (not atoms_range_negative)

    # --------------- Rotation -----------------
    alpha  = options.rotation_angle
    

    # --------------- Periodic repetitions -----------------
    p = options.periods
    if( p[0] <= 0 and p[1] <= 0 and p[2] <= 0 ):
        print "ERROR: At least one of period is not positive"
        exit()
    do_we_repeat = (p != [1,1,1])


    # --------------- Steps -------------------------------
    n_steps = len(file_xyz)
    is_there_any_step = (n_steps > 0)
    s = options.steps
    if(s == None):       # deafult case: all steps
        s = [1, n_steps]
    elif(s == (-1,-1)):  # last step
        s = [n_steps,n_steps]
    elif( s[0] > n_steps or s[1] > n_steps ):
        print "ERROR: Step range is larger than number of steps in OUTCAR"
        exit()
    elif( s[0] > s[1] ):
        print "ERROR: Max step is smaler that Min step"
        exit()
    ##############################
    #  loop over steps
    ##############################
    if(is_there_any_step):
        # step selection
        for i in range(s[0],s[1]+1):
            step = file_xyz[i-1]
#            print step
#            comm = "step no. " + str(i) + " TOTEN =
            comm = "I do not know how to obtain comment in ase.io.xyz.read_xyz()"

            # --- Translate ----
            if(do_we_translate):
                for i in range(a_from-1,a_to):
                    step.arrays['positions'][i] +=  t

             # --- Rotate ----
            if(alpha != 0.0):
                # set origin of rotation
                origin    = [0.0,0.0,0.0]
                ra   = options.rotate_around
                if(ra > 0 and ra <= natoms):
                    positions = step.arrays['positions']
                    origin    = positions[ra-1]
                # rotate selected atoms
                asekk.rotate_atoms(step, alpha, fromto=[a_from,a_to], axis=options.axis, origin=origin)

            # --- Repetytion  ----
            if(do_we_repeat):
                # read cell
                cell = [[],[],[]]
                f  = open(options.cell, "r")
                ls = f.read().splitlines()
                for i in range(3):
                    l = ls[i].split()
                    cell[i] = [float(l[0]), float(l[1]), float(l[2])]
                step.set_cell(cell)
                # multiply by periods
                step = step*p


            # ----- Write -----
            if(options.format == 'xyz'):
                write_xyz(sys.stdout,step,comment=comm)
            elif(options.format == 'aims'):
                write_aims("geometry.in",step)
