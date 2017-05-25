#!/usr/bin/env gnuplot
set term pos eps color solid font ",35"

set size 0.85,1

#set xlabel "Cluster size (nodes)"
set logscale x 2 
set xrange[24:768]
set ytics 10
set yrange [0:35]


set xlabel "Cluster size (#nodes)\n"

set output "eps/flap.eps"
set title "(a) #Flaps (x1000)"
#set ylabel "#Flaps (x1000)"
set key top left
plot \
    "dat/flap-real.dat"      u 1:($2/1000) with lp t "Real" lw 8 pt 6 ps 2 lc rgb "red", \
    "dat/flap-simu.dat"       u 1:($2/1000) with lp t "SCk"  lw 8 pt 8 ps 2 lc rgb "blue", \
    "dat/flap-fixed-real.dat" u 1:($2/1000) with lp t "Real +Fix" lw 7 dt 2 pt 6 ps 2 lc rgb "red", \
    "dat/flap-fixed-simu.dat" u 1:($2/1000) with lp t "SCk +Fix"  lw 3 dt 2 pt 8 ps 2 lc rgb "blue", \

