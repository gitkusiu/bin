#!/usr/bin/python



import sys
import ase.io.vasp
import ase.io.xyz
import ase.io.pov
from math import pi
from math import acos
import copy



import numpy as np
def find_index_of_nearest(array,value):
    norms = []
    for i in range(len(array)):
        lnorm = np.linalg.norm(array[i]-value)
        norms.append(lnorm)
    return np.array(norms).argmin()

def find_index(array,value):
    for i in range(len(array)):
        if((array[i] == value).all()):
            return i
    return -1


###############################################
#    function which check if atoms set A is a
#    subset of B
###############################################
def does_A_belong_to_B(A,B):
    eps = 0.001
    out = True
    AZ   = A.get_atomic_numbers()
    BZ   = B.get_atomic_numbers()
    Apos = A.positions
    Bpos = B.positions
    for Ar in Apos:
        Bi = find_index_of_nearest(Bpos,Ar)
        Ai = find_index(Apos,Ar)
        Br = Bpos[Bi]

        normAB           = np.linalg.norm(Br - Ar)
        theSamePos       = (Apos[Ai] == Ar).all()
        theSameAtomicNr  = (AZ[Ai]   == BZ[Bi]).all()

        is_A_theSameAs_B = (normAB < eps) and theSamePos and  theSameAtomicNr

        if( not is_A_theSameAs_B):
            out = False
            break
    return out


###############################################
#    function which check if atoms set A is a
#    subset of B
###############################################
def get_r_diff(A,B):
    eps = 0.001
    diff = 0.0
    AZ   = A.get_atomic_numbers()
    BZ   = B.get_atomic_numbers()
    Apos = A.positions
    Bpos = B.positions
    for Ar in Apos:
        Bi = find_index_of_nearest(Bpos,Ar)
#        Ai = find_index(Apos,Ar)
        Br = Bpos[Bi]
        diff = diff + np.linalg.norm(Br - Ar)

    return diff



###############################################
#    function which return array of z values 
#    without repetitions
###############################################
def get_array_of_z_positions(positions):
    eps = 0.0001
    z = []
    z.append(positions[0][2])
    for r in positions:
        for z_tmp in z:
            dz = abs(r[2]- z_tmp)
            r_is_in_z = dz < eps
            if(r_is_in_z):
                break
            elif(z_tmp == z[len(z)-1]):
                z.append(r[2])
    return z



def invert(atoms,ic):
    atoms.arrays['positions'] *= -1.0
    atoms.translate(np.array(ic)*2)




###################################################################################################
###################################################################################################
n = 1
m = 1

if( len(sys.argv) >= 3):
    n =  int(sys.argv[1])
    m =  int(sys.argv[2])


from ase.structure import TMDnanotube
from ase.structure import nanotube
#swnt_org = nanotube(11, 0, length=1,a0=3.44, TMsymbol='C', CHsymbol='C', d=0.0)
#swnt_org = nanotube(n, m, length=1,a0=2.5, TMsymbol='B', CHsymbol='N', d=0.0,center=False)
#swnt_org = nanotube(n, m, center=False)
swnt_org = TMDnanotube(n, m,center=False)
#swnt_org = nanotube(n, m)
swnt = copy.deepcopy(swnt_org)


ase.io.xyz.write_xyz('system.xyz', swnt)

swnt_1x1x3 = (copy.deepcopy(swnt))*(1,1,5)

c2 = swnt.get_cell()[2]
swnt_1x1x3.translate(-2.0*c2)
ase.io.xyz.write_xyz('system_1x1x3.xyz', swnt_1x1x3)

#print does_A_belong_to_B(swnt,swnt_1x1x3)


ic_zs = get_array_of_z_positions(swnt.positions)
ic_zs.sort()


a = 0.0
b = c2[2]
l = b-a
n = 333

ic_zs = [a+(l/n)*z for z in range(n)]

#print ic_zs



#print  does_A_belong_to_B(swnt,swnt_1x1x3)

tmp0 = copy.deepcopy(swnt)
invert(tmp0,(0.0, 0.0, 2.48260615752))
ase.io.xyz.write_xyz('system_inverted.xyz', tmp0)


#swnt_1x1x3.bis = swnt_1x1x3

#for ic_z in ic_zs:
for i in range(len(ic_zs)-1):
    ic_z = ic_zs[i]
    tmp0 = copy.deepcopy(swnt)
    invert(tmp0,(0.0, 0.0, ic_z))
    #print ic_z, does_A_belong_to_B(tmp0,swnt_1x1x3) 
#    print "KK1"
    print ic_z, get_r_diff(tmp0,swnt_1x1x3)
    ic_z = 0.5*(ic_zs[i+1] + ic_zs[i])
    tmp0 = copy.deepcopy(swnt)
    invert(tmp0,(0.0, 0.0, ic_z))
    #print ic_z, does_A_belong_to_B(tmp0,swnt_1x1x3)
#    print "KK2"
    print ic_z, get_r_diff(tmp0,swnt_1x1x3)


ic_z = ic_zs[len(ic_zs)-1]
tmp0 = copy.deepcopy(swnt)
invert(tmp0,(0.0, 0.0, ic_z))
#print ic_z, does_A_belong_to_B(tmp0,swnt_1x1x3)
print ic_z, get_r_diff(tmp0,swnt_1x1x3)





ase.io.xyz.write_xyz('system.invert.xyz', swnt)


ase.io.vasp.write_vasp("POSCAR",swnt,label="CNT4",direct=False,sort=True, vasp5=True)

#ase.io.xyz.write_xyz('system.xyz', swnt)
    



