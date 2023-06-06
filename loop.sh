#!/bin/bash
# Looping over FastHenry and FastHenryPy

for h in $(seq 2 1 10)
do
	for g in $(seq 0.1 0.1 1.0)
	do	
		for w in $(seq 0.1 0.1 2.0)
		do
			for d in $(seq 3 1 5)
			do
				turns=1
				while [$(echo "(3.14159*$d-$g-$w)/(4*$w)" |bc) -gt $turns] && [ $(echo "$h/$w" |bc) -gt $turns]
				do
					mkdir ./$h,$g,$w,5,$turns
					cd ./$h,$g,$w,5,$turns
					python ~/FastHenryPy/main.py $h $g $w 5 $turns ./FH.inp
					fasthenry ./FH.inp
					fasthenry ./FH.inp -f simple
					zbuf ./zbuf zbuffile -a90 -e80
				done
			done
		done
	done
done
echo All done
