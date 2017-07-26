#set terminal postscript eps enhanced size 12in, 10in color font 'Helvetica,10'
#set out "figure.eps"

set term wxt 0
set title ""

set style line 1 lc rgb '#7CFC00' lt 1 lw 2 pt 7 pi -1 ps 0.75
set style line 2 lc rgb '#0060AD' lt 1 lw 2 pt 7 pi -1 ps 0.75
set style line 3 lc rgb '#FF0000' lt 1 lw 2 pt 7 pi -1 ps 0.75
set pointintervalbox 1

set xlabel "Electric Field (10^9 V/m)"
set ylabel "Polarization (10^8 C/m^2)"

set autoscale x
set autoscale y
#set xrange [0.:160.]
#set yrange [-0.075:0.30]
set key outside
plot "pol.dat" using 1:2 with linespoints ls 1 title "Px",\
"pol.dat" using 1:3 with linespoints ls 2  title "Py",\
"pol.dat" using 1:4 with linespoints ls 3  title "Pz",\
"pol2.dat" using 1:2 with linespoints ls 1 title "",\
"pol2.dat" using 1:3 with linespoints ls 2 title "",\
"pol2.dat" using 1:4 with linespoints ls 3 title ""

pause -1 "Hit any key to continue"
