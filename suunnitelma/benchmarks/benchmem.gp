set term tikz size 8,6
set output "benchmarksmem.tex"

set style fill solid 0.25 border -1
set style boxplot outliers pointtype 7
set style data boxplot

set xtics ('C' 1, 'C++' 2, 'Rust' 3, 'Ada' 4, 'Go' 5)
set ylabel "kilotavua" offset -1
set style fill solid 1.0
set style boxplot nooutliers

set yrange [0 : 400]

plot for [i=1:5] "benchmarks_mem.csv" using (i):i notitle lt rgb "white"
