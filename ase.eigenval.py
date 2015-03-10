#!/usr/bin/python

import sys
from ase.calculators.vasp import Vasp





import numpy as np
import matplotlib.pyplot as plt

vasp=Vasp()
vasp.nbands=vasp.read_nbands()
eigen=vasp.read_eigenvalues()

#plt.figure(figsize=(1,8))
#fig, ax1 = plt.subplots()

#plt.figure(figsize=(1,8))
#plt.axes([0.1, 0.15, 0.8, 0.75])
#plt.ylabel("KKKK", fontsize=20)
#ax1.set_xlabel('time (s)')
#ax1.set_ylabel('Energy')

x=[0.0,1.0]
#line, = plt.plot(eigen, '--', linewidth=2)
for y in eigen:
    plt.plot(x,[y,y], '-', color='k', linewidth=1)

#plt.axis([0, 1, 10, 20])
plt.ylabel("Energy [eV]")
plt.show()
