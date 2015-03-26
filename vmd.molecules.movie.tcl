
# setup variables
set iorbit 85 
set forbit 92
set n [expr $forbit-$iorbit+1]
set clrID 1
set fmask "orbital_"

#create representations  (  CPK + Isosurface )
proc addReps {myMol SphereScale BondRadius Isoval1 Isoval2 } { 
	mol delrep 0 $myMol
	mol representation CPK $SphereScale $BondRadius 32 16
	mol color Name
	mol selection {all}
	mol addrep $myMol
	#mol color ColorID 2
	mol representation Isosurface $Isoval1 0 0 0 0
	mol addrep $myMol
	mol color ColorID 0
	mol representation Isosurface $Isoval2 0 0 0 0
	mol addrep $myMol
}

# update function on animation slider trace event
proc myUpdate {myMol frame color} { 
	set repid 1
    mol color ColorID $color
    lassign [ molinfo $myMol get "{rep $repid}" ] myrep
    mol representation [ lreplace $myrep 2 2 $frame ]
    mol modrep $repid $myMol
	set repid 2 
    mol color ColorID 0
    lassign [ molinfo $myMol get "{rep $repid}" ] myrep
    mol representation [ lreplace $myrep 2 2 $frame ]
    mol modrep $repid $myMol

}
proc update_iso {args} {
	global molL
	global clrID
	set frame [molinfo $molL get frame]
	puts " === Frame: $frame "
	myUpdate $molL $frame $clrID
}

# move slider & render picture
proc renderi {ii} {
	global fmask
	global iorbit
	animate goto [expr $ii-$iorbit]
	render TachyonInternal ${fmask}[expr $ii].tga
}


# Display settings
display projection Orthographic
display nearclip set 0.000000
display farclip  set 10.000000
display depthcue off
display antialias on
axes location off
color Display Background white
color Display Foreground black
color Display FPS black
color Axes Labels black
color Labels Bonds white

# load datafiles from disk
set molL [mol new $fmask[format "%04d.xsf" $iorbit] type xsf waitfor all]
for {set ii [expr $iorbit+1]} {$ii<=$forbit} {incr ii} {
mol addfile $fmask[format "%04d.xsf" $ii] type xsf waitfor all
}


addReps $molL 0.7 0.4 0.2 -0.2
set myMol $molL
trace variable vmd_frame($molL) w update_iso

## ambient occlusion setup
#display ambientocclusion on
#display aoambient 0.7
#display aodirect 0.7

# resize display
display resize 700 700
display update
display update ui

# setup camera
#rotate x by -10 
#rotate y by 180
scale by 1
translate by 0.0 0.0 0

 render all
#for {set ii 86} {$ii<=$n} {incr ii} {
#for {set ii 0} {$ii<$n} {incr ii} {
for {set ii $iorbit} {$ii<=$forbit} {incr ii} {
    renderi $ii
}

