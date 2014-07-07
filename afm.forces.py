#!/usr/bin/python
from os.path    import isdir
from os         import listdir
from re         import search
from numpy      import zeros
from subprocess import check_output

######## get all directory with a names such as 1.00, 2.23 ... etc
list =  listdir("./")
z = [f for f in list if(isdir(f) and search(r'\d[.]\d\d$', f))]
z.sort()

######## read TOTENs from corresponding OUTCARS
Etot = []
for dir in z:
    outcar = dir+"/OUTCAR"
    cmd    = "vasp.OUTCAR.py --get energy "+outcar
    out   =  check_output(cmd, shell=True)
    Etot.append(float(out))

######### calculate F_z = -dE_tot/dz
Fz = zeros(len(z))
for i in range(1,len(z)-1):
    dz    = float(z[i+1]) - float(z[i-1])
    dEtot = Etot[i+1]-Etot[i-1]
    Fz[i] = -(dEtot/dz)

for i in range(1,len(z)-1):
    print z[i], "\t", Fz[i]
