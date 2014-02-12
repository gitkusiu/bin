#!/bin/bash

list=`ls -d [0-9].[0-9][0-9]|sort -r`


rm approaching.movie.xyz

for dir in $list
do
	cd $dir
	vasp.POSCAR2xyz.py CONTCAR $dir
	cat poscar.xyz >> ../approaching.movie.xyz
	cd ..
done


