#!/bin/bash

outcar=$3
tip_begin=$1
tip_end=$2

buffor=100

natoms=`grep -m 1 NIONS $outcar | awk '{print $12}'`

linetot=`wc $outcar|awk '{print $1}'`
line_from_the_end=`tac $outcar | grep -n "free  energy   TOTEN"  -m 1  | awk '{print $1}'| sed -e 's/:.*//g'`
no_lices_to_pars=`echo "$line_from_the_end + $buffor" | bc`

tail -n $no_lices_to_pars $outcar | awk -v natoms=$natoms -v tip_begin=$tip_begin -v tip_end=$tip_end 'BEGIN {    
    is_found = 0;
    while(is_found == 0)
    {
        getline;
        if($1 == "total" && $2 == "charge")
        {
            is_found = 1;
        }
    }
    getline
    getline
    getline
    i=1
    magnet_sum=0.0
}
{
    if( i>=tip_begin && i<=tip_end && i <= natoms)
    {
        magnet_sum   = magnet_sum + $NF    
    }
    i = i+1
}

END {
    print magnet_sum;
}'
