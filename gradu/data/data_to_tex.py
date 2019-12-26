import csv

print("\\newgeometry{left=1.5cm,right=1.5cm,bottom=2cm}")
print("\\appendixsection{Mittaukset}")
print("\\appendixlabel{app:data}")
print("\\hl{Tänne lähdeviittaukset? Ehkä ainakin benchmarkkien selitteet?}")

rev_abbrev = {
    "keskiarvo": "keskiarvo",
    "binary": "binarytrees",
    "fannku": "fannkuchredux",
    "fasta": "fasta",
    "knucleo": "knucleotide",
    "nbody": "nbody",
    "pidigits": "pidigits",
    "regex": "regexredux",
    "spectrn": "spectralnorm",
    "revcom": "revcomp",
}

rev_lang = {
    "gcc": "C",
    "gpp": "C++",
    "rust": "Rust",
    "go": "Go",
    "gnat": "Ada",
    "purkka": "Purkka",
}

benchmarks = ["binarytrees", "fannkuchredux", "fasta", "knucleotide", "nbody",
        "pidigits", "regexredux", "spectralnorm", "revcomp"]
languages = ["gcc", "gpp", "rust", "go", "gnat", "purkka"]

raw_data = []

with open('../../bencher/summary/all_measurements.csv') as f:
    reader = csv.DictReader(f)

    for row in reader:
        raw_data.append(row) 

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

for benchmark in data:
    for lang in data[benchmark]:
        best_id = min(data[benchmark][lang], key=lambda x: x["elapsed(s)"])["id"]
        best_data[benchmark][lang] = list(row for row in data[benchmark][lang] if row["id"] == best_id)

def fint(num):
    l = list(num)[::-1]
    res = map(lambda x: "".join(x), [ l[i:i+3] for i in range(0, len(l), 3) ])
    return ",\\".join(res)[::-1]

print("{\large \\textbf{Suoritusaika(s)}} \\\\")
print("\\small")
print()
newline = False
for benchmark in benchmarks:
    print("\\begin{minipage}{0.49\\textwidth}")
    print("\\noindent\\textbf{", benchmark, "} \\\\[0.3cm]", sep="")
    print("\\begin{tabular}{@{} l l @{}} \\toprule")
    print("Kieli & Mittaukset \\\\ \\midrule")
    for lang in languages:
        print(f"{rev_lang[lang]} & {', '.join(map(lambda x: x['elapsed(s)'], best_data[benchmark][lang]))}\\\\")
    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\end{minipage}")
    if newline:
        print()
        newline = False
    else:
        print("\\hfill")
        newline = True

print("\\\\[1cm] {\large \\textbf{Muistinkäyttö(KB)}} \\\\")
print("\\small")
print()
newline = False
for benchmark in benchmarks:
    print("\\begin{minipage}{0.49\\textwidth}")
    print("\\noindent\\textbf{", benchmark, "} \\\\[0.3cm]", sep='')
    print("\\begin{tabular}{@{} l l @{}} \\toprule")
    print("Kieli & Mittaukset \\\\ \\midrule")
    for lang in languages:
        print(f"{rev_lang[lang]} & {', '.join(map(lambda x: fint(x['mem(KB)']), best_data[benchmark][lang]))}\\\\")
    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\end{minipage}")
    if newline:
        print()
        newline = False
    else:
        print("\\hfill")
        newline = True

print("\\\\[1cm] {\large \\textbf{Lähdekoodin koko (B)}} \\\\")
print("Lähdekoodin koko on mitattu poistamalla lähdekoodista kaikki kommentit sekä tyhjemerkit. Tämän jälkeen ohjelma ajetaan \\texttt{gzip}-pakkausohjelman läpi, ja mitataan pakatun lähdekoodin koko.")
print("\\small")
print()
newline = 1
for benchmark in benchmarks:
    print("\\begin{minipage}{0.19\\textwidth}")
    print("\\noindent\\textbf{", benchmark, "} \\\\[0.3cm]", sep='')
    print("\\begin{tabular}{@{} l l @{}} \\toprule")
    print("Kieli & Koko \\\\ \\midrule")
    for lang in languages:
        print(f"{rev_lang[lang]} & {fint(best_data[benchmark][lang][0]['size(B)'])}\\\\")
    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\end{minipage}")
    if newline % 5 == 0:
        print()
    else:
        print("\\hfill")
    newline += 1

print("\\begin{minipage}{0.19\\textwidth}")
print("\\hfill")
print("\\end{minipage}")
