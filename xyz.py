#!/usr/bin/python

import sys
from optparse import OptionParser


parser = OptionParser()
#parser.add_option("-f", "--format",           action="store", type="string", default="xyz",      help="format of the output file: xyz")
parser.add_option("-a", "--atoms",            action="store", type="int",    default=[-1,-1],       help="specify atoms to whcih changes (translation rotation etc. will be made)", nargs=2)
parser.add_option("-s", "--steps",            action="store", type="int",    default=[-1,-1],       help="specify steps ", nargs=2)
parser.add_option("-p", "--periods",          action="store", type="int",    default=[1,1,1],       help="repetition of the unit cell", nargs=3)
parser.add_option("-T", "--Translation",      action="store", type="float",  default=[0.0,0.0,0.0], help="ss", nargs=3)
parser.add_option("-r", "--rotation_angle",   action="store", type="float",  default=0.0,           help="rotation angle", nargs=1)
parser.add_option(      "--rotate_around",    action="store", type="int",    default=0, help="rotate around nth atom", nargs=1)
parser.add_option("-c", "--cell",          action="store", type="string", default="answer.lvs",  help="format of the output file: xyz")

(options, args) = parser.parse_args()

#print parser.parse_args()

num = len(sys.argv)



if(num < 2):
    parser.print_help()
else:

    f     = open(sys.argv[num-1], "r")
    lines = f.read().splitlines()
    no_lines    = len(lines)                  # number of lines in a file
    no_atoms    = int(lines[0].split()[0])    # number of atoms of a system
    no_steps    = int(no_lines/no_atoms)      # number of simulation steps
    no_lines_in_step = no_atoms + 2
    print no_steps, no_lines, no_atoms

    # --------------- Atoms -----------------
    a = options.atoms # do not use/modify options.atoms
    is_there_any_atom_specified = (a[1]-a[0] >= 0)
    if(a == [-1,-1]):
        a = [no_atoms, no_atoms]       

    # --------------- Steps -----------------
    s = options.steps # 
    if(s == [-1,-1]):
        s = [no_steps,no_steps]

    # --------------- Translation -----------------
    # translation
    t = options.Translation
    is_translation_nonzero          = (t != (0.0,0.0,0.0))
    do_we_translate = is_translation_nonzero and is_there_any_atom_specified


    print "steps", s, range(s[0],s[1]+1)
    # ---- LOOP OVER STEPS -----
    for i in range(s[0],s[1]+1):
        # copy whole step from the lines table
        i_from = (i-1)*no_lines_in_step + 1
        i_to   = (i-1)*no_lines_in_step + no_lines_in_step
        print i, i_from, i_to
        step   = lines[i_from-1:i_to]
        print "------------------------------", len(step)

        # translate what you have to
        if(do_we_translate):
            a_from = a[0]+1
            a_to   = a[1]+2
            print "trans", a_from,a_to
#            for atom in step[a_from:a_to]:
#                elem = atom.split()[0]
#                r = atom.split()[1:4]
#                atom = str(elem) +  "     " + str(float(r[0])+t[0]) + "     " + str(float(r[1])+t[1]) + "     " + str(float(r[2])+t[2])
#                print atom
            for j in range(a_from,a_to):
                at   = step[j].split()
                elem = at[0]
                r    = at[1:4]
                step[j] = str(elem) +  "     " + str(float(r[0])+t[0]) + "     " + str(float(r[1])+t[1]) + "     " + str(float(r[2])+t[2])


        # printing
        for atom in step:
            print atom


                  
#             print w
#        print lines[100]
#        for line in 
#        worlds = line.split()
#        nw = len(worlds)
#        if( nw==1 && int(worlds[0])==n ):
#            print worlds[0]
#        elif( nw != 4 ):
#            print worlds
#        else:
#            t = options.Translation
#            is_translation_nonzero          = (t != (0.0,0.0,0.0))
#            is_there_any_atoms_to_translate = (a[1]-a[0] >= 0)
#            for i in range(a[0]-1, a[1]):
#            xyz.arrays['positions'][i] +=  t

   

#    for line in xyz_file:
#        



#    # --------------- Translations -----------------
#    t = options.Translation
#    is_translation_nonzero          = (t != (0.0,0.0,0.0))
#    is_there_any_atoms_to_translate = (a[1]-a[0] >= 0)
#    if( is_translation_nonzero and is_there_any_atoms_to_translate ):
#        for i in range(a[0]-1, a[1]):
#            xyz.arrays['positions'][i] +=  t


#    # --------------- Rotation -----------------
#    alpha  = options.rotation_angle
##    v      = options.rotation_vector

#    if(alpha != 0.0):
#        l_positions = xyz.get_positions()
#        l_numbers   = xyz.get_atomic_numbers()
#        l_cell      = xyz.get_cell()
#        l_from      = a[0]-1
#        l_to        = a[1]-1

#        constr = xyz._get_constraints()

#        l_sur1_pos            = l_positions[0      : l_from]
#        l_tip_pos             = l_positions[l_from : l_to+1]
#        l_sur2_pos            = l_positions[l_to+1 : natoms]

#        l_sur1_atomic_numbers = l_numbers[0      : l_from]
#        l_tip_atomic_numbers  = l_numbers[l_from : l_to+1]
#        l_sur2_atomic_numbers = l_numbers[l_to+1 : natoms]

#        l_center  = l_positions[options.rotate_around-1]

#        sur2 = Atoms(positions=l_sur2_pos, numbers=l_sur2_atomic_numbers, cell=l_cell, pbc = True)
#        sur1 = Atoms(positions=l_sur1_pos, numbers=l_sur1_atomic_numbers, cell=l_cell, pbc = True)
#        tip  = Atoms(positions=l_tip_pos,  numbers=l_tip_atomic_numbers, cell=l_cell, pbc = True)

##        c = tip.get_cell()
##        tip.set_cell(c*(2,2,0))
#        tip.rotate(v='y',a=(alpha/180.)*pi, center=l_center,rotate_cell=True)
#        #tip.rotate(v='z',a=(alpha/180.)*pi, center=l_center,rotate_cell=True)
#        tip.set_cell(xyz.get_cell())

#        xyz = sur1+tip+sur2
#        xyz.set_constraint(constr)


#    # --------------- unit cell scaling facto -----------------
#    u = options.cell_scale
#    if( u != [1.0, 1.0, 1.0] ):
#        cell = xyz.get_cell()
#        xyz.set_cell(cell*u)

#    # --------------- Periodic repetitions -----------------
#    p = options.periods
#    if( p != [1,1,1]):
#        xyz = xyz*(p[0], p[1], p[2])
##        print p


#    # --------------- Wirting out in proper format -----------------
#    if(options.format == "xyz"):
#        write_xyz(sys.stdout,xyz,options.comment)
##        write_vasp(sys.stdout,xyz,label=options.comment, direct=False,sort=False,vasp5=True)
##    elif(options.format == "xyz"):
#        
