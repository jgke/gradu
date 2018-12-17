tmpfile=$(mktemp)
for i in `cat benchmarks-list`; do
    curl $i > $tmpfile 2>/dev/null
    grep "title" $tmpfile | head -n 1 | sed "s/.*>//" | sed "s/<.*//"
    echo -n "C "
    grep -P -A 2 'C(?!a).*gcc' $tmpfile | grep best | sed 's/.*>//'
    echo -n "C++ "
    grep -A 2 "C++" $tmpfile | grep best | sed "s/.*>//"
    echo -n "Rust "
    grep -A 2 "Rust" $tmpfile | grep best | sed "s/.*>//"
    echo -n "Go "
    grep -A 2 "Go" $tmpfile | grep best | sed "s/.*>//"
    echo -n "Ada "
    grep -A 2 "Ada" $tmpfile | grep best | sed "s/.*>//"
done
