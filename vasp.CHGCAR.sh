#!/bin/bash

atoms_line=`head -n 7 $1 | tail -n 1`
atoms_nr=`echo $atoms_line | awk '{ s = 0; for (i = 1; i <= NF; i++) s = s+$i; print s }'`


#  line in which first mech indicators are placed
mesh_line1_nr=`echo "$atoms_nr + 10" | bc`
mesh_line1=`head -n $mesh_line1_nr $1| tail -n 1`


#  line in which second mech indicators are placed
mesh_line2_nr=`grep -n "$mesh_line1" $1 | tail -n 1 | cut -f1 -d:`

# No. of lines of the file
file_line_nr=`wc -l $1 | awk '{print $1}'`

# No. of files to be cuted from a back of file
back_line_nr=`echo "$file_line_nr - $mesh_line2_nr" | bc`

# cut the file from the top and from the bottom
head -n $mesh_line1_nr $1
tail -n $back_line_nr $1

