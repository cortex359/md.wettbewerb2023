#!/usr/bin/env zsh

function plot_and_optimize() {
    local i=$1
    python plot.py ../input/forest${i}.txt result_files/current_best/forest${i}.txt.out forest${i} && npx svgo plots/forest${i}.svg
}

function plot_and_optimize_all() {
    for i in {01..14} ; do {
        plot_and_optimize $i &
    }; done
}

function check_all() {
    for i in {01..14} ; do {
        env LC_ALL=en_US java -jar ../vendor/checker.jar ../input/forest${i}.txt result_files/current_best/forest${i}.txt.out
    }; done
}
