#!/usr/bin/python


#TODO this is supposed to be a quite large converter scirpt 
# ase.convert.py -i inport_format -o output_format
import sys
import os.path

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

parser = OptionParser()
parser.add_option("-i", "--input",    action="store",       type="string", help="input file format")
parser.add_option("-o", "--output",   action="store",       type="string", help="output file format")
parser.add_option(      "--comment",  action="store",       type="string", help="comment line",     default="this file was created by ase.convert.py script")
parser.add_option(      "--vaspold",  action="store_false",                help="comment line",     default=True)
parser.add_option(      "--vaspsort", action="store_true",                 help="comment line",     default=False)
parser.add_option(      "--xyzcell",  action="store",       type="string", help="file of xyz cell", default=xyzCellFile)
(options, args) = parser.parse_args()

iformat = options.input
if(options.output != None): # default output format
    oformat = options.output
else:
    oformat = options.input
ostream = sys.stdout

atoms=[]
field=[]

if(num < 2):
    parser.print_help()
else:

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

    elif(iformat == "cube"):
        cube = read_cube(sys.argv[num-1],read_data=True)
        atoms = cube[1]
        field = cube[0]
        print atoms.get_cell()
        print len(field), len(field[0]), len(field[0][0])




    if(oformat == "geometry.in"):
        tmpname="geometry.in.tmp"
        write_aims(tmpname, atoms)
        f = open(tmpname, 'r')
        print f.read()
        f.close()
        os.remove(tmpname)
#        write_aims("geometry.in", atoms)
#    elif(oformat == "cube"):
#        write_cube(`,xsf[1],xsf[0])
#    elif(oformat == "xsf"):
#        write_xsf(sys.stdout,xsf[1],xsf[0])

    elif(oformat == "POSCAR"):
        write_vasp(ostream, atoms, label=options.comment, direct=False,sort=options.vaspsort,vasp5=options.vaspold)

    if(oformat == "xyz"):
        write_xyz(ostream, atoms)

    if(oformat == "xsf"):
        write_xsf(sys.stdout,atoms,field)

##write_cube("tmp.cube",xsf[1],xsf[0])
