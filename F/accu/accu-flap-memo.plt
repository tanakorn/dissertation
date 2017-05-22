#!/usr/bin/env gnuplot
set term pos eps color solid font ",27"

set size 0.7,0.7

#set xlabel "Cluster size (nodes)"
set logscale x 2 
set xrange[24:768]
set ytics 10
set yrange [0:35]



set output "eps/flap_memo.eps"
set title "(a) #Flaps (x1000)"
#set ylabel "#Flaps (x1000)"
set key top left
plot \
    "dat/flap-real.dat"      u 1:($2/1000) with lp t "Real" lw 8 pt 6 ps 2 lc rgb "red", \
    "dat/flap-memo.dat"       u 1:($2/1000) with lp t "SCk-MEMO"  lw 8 pt 8 ps 2 lc rgb "blue"

