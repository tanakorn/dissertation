#!/usr/bin/env gnuplot

set term pos eps color solid font ",27"

set size 0.7,0.75
set output "eps/vold1.eps"
set title "(e) Duration (x1000 sec) of\nVoldemort Rebalance (v1212)"
set key top left
#set ylabel "Rebalance time (s)"
#set xlabel "Cluster size (nodes)"
set logscale x 2
set xrange[24:384]
set yrange[0:99]

set ytic 20

plot "dat/vold1-real.dat" u 1:($2/1000) w lp title "Real" lw 8 pt 6 ps 2 lc rgb "red", \
     "dat/vold1-test.dat" u 1:($2/1000) w lp title "SCk"  lw 8 pt 8 ps 2 lc rgb "blue"

