#!/usr/bin/env zsh

projectPath="/${(j./.)${(s./.)PWD}[1,${${(s./.)PWD}[(I)md.wettbewerb2023]}]}"

function check_files() {
  if (( ARGC < 2 )) {
    echo "${0} [01..14] [resultFile1] [resultFile2] [...]"
    return -1
  }
  i=$1
  for a in ${argv[2,-1]} ; do
    env LC_ALL=en_US java -jar ${projectPath}/vendor/checker.jar ${projectPath}/input/forest${i}.txt ${a:a}
  done
}

function compare_results() {
  if (( ARGC < 2 )) {
    echo "${0} [01..14] [resultFile1] [resultFile2] [...]"
    return -1
  }
  i=$1
  python ${projectPath}/scoring/score.py ${projectPath}/input/forest${i}.txt \
    ${projectPath}/results/current_best/forest${i}.txt.out ${argv[2,-1]}
}
