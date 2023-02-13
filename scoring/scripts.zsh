#!/usr/bin/env zsh

forest=forest03

for seg in $(seq 0 0.25 1.75); do
    { for i in $(seq $((seg)) 0.001 ${${$((seg + 0.25))}[0,5]} ); do {
        ./bin/Release-linux-x86_64/04/04 inputs/${forest}.txt results/${forest}.w${i}.txt ${i}
      }; done
    } &
; done
