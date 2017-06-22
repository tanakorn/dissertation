#!/usr/bin/env gnuplot

set term pos eps color solid font 27 "NimbusSanL-Regu" fontfile "/usr/local/texlive/2014/texmf-dist/fonts/type1/urw/helvetic/uhvr8a.pfb"
set size 0.7,0.75

#set yrange[0:1200000]
set output "eps/cass2.eps"
set title "(a) #Flaps (x1000) in\n Cassandra Decommission (c3831)"
set key top left
#set ylabel "#False failure detection"
#set xlabel "Cluster size (nodes)"
set logscale x 2
set xrange[24:384]

set ytics 100

#set size 0.9,1

set yrange[0:320]

plot \
  "dat/cass2-real.dat" u 1:($2/1000) with lp t "Real" lw 8 pt 6 ps 2 lc rgb "red", \
  "dat/cass2-simu.dat" u 1:($2/1000) with lp t "SCk"  lw 8 pt 8 ps 2 lc rgb "blue"


  
  #  "dat/cass2-fixed-real.dat" u 1:($2/1000) with lp t "Real Fixed" lw 7 pt 2 dt 2 ps 2 lc rgb "red", \
