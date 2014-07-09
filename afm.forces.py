#!/usr/bin/python
from os.path    import isdir
from os         import listdir
from re         import search
from subprocess import Popen
from subprocess import PIPE
#from subprocess import check_output
 

######## get all directory with a names such as 1.00, 2.23 ... etc
list =  listdir("./")
dirs = [f for f in list if(isdir(f) and search(r'\d[.]\d\d$', f))]
dirs.sort()


######## read TOTENs from corresponding OUTCARS
E = []
for d in dirs:
    cmd = "vasp.OUTCAR.py --get energy "+d+"/OUTCAR"
#    out = check_output(cmd, shell=True)
    out, err = Popen( cmd, stdout=PIPE, shell=True ).communicate()
    E.append(float(out))


######## calculate F_z = -dE_tot/dz
z = [float(d) for d in dirs]
Fz = [None]
for i in range(1,len(z)-1):
    dz    = z[i+1] - z[i-1]
    dEtot = E[i+1] - E[i-1]
    Fz.append(-dEtot/dz)


####### plot Fz vs z ############
for i in range(1,len(z)-1):
    #TODO: try to format an output
    print z[i], "\t", Fz[i]
