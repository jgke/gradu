import csv
import sys

field = sys.argv[1]

with open('data.csv') as f:
    reader = csv.DictReader(f)

    data = {}

    languages = ['gcc', 'gpp', 'rust', 'gnat', 'go']

    # name,lang,id,n,size(B),cpu(s),mem(KB),status,load,elapsed(s)
    for row in reader:
        name = row["name"]
        lang = row["lang"]
        data[name] = data.get(name, {})
        if float(row[field]) > 0 and (not data[name].get(lang) or data[name][lang] > float(row[field])):
            data[name][row["lang"]] = float(row[field])

print("C C++ Rust Ada Go")

for benchmark in data:
    for language in languages:
        if language not in data[benchmark]:
            break
    else:
        for language in languages:
            this = data[benchmark][language]
            reference = data[benchmark]['gcc']
            print(100+100*(this-reference)/reference,end=' ')
    print()
