set term tikz size 8,6
set output "benchmarkslines.tex"

set style fill solid 0.25 border -1
set style boxplot outliers pointtype 7
set style data boxplot

set xtics ('C' 1, 'C++' 2, 'Rust' 3, 'Ada' 4, 'Go' 5)
set ylabel "\\shortstack{Lähdekoodissa tavuja \\\\ C:hen verrattuna (\\%)}" offset -1.5
set style fill solid 1.0
set style boxplot nooutliers

set arrow 1 from graph 0,first 100 to graph 1,first 100 nohead dt "-"

set yrange [0 : 370]

plot for [i=2:5] "benchmarks_lines.csv" using (i):i notitle lt rgb "white"
