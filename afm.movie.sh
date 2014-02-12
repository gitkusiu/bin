#!/bin/bash

list=`ls -d [0-9].[0-9][0-9]|sort -r`

if (( $# > 2 )) ; then
    rep=$1"x"$2"x"$3
    XYZ_FILE=approaching.movie.$rep.xyz
else
    rep="1x1x1"
    XYZ_FILE=approaching.movie.xyz
fi

#echo $XYZ_FILE
rm $XYZ_FILE

for dir in $list
do
	cd $dir
	vasp.POSCAR2xyz.py -c $dir -r $rep CONTCAR
	cat poscar.$rep.xyz >> ../$XYZ_FILE
    rm poscar.$rep.xyz
	cd ..
done


