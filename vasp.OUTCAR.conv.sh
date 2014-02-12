#!/bin/bash

outcars=`find . -name OUTCAR | sort -r`

for file in $outcars
do
    check=`tail -n 1000 $file | grep "reached required accuracy"`
#    check=`grep "reached required accuracy" $file`
    if(( ${#check} == 0 )); then
            check="Error: VASP did not reached required accuracy"
    fi
    echo -e $file "\t" $check
done
