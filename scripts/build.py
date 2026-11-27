from pathlib import Path
import hashlib, json, shutil
from content import validate
root = Path(__file__).resolve().parents[1]
data = json.loads((root/'site/data/issues.json').read_text())
validate(data)
# Only generated dist is replaced. Source and unrelated projects are untouched.
out = root/'dist'
if out.exists(): shutil.rmtree(out)
shutil.copytree(root/'site', out)
# Version both application assets and content so browsers do not reuse a prior issue.
content_version = hashlib.sha256((out/'data/issues.json').read_bytes()).hexdigest()[:12]
app = out/'assets/app.js'
app.write_text(app.read_text().replace('__CONTENT_VERSION__', content_version))
index = out/'index.html'
html = index.read_text()
for asset in ('assets/app.js', 'assets/style.css'):
    digest = hashlib.sha256((out/asset).read_bytes()).hexdigest()[:12]
    html = html.replace(f'"{asset}"', f'"{asset}?v={digest}"')
index.write_text(html)
(out/'.nojekyll').touch()
print(f'Validated and built {len(data["issues"])} issue(s) into {out}')
