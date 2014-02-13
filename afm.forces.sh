#!/bin/bash

list=`ls -d [0-9].[0-9][0-9]|sort -r`

for dir in $list
do
	cd $dir
	force=`vasp.OUTCAR.py --get force --atoms $1 $2 --steps -1 1 OUTCAR`
	echo -e $dir '\t' $force
	cd ..
done

#echo $1 $2

