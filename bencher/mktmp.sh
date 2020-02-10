#!/bin/sh

trap "exit" INT
set -eu

cd "$(dirname "$0")"

mkdir -p tmp

#python2 bin/bencher.py

./tmp/fasta/tmp/fasta.*_run 250000 > tmp/knucleotide/knucleotide-input250000.txt 
./tmp/fasta/tmp/fasta.*_run 2500000 > tmp/knucleotide/knucleotide-input2500000.txt 
./tmp/fasta/tmp/fasta.*_run 25000000 > tmp/knucleotide/knucleotide-input25000000.txt 

./tmp/fasta/tmp/fasta.*_run 50000 > tmp/regexredux/regexredux-input50000.txt 
./tmp/fasta/tmp/fasta.*_run 500000 > tmp/regexredux/regexredux-input500000.txt 
./tmp/fasta/tmp/fasta.*_run 5000000 > tmp/regexredux/regexredux-input5000000.txt 

./tmp/fasta/tmp/fasta.*_run 250000 > tmp/revcomp/revcomp-input250000.txt 
./tmp/fasta/tmp/fasta.*_run 100000000 > tmp/revcomp/revcomp-input100000000.txt 
