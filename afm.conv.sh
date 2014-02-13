#!/bin/bash

outcars=`find . -name OUTCAR | sort -r`

for file in $outcars
do
    check=`vasp.OUTCAR.py --get conv $file`
    echo -e $file "\t" $check
done
