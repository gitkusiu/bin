#!/bin/bash

#outcars=`find . -name OUTCAR | sort -r`

list=`ls -d [0-9].[0-9][0-9]|sort -r`

for d in $list
do
    file=$d/OUTCAR
    check=`vasp.OUTCAR.py --get conv $file`
    echo -e $file "\t" $check
done
