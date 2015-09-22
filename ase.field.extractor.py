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

num = len(sys.argv)
ifile = sys.argv[num-1]
xyzCellFile = os.path.splitext(ifile)[0]+".lvs"

bohr2ang=0.529177249

parser = OptionParser()
parser.add_option("-i", "--input",    action="store",       type="string", help="input file format")
parser.add_option("-o", "--output",   action="store",       type="string", help="output file format")
parser.add_option("-g", "--get",      action="store",       type="string", help="Type of data we want to get")
parser.add_option(      "--average",  action="store",       type="string", help="Calculate derrivative allong x y or z direction")
parser.add_option(      "--profileX", action="store",       type="float", help="Calculate derrivative allong x y or z direction", nargs=2)
parser.add_option(      "--profileY", action="store",       type="float", help="Calculate derrivative allong x y or z direction", nargs=2)
parser.add_option(      "--profileZ", action="store",       type="float", help="Calculate derrivative allong x y or z direction", nargs=2)
parser.add_option(      "--max",     action="store_true",                 help="Calculate difference between field 1 and field 2")
parser.add_option(      "--min",     action="store_true",                 help="Calculate difference between field 1 and field 2")
parser.add_option(      "--comment",  action="store",       type="string", help="comment line",     default="this file was created by ase.convert.py script")
(options, args) = parser.parse_args()

iformat = options.input
if(options.output != None): # default output format
    oformat = options.output
else:
    oformat = options.input
ostream = sys.stdout

atoms=[]
field=[]

atoms2=[]
field2=[]

if(num < 2):
    parser.print_help()
else:


    
    opt_av  = options.average
    opt_min = options.min
    opt_max = options.max

    vol_orgin = [0.0,0.0,0.0]
####### READING THE FILE #############
    if(iformat == "cube"):
        field,  atoms  = read_cube(sys.argv[num-1],read_data=True)
        f = open(sys.argv[num-1], 'r')
        f.readline()
        f.readline()
        vol_orgin = np.array(f.readline().split()[1:4]).astype(float)
        vol_orgin *= bohr2ang


    cell  = np.array(atoms.get_cell())
    shape = np.array(field.shape)
    dr    = np.empty(3)            # gradation of unit cell
    for i in range(3):
        tmp = np.array(shape)
        if(tmp[i] % 2 == 1): tmp[i] +=  1
        dcell = cell[i]/tmp[i]
        dr[i] = np.linalg.norm(dcell)
    l = shape*dr

    cell_mesh = np.array( [ np.arange(0.0,l[0],dr[0]),\
                            np.arange(0.0,l[1],dr[1]),\
                            np.arange(0.0,l[2],dr[2]) ] )

####### MANIPULATE #############
    # Calculate average along direxction x,y,or z
    if( opt_av != None ):
        if  ( opt_av == "x" ):
            r = np.arange(0.0,l[0],dr[0])
            for i in range(shape[0]): print r[i], np.average(field[i,:,:])
        if  ( opt_av == "y" ):
            r = np.arange(0.0,l[1],dr[1])
            for i in range(shape[1]): print r[i], np.average(field[:,i,:])
        elif( opt_av == "z" ):
            r = np.arange(0.0,l[2],dr[2])
            for i in range(shape[2]): print r[i], np.average(field[:,:,i])


    opt_profx  = options.profileX
    opt_profy  = options.profileY
    opt_profz  = options.profileZ

    if( opt_profx != None or opt_profy != None or opt_profz != None ):

        lvs = cell

        vol = lvs[0][0] * ( lvs[1][1]*lvs[2][2]-lvs[1][2]*lvs[2][1] ) +\
              lvs[0][1] * ( lvs[1][2]*lvs[2][0]-lvs[1][0]*lvs[2][2] ) +\
              lvs[0][2] * ( lvs[1][0]*lvs[2][1]-lvs[1][1]*lvs[2][0] )

        ax = ( lvs[1][1]*lvs[2][2] - lvs[1][2]*lvs[2][1] ) / vol
        ay = ( lvs[1][2]*lvs[2][0] - lvs[1][0]*lvs[2][2] ) / vol
        az = ( lvs[1][0]*lvs[2][1] - lvs[1][1]*lvs[2][0] ) / vol
        a = np.array([ax,ay,az])

        bx = ( lvs[2][1]*lvs[0][2] - lvs[2][2]*lvs[0][1] ) / vol
        by = ( lvs[2][2]*lvs[0][0] - lvs[2][0]*lvs[0][2] ) / vol
        bz = ( lvs[2][0]*lvs[0][1] - lvs[2][1]*lvs[0][0] ) / vol
        b = np.array([bx,by,bz])

        cx = ( lvs[0][1]*lvs[1][2] - lvs[0][2]*lvs[1][1] ) / vol
        cy = ( lvs[0][2]*lvs[1][0] - lvs[0][0]*lvs[1][2] ) / vol
        cz = ( lvs[0][0]*lvs[1][1] - lvs[0][1]*lvs[1][0] ) / vol
        c = np.array([cx,cy,cz])

        if( opt_profx != None ):
            for i in range(shape[0]): print cell_mesh[0][i], field[i,  ny, nz  ]
        if( opt_profy != None ):
            for i in range(shape[2]): print cell_mesh[1][i], field[nx, i,  nz  ]
        if( opt_profz != None ):
            r  = np.array([opt_profz[0], opt_profz[1], 1.0] )
            r  = r-vol_orgin
            r2 = np.array([ a.dot(r), b.dot(r), c.dot(r) ])

            nx = int(r2[0]*shape[0])
            ny = int(r2[1]*shape[1])
            nz = int(r2[2]*shape[2])
            for i in range(shape[2]): print cell_mesh[2][i] + vol_orgin[2], field[nx, ny, i   ]

#            print nx,ny,nz
#            print shape
#            print vol_orgin


