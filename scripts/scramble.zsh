#!/usr/bin/env zsh

./scramble.run forest01.txt.out 500 200 2
tac forest01.txt.out
tac forest01.txt.out > forest01
mv forest01 forest01.txt.out

./scramble.run forest02.txt.out 1000 1000 2

cat forest03.txt.out | sort -R | sort -R > forest03
mv forest03 forest03.txt.out

./scramble.run forest04.txt.out 1000 1000 2
tac forest04.txt.out > forest04
mv forest04 forest04.txt.out

./scramble.run forest05.txt.out 1000 1000 2
tac forest05.txt.out > forest05
mv forest05 forest05.txt.out

./scramble.run forest06.txt.out 1800 200 2

./scramble.run forest07.txt.out 1800 200 2
tac forest07.txt.out > forest07
mv forest07 forest07.txt.out

# forest09 as is

tac forest09.txt.out > forest09
mv forest09 forest09.txt.out

# forest10 as is

./scramble.run forest11.txt.out 4000 4000 2

./scramble.run forest12.txt.out 600 300 1

./scramble.run forest13.txt.out 1600 1600 2
