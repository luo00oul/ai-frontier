"""Convert the current known plain-text formulas; preserve prose, citations and IDs."""
from pathlib import Path
import argparse
import copy
import json
import os
import re
import tempfile

MATH = re.compile(r'(\$\$[\s\S]*?\$\$|\$(?:\\.|[^$\\])+\$)')
OLD_WORLD = 'z_t = encode(o_≤t)    ·    ẑ_(t+1) = f(z_t, a_t)'
WORLD = (
    r'$$\begin{aligned}'
    r'\mathbf{z}_t &= \mathrm{encode}(\mathbf{o}_{\le t}), \\ '
    r'\widehat{\mathbf{z}}_{t+1} &= \mathrm{f}(\mathbf{z}_t,\mathbf{a}_t).'
    r'\end{aligned}$$'
)
SYMBOLS = [
    {'symbol': r'$\mathbf{o}_{\le t}$', 'description': '截至时刻 t 的观察序列；粗体表示向量。'},
    {'symbol': r'$\mathbf{z}_t$', 'description': '时刻 t 的隐状态向量。'},
    {'symbol': r'$\mathbf{a}_t$', 'description': '时刻 t 的行动向量。'},
    {'symbol': r'$\widehat{\mathbf{z}}_{t+1}$', 'description': '模型预测的下一时刻隐状态；帽号表示预测值。'},
    {'symbol': r'$\mathrm{encode}$', 'description': '将观察序列编码为隐状态的编码器。'},
    {'symbol': r'$\mathrm{f}$', 'description': '根据当前隐状态和行动预测后继状态的动力学函数。'}
]

def convert_text(text):
    parts = MATH.split(text)
    for index in range(0, len(parts), 2):
        value = parts[index]
        value = value.replace('Δx = 0.8a + 0.1', r'$\Delta x = 0.8a + 0.1$')
        value = value.replace('Δx = wa + b', r'$\widehat{\Delta x} = wa + b$')
        value = value.replace('位置 x，', '位置 $x$，')
        value = value.replace('动力学模型 f ', r'动力学模型 $\mathrm{f}$ ')
        for plain, latex in (
            ('o_t', r'$\mathbf{o}_t$'),
            ('z_t', r'$\mathbf{z}_t$'),
            ('a_t', r'$\mathbf{a}_t$')
        ):
            value = re.sub(r'(?<![A-Za-z0-9_\\])' + re.escape(plain) + r'(?![A-Za-z0-9_])',
                           lambda match, replacement=latex: replacement, value)
        parts[index] = value
    return ''.join(parts)

def convert(data):
    result = copy.deepcopy(data)
    for issue in result['issues']:
        for section in issue['sections']:
            for field in ('paragraphs', 'items'):
                if field in section:
                    section[field] = [convert_text(text) for text in section[field]]
            if 'formula' not in section:
                continue
            raw = section['formula'].strip()
            if raw == OLD_WORLD:
                section['formula'] = WORLD
            elif not (raw.startswith('$$') and raw.endswith('$$')):
                raise ValueError(f"Unknown formula in {issue['id']}/{section['id']}: {raw}")
            if section['formula'] == WORLD:
                section['formulaTitle'] = '状态编码与单步预测'
                section['symbols'] = copy.deepcopy(SYMBOLS)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'site/data/issues.json')
    args = parser.parse_args()
    path = args.file.resolve()
    original = json.loads(path.read_text(encoding='utf-8'))
    converted = convert(original)
    # The converter must be safe to run a second time.
    assert convert(converted) == converted, 'Conversion is not idempotent'
    payload = json.dumps(converted, ensure_ascii=False, indent=2) + '\n'
    assert json.loads(payload) == converted
    if original != converted:
        fd, name = tempfile.mkstemp(dir=path.parent, prefix='.math-', suffix='.json')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as stream:
                stream.write(payload)
            os.replace(name, path)
        finally:
            if os.path.exists(name):
                os.unlink(name)
    print(f'Validated {len(converted["issues"])} issue(s); JSON is valid; conversion is idempotent.')

if __name__ == '__main__':
    main()
