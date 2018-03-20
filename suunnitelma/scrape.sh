#!/bin/bash

OAUTH=0b74967f92022394a7385cec6d46658dc04d4fcb

LICENSES="afl-3.0 apache-2.0 artistic-2.0 bs1-1.0 bsd-2-clause bsd-3-clause bsd-3-clause-clear cc cc0-1.0 cc-by-4.0 cc-by-sa-4.0 wtfpl ecl-2.0 epl-1.0 eupl-1.1 agpl-3.0 gpl gpl-2.0 gpl-3.0 lgpl lgpl-2.1 lgpl-3.0 isc lppl-1.3c ms-pl mit mpl-2.0 osl-3.0 postgresql ofl-1.1 ncsa unlicense zlib"
LANGUAGES="Ada C C%2B%2B D Go Java JavaScript Rust TypeScript"

SEP="&"

echo -n "\\begin{tabular}{l l "
for lang in $LANGUAGES; do
    echo -n "l "
done
echo "} \\toprule"
for lang in $LANGUAGES; do
    echo -n "$SEP" "$lang "
done
echo "\\\\ \\midrule"

for lic in $LICENSES; do
    echo -n "$lic"
    for lang in $LANGUAGES; do
        count=$(curl -sH "Authorization: token $OAUTH" "https://api.github.com/search/repositories?q=license:$lic+language:$lang" |jq -r ".total_count")
        echo -n " $SEP" "$count" 
    done
    echo " \\\\"
    sleep 60
done
echo "\\bottomrule\n\\end{tabular}"
