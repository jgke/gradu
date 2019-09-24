set term tikz size 16,6 createstyle
set output "benchmarksmem2.tex"

set style fill solid 0.25 border -1
set style boxplot outliers pointtype 7
set style data boxplot

header = "`head -1 benchmarks_mem2.csv | cut -b 2-`"
set for [i=1:words(header)] xtics (word(header, i) i)

set ylabel "\\shortstack{Muistinkäyttö kesto\\\\ C:hen verrattuna (\\%)}" offset -1.5
set style fill solid 1.0
set style boxplot nooutliers

set arrow 1 from graph 0,first 100 to graph 1,first 100 nohead dt "-"

#set yrange [80 : 110]

plot for [i=1:5] "benchmarks_mem2.csv" using (i):i notitle lt rgb "white"
