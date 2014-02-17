#!/bin/bash

list=`ls -d [0-9].[0-9][0-9]|sort -r`

if (( $# > 2 )) ; then
    rep="$1 $2 $3"
    XYZ_FILE=approaching.movie.$1x$2x$3.xyz
else
    rep="1 1 1"
    XYZ_FILE=approaching.movie.xyz
fi

rm $XYZ_FILE $XYZ_FILE.gz

for dir in $list
do
	cd $dir
	#echo "vasp.POSCAR.py --comment $dir --periods $rep -f xyz CONTCAR"
	vasp.POSCAR.py --comment $dir --periods $rep -f xyz CONTCAR >> ../$XYZ_FILE
	cd ..
done

gzip $XYZ_FILE
