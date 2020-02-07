set term tikz size 8,6 createstyle
set output "benchmarkscpu3.tex"

set style fill solid 0.25 border -1
set style boxplot outliers pointtype 7
set style data boxplot

set xtics ('C' 1, 'Prk' 2, 'C++' 3, 'Rust' 4, 'Ada' 5, 'Go' 6)
set ylabel "\\shortstack{Suorituksen kesto\\\\ C:hen verrattuna (\\%)}" offset -1.5
set style fill solid 1.0
set style boxplot nooutliers

set arrow 1 from graph 0,first 100 to graph 1,first 100 nohead dt "-"

set yrange [40 : 3000]
set logscale y 10

plot for [i=2:6] "benchmarks_cpu.csv" using (i):i notitle lt rgb "white"
