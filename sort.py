from pathlib import Path
import re
from collections import defaultdict


def type_of(line: str) -> str:
    return re.search('">([tru])=', line).group(0)


p = Path('tv.bilibili.player.xml')
with p.open(encoding='utf8') as f:
    lines = f.readlines()
lines = map(
    lambda l: l.strip(),
    lines
)
lines = filter(
    lambda l: len(l) > 0 and 'filters' not in l,
    lines
)
lines_by_type = defaultdict(list)
for line in lines:
    lines_by_type[type_of(line)].append(line)

with p.open('w', encoding='utf8') as f:
    f.write('<filters>\n')
    for t, lines in lines_by_type.items():
        for line in lines:
            f.write(f'    {line}\n')
        f.write('\n')
    f.write('</filters>\n')
