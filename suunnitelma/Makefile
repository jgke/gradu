.PHONY: suunnitelma.txt
suunnitelma.txt:
	pandoc suunnitelma.tex -w plain -o - \
	    | sed -E "s/\[[^]]+\]//g" \
	    | sed -E "s/\(engl. [^)]+\)_//g" \
	    | sed -E "s/C\\+\\+:([a-z]+)/C++/g" \
	    | sed -E "s/[a-z]+(_[a-z]+)+ ?-/jonkin /g" \
	    | grep -v "Avainsanat ovat and, and" \
	    | grep -v "or_eq, xor" \
	    | sed "s/ / /g" > suunnitelma.txt
