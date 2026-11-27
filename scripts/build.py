from pathlib import Path
import json, shutil
from content import validate
root = Path(__file__).resolve().parents[1]
data = json.loads((root/'site/data/issues.json').read_text())
validate(data)
# Only generated dist is replaced. Source and unrelated projects are untouched.
out = root/'dist'
if out.exists(): shutil.rmtree(out)
shutil.copytree(root/'site', out)
(out/'.nojekyll').touch()
print(f'Validated and built {len(data["issues"])} issue(s) into {out}')
