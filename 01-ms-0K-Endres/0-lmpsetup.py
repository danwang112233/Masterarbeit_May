HEADER = \
"""
    Calculates Spontaneous polarization through Molecular Static Simulation
    of Rhombohedral Barium Titanate at 0K with an electric field applied
    in [1 1 1] direction.
    
    Vishal Boddu, May 2016
"""
from mpi4py import MPI
from computepol import pol
from lammps import lammps
import math
import numpy as np
import os
import sys

#-------------------------------------------------SETUP MPI
rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()
print "Proc %d out of %d procs has" %( rank, size )

#-------------------------------------------------PARSING ARGSC
if len(sys.argv) != 4:
    sys.exit(""" Usage: python mpirun.py <a> <alpha> <n>
                where `a` and `alpha` are lattice parameters and 
                `n` is the numeber of RVE replica in each direction """)
else: 
    a     = float( sys.argv[1] )
    alpha = float( sys.argv[2] )
    n     =   int( sys.argv[3] )
#-------------------------------------------------FULL PARAMETER LIST
thermo_flag = "20"  # Print thermodynamics info every this many timesteps
displ_flag  = "100" # Write displacement info to file every this many timesteps 
max_iter    = "20000"                       #Maximum iterations of minimizer
ext_ef      = -0.0005                        # Strengh of electric field 
ex=ey=ez    = str(ext_ef/math.sqrt(3.0))    # Electric field vector \E
stp_ef      = 0.0005                        # \delta E
rng_ef      = range(0,2,1)                  # Range of \E
simbox      = { 'a' : a,'n' : n, 'alpha' : alpha }
#-------------------------------------------------SIMULATION BOX SETTINGS
alpha_r    = alpha * math.pi / 180.0
XY_DELTA   = a * n * math.cos( alpha_r )
YZ_DELTA   = a * n * math.cos( alpha_r )
XZ_DELTA   = a * n * math.cos( alpha_r )

#-------------------------------------------------INITIALIZATION SETTINGS
lmp = lammps()
lmp.file("manual.system.in")
lmp.command("change_box all triclinic xy delta %s yz delta %s xz delta %s" \
            " remap" %( XY_DELTA, YZ_DELTA, XZ_DELTA ) )
lmp.command("compute dr all displace/atom" )

#-------------------------------------------------OUTPUT CONTROL SETTINGS
lmp.command("thermo %s" % thermo_flag )
lmp.command("thermo_style custom step etotal epair evdwl ecoul elong ebond "\
            "fnorm lx ly lz temp press")
lmp.command("dump dump_positions all atom 100 atomdump")
lmp.command("dump dump_displace all custom %s displdump " % displ_flag + 
            " id type c_dr[1] c_dr[2] c_dr[3]" )

#-------------------------------------------------SIMULATION SETTINGS
if rank == 0:
    POL = np.array([0., 0., 0., 0., 0.])
for de in rng_ef:
    ext_ef -= de*stp_ef
    ex = ey = ez = str( ext_ef/math.sqrt(3.0) ) 
    lmp.command("fix ef all efield %s %s %s" %( ex, ey, ez) )
    lmp.command("fix_modify ef energy yes")
    #lmp.command("min_style quickmin")
    #lmp.command("minimize 0.0 1e-05 %s 100000" % max_iter )
    lmp.command("min_style fire")
    lmp.command("minimize 0.0 1e-05 %s 100000" % max_iter )
    if rank == 0:
        POL = np.vstack( ( POL, np.append( ext_ef, pol("displdump", simbox)) ) )
        print "Done with de", de, "\n"
        print POL  
    lmp.command("unfix ef")
    lmp.command("min_style fire")
    lmp.command("minimize 0.0 1e-05 %s 100000" % max_iter )
    if rank == 0:
        POL = np.vstack( ( POL, np.append( ext_ef, pol("displdump", simbox)) ) )
        print "Done with de", de, "\n"
        print POL  
if rank == 0:
    with open("%d_pol.dat" %n, 'w') as file_handle:
        np.savetxt( file_handle, POL, delimiter='\t', header=HEADER)
#-------------------------------------------------END LAMMPS
MPI.Finalize()
