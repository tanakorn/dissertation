set term pos eps size 7 in, 9.25 in
set style data histogram
set style histogram rowstacked
set style fill solid border lt -1
set boxwidth 0.5

set output '../eps/all.eps'

# for dashed line placement
stats '../dat/zookeeper.dat' using 3:4 name 'zk' nooutput
stats '../dat/mapreduce.dat' using 3:4 name 'mr' nooutput
stats '../dat/cassandra.dat' using 3:4 name 'ca' nooutput

set size 1,0.12
set border 3
set xtics out nomirror rotate by 60 offset character -1.5, -1.7, 0
set bmargin 3
set ylabel "Number of\nCrashes/Reboots"
set ytics out nomirror
set arrow from zk_records + 1.5,0 to zk_records + 1.5,6 nohead ls 2
set arrow from zk_records + mr_records + 2 + 1.5,0 to zk_records + mr_records + 2 + 1.5,6 nohead ls 2
plot '../dat/zookeeper.dat' u 3 title '#Crashes ' lt 1 lc rgb 'black', '' u 4:xticlabel(2) title '#Restarts ' lt 1 lc rgb 'grey', \
     newhistogram, '../dat/mapreduce.dat' u 3 notitle lt 1 lc rgb 'black', '' u 4:xticlabel(2) notitle lt 1 lc rgb 'grey', \
     newhistogram, '../dat/cassandra.dat' u 3 notitle lt 1 lc rgb 'black', '' u 4:xticlabel(2) notitle lt 1 lc rgb 'grey';

