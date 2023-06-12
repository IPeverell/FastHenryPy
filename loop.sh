#!/bin/bash
# Looping over FastHenry and FastHenryPy

original_dir=$(pwd)

for h in $(seq 2 1 10)
do
	for g in $(seq 0.1 0.1 1.0)
	do	
		for w in $(seq 0.1 0.1 2.0)
		do
			for d in $(seq 5 1 11)
			do
				turns=1
				while (( $(echo "(3.14159*$d-$g)/(4*($w+$g)) > $turns" |bc -l) )) && (( $(echo "2*$turns*$w+(2*$turns-1)*$g < $h" |bc -l) ))
				do
					mkdir "./$h,$g,$w,$d,$turns"
					cd "./$h,$g,$w,$d,$turns"
					python ~/documents/FastHenryPy/main.py $h $g $w $d $turns ./FH.inp
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
