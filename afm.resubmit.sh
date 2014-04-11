#!/bin/bash


last_sur=`echo "$1-1" | bc`



run=$1.run$2

echo $1 $2 $run

mv $1 $run
mkdir $1
cd $run
cp CONTCAR ../$1/POSCAR
cp POTCAR INCAR KPOINTS run.pbs ../$1
