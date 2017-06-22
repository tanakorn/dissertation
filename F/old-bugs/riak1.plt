#!/usr/bin/env gnuplot

set term pos eps color solid font 27 "NimbusSanL-Regu" fontfile "/usr/local/texlive/2014/texmf-dist/fonts/type1/urw/helvetic/uhvr8a.pfb"

set size 0.7,0.85

set output "eps/riak1.eps"
set title "(d) Duration (x1000 sec)\nof Riak Bootstrap (r3926)"
set key top left
#set ylabel "Bootstrapping time (s)"
set xlabel "Cluster size (#nodes)"
set logscale x 2
set xrange[24:384]
set yrange [0:12]

set ytics ("   0" 0, "   4" 4, "   8" 8, "  12" 12, "  16" 16)

#set ytics 8

plot\
  "dat/riak1-real.dat"     u 1:($2/1000) w lp t "Real" lw 8 pt 6 ps 2 lc rgb "red", \
  "dat/riak1-simu.dat"     u 1:($2/1000) w lp t "SCk"  lw 8 pt 8 ps 2 lc rgb "blue"


  # "dat/riak1-real-512.dat" u 1:($2/1000) w p not pt 3 ps 4 lc rgb "red",



