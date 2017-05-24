#!/usr/bin/env gnuplot
set term pos eps color solid font ",27"

set size 0.7,0.85

    
################## whisker plot ################## 

set boxwidth 0.5 absolute
set bars 4.0
set style fill empty

set xrange[0:12]
set autoscale y

unset logscale x
unset logscale y

set logscale y 2

set key top left

set yrange[1:1e6]

set ytics (" 1e5" 100000, "1e4" 10000, "1e3" 1000, "1e2" 100, "1e1" 10, "1e0" 1)

set xlabel "Cluster size (#nodes)"

set output "eps/proc.eps"
set title "(f) Rebalance Process Time (ms)\nper Message in Riak (r3926)"
#set ylabel "Message processing time (sec)"
set xtics ("32" 1.5, "64" 4.5, "128" 7.5, "256" 10.5, "512" 13.5)

plot "dat/proc-real.dat" u 1:($4*1000):($3*1000):($7*1000):($6*1000) t "Real" with candlesticks whiskerbars lc rgb "red" lw 4, \
    "" u 1:($5*1000):($5*1000):($5*1000):($5*1000) with candlesticks lt -1 lc rgb "red" lw 2 notitle, \
    "dat/proc-simu.dat" u 1:($4*1000):($3*1000):($7*1000):($6*1000) t "SCk" with candlesticks whiskerbars lc rgb "blue" lw 4, \
    "" u 1:($5*1000):($5*1000):($5*1000):($5*1000) with candlesticks lt -1 lc rgb "blue" lw 2 notitle, \
