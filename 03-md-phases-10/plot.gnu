#set terminal postscript eps enhanced size 12in, 10in color font 'Helvetica,10'
#set out "figure.eps"
set term wxt 0
set multiplot layout 2,1 title "Temperature dependence" font ",14"

#-------------------------------------------------FIGURE 1
set title ""

set style line 1 lc rgb '#7CFC00' lt 1 lw 2 pt 7 pi -1 ps 1.
set style line 2 lc rgb '#0060AD' lt 1 lw 2 pt 7 pi -1 ps 1.
set style line 3 lc rgb '#FF0000' lt 1 lw 2 pt 7 pi -1 ps 1.
set pointintervalbox 1

set xlabel "Temperature (Kelvin)"
set ylabel "Polarization (10^8 C/m^2)"

set autoscale x
set autoscale y
#set xrange [0.:160.]
set yrange [-0.02:0.20]
set key outside
plot "pol-tmp.dat" using 1:2 with linespoints ls 1 title "Px", \
"pol-tmp.dat" using 1:3 with linespoints ls 2  title "Py", \
"pol-tmp.dat" using 1:4 with linespoints ls 3  title "Pz"

#-------------------------------------------------FIGURE 2
set title ""

set xlabel "Temperature (Kelvin)"
set ylabel "Lattice Parameters (Angstrom)"

set style line 1 lc rgb '#7CFC00' lt 1 lw 2 pt 7 pi -1 ps 1.
set style line 2 lc rgb '#0060AD' lt 1 lw 2 pt 7 pi -1 ps 1.
set style line 3 lc rgb '#FF0000' lt 1 lw 2 pt 7 pi -1 ps 1.
set pointintervalbox 1

set autoscale x
set autoscale y

#set xrange [0.:160.]
set yrange [3.97:4.06]
set key outside
plot "pol-tmp.dat" using 1:6 with linespoints ls 1 title "a", \
"pol-tmp.dat" using 1:7 with linespoints ls 2  title "b", \
"pol-tmp.dat" using 1:8 with linespoints ls 3  title "c"

unset multiplot

set term wxt 1
set title ""

set style line 1 lc rgb '#7CFC00' lt 1 lw 2 pt 7 pi -1 ps 1.
set style line 2 lc rgb '#0060AD' lt 1 lw 2 pt 7 pi -1 ps 1.
set style line 3 lc rgb '#FF0000' lt 1 lw 2 pt 7 pi -1 ps 1.
set pointintervalbox 1

set xlabel "Temperature (Kelvin)"
set ylabel "Polarization (10^8 C/m^2)"

set autoscale x
set autoscale y
#set xrange [0.:160.]
set yrange [-0.02:0.15]
set key outside

plot "pol-tmp.dat" using 1:2 with linespoints ls 1 title "Px", \
"pol-tmp.dat" using 1:3 with linespoints ls 2  title "Py", \
"pol-tmp.dat" using 1:4 with linespoints ls 3  title "Pz"

set xlabel "Temperature (Kelvin)"
set ylabel "Lattice Parameters (Angstrom)"

set style line 1 lc rgb '#7CFC00' lt 1 lw 2 pt 7 pi -1 ps 1.
set style line 2 lc rgb '#0060AD' lt 1 lw 2 pt 7 pi -1 ps 1.
set style line 3 lc rgb '#FF0000' lt 1 lw 2 pt 7 pi -1 ps 1.
set pointintervalbox 1

set term wxt 2
set title ""
set autoscale x
set autoscale y
#set xrange [0.:160.]
set yrange [3.97:4.06]
set key outside
plot "pol-tmp.dat" using 1:6 with linespoints ls 1 title "a", \
"pol-tmp.dat" using 1:7 with linespoints ls 2  title "b", \
"pol-tmp.dat" using 1:8 with linespoints ls 3  title "c"

pause -1 "Hit any key to continue"
