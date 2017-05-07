""" This python scripts generates moltemplate files and autogenerates 
    data files for atomistic simulations.
"""
import os
import shutil
import subprocess
import sys

#------------------------------------------------
if  len(sys.argv) != 2:
    sys.exit(""" Usage: python molsetup.py <a> <n>
                where `a` (double) : lattice constant ( the simulation box)
                and `n` (int) : number of replicated RVEs in all direction.
             """)
else: 
    a = sys.argv[1]
    #n = sys.argv[2]
#l = str (float(a) * 3)

raw_txt  = """
# Generates atom.data which consists of 5n^3 atoms (core+shell=atom). 
# This file aids in creation of data files, through moltemplate
# compatible with read_data in lammps. Data file is according 
# to the Isotropic-anharmonic Shell Model proposed by Tinte based on 
# Local Density Approximation(LDA) to Density Functional Theory(DFT):
# doi:10.1016/j.cossms.2006.05.002 \n
import "%s-unit.lt" \n \n 
%sCUBIC_BaTiO3_UNIT.scale( %s ) \n
# Periodic boundary conditions:
write_once("Data Boundary") {
   0.0  %s xlo xhi
   0.0  %s ylo yhi
   0.0  %s zlo zhi
}
CUBIC_BaTiO3 = new %sCUBIC_BaTiO3_UNIT[%s].move(  %s, 0.0, 0.0)
                                      [%s].move( 0.0,  %s, 0.0)
                                      [%s].move( 0.0, 0.0,  %s)
"""%( "bt",        "", a, 8.02, 20.05, 4.010,     "", 2, a, 5, a, 0, a )


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
