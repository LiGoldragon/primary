#!/usr/bin/env python3
"""Emit index.datom from the frozen modules, then compose the psyche-medium base.

    python3 assemble.py

No flags. The module bodies under modules/ are the frozen inputs; nothing is
fetched. This writes index.datom, claude-base.md (through compose.py, the
f55ec8 anatomy composer, extended here with the Psyche role kind), and
artifact-manifest.json. first-prompt.md is authored, not generated, and is only
hashed into the manifest.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODULES = ROOT / 'modules'

SKILL_LOCATION = '/home/li/wt/github.com/LiGoldragon/Curriculum/efa157-branches/skills/'

HEADER = ['header/authority', 'header/identity', 'header/harness-rules']
FROZEN_HEADING = 'header/frozen-heading'


def quoted(text: str) -> str:
    return '«' + text.replace('»', '\\»') + '»'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def listing(subdir: str):
    return sorted(p for p in (MODULES / subdir).glob('*.md'))


def main() -> int:
    modules, order = [], []

    for name in HEADER + [FROZEN_HEADING]:
        path = MODULES / 'header' / (name.split('/')[1] + '.md')
        modules.append((name, path, 'Bare', ''))

    def add_source(name, path, emitted):
        modules.append((name, path, 'Source', emitted))
        return name

    def add_skill(name, path, skill_name):
        modules.append((name, path, 'Skill', skill_name))
        return name

    order += HEADER

    for path in listing('sources/skills'):
        order.append(add_skill('sources/skills/' + path.name, path, path.stem))
    for path in listing('sources/spirit'):
        order.append(add_source('sources/spirit/' + path.name, path,
                                'sources/spirit/' + path.name))
    for path in listing('sources/intent'):
        order.append(add_source('sources/intent/' + path.name, path,
                                'sources/intent/' + path.name))
    for path in listing('sources/Vision'):
        order.append(add_source('sources/Vision/' + path.name, path,
                                'sources/Vision/' + path.name))

    order.append(FROZEN_HEADING)

    for lane in ('b49251', 'f55ec8', 'efa157'):
        for path in sorted((MODULES / 'sources' / lane).rglob('*.md')):
            rel = 'sources/' + str(path.relative_to(MODULES / 'sources'))
            order.append(add_source(rel, path, rel))

    module_rows = []
    for name, path, wrap, extra in modules:
        if not path.is_file():
            print('Refused.MissingModule.{ %s %s }' % (quoted(name), quoted(str(path))))
            return 1
        rel = str(path.relative_to(ROOT))
        if wrap == 'Bare':
            wrap_text = 'Bare'
        elif wrap == 'Source':
            wrap_text = 'Source.' + quoted(extra)
        else:
            wrap_text = 'Skill.{ %s %s }' % (quoted(extra),
                                             quoted(SKILL_LOCATION + path.name))
        module_rows.append('   { %s %s %s %s }'
                           % (quoted(name), quoted(rel), digest(path), wrap_text))

    provenance = '{ «flows/b49251/vision/psycheFlows.md» «The psyche stack on Claude» }'
    models = [
        '{ «claude-fable-5-1[1m]» «Fable, the high-effort psyche seat» Claude Wise Million %s }' % provenance,
        '{ «claude-opus-4-7[1m]» «the old Opus, the medium-effort psyche seat» Claude Wise Million %s }' % provenance,
        '{ «claude-sonnet-5» «Sonnet 5, the low-effort psyche seat» Claude Doer Standard %s }' % provenance,
        '{ «astra» «Astra, the high-effort psyche seat on Codex» Codex Martian Standard %s }' % provenance,
        '{ «sol» «Sol, the no-consideration seat on Codex» Codex Doer Standard %s }' % provenance,
    ]
    impersonations = [
        '{ Psyche.High «claude-fable-5-1[1m]» «Fable on high power on the cloud side» %s }' % provenance,
        '{ Psyche.Medium «claude-opus-4-7[1m]» «Medium is old Opus» %s }' % provenance,
        '{ Psyche.Low «claude-sonnet-5» «Low level is going to be Sonnet; Sonnet 5 for now» %s }' % provenance,
        '{ Psyche.High «astra» «The same stack on Codex is Astra for the high power» %s }' % provenance,
        '{ Psyche.Low «sol» «no consideration with Sol» %s }' % provenance,
    ]
    installs = [
        '{ Claude «--system-prompt-file» Replace Top «replaces the whole system prompt» }',
        '{ Claude «--append-system-prompt-file» Append Top «adds to the end of the stock one» }',
        '{ Codex «-c model_instructions_file=» Replace Top «replaces the base instructions» }',
    ]

    index = ['; The psyche-medium base index. Read by compose.py; written by assemble.py.',
             '; Schema: the f55ec8 model and flow anatomy, with Role extended by Psyche.Effort.',
             '{', ' {', '  [']
    index += ['   ' + row for row in models]
    index += ['  ]', '  [']
    index += ['   ' + row for row in impersonations]
    index += ['  ] }', ' [ ; the modules']
    index += module_rows
    index += [' ]', ' [ ; the compositions, per role and harness',
              '  { Psyche.Medium Claude [']
    index += ['   ' + quoted(name) for name in order]
    index += ['  ] }', ' ]', ' [ ; the install rows']
    index += ['  ' + row for row in installs]
    index += [' ] }', '']
    (ROOT / 'index.datom').write_text('\n'.join(index))

    out = ROOT / 'claude-base.md'
    result = subprocess.run(
        [sys.executable, str(ROOT / 'compose.py'),
         'Compose.{ «psyche-medium» «claude» %s }' % quoted(str(out))],
        capture_output=True, text=True)
    print(result.stdout.strip() or result.stderr.strip())
    if result.returncode != 0:
        return result.returncode

    text = out.read_text()
    for name, path, wrap, _ in modules:
        body = path.read_text()
        assert (body.rstrip('\n') if wrap == 'Bare' else body) in text, name

    artifacts = {}
    for path in sorted(ROOT.rglob('*')):
        if path.is_file() and path.name != 'artifact-manifest.json' \
                and '__pycache__' not in path.parts:
            artifacts[str(path.relative_to(ROOT))] = digest(path)
    (ROOT / 'artifact-manifest.json').write_text(json.dumps(artifacts, indent=2) + '\n')

    print(json.dumps({'modules': len(modules), 'composed': len(order),
                      'baseBytes': len(text.encode()),
                      'firstPromptBytes': len((ROOT / 'first-prompt.md').read_bytes())}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
