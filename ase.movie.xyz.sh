#!/bin/bash

list=`ls -d [0-9][0-9].[0-9][0-9]| sort -r`
for dir in $list
do
    cd $dir
        ase.xyz.py -p $1 $2 $3 -s -1 -1 answer.xyz
    cd ..
done
