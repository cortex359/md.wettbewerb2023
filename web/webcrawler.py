import os
import re
import time

from Team import Team, get_page

# Top 10 + one entry from "inaktive Teams (7)"
groups = ['koeln', 'coca-cola-und-nutella', 'uka', 'pi', 'ets', 'horst', 'bug-prevention', 'fabio-palmen',
    'mongulus-und-bongulus', 'suffkapuff', 'art-club']

# known groups
# groups = ["art-club", "coca-cola-und-nutella", "ets", "fabio-palmen", "horst", "koeln", "mongulus-und-bongulus",
#     "pi", "solo-leveling", "stc", "suffkapuff", "team-baeume", "uka"
# ]


def create_team_list() -> list[Team]:
    teams: list[Team] = []

    # <tr><td>1.</td><td><a href="groups/koeln/" target="_top">koeln</td><td align=right>50</td><td align=right>7876</td></tr>\n<tr>
    matches = re.findall(r'groups/([0-9a-z_-]+)/"(?:[^>]+>){3}([0-9]+|&nbsp;)(?:[^>]+>){2}([0-9]+)(?:</td></tr>)', get_page(""))

    live_groups = [g[0] for g in matches]

    for g in [x for x in live_groups if x not in groups]:
        print(f'[INFO] New group seen: {g}')

    for g in matches:
        if g[1] == '&nbsp;':
            bonus = 0
        else:
            bonus = int(g[1])
        time.sleep(2.)
        teams.append(Team(g[0], score=int(g[2]), bonus=bonus))

    return teams


if __name__ == "__main__":
    teams = create_team_list()