#!/bin/bash
# Looping over FastHenry and FastHenryPy

original_dir=$(pwd)

for h in $(seq 2 1 10)
do
	for g in $(seq 0.1 0.1 1.0)
	do	
		for w in $(seq 0.1 0.1 2.0)
		do
			for d in $(seq 3 1 5)
			do
				turns=1
				while [ $(echo "(3.14159*$d-$g)/(4*($w+$g))" |bc) -gt $turns ] && [ $(echo "2*$turns*w+(2*$turns-1)*g" |bc) -lt $h ]
				do
					mkdir "./$h,$g,$w,5,$turns"
					cd "./$h,$g,$w,5,$turns"
					python ~/documents/FastHenryPy/main.py $h $g $w 5 $turns ./FH.inp
					fasthenry ./FH.inp
					fasthenry ./FH.inp -f simple
					zbuf ./zbuf zbuffile -a90 -e80
					cd "$original_dir"
					((turns++)) #increment turns by one until geometry broken
				done
			done
		done
	done
done
echo All done
