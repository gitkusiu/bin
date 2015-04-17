import numpy as np
from math import cos, sin, pi

#####################################
#
# rotate - rotate 'vector' around 'axis'
#          by angle 'alpha' in respect to 'origin' 
#
#######################################
def rotate(vector, alpha, axis='z', origin=[0.0,0.0,0.0]):
    a=(alpha*pi)/180.0
    o=np.array(origin)
    v=np.array(vector)
    v1=np.add(v,-o)
    matrix = []
    if(axis=='z'):
        matrix.append([ cos(a),-sin(a), 0.0   ])
        matrix.append([ sin(a), cos(a), 0.0   ])
        matrix.append([ 0.0   , 0.0   , 1.0   ])
    elif(axis=='x'):
        matrix.append([ 1.0   , 0.0   , 0.0   ])
        matrix.append([ 0.0   , cos(a),-sin(a)])
        matrix.append([ 0.0   , sin(a), cos(a)])
    elif(axis=='y'):
        matrix.append([ cos(a), 0.0   , sin(a)])
        matrix.append([ 0.0   , 1.0   , 0.0   ])
        matrix.append([-sin(a), 0.0   , cos(a)])
    m = np.array(matrix)
    v2=np.dot(m,v1)
    return np.add(o,v2)


#####################################
#
# rotate secected atoms
#
#######################################
def rotate_atoms(atoms, alpha, fromto=[-1,-1], axis='z', origin=[0.0,0.0,0.0]):
    p=atoms.arrays['positions']
    n=len(p)
    ifrom, ito  = 0,0
    if(fromto[0]==-1 and fromto[1]==-1):
        ifrom  = 1
        ito    = len(atoms)
    else:
        ifrom  = fromto[0]
        ito    = fromto[1]
    for i in range(ifrom-1,ito):
        p[i] = rotate(p[i],alpha,axis=axis,origin=origin)
#        p[i] = asekk.rotate(p[i],alpha,axis=axis,origin=origin)







#####################################
#
# print Atoms in bas format
#
#######################################
def write_bas(atoms):
    p=atoms.arrays['positions']
    print("position")

