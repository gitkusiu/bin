#!/bin/bash
    
wavecars=`find $1 -name WAVECAR`
chgcars=`find $1 -name CHGCAR`

files_to_backup=$wavecars' '$chgcars


backup_dir=$1.backup
mkdir $backup_dir

for i in $files_to_backup
do
    echo $i
    directory=$backup_dir/`dirname $i`
    mkdir -p $directory
    echo $i $directory
    mv $i $directory
    ls $directory
done
echo "Done"
