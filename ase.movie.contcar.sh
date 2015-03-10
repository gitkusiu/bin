#!/bin/bash

list=`ls -d [0-9][0-9].[0-9][0-9]| sort -r`
for dir in $list
do
    cd $dir
        ase.poscar.py -p $1 $2 $3 -f xyz CONTCAR
    cd ..
done
