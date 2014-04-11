#!/bin/bash


last_sur=`echo "$1-1" | bc`

echo $last_sur


afm.conv.sh  >  approaching.conv.dat

afm.forces.sh  $1 $2 >  approaching.force.dat
afm.forces.py  $1 $2 >  approaching.force.diff.dat

afm.charge.sh $1 $2 > approaching.charge.tip.dat
afm.magnet.sh $1 $2 > approaching.magnet.tip.dat

afm.charge.sh 1 $last_sur > approaching.charge.surface.dat
afm.magnet.sh 1 $last_sur > approaching.magnet.surface.dat

afm.movie.sh
afm.movie.sh 3 3 1





