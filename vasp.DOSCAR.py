#!/usr/bin/python

import sys
#import numpy as np 

from ase.io.vasp import read_vasp
from ase.io.vasp import write_vasp
from ase.io.xyz import write_xyz

from ase.calculators.vasp import VaspDos

from optparse import OptionParser

import copy


####################################################
#
# function get_total_site_dos(doscar, atom):
#
#          extract a teble of total DOS sum over all 
#          orbitals
#
####################################################
def get_total_site_dos(doscar, atom):

    n_of_orb = len(doscar._site_dos[atom]) - 1

    dos = doscar.site_dos(atom,0)
    for i in range(1,n_of_orb):
        dos = dos + doscar.site_dos(atom,i)
    return dos

####################################################
#
# function get_site_dos(doscar, atom, l=-1) :
#
#          extract a teble of DOS of an orbital 'l' 
#          located on particular atom
#
####################################################
def get_site_dos_table(doscar, atom, l=-1):

#    atom = atom-1
    n        = len(doscar._site_dos)
    n_of_orb = len(doscar._site_dos[atom-1])-1
    n_dos    = len(doscar._site_dos[atom-1][0])

    dos = [0.0]*n_dos
    if(n_of_orb >= l and 0 <= l  ):
        if(l==0):
            for i in [0,1]:
                dos = dos + doscar.site_dos(atom,i)
        elif(l==1):
            for i in [2,3,4,5,6,7]:
                dos = dos + doscar.site_dos(atom,i)
        elif(l==2):
            for i in [8,9,10,11,12,13,14,15,16,17]:
                dos = dos + doscar.site_dos(atom,i)
        elif(l==3):
            for i in [8,9,10,11,12,13,14,15,16,17]:
                dos = dos + doscar.site_dos(atom,i)
    elif(l == -1):
        dos = copy.deepcopy(doscar.site_dos(atom-1,0))
#        print "KK",n, n_of_orb, 
        for i in range(1,n_of_orb):
#            print i
            dos = dos + doscar.site_dos(atom-1,i)
        return dos
    else:
        print "Error"



def get_l(number_of_orbitals, spin):
    n = number_of_orbitals
    if(spin):
        n = n/2
    if(n == 1):
        return 0
    elif(n == 4):
        return 1
    elif(n == 9):
        return 2
    elif(n == 18):
        return 3
    else:
        print "ERROR: Unknown number of orbitals"


#def get_site_dos(n, doscar, orbital):
#    
#    if(orbital.lower() == "s"):
#        s_u = doscar.site_dos(n,1)
#        s_d = doscar.site_dos(n,2)
#        return s_u + s_d

#    if(orbital.lower() == "p"):
#        p = doscar.site_dos(n,3)
#        for i in range(4,9):   
#            p = p + doscar.site_dos(n,i)
#        return p

#    if(orbital.lower() == "d"):
#        d = doscar.site_dos(n,9)
#        for i in range(10,19):
#            d = d + doscar.site_dos(n,i)
#        return d

#    if(orbital.lower() == "f"):
#        f = doscar.site_dos(n,19)
#        for i in range(20,33):
#            f = f + doscar.site_dos(n,i)
#        return f


parser = OptionParser()
parser.add_option("-g", "--get",              action="store",       type="string", default="total_dos",     help="what kind of DOS data do you what to print: site_dos (default) - print, total_dos - ")
parser.add_option("-s", "--spin",             action="store",       type="string", default="+-",      help="Fermi level ")
parser.add_option(      "--ferm",             action="store",       type="float",  default="0.0",          help="If this value is given. Ferme level is shifted to 0.0")
parser.add_option(      "--per_atom",         action="store_false",                default=False,          help="If DOS should be devided by number of atoms")
parser.add_option("-a", "--atoms",            action="store", type="int",    default=[-1,-1],        help="specify atoms for which atoms will be printed", nargs=2)
parser.add_option("-o", "--orbital",         action="store",  type="string",    default="all",            help="specify orbitals for which atoms will be printed", nargs=1)
(options, args) = parser.parse_args()

num = len(sys.argv)

if(num < 2):
    parser.print_help()
else:
    doscar=VaspDos(sys.argv[num-1])

    # get number of atoms
    dos_size = len(doscar._site_dos[0][0])
    number_of_atoms = len(doscar._site_dos)
    energy   = doscar._get_energy()

    if(dos_size != len(energy)):
        print "Error: The DOS array size (",dos_size,") is difrent than the energy array size (", len(energy) ,")"

    # atoms seting
    a = []
    if(options.atoms[0] == -1 and options.atoms[1] == -1):
        a = [1, number_of_atoms]
    else:
        a = options.atoms
        options.get = "site_dos"
#    o = options.orbital
    dos = [0.0]*len(energy)
    doses = []
    sign = 1.0
    
    if options.spin == "-" : sign = -1.0
    if  options.get == "total_dos" :
        dos_ud = doscar._get_dos()
        if   options.spin == "+-" : dos = dos_ud[0]+dos_ud[1]
        elif options.spin == "+"  : dos = dos_ud[0]
        elif options.spin == "-"  : dos = dos_ud[1]
    elif options.get == "site_dos" :
        s_up   = ["s+"]
        p_up   = ["py+",  "pz+",  "px+"]
        d_up   = ["dxy+", "dyz+", "dz2+", "dxz+", "dxz+"]
        f_up   = ["f-3+", "f-2+", "f-1+", "f0+",  "f1+",  "f2+",  "f3+"]
        all_up = s_up + p_up + d_up + f_up
        s_down = ["s-"]
        p_down = ["py-",  "pz-",  "px-"]
        d_down = ["dxy-", "dyz-", "dz2-", "dxz-", "dxz-"]
        f_down = ["f-3-", "f-2-", "f-1-", "f0-",  "f1-",  "f2-",  "f3-"]
        all_down = s_down + p_down + d_down + f_down
        o = options.orbital
        orbitals = []
        if  options.spin == "+-":
            if   o == 's'  : orbitals = s_up + s_down
            elif o == 'p'  : orbitals = p_up + p_down
            elif o == 'd'  : orbitals = d_up + d_down
            elif o == 'f'  : orbitals = f_up + f_down
            elif o == 'all': orbitals = all_up + all_down
            else           : orbitals = [o]
        elif options.spin == "+":
            if   o == 's'  : orbitals = s_up
            elif o == 'p'  : orbitals = p_up
            elif o == 'd'  : orbitals = d_up
            elif o == 'f'  : orbitals = f_up
            elif o == 'all': orbitals = all_up
            else           : orbitals = [o]
        elif options.spin == "-":
            if   o == 's'  : orbitals = s_down
            elif o == 'p'  : orbitals = p_down
            elif o == 'd'  : orbitals = d_down
            elif o == 'f'  : orbitals = f_down
            elif o == 'all': orbitals = all_down
            else           : orbitals = [o]
#        print range(a[0], a[1]+1)
        for orbit in orbitals:
            for i in range(a[0]-1, a[1]):
                dos = dos + doscar.site_dos(i,orbit)

    for i in range(len(energy)):
        l_en  = energy[i]-options.ferm
        l_dos = dos[i]
        if(options.per_atom == "True"):
            l_dos = l_dos/float(a[1]-a[0]+1)

#        print l_en,l_dos
        print l_en, sign*dos[i]




