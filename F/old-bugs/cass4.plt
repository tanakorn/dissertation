#!/usr/bin/env gnuplot

set term pos eps color solid font ",27"

set size 0.7,0.75

#set yrange[0:1200000]
set output "eps/cass4.eps"
set title "(c) #Flaps (x1000) in\n Cassandra Scale-Out (c5456)"
set key top left
#set ylabel "#False failure detection"
#set xlabel "Cluster size (nodes)"
set logscale x 2
set xrange[24:384]

set ytics ("   8" 8, "   6" 6, "   4" 4, "   2" 2)


#set size 0.9,1

set yrange[0:8]

plot \
  "dat/cass4-real.dat"    u 1:($2/1000) with lp t "Real" lw 8 pt 6 ps 2 lc rgb "red", \
  "dat/cass4-simu.dat"       u 1:($2/1000) with lp t "SCk" lw 8 pt 8 ps 2 lc rgb "blue"


#  "dat/cass4-fixed-real.dat" using 1:2 with linespoint title "Real Fixed" lw 7 pt 2 dt 2 ps 2 lc rgb "red", \  


