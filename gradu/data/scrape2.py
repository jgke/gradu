import csv
import sys

language = 'purkka'

fastest_gcc = {} 
best_gcc = {} 

raw_data = []

with open('summary/all_measurements.csv') as f:
    reader = csv.DictReader(f)

    for row in reader:
        raw_data.append(row) 

benchmarks = list(set(row["name"] for row in raw_data))

n = {}

for benchmark in benchmarks:
    n[benchmark] = max(row["n"] for row in raw_data if row["name"] == benchmark)

data = {benchmark:
        {row["lang"]: [] for row in raw_data if row["name"] == benchmark}
        for benchmark in benchmarks}

print(data)
