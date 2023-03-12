# Team π - Mathe Dual: Programmierwettbewerb 2023

## Endstand
[![](media/scores.png)](https://wettbewerb.mathe-dual.de/)

| Platz  | Team                  |   Bonus |  Gesamt Score |
|-------:|:----------------------|--------:|--------------:|
|     1. | pi                    |     100 |          9025 |
|     2. | koeln                 |      50 |          8794 |
|     3. | coca-cola-und-nutella |      25 |          8538 |
|     4. | uka                   |         |          8030 |
|     5. | ets                   |         |          7046 |
|     6. | fabio-palmen          |         |          5424 |
|     7. | horst                 |         |          5085 |
|     8. | bug-prevention        |         |          4688 |
|     9. | mongulus-und-bongulus |         |          1340 |
|    10. | suffkapuff            |         |          1220 |

[Finale Auswertung](https://wettbewerb.mathe-dual.de/)
und [Vergleichsübersicht](https://wettbewerb.mathedual.de/index_main.html)
sowie [Info-Seite](https://www.mathe-dual.de/index.php/wettbewerb-link) auf [mathe-dual.de](https://www.mathe-dual.de).

## Links
Repository zur offiziellen Einreichung der Ergebnisse [md2022/groups/pi](https://git-ce.rwth-aachen.de/md2022/groups/pi)

Rankail's solver in C++ [Rankail/md-wettbewerb-2023](https://github.com/Rankail/md-wettbewerb-2023)

Cortex's analytics, research, batch jobs and approaches [cortex359/md.wettbewerb2023](https://github.com/cortex359/md.wettbewerb2023) [Internal GitLab Repo](https://git-ce.rwth-aachen.de/cortex/md.wettbewerb2023)

---

# This Repository

![](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![](https://img.shields.io/badge/SciPy-654FF0?style=for-the-badge&logo=SciPy&logoColor=white)
![](https://img.shields.io/badge/Arch_Linux-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white)

[![](https://img.shields.io/badge/GitLab-330F63?style=for-the-badge&logo=gitlab&logoColor=white)](https://git-ce.rwth-aachen.de/cortex/md.wettbewerb2023)
[![](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/cortex359/md.wettbewerb2023)

A list with relevant research publications can be found here: [RESEARCH.md](RESEARCH.md)

An overview over our best results: [results/current_best/README.md](results/current_best/README.md)

The latest comparisons of our results with other teams:
- [Final Overview](web/relative_score_tables/overview-final.md)
- [2023-03-06 22:48](web/relative_score_tables/overview-2023-03-06_22-48.md)
- [2023-03-06 16:03](web/relative_score_tables/overview-2023-03-06_16-03.md)
- [2023-03-06 10:43](web/relative_score_tables/overview-2023-03-06_10-43.md)
- [2023-03-05 22:50](web/relative_score_tables/overview-2023-03-05_22-50.md)
- [2023-03-05 21:38](web/relative_score_tables/overview-2023-03-05_21-38.md)


## Installation

In order to use the python scripts, some packages need to be installed in your environment.

```zsh
pip install -r requirements.txt
```

## Webcrawler

### Usage
Generate relative score tables:

Fetch snapshots with `python webcrawler.py` and extract current snapshot.zip:

```zsh
snapshot="snapshot_060323_2300"
teams=( koeln coca-cola-und-nutella uka ets fabio-palmen bug-prevention horst )

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
![](https://forthebadge.com/images/badges/works-on-my-machine.svg)
