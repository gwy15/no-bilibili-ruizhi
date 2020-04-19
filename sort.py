from pathlib import Path
import re
from collections import defaultdict


class Filter:
    def __init__(self, s: str):
        result = re.search(r'">([tru])=([^<]+)<', s)
        if result is None:
            raise RuntimeError(f'{s} parse failed.')
        self.type = result.group(1)
        self.content = result.group(2)

    def xml(self) -> str:
        return f'    <item enabled="true">{self.type}={self.content}</item>\n'


p = Path('tv.bilibili.player.xml')
with p.open(encoding='utf8') as f:
    lines = f.readlines()
lines = map(lambda l: l.strip(), lines)
lines = filter(
    lambda l: len(l) > 0 and 'filters' not in l,
    lines
)
filters = map(Filter, lines)
filters_by_type = defaultdict(list)
for filter in filters:
    filters_by_type[filter.type].append(filter)

with p.open('w', encoding='utf8') as f:
    f.write('<filters>\n')
    for type in sorted(filters_by_type.keys()):
        filters = sorted(
            filters_by_type[type],
            key=lambda f: f.content
        )
        for filter in filters:
            f.write(filter.xml())
        f.write('\n')
    f.write('</filters>\n')
