#!/usr/bin/python

import sys
import numpy as np 

from ase.io.vasp import read_vasp
from ase.io.vasp import write_vasp
from ase.io.xyz import write_xyz

from ase.calculators.vasp import VaspDos

from optparse import OptionParser

def get_total_site_dos(doscar, atom):

    n_of_orb = len(doscar._site_dos[atom]) - 1

    dos = doscar.site_dos(atom,0)
    for i in range(1,n_of_orb):
        dos = dos + doscar.site_dos(atom,i)
    return dos

def get_site_dos(doscar, atom, l=-1):

    n        = len(doscar._site_dos)
    n_of_orb = len(doscar._site_dos[atom])-1

    dos = [0.0]*n
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
    elif(l == -1):
        dos = doscar.site_dos(atom,0)
        for i in range(1,n_of_orb):
            dos = dos + doscar.site_dos(atom,i)
        return dos
    else:
        print "Error"

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
parser.add_option("-f", "--format",           action="store", type="string", default="POSCAR",      help="format of the output file: POSCAR, (xyz in preparation)")
parser.add_option("-a", "--atoms",            action="store", type="int",    default=[-1,-1],       help="specify the atoms to whcih changes (translation rotation etc. will be made)", nargs=2)
parser.add_option("-p", "--periods",          action="store", type="int",    default=[1,1,1],       help="repetition of the unit cell", nargs=3)
parser.add_option("-T", "--Translation",      action="store", type="float",  default=[0.0,0.0,0.0], help="ss", nargs=3)
parser.add_option("-u", "--cell_scale",       action="store", type="float",  default=[1.0,1.0,1.0],           help="unit cell scalling factor", nargs=3)
parser.add_option("-c", "--comment",          action="store", type="string", default=" ")
(options, args) = parser.parse_args()

num = len(sys.argv)

doscar=VaspDos("DOSCAR")


n = len(doscar._site_dos)

#print len(doscar._site_dos[0])

e   = doscar._get_energy()


#### total DOS as a summ over sites DOS'es
dos_summ_of_sites = get_total_site_dos(doscar, 0)
for j in range(1,n):
    dos_summ_of_sites = dos_summ_of_sites + get_total_site_dos(doscar, j)


#### site total DOSes 
dos_on_sites = []
for j in range(n):
    dos_on_sites.append(get_site_dos(doscar, j))


#### total DOS 
dos_ud = doscar._get_dos()
dos = dos_ud[0] + dos_ud[1]

for i in range(len(e)):
    print e[i],
    for j in range(n):
        print dos_on_sites[j][i],
    print ""
#    print dos_summ_of_sites[i], dos[i]



