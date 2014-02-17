#!/bin/bash

outcar=$3
tip_begin=$1
tip_end=$2

#echo $outcar 
number_of_steps=`grep POSITION $outcar | wc | awk '{print $1}'`


awk -v nsteps=$number_of_steps -v tip_begin=$tip_begin -v tip_end=$tip_end 'BEGIN {    
    getline;
    is_found = 0;
    n_atoms
        while(is_found < nsteps)
    {

        if($10 == "NIONS")
        {
            n_atoms = $12
        }
        if($1 == "POSITION")
        {
            is_found = is_found+1;
        }
        getline;
    }
    i=1
    force_sum[1] = 0.0
    force_sum[2] = 0.0
    force_sum[3] = 0.0
}

{

#    print i, tip_begin, tip_end 
    if( i>=tip_begin && i<=tip_end && i <= n_atoms)
    {
#        forces[i,1] = $4
#        forces[i,2] = $5
#        forces[i,3] = $6
        force_sum[1] = force_sum[1] + $4
        force_sum[2] = force_sum[2] + $5
        force_sum[3] = force_sum[3] + $6
    }
    i = i+1
}

END {
#    for(i=tip_begin; i<=tip_end; i++)
#    {
#        printf "%e   %e   %e\n", forces[i,1], forces[i,2], forces[i,3];
#    }
#    print "ssss"

    printf "%e   %e   %e \n", force_sum[1], force_sum[2], force_sum[3]; 

}' $outcar


#awk -v nsteps=$number_of_steps -f $HOME/bin/dft/vasp.OUTCAR.last.forces.awk $1



