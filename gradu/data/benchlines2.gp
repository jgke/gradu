set term tikz size 16,6
set output "benchmarkslines2.tex"

set title "foo"
set ylabel "\\shortstack{Lähdekoodissa tavuja\\\\ C:hen verrattuna (\\%)}" offset -1.5
set arrow front from -0.5,100 to 4.5,100 nohead dt "-"
set yrange [40 : 120]

set boxwidth 0.5
plot "benchmarks_lines2.csv" using 1:3:xtic(2) with boxes lc rgb "#000000" notitle
