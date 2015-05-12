#!/bin/bash


grep "| Change of sum of eigenvalues" $1 | awk '{print $8}' > sc_ev.dat
grep "| Change of charge density"     $1 | awk '{print $7}' > sc_rho.dat
grep "| Change of total energy"       $1 | awk '{print $7}' > sc_etot.dat
