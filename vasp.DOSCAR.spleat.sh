#!/bin/bash

echo $1 $2


for d in $(seq -w $1 1 $2)
do
    echo $d
    vasp.DOSCAR.py -a $d $d  DOSCAR > dos_$d.dat    
done
