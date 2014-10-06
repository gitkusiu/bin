#!/bin/bash

fname=CHGCAR_up-down
rm CHG CHGCAR WAVECAR PROCAR DOSCAR
gzip -r ./*
gunzip OUTCAR.gz CONTCAR.gz

