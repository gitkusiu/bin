#!/usr/bin/python
from os import listdir, rename
from os.path import isfile, isdir, join
import re

#read all directories
mypath="."
#print listdir(mypath)
#tobemoved=[f for f in listdir(mypath) if "_.9" in f]
tttt = [f for f in listdir(mypath) if "_.9" in f]
print tttt
tobemoved = [ff for ff in tttt if isdir(ff)]
#onlydirs = [f for f in listdir(mypath) if isdir(join(mypath, f))]
print tobemoved

for d in tobemoved:
	tmp = d.split("_")
	source = d
	dest   = tmp[0] + "_0"+tmp[1]
	print source
	print dest
	rename(source, dest)
