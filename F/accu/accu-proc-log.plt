#!/usr/bin/env gnuplot
set term pos eps color solid font 35   "NimbusSanL-Regu" fontfile "/usr/local/texlive/2014/texmf-dist/fonts/type1/urw/helvetic/uhvr8a.pfb"
set size 0.85,1

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
    
# --------------

set key off

set logscale y 2
set yrange[1:24000]
#set yrange[1:9000]
set ytics ("1e4" 10000, "1e3" 1000, "1e2" 100, "1e1" 10, "1e0" 1)
set output "eps/proc-log.eps"
set title "(d) Update process time (ms)"
#set ylabel "Time (ms)"
set xtics ("32" 1.5, "64" 4.5, "128" 7.5, "256" 10.5, "512" 13.5)
plot "dat/proc-real.dat" u 1:($4*1000):($3*1000):($7*1000):($6*1000) t "Real" with candlesticks whiskerbars lc rgb "red" lw 4, \
    "" u 1:($5*1000):($5*1000):($5*1000):($5*1000) with candlesticks lt -1 lc rgb "red" lw 4 notitle, \
    "dat/proc-simu.dat" u 1:($4*1000):($3*1000):($7*1000):($6*1000) t "SCk+PIL" with candlesticks whiskerbars lc rgb "blue" lw 2, \
    "" u 1:($5*1000):($5*1000):($5*1000):($5*1000) with candlesticks lt -1 lc rgb "blue" lw 2 notitle, \
