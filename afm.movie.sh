#!/bin/bash

list=`ls -d [0-9].[0-9][0-9]|sort -r`

rep=""
if (( $# > 2 )) ; then
    rep="-r "$1"x"$2"x"$3
fi

rm approaching.movie.xyz

for dir in $list
do
	cd $dir
	vasp.POSCAR2xyz.py -c $dir $rep CONTCAR
	cat poscar.xyz >> ../approaching.movie.xyz
	cd ..
done


