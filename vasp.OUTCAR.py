#!/usr/bin/python

import sys
import numpy as np 
import re
import os

from ase.io.vasp import read_vasp_out
from ase.io.xyz import write_xyz

from optparse import OptionParser


parser = OptionParser()
parser.add_option("--forces"   , action="store_true")
#parser.add_option("--afm_forces"   , action="store_true")
parser.add_option("--xyz",  action="store_true")

#parser.add_option("-afm",   "--afm_forces", action="store", type="string")
parser.add_option("-s",     "--steps",      action="store", type="string")
parser.add_option("-a",     "--atoms",      action="store", type="string")
parser.add_option("-r",     "--repeat",     action="store", type="string")
(options, args) = parser.parse_args()

num = len(sys.argv)


if(num < 2):
    parser.print_help()
else:
    outcar = read_vasp_out(sys.argv[num-1], slice(1,None,1))
    n = len(outcar)

# --------------- step index range ------------------------
    if(options.steps != None):
        steps = map(int, re.findall(r'\d+', options.steps) )
        no_steps = len(steps)
        if(no_steps > 0 & no_steps < 3):
            if( no_steps == 2 ):
                ni = int(steps[0])
                nf = int(steps[1])
            elif( no_steps == 1 & int(steps[0]) > 0 ):
                ni = 1
                nf = int(steps[0])
        else:
            ni = 1
            nf = n
    else:
        ni = 1
        nf = n


# --------------- atoms index range ------------------------
    natoms = outcar[0].get_number_of_atoms()
#    print natoms
    if(options.atoms != None):
        i_atoms = map(int, re.findall(r'\d+', options.atoms) )
        i_atoms_len = len(i_atoms)
        if(i_atoms_len > 0 & i_atoms_len < 3):
            if( i_atoms_len == 2 ):
                ai = int(i_atoms[0])
                af = int(i_atoms[1])
            elif( i_atoms_len == 1 & int(i_atoms[0]) > 0 ):
                ai = 1
                af = int(i_atoms[0])
        else:
            ai = 1
            af = natoms
    else:
        ai = 1
        af = natoms



# --------------- nit cell repetition ------------------------
    if(options.repeat != None):
        net      = map(int, re.findall(r'\d+', options.repeat) )
    else:
        net = [1,1,1]

#    print n, ni, nf
#    print net

    filenamexyz = 'outcar_steps.'+str(ni)+'-'+str(nf)+'_atoms.'+str(ai)+'-'+str(af)+'.xyz'
    cat_outcar="cat outcar.xyz >> " + filenamexyz

    for i in range(ni,nf+1):
#        print i

        step_tmp = outcar[i-1]
        step = step_tmp*net

        if(options.xyz):
            comm = "step no. " + str(i) + " TOTEN = " + str(step_tmp.get_total_energy())
            write_xyz("outcar.xyz", step, comment=comm )
            os.system(cat_outcar);
            os.system("rm outcar.xyz");

#        if(options.afm_forces):
#            tip_force = [0.0,0.0,0.0]
#            for j in range(ai,af+1):
#                tip_force += forces[i]
#        #    print i, tip_force
#    print tip_force[0],tip_force[1],tip_force[2],

#    elif(options.acction == "forces"):
#        if(options.steps == None):
#            ni = 0
#            nf = n-1
#        else:
#            steps = map(int, re.findall(r'\d+', options.steps) )
#            print steps
#            if(len(steps) == 2):
#                ni = steps[0]
#                nf = steps[1]




#    for i in range(ni, nf+1):
#            print i

#narg = len(sys.argv)

#if( narg < 2 ):
#	print "You have passed " + str(narg-1) + " arguments to the script"
#	print "This script needs 2 parameters"
#	print "Scrips exits"
#	exit()

#arg1 = sys.argv[1]

#if( arg1 == "conv"):
#    print "Brawo.\n";
#elif(True):
#    print "Only single-digit numbers are allowed\n";
