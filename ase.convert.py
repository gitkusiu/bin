#!/usr/bin/python


#TODO this is supposed to be a quite large converter scirpt 
# ase.convert.py -i inport_format -o output_format
import sys
from ase.io.xsf  import read_xsf
from ase.io.cube import read_cube
from ase.io.aims import read_aims
from ase.io.vasp import read_vasp

from ase.io.xsf  import write_xsf
from ase.io.cube import write_cube
from ase.io.aims import write_aims
from ase.io.vasp import write_vasp



from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--input",    action="store",       type="string", help="input file format")
parser.add_option("-o", "--output",   action="store",       type="string", help="output file format")
parser.add_option(      "--comment",  action="store",       type="string", help="comment line", default="this file was created by ase.convert.py script")
parser.add_option(      "--vaspold",  action="store_false",                help="comment line", default=True)
parser.add_option(      "--vaspsort", action="store_true",                 help="comment line", default=False)
(options, args) = parser.parse_args()

iformat=options.input
oformat=options.output
num = len(sys.argv)

ostream = sys.stdout

atoms=[]

if(num < 2):
    parser.print_help()
else:
    if(iformat == "geometry.in"):
        atoms = read_aims(sys.argv[num-1])
#    elif(iformat == "cube"):
#        atoms = read_cube(sys.argv[num-1])
#    elif(iformat == "xsf"):
#        atoms = read_xsf(sys.argv[num-1],read_data=True)

    if(oformat == "geometry.in"):
        write_aims(ostream, atoms)
    elif(oformat == "POSCAR"):
        write_vasp(ostream, atoms, label=options.comment, direct=False,sort=options.vaspsort,vasp5=options.vaspold)

#    elif(oformat == "cube"):
#        write_cube(`,xsf[1],xsf[0])
#    elif(oformat == "xsf"):
#        write_xsf(sys.stdout,xsf[1],xsf[0])
##write_cube("tmp.cube",xsf[1],xsf[0])
