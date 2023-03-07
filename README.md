# Programmierwettbewerb 2023 - Mathe Dual 

## Aktuelle Übersicht
![](https://wettbewerb.mathe-dual.de/scores.png)

[Finale Auswertung](https://wettbewerb.mathe-dual.de/)
und [Vergleichsübersicht](https://wettbewerb.mathedual.de/index_main.html)
sowie [Info-Seite](https://www.mathe-dual.de/index.php/wettbewerb-link) auf [mathe-dual.de](https://www.mathe-dual.de).

## Links und Informationen

Repository zur offiziellen Einreichung der Ergebnisse [md2022/groups/pi](https://git-ce.rwth-aachen.de/md2022/groups/pi)

Rankail's solver in C++ [thesing.samuel/pi-cpp](https://git-ce.rwth-aachen.de/thesing.samuel/pi-cpp)

Cortex's analytics, research, batch jobs and approaches [cortex/md.wettbewerb2023](https://git-ce.rwth-aachen.de/cortex/md.wettbewerb2023)

![](https://forthebadge.com/images/badges/works-on-my-machine.svg)

---

![](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![](https://img.shields.io/badge/SciPy-654FF0?style=for-the-badge&logo=SciPy&logoColor=white)
![](https://img.shields.io/badge/Arch_Linux-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white)

![](https://img.shields.io/badge/GitLab-330F63?style=for-the-badge&logo=gitlab&logoColor=white)
![](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

## Installation

In order to use the python scripts, some packages need to be installed in your environment.

```zsh
pip install -r requirements.txt
```

## Usage
Generate webtable process:

Fetch snapshots with `python webcrawler.py` and extract current snapshot.zip.

```zsh
snapshot="snapshot_060323_1603"
teams=( koeln uka coca-cola-und-nutella ets )

for t in $teams; do
  mkdir "web/data/${t}/${snapshot}"
  unzip -d "web/data/${t}/${snapshot}" "web/data/${t}/${snapshot}.zip"
done

```


Enter the group directory and extract tables:
```zsh
for t in ${teams}; do
  for i in {01..14} ; do 
    pcre2grep -Me '(?:<pre>)([^<]+[\n\s]*)+(?:<\/pre>)' -m1 --output '$1' web/data/${t}/${snapshot}/forest${i}.txt.html >| web/data/${t}/${t}.forest${i}.table 
  done
done

```
parse tables and save relative scores:
```zsh
{
  for i in {01..14} ; do
    python web/score_webtable.py forest${i} ${teams};
  done
} >| web/relative_score_tables/overview-$(date +'%F_%H-%M').md
```