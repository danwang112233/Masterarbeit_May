from mpi4py import MPI
from computepol import pol, find_temp, find_lat
from datetime import datetime
from lammps import lammps
import bisect
import math
import numpy as np
import os
import sys
rank = MPI.COMM_WORLD.Get_rank()
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
thermo_flag = 100   # Print thermodynamics info every this many timesteps
dump_flag   = 1000  # Write pos & displ info to file every this many timesteps
m_iter      = 30000                 # Maximum iterations of minimizer
ex=ey=ez    = 0.0005/math.sqrt(3.0) # Electric field vector \E - Init Pol
#Ti          = 5                     # First MD run at Ti
#DT          = 25                     # \delta T
#Tf          = 310                  # Last MS run at Tf-DT
#rng_T       = range(Ti,Tf,DT)       # Range of \T
Tg          = 10
Tdamp       = 0.1
Pdamp       = 0.1
tequilib    = 10000
trun        = 30000
#-------------------------------------------------DATA FILE NAMES
f_ave_temp  = "ave_temp"
f_ave_lat   = "ave_lat"
f_atom_dump = "atomdump"
f_atom_disp = "displdump"
f_core_disp = "displcoredump"
#-------------------------------------------------SIMULATION BOX SETTINGS
alpha_r    = alpha * math.pi / 180.0
XY_DELTA   = a * nz * math.cos( alpha_r )
YZ_DELTA   = a * nx * math.cos( alpha_r )
XZ_DELTA   = a * ny * math.cos( alpha_r )
#-------------------------------------------------HEADER
HEADER = \
"""
    Polarization at various temperatures through Molecular Dynamics
    Simulation. A Rhombohedral Barium Titanate molecular system consisting of
    n^3 unit cells at 0 K, polarized using a small electric field in
    [1 1 1] direction, is taken to 400 K incrementally (10 K steps) in an
    isothermal-isobaric (NPT) ensemble at 0 bar pressure. The molecular system
    is periodic and all its lattice parameters are allowed to vary.
    The timestep used is 0.4 fs, the system is equilibrated for 4 ps,
    followed by a simulation run of 12 ps.

    Coupling parameters: Tdamp = 0.1 and Pdamp = 0.1

    Polarization along with lattice parameters at varius temperatures are
    stored in a single file with the name n_pol_Tdamp_Pdamp.dat

    Vishal Boddu, %s
""" %( datetime.now().strftime('%d-%m-%Y_%H:%M:%S') )
#-------------------------------------------------INITIALIZATION SETTINGS
lmp = lammps()
lmp.file("manual.system.in")
lmp.command("change_box all triclinic xy delta %s yz delta %s xz delta %s" \
            " remap" %( XY_DELTA, YZ_DELTA, XZ_DELTA ) )
lmp.command("compute dr all displace/atom" )
lmp.command("reset_timestep 0")
lmp.command("dump dump_positions all atom %d %s" % (dump_flag, f_atom_dump ))
lmp.command("dump dump_displace all custom %d %s " % (dump_flag, f_atom_disp) +
            "id type c_dr[1] c_dr[2] c_dr[3]" )
#-------------------------------------------------OUTPUT CONTROL SETTINGS
lmp.command("thermo %d" % thermo_flag )
lmp.command("thermo_style custom step etotal pe ke fnorm ecoul elong ebond " \
            "temp press pxx pyy pzz lx ly lz")
lmp.command("compute CSequ all temp/cs cores shells")
lmp.command("thermo_modify temp CSequ")
lmp.command("fix EF all efield %f %f %f" %( ex, ey, ez) )
lmp.command("fix_modify EF energy yes")
lmp.command("min_style quickmin")
lmp.command("minimize 0.0 1e-04 %d 100000" % m_iter )
lmp.command("unfix EF")
lmp.command("min_style fire")
lmp.command("minimize 0.0 1e-05 %d 100000" % (2*m_iter) )
#-------------------------------------------------COMPUTE AND OUTPUT CONTROL
lmp.command("reset_timestep 0")
lmp.command("variable la equal lx")
lmp.command("variable lb equal ly")
lmp.command("variable lc equal lz")
lmp.command("fix AVE_LAT all ave/time %d %d %d v_la v_lb v_lc file %s" \
            %(1, trun, trun+tequilib, f_ave_lat) )
lmp.command("fix AVE_ATOM all ave/atom %d %d %d c_dr[1] c_dr[2] c_dr[3]" \
            %(1, trun, trun+tequilib) )
lmp.command("dump core_displ all custom %d displcoredump " %(trun+tequilib) +
            "id type f_AVE_ATOM[1] f_AVE_ATOM[2] f_AVE_ATOM[3]" )
lmp.command("variable TEMP equal temp")
lmp.command("fix AVE_T all ave/time %d %d %d v_TEMP file %s" \
            %(1, trun, trun+tequilib, f_ave_temp) )
if rank == 0:
    POL = np.asarray( [ 0.] + pol("displdump", a, alpha, nx, ny, nz) + [ a, a, a ] )
#-------------------------------------------------MD SIMULATION SETTINGS
lmp.command("velocity all create %d 146981634 dist gaussian " % (Tg) +
            "mom yes rot no bias yes temp CSequ")

lmp.command("timestep 0.0004")
bisect.insort(Tg, 182.5)
bisect.insort(Tg, 187.5)
bisect.insort(Tg, 252.5)
bisect.insort(Tg, 257.5)
bisect.insort(Tg, 342.5)
bisect.insort(Tg, 347.5) 
#for T in rng_T:
lmp.command("velocity all scale %d temp CSequ" % (Tg) )
lmp.command("fix NPT all npt temp %d %d %f tri 1. 1. %f" %(Tg,Tg,Tdamp,Pdamp))
lmp.command("fix_modify NPT temp CSequ")
lmp.command("run %d" %tequilib)
lmp.command("unfix NPT")
lmp.command("fix NPT all npt temp %d %d %f tri 1. 1. %f" %(Tg,Tg,Tdamp,Pdamp))
lmp.command("fix_modify NPT temp CSequ")
lmp.command("run %d" %trun)
lmp.command("unfix NPT")
lx = lmp.extract_variable( "la", "all", 0 )
ly = lmp.extract_variable( "lb", "all", 0 )
lz = lmp.extract_variable( "lc", "all", 0 )
if rank == 0:
    lmp.command("variable STEP equal step")
    step = lmp.extract_variable( "STEP", "all", 0 )
    temp = float(find_temp( step, f_ave_temp))
    lat  = find_lat( step, f_ave_lat)
    POL = np.vstack((POL, np.asarray([temp]+pol("displcoredump", a, alpha, nx, ny, nz) + \
          [float(lat[0])/nx,float(lat[1])/ny,float(lat[2])/nz ])))
    print POL
if rank == 0:
    with open("%d%d%d_pol_%d_%.2f_%.2f.dat" %(nx,ny,nz, Tg, Tdamp, Pdamp), 'w') as file_handle:
        np.savetxt( file_handle, POL, delimiter='\t', header=HEADER, fmt='%.6e')
lmp.command("unfix AVE_T")
lmp.command("unfix AVE_ATOM")
lmp.command("unfix AVE_LAT")
#-------------------------------------------------END LAMMPS
MPI.Finalize()
