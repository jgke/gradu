import csv
import sys

data = {}
languages = ['purkka']

with open('summary/all_measurements.csv') as f:
    reader = csv.DictReader(f)
    
    # format:
    #   name,lang,id,n,size(B),cpu(s),mem(KB),status,load,elapsed(s)
    for row in reader:
        name = row["name"]
        lang = row["lang"]
        data[name] = data.get(name, {})
        data[name][lang] = data[name].get(lang, {})
        n = int(row["n"])
        data[name][lang][n] = data[name][lang].get(n, [])
        data[name][lang][n].append(row)

gcc = {
        "elapsed(s)": {},
        "mem(KB)": {},
        "size(B)": {}
}

for benchmark in data:
    biggest_n = max(data[benchmark]['gcc'].keys())
    rows = data[benchmark]['gcc'][biggest_n]
    best = min(rows, key=(lambda x: float(x["elapsed(s)"])))
    print("Fastest GCC for {:<14} gcc-{} ({}s, {} kB, {} B)".format(
        benchmark + ":",
        best["id"],
        best["elapsed(s)"],
        best["mem(KB)"],
        best["size(B)"],
    ))
    gcc["elapsed(s)"][benchmark] = best["elapsed(s)"]
    gcc["mem(KB)"][benchmark] = best["mem(KB)"]
    gcc["size(B)"][benchmark] = best["size(B)"]

print()

for benchmark in data:
    print(benchmark)
    for language in languages:
        if language not in data[benchmark]:
            print("Language {} not found for benchmark {}".format(language, benchmark))
            break
    else:
        for language in languages:
            this = data[benchmark][language]
            biggest_n = max(this.keys())
            row = this[biggest_n][0]
            print("{}: time taken {}s, memory usage {} kB, file size {} B".format(benchmark, row["elapsed(s)"], row["mem(KB)"], row["size(B)"]))
            for ty in ["elapsed(s)", "mem(KB)", "size(B)"]:
                reference = float(gcc[ty][benchmark])
                current = float(row[ty])
                print("  {}: Compared to GCC: {:.2f}% (lower is better)".format(ty, 100+100*(current-reference)/reference))
            print("\n")
