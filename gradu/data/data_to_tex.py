import csv

print("\\appendixsection{Mittaukset}")
print("\\appendixlabel{app:data}")
print("\\begingroup")

print("{\large \\textbf{Ohjelmien selitteet}}")

print()
print("\\noindent\\textbf{binarytrees} \\\\[0.1cm]", sep="")
print("Ohjelma on moniosainen: ensin luodaan binääripuu ja poistetaan se. Tämän jälkeen luodaan binääripuu, joka poistetaan vasta ohjelman loputtua. Tämän jälkeen luodaan useita binääripuita, joista lasketaan solmujen määrä.")

print()
print("\\noindent\\textbf{fannkuchredux} \\\\[0.1cm]", sep="")
print("Ohjelma laskee jokaiselle joukon ${1,...,n}$ permutaatioista tarkistussumman, joka lasketaan seuraavalla kaavalla: permutaatiosta otetaan ensimmäinen luku $x$. Permutaation ensimmäisen $x$ alkion järjestys muutetaan päinvastaiseksi. Näitä kahta operaatiota toistetaan, kunnes ensimmäinen alkio on 1. Jos permutaatio on pariton, tarkistussumma on kierrosten määrä, muuten tämän negaatio. Tarkistussummat lasketaan yhteen.")

print()
print("\\noindent\\textbf{fasta} \\\\[0.1cm]", sep="")
print("Ohjelmassa luodaan suuri määrä DNA-sekvenssejä joko kopioiden annettua sekvenssiä tai painotetulla satunnaisella valinnalla kahdesta aakkostosta.")

print()
print("\\noindent\\textbf{knucleotide} \\\\[0.1cm]", sep="")
print("Ohjelma lukee \emph{fasta}-ohjelman luoman tiedoston ja laskee siinä esiintyvien nukleotidisarjojen määrän 1, 2, 3, 4, 6, 12 ja 18 nukleotidin pituisille sarjoille.")

print()
print("\\noindent\\textbf{nbody} \\\\[0.1cm]", sep="")
print("Ohjelmassa simuloidaan symplektisellä integroinnilla planeettojen sijaintia.")

print()
print("\\noindent\\textbf{pidigits} \\\\[0.1cm]", sep="")
print("Ohjelmassa lasketaan $\pi$:n desimaaleja tietyllä algoritmilla.")

print()
print("\\noindent\\textbf{regexredux} \\\\[0.1cm]", sep="")
print("Ohjelma lukee \emph{fasta}-ohjelman muodostaman tiedoston ja ajaa ennalta määritettyjä säännöllisiä lausekkeita tiedoston sisältöön.")


print()
print("\\noindent\\textbf{spectralnorm} \\\\[0.1cm]", sep="")
print("Ohjelma laskee annetun matriisin spektraalisäteen.")

print()
print("\\noindent\\textbf{revcomp} \\\\[0.1cm]", sep="")
print("Ohjelma lukee \emph{fasta}-ohjelman muodostaman tiedoston ja muodostaa tiedoston DNA-sekvenssien komplementin.")

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
    return "\\verythinspace "[::-1].join(res)[::-1]

print()
print("{\large \\textbf{Suoritusaika(s)}} \\\\")
print("\\footnotesize")
print()
newline = False
#print("\\begin{adjustbox}{center}")
for benchmark in benchmarks:
    print("\\begin{minipage}{0.49\\textwidth}")
    print("\\noindent\\textbf{", benchmark, "} \\\\[0.1cm]", sep="")
    print("\\begin{tabularx}{\linewidth}{@{} l l @{}} \\toprule")
    print("Kieli & Mittaukset \\\\ \\midrule")
    for lang in languages:
        print(f"{rev_lang[lang]} & {', '.join(map(lambda x: x['elapsed(s)'], best_data[benchmark][lang]))}\\\\")
    print("\\bottomrule")
    print("\\end{tabularx}")
    print("\\end{minipage}")
    if newline:
        print("\\\\[0.3cm]")
        #print("\\end{adjustbox}")
        #print("")
        #print("\\begin{adjustbox}{center}")
        newline = False
    else:
        print("\\hfill")
        newline = True

#print("\\end{adjustbox}")
print("\hspace{1cm}")

print("\\\\[1cm] {\large \\textbf{Muistinkäyttö(KB)}} \\\\[0.3cm]")
print("{\\normalsize Muistinkäyttö on mitattu 200 millisekunnin välein \\texttt{libgtop2}-kirjastolla ja kunkin suorituksen muistinkäytöksi on merkitty suurin mitattu muistikäyttö.}")
print("\\footnotesize")
print()
newline = False
for benchmark in benchmarks:
    width = {
            "binarytrees": 0.54,
            "fannkuchredux": 0.44,
            "fasta": 0.46,
            "knucleotide": 0.52,
            "nbody": 0.46,
            "pidigits": 0.46,
            "regexredux": 0.54,
            "spectralnorm": 0.44,
            "revcomp": 0.60
    }
    print(f"\\begin{{minipage}}{{{width[benchmark]}\\textwidth}}")
    print("\\noindent\\textbf{", benchmark, "} \\\\[0.3cm]", sep='')
    print("\\begin{tabularx}{\\linewidth}{@{} l l @{}} \\toprule")
    print("Kieli & Mittaukset \\\\ \\midrule")
    for lang in languages:
        print(f"{rev_lang[lang]} & {', '.join(map(lambda x: fint(x['mem(KB)']), best_data[benchmark][lang]))}\\\\")
    print("\\bottomrule")
    print("\\end{tabularx}")
    print("\\end{minipage}")
    if newline:
        print()
        newline = False
    else:
        print("\\hfill")
        newline = True

print("\\\\[1cm] {\large \\textbf{Lähdekoodin koko (B)}} \\\\[0.3cm]")
print("{\\normalsize Lähdekoodin koko on mitattu poistamalla lähdekoodista kaikki kommentit sekä tyhjämerkit, jotta lähdekoodin asettelu ei vaikuta mittauksiin. Tämän jälkeen ohjelma ajetaan \\texttt{gzip}-pakkausohjelman läpi ja mitataan pakatun lähdekoodin koko.}")
print("\\footnotesize")
print()
newline = 1
for benchmark in benchmarks:
    print("\\begin{minipage}{0.19\\textwidth}")
    print("\\noindent\\textbf{", benchmark, "} \\\\[0.1cm]", sep='')
    print("\\begin{tabular}{@{} l l @{}} \\toprule")
    print("Kieli & Koko \\\\ \\midrule")
    for lang in languages:
        print(f"{rev_lang[lang]} & {fint(best_data[benchmark][lang][0]['size(B)'])}\\\\")
    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\end{minipage}")
    if newline % 5 == 0:
        print("\\\\[0.1cm]")
    else:
        print("\\hfill")
    newline += 1

print("\\begin{minipage}{0.19\\textwidth}")
print("\\hfill")
print("\\end{minipage}")
print("\\endgroup")
