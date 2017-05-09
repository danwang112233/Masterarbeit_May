#!/bin/bash

#-------------------------------------------------LATTICE PARAMETER a
a="4.010"

#-------------------------------------------------LATTICE PARAMETER alpha
alpha="89.81"

#-------------------------------------------------REPLICAS IN EACH DIRECTION
n="5"

#-------------------------------------------------GENERATE DATA FILE
python molsetup.py $a $n

#-------------------------------------------------SPONTANEOUS POLARIZATION
# 0-lmpsetup.py 
# Calculating Spontaneous polarization through Molecular Static Simulation 
# of Rhombohedral Barium Titanate at 0K with an electric field applied 
# in [1 1 1] direction.

#mpirun -np 8 python 0-lmpsetup.py $a $alpha $n

#-------------------------------------------------POLARIZATION HYSTERESIS LOOP
# 1-lmpsetup.py 
# Write Polarization Vs Electric Field to file after  Molecular Static 
# Simulation of Rhombohedral Barium Titanate at 0K with an electric field 
# applied in [1 1 1] direction.

mpirun -np 8 python 1-lmpsetup.py $a $alpha $n

#-------------------------------------------------GNUPLOT
gnuplot plot.gnu
