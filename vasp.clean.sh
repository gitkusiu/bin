#!/bin/bash


wavecars=`find . -name WAVECAR`
chgcars=`find . -name CHGCAR`
chgs=`find . -name CHG`

outcars=`find . -name OUTCAR`
doscars=`find . -name DOSCAR`
runs=`find . -name vasprun.xml`
procars=`find . -name PROCAR`


to_remove=$wavecars' '$chgs' '$chgcars
to_archive=$outcars' '$doscars' '$runs' '$procars


#to_remove=$wavecars
if [ $1 == 'force' ] ; then
	echo "Following files are removing:" 
	for i in $to_remove
	do
		echo -e '\t' $i
	done

	rm $to_remove
	echo "Following files are gziping:"
	for i in $to_archive
	do
		echo -e '\t' $i
	done
	gzip $to_archive
else
	echo ""
	echo "This is only informative mode of the vasp.clean.sh script."
	echo "If you wish to realy clean VASP files type 'vasp.clean.sh force' command."
	echo ""

	echo "Following files will be removed:" 
	for i in $to_remove
	do
		echo -e '\t' $i
	done

	echo "Following files will be gziped:"
	for i in $to_archive
	do
		echo -e '\t' $i
	done
	echo ""
fi


