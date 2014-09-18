#!/bin/bash

if [ "$#" -eq "0" ]
then
    file=OUTCAR
else
    file=$1
fi

vasp.OUTCAR.py -g max_force $file
