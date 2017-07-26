HEADER= \
""" 
    Write Polarization Vs Electric Field values to file after Molecular Static 
    Simulation of Rhombohedral Barium Titanate at 0K with an electric field 
    applied in [1 1 1] direction. Potential used in simualtion is the 
    isotropic-anharmonic Shell Model proposed by Vielma and Schneider based on 
    PBE Generalized Gradient Approximation(GGA) to Density Functional Theory
    (DFT): [Vielma Schneider 2013](http://dx.doi.org/10.1063/1.4827475)
    
    Vishal Boddu, June 2016
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
if len(sys.argv) != 6:
    sys.exit(""" Usage: python mpirun.py <a> <alpha> <nx> <ny> <nz>
                where `a` and `alpha` are lattice parameters and
                `n` is the number of RVE replica in each direction """)
else:
    a     = float( str( sys.argv[1] ) )
    alpha = float( str( sys.argv[2] ) )
    nx     =   int( str( sys.argv[3] ) )
    ny     =   int( str( sys.argv[4] ) )
    nz     =   int( str( sys.argv[5] ) )

#-------------------------------------------------FULL PARAMETER LIST
thermo_flag = "50"  # Print thermodynamics info every this many timesteps
displ_flag  = "100" # Write displacement info to file every this many timesteps 
max_iter    = "20000"                       # Maximum iterations of minimizer
ext_ef      = 0.0000                        # Strengh of electric field 
ex=ey=ez    = str(ext_ef/math.sqrt(3.0))    # Electric field vector \E
stp_ef      = 0.005                         # \delta E
#aef_ef      = range( 1, -20,-1)             # Range of \E : a-e-f [Endres 2015]
abc_ef      = range(-40,  40, 1)             # Range of \E : a-b-c [Endres 2015]
simbox      = { 'a' : a,'nx' : nx, 'ny' : ny, 'nz' : nz,  'alpha' : alpha }
#-------------------------------------------------SIMULATION BOX SETTINGS
alpha_r    = alpha * math.pi / 180.0
XY_DELTA   = a * nz * math.cos( alpha_r )
YZ_DELTA   = a * nx * math.cos( alpha_r )
XZ_DELTA   = a * ny * math.cos( alpha_r )
#-------------------------------------------------INITIALIZATION SETTINGS
lmp = lammps()
lmp.file("manual.system.in")
lmp.command("change_box all triclinic xy delta %s yz delta %s xz delta %s" \
            " remap" %( XY_DELTA, YZ_DELTA, XZ_DELTA ) )
lmp.command("compute dr all displace/atom" )

#-------------------------------------------------OUTPUT CONTROL SETTINGS
lmp.command("thermo %s" % thermo_flag )
lmp.command("thermo_style custom step etotal epair evdwl ecoul elong ebond "\
            "fnorm lx ly lz temp press pxx pyy pzz")
lmp.command("dump dump_positions all atom 100 atomdump")
lmp.command("dump dump_displace all custom %s displdump " % displ_flag + 
            " id type c_dr[1] c_dr[2] c_dr[3]" )

#-------------------------------------------------SIMULATION SETTINGS
if rank == 0:
    POL = np.array([0., 0., 0., 0., 0.])
for de in abc_ef:
    if not de == 0:
        ds = np.sign( de )
        ext_ef += ds * stp_ef
    else:
        ext_ef = 0.
    ex = ey = ez = str( ext_ef/math.sqrt(3.0) ) 
    lmp.command("fix ef all efield %s %s %s" %( ex, ey, ez) )
    lmp.command("fix_modify ef energy yes")
    lmp.command("min_style fire")
    lmp.command("minimize 0.0 1e-06 %s 100000" % max_iter )
    lmp.command("min_style quickmin")
    lmp.command("minimize 0.0 1e-06 %s 100000" % max_iter )
    if rank == 0:
        POL = np.vstack( ( POL, np.append( ext_ef, pol("displdump", simbox)) ) )
        print "Done with de", de, "\n"
        print POL  
    lmp.command("unfix ef")
if rank == 0:
    with open("%d_pol.dat" %n, 'a') as file_handle:
        np.savetxt( file_handle, POL, delimiter='\t', header=HEADER)
#-------------------------------------------------END LAMMPS
MPI.Finalize()
