#!/bin/bash

#-------------------------------------------------LATTICE PARAMETER a
a="4.010"

#-------------------------------------------------LATTICE PARAMETER alpha
alpha="89.81"

#-------------------------------------------------REPLICAS IN EACH DIRECTION
nx="10"
ny="10"
nz="14"

#-------------------------------------------------GENERATE DATA FILE
python molsetup.py $a $nx $ny $nz

#-------------------------------------------------SPONTANEOUS POLARIZATION
# 0-lmpsetup.py 
# Write Polarization Vs Temperature to file after  Molecular Static 
# Simulation of Rhombohedral Barium Titanate at 0K with an electric field 
# applied in [1 1 1] direction.

mpirun -np 4 python 0-lmpsetup.py $a $alpha $nx $ny $nz

#-------------------------------------------------GNUPLOT
# Plot polarization 
gnuplot plot.gnu
