#!/usr/bin/env gnuplot
set term pos eps color solid font 35  "NimbusSanL-Regu" fontfile "/usr/local/texlive/2014/texmf-dist/fonts/type1/urw/helvetic/uhvr8a.pfb"
set size 0.85,1

set key top left

#set xlabel "Cluster size (nodes)"
set ytics 10
set yrange [0:35]

################## whisker plot ################## 

set boxwidth 0.5 absolute
set bars 4.0
set style fill empty

set xrange[0:16]
set autoscale y

set xlabel "Cluster size (#nodes)\n"
    
set output "eps/hb.eps"
set title "(c) T-lastGossip every A-B pair (sec)"
#set ylabel "Time (s)"
set xtics ("32" 1.5, "64" 4.5, "128" 7.5, "256" 10.5, "512" 13.5)
plot "dat/hb-real.dat" u 1:4:3:7:6 t "Real" with candlesticks whiskerbars lc rgb "red" lw 4, \
    "" u 1:5:5:5:5 with candlesticks lt -1 lc rgb "red" lw 4 notitle, \
    "dat/hb-simu.dat" u 1:4:3:7:6 t "SCk+PIL" with candlesticks whiskerbars lc rgb "blue" lw 2, \
    "" u 1:5:5:5:5 with candlesticks lt -1 lc rgb "blue" lw 2 notitle, \

