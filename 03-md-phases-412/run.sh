
#!/bin/bash

#-------------------------------------------------LATTICE PARAMETER a
a="4.010"

#-------------------------------------------------LATTICE PARAMETER c/a
cbya="1.011"

#-------------------------------------------------REPLICAS IN EACH DOMAIN
nx="10"
ny="10"
nz="12"

#-------------------------------------------------NUMBER OF DOMAINS
m="1"

#-------------------------------------------------NUMBER OF UPWARD POLLED UNITCELLS
up="12"

#-------------------------------------------------GENERATE DATA FILE
python molsetup.py $a $cbya $nx $ny $nz $m

#-------------------------------------------------SPONTANEOUS POLARIZATION
# 0-lmpsetup.py
# Write Polarization Vs Temperature to file after  Molecular Static
# Simulation of Rhombohedral Barium Titanate at 0K with an electric field
# applied in [1 1 1] direction.

#mpirun -np 8 python 0-lmpsetup.py $a $cbya $n $m

# NPT ensemble
mpirun -np 8 python 1-lmpsetup.py $a $cbya $nx $ny $nz $m $up

#-------------------------------------------------GNUPLOT
# Plot polarization
#gnuplot plot.gnu
