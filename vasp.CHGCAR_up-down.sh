#!/bin/bash

fname=CHGCAR_up-down
mkdir $fname
vasp.CHGCAR.sh CHGCAR > $fname/CHGCAR
