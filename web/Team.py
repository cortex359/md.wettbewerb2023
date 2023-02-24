import functools
import os
import regex as re
import shutil
import time
import requests

save_path = './data/'
base_url = 'https://wettbewerb.mathe-dual.de/'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}


def mkdir_p(path: str):
    path = os.path.join(save_path, path)
    try:
        os.makedirs(path, exist_ok=True)
        print(f'[OK] {path}')
    except OSError as error:
        print(f'[ERR] Could not create dirs at "{path}". Error: {error}')


def get_files(path):
    try:
        if os.path.exists(path) and os.path.isdir(path):
            for file in os.listdir(path):
                if os.path.isfile(os.path.join(path, file)):
                    yield file
    except FileNotFoundError:
        pass


def get_page(path: str = ""):
    path = path.removeprefix('/')
    cache_file = os.path.join(save_path, "cache", "cache_" + path.replace('/', '_'))
    if os.path.isfile(cache_file):
        if time.time() - os.path.getmtime(cache_file) < 600:
            print(f'[CACHE] Loading file "{path}"')
            with open(cache_file, 'r') as c:
                return c.read()
        else:
            print(f'[CACHE] Refreshing "{path}"')

    try:
        print(f'[INFO] Requesting page "{path}"')
        r = requests.get(base_url + path, headers=headers, timeout=2.0)
        if r.status_code == requests.codes.ok:
            mkdir_p("cache")
            with open(cache_file, 'w') as c:
                c.write(r.text)
            return r.text
        else:
            print(f'[ERR] Page "{path}" returned status {r.status_code}.')
    except requests.RequestException as e:
        print(f'[ERR] Could not fetch page "{path}":\n\t{e}')
    except IOError as e:
        print(f'[ERR] Could not save fetched page "{path}" at "{cache_file}":\n\t{e}')


def download_snapshot(group: str, file: str):
    url = base_url + 'groups/' + group + '/' + file
    out_file_path = os.path.join(save_path, group, file)
    if os.path.exists(out_file_path):
        print(f'[OK] File exists: {group}/{file}')
    else:
        with requests.get(url, stream=True, headers=headers) as r:
            mkdir_p(group)
            with open(out_file_path, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)


@functools.total_ordering
class Team:
    name: str
    score: int
    bonus: int
    current_snapshot: str
    loaded_snapshots: list[str]

    def init_loaded_snapshots(self):
        self.loaded_snapshots = [f for f in get_files(os.path.join(save_path, self.name))
            if re.fullmatch("snapshot_[0-9]{6}_[0-9]{4,6}\.zip", f) is not None]

    def fetch_current_snapshot(self):
        matches = re.findall(r'(?<=href=")(snapshot_[0-9]{6}_[0-9]{4,6}.zip)(?=">)', get_page(f'groups/{self.name}/'))
        if len(matches) != 1:
            print(f'[ERR] Could not parse page groups/{self.name}/')
            return
        else:
            self.current_snapshot = matches[0]

        if self.current_snapshot not in self.loaded_snapshots:
            try:
                download_snapshot(self.name, self.current_snapshot)
                self.loaded_snapshots.append(self.current_snapshot)
            except IOError:
                print(f'[ERR] With Snapshot "{self.current_snapshot}".')

    def __str__(self):
        return f'{self.name}, score: {self.score}'

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.score < other.score

    def __init__(self, name: str, score: int = 0, bonus: int = 0):
        self.name = name
        self.score = score
        self.bonus = bonus
        self.init_loaded_snapshots()
        self.fetch_current_snapshot()
