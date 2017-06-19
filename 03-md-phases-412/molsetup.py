""" This python scripts generates moltemplate files and autogenerates
    data files for atomistic simulations.
"""
import os
import shutil
import subprocess
import sys

#------------------------------------------------
if  len(sys.argv) != 7:
    sys.exit(""" Usage: python molsetup.py <a> <n>
                where `a` (double) : lattice constant ( the simulation box)
                and `n` (int) : number of replicated RVEs in all direction.
             """)
else:
    a    = float(sys.argv[1])
    cbya = float(sys.argv[2])
    nx   =   int(sys.argv[3])
    ny   =   int(sys.argv[4])
    nz   =   int(sys.argv[5])
    m    =   int(sys.argv[6])

lx = a * nx
ly = a * ny
lz = cbya * a * nz

raw_txt  = """
# Generates atom.data which consists of 5*nx*ny*nz atoms (core+shell=atom).
# This file aids in creation of data files, through moltemplate
# compatible with read_data in lammps. Data file is according
# to the Isotropic-anharmonic Shell Model proposed by Tinte based on
# Local Density Approximation(LDA) to Density Functional Theory(DFT):
# doi:10.1016/j.cossms.2006.05.002 \n
import "../../commons/molsetup/%s-unit-dyn-vs.lt" \n \n
%sCUBIC_BaTiO3_UNIT.scale( %f ) \n
# Periodic boundary conditions:
write_once("Data Boundary") {
   0.0  %f xlo xhi
   0.0  %f ylo yhi
   0.0  %f zlo zhi
}
CUBIC_BTO {
CBTO = new %sCUBIC_BaTiO3_UNIT[%d].move(  %f, 0.0, 0.0)
                              [%d].move( 0.0,  %f, 0.0)
                              [%d].move( 0.0, 0.0,  %f)
}

cubic_BaTiO3 = new CUBIC_BTO[%d].move(  %f, 0.0, 0.0)
"""%( "tb",        "", a, m*lx, ly, lz, "", nx, a, ny, a, nz, a, m, lx )

#-------------------------------------------------CREATE MOLTEMPLATE FILE
lt_file_name = "atom.lt"
lt_file = open( lt_file_name, "w" )
lt_file.write("%s" % raw_txt )
lt_file.close()

#-------------------------------------------------GENERATE DATA FILE FOR LAMMPS
subprocess.check_call( [ "moltemplate.sh", lt_file_name, "-nocheck" ])

#-------------------------------------------------DELETE TEMP FILES
in_file_name = lt_file_name.replace( "lt", "in" )
os.remove( lt_file_name )
os.remove( in_file_name )
shutil.rmtree( "output_ttree" )
