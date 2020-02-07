all: benchmarkscpu.tex benchmarksmem.tex benchmarkslines.tex benchmarkscpu2.tex benchmarksmem2.tex benchmarkslines2.tex data.tex

SUMMARY=../../bencher/parse3.py ../../bencher/summary/all_measurements.csv

benchmarkscpu.tex: benchcpu.gp ${SUMMARY}
	(cd ../../bencher && python3 parse3.py all "elapsed(s)" >/dev/null 2> ../gradu/data/benchmarks_cpu.csv)
	gnuplot benchcpu.gp
benchmarksmem.tex: benchmem.gp ${SUMMARY}
	(cd ../../bencher && python3 parse3.py all "mem(KB)" >/dev/null 2> ../gradu/data/benchmarks_mem.csv)
	gnuplot benchmem.gp
benchmarkslines.tex: benchlines.gp ${SUMMARY}
	(cd ../../bencher && python3 parse3.py all "size(B)" >/dev/null 2> ../gradu/data/benchmarks_lines.csv)
	gnuplot benchlines.gp
benchmarkscpu2.tex: benchcpu2.gp ${SUMMARY}
	(cd ../../bencher && python3 parse3.py purkka "elapsed(s)" >/dev/null 2> ../gradu/data/benchmarks_cpu2.csv)
	gnuplot benchcpu2.gp
benchmarksmem2.tex: benchmem2.gp ${SUMMARY}
	(cd ../../bencher && python3 parse3.py purkka "mem(KB)" >/dev/null 2> ../gradu/data/benchmarks_mem2.csv)
	gnuplot benchmem2.gp
benchmarkslines2.tex: benchlines2.gp ${SUMMARY}
	(cd ../../bencher && python3 parse3.py purkka "size(B)" >/dev/null 2> ../gradu/data/benchmarks_lines2.csv)
	gnuplot benchlines2.gp

benchmarkcpu3.tex: benchmarkscpu.tex
	gnuplot benchcpu3.gp

benchmarkmem3.tex: benchmarksmem.tex
	gnuplot benchmem3.gp

data.tex: ${SUMMARY} data_to_tex.py
	python3 data_to_tex.py > data.tex
