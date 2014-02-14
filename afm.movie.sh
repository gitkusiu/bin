#!/bin/bash

list=`ls -d [0-9].[0-9][0-9]|sort -r`

if (( $# > 2 )) ; then
    rep=$1"x"$2"x"$3
    XYZ_FILE=approaching.movie.$rep.xyz
else
    rep="1x1x1"
    XYZ_FILE=approaching.movie.xyz
fi

rm $XYZ_FILE $XYZ_FILE.gz

for dir in $list
do
	cd $dir
	vasp.POSCAR.py --comment $dir --periods $1 $2 $3 -f xyz CONTCAR >> ../$XYZ_FILE
	cd ..
done

gzip $XYZ_FILE


