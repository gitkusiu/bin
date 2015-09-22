#!/usr/bin/python

######################################
#
#   Script which calculate average
#   efective potential basing on the
#   v_eff.dat file 
#
######################################
import sys
import numpy as np


from optparse import OptionParser
from numpy    import array
from numpy    import linalg
#from numpy    import 

parser = OptionParser()
parser.add_option("-f", "--fermi",  action="store", help="Set Ferme level and shift it to 0.0")
parser.add_option("--k_old",        action="store", help="Type of data we want to get"        , type="float", nargs=3, default=[0.,0.,0.] )
parser.add_option("-r","--range",        action="store", help="Range of engenvalues"        , type="int", nargs=2)
parser.add_option("-k",             action="store", help="Type of data we want to get"        , type="float", default=0.0)
parser.add_option("-n",             action="store", help="number of files"        , type="int", default=1)
(options, args) = parser.parse_args()

num = len(sys.argv)


lines = []
for i in range(options.n,0,-1):
    f  = open(sys.argv[num-i], "r")
    lines += f.read().splitlines()


# read: n - number od KS eigenvalues, index of laste eigenvalues bloc
n, index = 0, 0
fermi = 0.0
k     = array(options.k)
k_old = array(options.k_old)

for i, line in enumerate(lines):
    l = line.split()
    n = len(l)
    nbands = int((n-4)/2)


    k_new = array(l[1:4], dtype='f')
    dk    = linalg.norm(k_new-k_old)
    k += dk
    sys.stdout.write(str(k)+"    ")
    k_old = k_new

    r = options.range
    if(r == None):
        r = array([1,nbands])

    for j in range(r[0],r[1]+1):
        sys.stdout.write(l[3+j*2]+"    ")
    sys.stdout.write("\n")


