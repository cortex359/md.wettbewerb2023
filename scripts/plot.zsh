#!/usr/bin/env zsh

projectPath="/${(j./.)${(s./.)PWD}[1,${${(s./.)PWD}[(I)md.wettbewerb2023]}]}"

function plot_and_optimize() {
    local i=$1
    python ${projectPath}/scoring/plot.py ${projectPath}/input/forest${i}.txt ${projectPath}/results/current_best/forest${i}.txt.out forest${i} \
      && npx svgo ${projectPath}/scoring/plots/forest${i}.svg \
      && cp ${projectPath}/scoring/plots/forest${i}.svg ${projectPath}/results/current_best/plots/forest${i}.svg
}

function plot_and_optimize_all() {
    for i in {01..14} ; do {
        plot_and_optimize $i &
    }; done
}

function check_all() {
    for i in {01..14} ; do {
        env LC_ALL=en_US java -jar ${projectPath}/vendor/checker.jar ${projectPath}/input/forest${i}.txt ${projectPath}/results/current_best/forest${i}.txt.out
    }; done
}
