"""Validate an entire incoming issue before atomic insertion. Never replaces existing content."""
from pathlib import Path
import argparse, json, os, tempfile
from content import validate
p=argparse.ArgumentParser()
p.add_argument('file', type=Path)
p.add_argument('--dry-run', action='store_true')
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
target=root/'site/data/issues.json'
data=json.loads(target.read_text())
incoming=json.loads(a.file.read_text())
previous=next((i for i in data['issues'] if i['id']==incoming['id']),None)
if previous:
    if previous == incoming:
        print('Identical issue already present; no change.'); raise SystemExit(0)
    raise SystemExit('Refusing to overwrite existing issue. Review the differences manually.')
data['issues'].append(incoming)
data['issues'].sort(key=lambda i:i['date'],reverse=True)
validate(data)
if a.dry_run:
    print('Valid issue; dry run only.'); raise SystemExit(0)
fd,name=tempfile.mkstemp(dir=target.parent,prefix='.issues-',suffix='.json')
try:
    with os.fdopen(fd,'w') as f: json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
    os.replace(name,target)
finally:
    if os.path.exists(name): os.unlink(name)
print('Added issue:', incoming['id'])
