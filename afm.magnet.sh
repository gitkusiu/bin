#!/bin/bash

list=`ls -d [0-9].[0-9][0-9]|sort -r`

for dir in $list
do
	cd $dir
	force=`vasp.OUTCAR.magnet.sh $1 $2 OUTCAR`
	echo -e $dir '\t' $force
	cd ..
done
