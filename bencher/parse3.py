import csv
import sys

languages = ['gcc', 'purkka', 'gpp', 'rust', 'gnat', 'go']

action = sys.argv[1]
measurement = sys.argv[2]

abbrv_benchmark = {
    "binarytrees": "binary",
    "fannkuchredux": "fannkuch",
    "fasta": "fasta",
    "knucleotide": "knucleo",
    "nbody": "nbody",
    "pidigits": "pidigits",
    "regexredux": "regex",
    "spectralnorm": "spectrn",
}

fastest_gcc = {} 
best_gcc = {} 

raw_data = []

with open('summary/all_measurements.csv') as f:
    reader = csv.DictReader(f)

    for row in reader:
        raw_data.append(row) 

benchmarks = sorted(list(set(row["name"] for row in raw_data)))

max_n = {}
data = {}
best_data = {}

for benchmark in benchmarks:
    max_n[benchmark] = max(int(row["n"]) for row in raw_data if row["name"] == benchmark)

for benchmark in benchmarks:
    data[benchmark] = { row["lang"]: [] for row in raw_data if row["name"] == benchmark and row["lang"] in languages}
    best_data[benchmark] = { row["lang"]: [] for row in raw_data if row["name"] == benchmark and row["lang"] in languages}

for row in raw_data:
    benchmark = row["name"]
    n = row["n"]
    lang = row["lang"]

    if int(n) == max_n[benchmark] and lang in languages:
        data[benchmark][lang].append(row)

elapsed = "elapsed(s)"
mem = "mem(KB)"
size = "size(B)"

for benchmark in data:
    for lang in data[benchmark]:
        best_id = min(data[benchmark][lang], key=lambda x: x[elapsed])["id"]
        best_data[benchmark][lang] = list(row for row in data[benchmark][lang] if row["id"] == best_id)

data = None

gcc_averages = {}
for benchmark in benchmarks:
    gcc_averages[benchmark] = {}
    count = len(best_data[benchmark]['gcc'])
    gcc_averages[benchmark][elapsed] = sum(float(row[elapsed] )for row in best_data[benchmark]['gcc'])/count
    gcc_averages[benchmark][mem] = sum(float(row[mem]) for row in best_data[benchmark]['gcc'])/count
    gcc_averages[benchmark][size] = sum(float(row[size]) for row in best_data[benchmark]['gcc'])/count


for benchmark in benchmarks:
    for lang in best_data[benchmark]:
        for run in best_data[benchmark][lang]:
            print("{:>6}-{} {}: time taken {: >8}s/{: >7.2f}%, memory usage {: >6} kB/{: >6.2f}%, file size {: >7} B/{: >6.2f}%".format(
                run["lang"], run["id"],
                benchmark,
                run[elapsed], 100*float(run[elapsed])/gcc_averages[benchmark][elapsed],
                run[mem], 100*float(run[mem])/gcc_averages[benchmark][mem],
                run[size], 100*float(run[size])/gcc_averages[benchmark][size]))
    print()

if action == "all":
    print("# ", file=sys.stderr, end=' ')
    for lang in languages:
        print(lang, file=sys.stderr, end=' ')
    print(file=sys.stderr)
    for benchmark in benchmarks:
        for i in range(len(best_data[benchmark]['gcc'])):
            for lang in languages:
                if lang in best_data[benchmark] and len(best_data[benchmark][lang]) > i:
                    this = float(best_data[benchmark][lang][i][measurement])
                    reference = gcc_averages[benchmark][measurement]
                    print(100.0*this/reference, file=sys.stderr, end=' ')
                else:
                    print(100.0, file=sys.stderr, end=' ')
            print(file=sys.stderr)
    print(file=sys.stderr)
elif measurement != "size(B)":
    print("# ", file=sys.stderr, end=' ')
    for benchmark in benchmarks:
        if action in best_data[benchmark]:
            print(abbrv_benchmark.get(benchmark, benchmark[0:6]), file=sys.stderr, end=' ')
    print(file=sys.stderr)
    
    for i in range(len(best_data['binarytrees'][action])):
        for benchmark in benchmarks:
            if action in best_data[benchmark]:
                this = float(best_data[benchmark][action][i][measurement])
                reference = gcc_averages[benchmark][measurement]
                print(100.0*this/reference, file=sys.stderr, end=' ')
        print(file=sys.stderr)
elif action != "all":
    i = 0
    for benchmark in benchmarks:
        if action in best_data[benchmark]:
            this = float(best_data[benchmark][action][0][measurement])
            reference = gcc_averages[benchmark][measurement]
            print(i, abbrv_benchmark.get(benchmark, benchmark[0:6]), 100.0*this/reference, file=sys.stderr)
            i = i + 1
else:
    panic()
