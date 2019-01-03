all: benchmarkscpu.tex benchmarksmem.tex benchmarkslines.tex

benchmarks_cpu.csv: data.csv scrape.py
	python3 scrape.py "cpu(s)" > benchmarks_cpu.csv
benchmarks_mem.csv: data.csv scrape.py
	python3 scrape.py "mem(KB)" > benchmarks_mem.csv
benchmarks_lines.csv: data.csv scrape.py
	python3 scrape.py "size(B)" > benchmarks_lines.csv

benchmarkscpu.tex: benchcpu.gp benchmarks_cpu.csv
	gnuplot benchcpu.gp
benchmarksmem.tex: benchmem.gp benchmarks_mem.csv
	gnuplot benchmem.gp
benchmarkslines.tex: benchlines.gp benchmarks_lines.csv
	gnuplot benchlines.gp
