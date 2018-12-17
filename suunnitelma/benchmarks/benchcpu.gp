set term tikz size 8,6
set output "benchmarkscpu.tex"

set style fill solid 0.25 border -1
set style boxplot outliers pointtype 7
set style data boxplot

set xtics ('C' 1, 'C++' 2, 'Rust' 3, 'Ada' 4, 'Go' 5)
set ylabel "sekuntia" offset -1
set style fill solid 1.0
set style boxplot nooutliers

set yrange [0 : 30]

plot for [i=1:5] "benchmarks_cpu.csv" using (i):i notitle lt rgb "white"
