#!/usr/bin/env python3
"""Seed the module tree from the launched v6 base, and write index.datom.

    seed.py --extract <v6-directory>   one-time: split the v6 base into modules
    seed.py --index                    rewrite index.datom from the plan below

--extract needs the v6 successor package (its sources/ and its claude-base.md);
--index needs only the module tree, which is committed. The composition plan,
the model rows and the impersonation rows live here and nowhere else; index.datom
is their emission and is what compose.py reads.
"""

import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODULES = ROOT / 'modules'

SKILL_LOCATION = '/home/li/wt/github.com/LiGoldragon/Curriculum/efa157-branches/skills/'

# The nine paragraphs of the v6 header, in order, as seed.py splits them.
HEADER_PARTS = ['header/title-primary-claude', 'header/authority', 'header/succession',
                'header/precedence', 'header/harness-operation', 'header/layer-ownership',
                'header/first-work', 'header/quota', 'header/frozen-heading']


def q(text: str) -> str:
    return '«' + text.replace('»', '\\»') + '»'


# ---------------------------------------------------------------- extraction

def extract(v6: Path) -> None:
    base = (v6 / 'claude-base.md').read_text()
    head = base.partition('\n\n<source path=')[0]
    parts = head.split('\n\n')
    if len(parts) != len(HEADER_PARTS):
        raise SystemExit(f'header split gave {len(parts)} parts, expected {len(HEADER_PARTS)}')
    for name, body in zip(HEADER_PARTS, parts):
        out = MODULES / (name + '.md')
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(body + '\n')
    for src in sorted((v6 / 'sources').rglob('*.md')):
        rel = src.relative_to(v6)
        out = MODULES / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out)
    print(f'extracted {len(HEADER_PARTS)} header modules and '
          f'{len(list((MODULES / "sources").rglob("*.md")))} frozen modules')


# --------------------------------------------------------------------- plan

def frozen_names() -> list:
    return [str(p.relative_to(MODULES)) for p in sorted((MODULES / 'sources').rglob('*.md'))]


def group(prefix: str) -> list:
    return [n for n in frozen_names() if n.startswith('sources/' + prefix)]


def harness_skill(harness: str) -> str:
    return 'sources/skills/%s-harness.md' % harness.lower()


def frozen_for(harness: str) -> list:
    other = harness_skill('codex' if harness == 'Claude' else 'claude')
    return [n for n in frozen_names() if n != other]


def skills(harness: str, stems) -> list:
    out = []
    for stem in stems:
        name = ('sources/skills/%s-harness.md' % harness.lower()) if stem == 'harness' \
            else 'sources/skills/%s.md' % stem
        out.append(name)
    return out


SUBFLOW_KINDS = {
    'Checkup': (['spirit', 'behavior'], []),
    'Audit': (['spirit', 'psyche', 'behavior'], ['sources/Vision/distillation.md']),
    'Witness': (['spirit', 'testing', 'behavior'], []),
    'Proof': (['spirit', 'testing'], ['sources/Vision/ethos.md', 'sources/Vision/datom.md']),
    'Send': (['spirit', 'prompt-crafting'], []),
    'Illustrate': (['spirit', 'prompt-crafting'], ['sources/Vision/highLevelView.md']),
    'LowPowerThinking': (['spirit', 'psyche'],
                         ['sources/Vision/ethos.md', 'sources/Vision/datom.md',
                          'sources/Vision/protos.md', 'sources/Vision/highLevelView.md']),
    'Distillation': (['spirit', 'psyche-interraction'],
                     ['sources/Vision/distillation.md',
                      'sources/efa157/vision/distillation.md']),
}


def compositions() -> list:
    out = []
    for harness in ('Claude', 'Codex'):
        title = 'header/title-primary-claude' if harness == 'Claude' \
            else 'header/title-primary-codex'
        operation = 'header/harness-operation' if harness == 'Claude' \
            else 'role/codex-harness-operation'
        out.append(('Main.Primary', harness,
                    [title, 'header/authority', 'header/succession', 'header/precedence',
                     operation, 'header/layer-ownership',
                     'header/first-work', 'header/quota', 'header/frozen-heading']
                    + frozen_for(harness)))
        out.append(('Main.Secondary', harness,
                    ['header/title-secondary', 'header/authority', 'header/precedence',
                     operation, 'role/secondary-ownership',
                     'role/ascent-audit', 'header/quota', 'header/frozen-heading']
                    + group('spirit/') + group('intent/') + group('Vision/')
                    + skills(harness, ['spirit', 'behavior', 'correction', 'testing',
                                       'subflow', 'main-flow', 'edit-coordination',
                                       'nexus', 'vocabulary', 'harness'])))
        out.append(('Main.Tertiary', harness,
                    ['header/title-tertiary', 'header/authority',
                     operation, 'role/tertiary-ownership',
                     'role/ascent-audit', 'role/effort-medium', 'header/frozen-heading']
                    + group('spirit/')
                    + skills(harness, ['spirit', 'behavior', 'correction', 'subflow',
                                       'main-flow', 'harness'])))
        out.append(('Main.Quaternary', harness,
                    ['header/title-quaternary', 'header/authority', operation,
                     'role/quaternary-ownership', 'role/ascent-audit',
                     'role/effort-medium', 'header/frozen-heading']
                    + group('spirit/')
                    + skills(harness, ['spirit', 'behavior', 'correction'])))
    for kind, (stems, extra) in SUBFLOW_KINDS.items():
        slug = ''.join(('-' + c.lower()) if c.isupper() and i else c.lower()
                       for i, c in enumerate(kind))
        out.append(('Sub.' + kind, 'Claude',
                    ['header/title-subflow-' + slug, 'header/authority',
                     'header/harness-operation', 'role/subflow-common',
                     'subflow/' + slug, 'header/frozen-heading']
                    + skills('Claude', stems) + extra))
    return out


MODELS = [
    ('claude-fable-5-1', 'Fable', 'Claude', 'Wise', 'Standard',
     'flows/f55ec8/vision/modelRoles.md', 'Two Opus models, named by role'),
    ('claude-fable-5-1[1m]', 'Fable, million context', 'Claude', 'Wise', 'Million',
     'flows/f55ec8/vision/modelRoles.md', 'Two Opus models, named by role'),
    ('claude-opus-5', 'the newer Opus', 'Claude', 'Doer', 'Standard',
     'flows/f55ec8/vision/modelRoles.md', 'Two Opus models, named by role'),
    ('claude-opus-5[1m]', 'the newer Opus, million context', 'Claude', 'Doer', 'Million',
     'flows/f55ec8/vision/modelRoles.md', 'Two Opus models, named by role'),
    ('claude-opus-4-7', 'the older Opus, the wiser one', 'Claude', 'Wise', 'Standard',
     'flows/f55ec8/vision/layers.md', 'The model for the lower layers'),
    ('claude-opus-4-7[1m]', 'the older Opus, million context', 'Claude', 'Wise', 'Million',
     'flows/f55ec8/vision/layers.md', 'The model for the lower layers'),
    ('claude-opus-4-6', 'the thinking Opus, the gold standard for exchange of ideas',
     'Claude', 'Wise', 'Standard',
     'flows/efa157/vision/modelRoles.md', 'Keep the Fable-to-all-model ratio in Claude in line'),
    ('claude-opus-4-6[1m]', 'the thinking Opus, million context', 'Claude', 'Wise', 'Million',
     'flows/f55ec8/vision/layers.md', 'The model for the lower layers'),
    ('claude-sonnet', 'Sonnet', 'Claude', 'Doer', 'Standard',
     'flows/efa157/vision/subflowDispatch.md', 'Opus 4.6 used more to think'),
    ('claude-haiku', 'Haiku', 'Claude', 'Doer', 'Standard',
     'flows/efa157/vision/subflowDispatch.md', 'Opus 4.6 used more to think'),
    ('astra', 'Astra', 'Codex', 'Martian', 'Standard',
     'flows/f55ec8/vision/modelRoles.md', 'Astra belongs on the thinking, design, psyche side'),
    ('sol', 'Sol', 'Codex', 'Doer', 'Standard',
     'flows/f55ec8/vision/modelRoles.md', 'The main flow of the lower layer is the old Opus'),
    ('terra', 'Terra', 'Codex', 'Doer', 'Standard',
     'flows/f55ec8/vision/modelRoles.md', 'Astra belongs on the thinking, design, psyche side'),
    ('gpt-5.6-luna', 'Luna', 'Codex', 'Doer', 'Standard',
     'flows/f55ec8/vision/layers.md', 'The tertiary and quaternary run on lower-cost models'),
    ('open-source-unnamed', 'the third seat, large and wise, unnamed', 'OpenSource',
     'Unnamed', 'Standard',
     'flows/f55ec8/vision/modelRoles.md', 'Astra belongs on the thinking, design, psyche side'),
]

IMPERSONATIONS = [
    ('Main.Primary', 'claude-fable-5-1',
     'all thinking, design and psyche interaction on the old Opus or the newest Fable',
     'flows/f55ec8/vision/modelRoles.md', 'Two Opus models, named by role'),
    ('Main.Primary', 'astra', 'on the Codex side, at the higher layer, it is Astra',
     'flows/f55ec8/vision/modelRoles.md',
     'The main flow of the lower layer is the old Opus'),
    ('Main.Primary', 'open-source-unnamed',
     'the further seat on the thinking side, chartered, the model not yet named',
     'flows/f55ec8/vision/modelRoles.md', 'Astra belongs on the thinking, design, psyche side'),
    ('Main.Secondary', 'claude-opus-4-7', 'the main flow of the lower layer is the old Opus',
     'flows/f55ec8/vision/modelRoles.md',
     'The main flow of the lower layer is the old Opus'),
    ('Main.Secondary', 'sol', 'on the Codex side, the latest Sol',
     'flows/f55ec8/vision/modelRoles.md',
     'The main flow of the lower layer is the old Opus'),
    ('Main.Tertiary', 'claude-opus-4-7',
     'lower cost, medium effort, real-time communication and quick thinking',
     'flows/f55ec8/vision/layers.md', 'The model for the lower layers'),
    ('Main.Tertiary', 'sol', 'the Codex half of the tertiary layer',
     'flows/f55ec8/vision/modelRoles.md',
     'The main flow of the lower layer is the old Opus'),
    ('Main.Quaternary', 'claude-opus-4-6[1m]',
     'the filter layer, more instinctive than Mercury, lower cost, medium effort',
     'flows/f55ec8/vision/layers.md', 'The lower layers, more quick and instinctive'),
    ('Main.Quaternary', 'gpt-5.6-luna',
     'the two bottom layers on the two lower-cost models',
     'flows/f55ec8/vision/layers.md',
     'The tertiary and quaternary run on lower-cost models'),
    ('Sub.LowPowerThinking', 'claude-opus-4-6',
     'low power background thinking; the type that starts the 4.6 job',
     'flows/efa157/vision/subflowDispatch.md',
     'The main flow triggers the subagent by the way it responds'),
    ('Sub.Audit', 'claude-opus-4-7',
     'qualitative audits, like comparing vision',
     'flows/f55ec8/vision/modelRoles.md', 'Two Opus models, named by role'),
    ('Sub.Distillation', 'claude-opus-4-6',
     'the first-pass mass reading that gives a predigested view',
     'flows/efa157/vision/subflowDispatch.md', 'Opus 4.6 used more to think'),
    ('Sub.Checkup', 'claude-haiku', 'Haiku for really small, trivial jobs',
     'flows/efa157/vision/subflowDispatch.md', 'Opus 4.6 used more to think'),
    ('Sub.Send', 'claude-haiku', 'Haiku for really small, trivial jobs, like running',
     'flows/efa157/vision/subflowDispatch.md', 'Opus 4.6 used more to think'),
    ('Sub.Witness', 'claude-opus-5', 'Opus 5 if it is a doing-work model',
     'flows/efa157/vision/subflowDispatch.md', 'Opus 4.6 used more to think'),
    ('Sub.Proof', 'claude-opus-5', 'Opus 5 if it is a doing-work model',
     'flows/efa157/vision/subflowDispatch.md', 'Opus 4.6 used more to think'),
    ('Sub.Illustrate', 'terra', 'Terra and Luna, who are also really useful',
     'flows/f55ec8/vision/modelRoles.md', 'Astra belongs on the thinking, design, psyche side'),
    ('Sub.Proof', 'astra',
     'Astra may set Opus agents to creative coding when the quota allows',
     'flows/f55ec8/vision/modelRoles.md', 'Astra belongs on the thinking, design, psyche side'),
]

INSTALLS = [
    ('Claude', '--system-prompt-file <composed>', 'Replace', 'Top',
     'replaces the whole system prompt; tool schemas, permissions, hooks and '
     'entry-file injection persist outside it'),
    ('Claude', '--append-system-prompt-file <composed>', 'Append', 'Top',
     'adds to the end of the stock system prompt; used when only a module is added'),
    ('Codex', '-c model_instructions_file=<composed>', 'Replace', 'Top',
     'replaces the base instructions sent as the Responses API instructions field; '
     'outranks the instructions config key'),
    ('Codex', 'developer_instructions', 'Append', 'Middle',
     'a developer-role message beside the base instructions, never part of them; '
     'the developer role outranks the user role within the input array'),
    ('OpenSource', 'unnamed', 'Replace', 'Top',
     'the third seat is chartered and not active; no harness, flag or model is named'),
]


# ------------------------------------------------------------------- writing

def module_rows() -> list:
    rows = []
    for path in sorted(MODULES.rglob('*.md')):
        name = str(path.relative_to(MODULES))
        if name.endswith('.md') and not name.startswith('sources/'):
            name = name[:-3]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if name.startswith('sources/skills/'):
            stem = Path(name).stem
            wrap = 'Skill.{ %s %s }' % (stem, q(SKILL_LOCATION + Path(name).name))
        elif name.startswith('sources/'):
            wrap = 'Source.%s' % q(name)
        else:
            wrap = 'Bare'
        rows.append('  { %s %s %s %s }' % (q(name), q('modules/' + str(path.relative_to(MODULES))),
                                           digest, wrap))
    return rows


def write_index() -> None:
    lines = ['; The model and flow anatomy index. Read by compose.py; written by seed.py.',
             '; Position and meaning are given by Index in modelFlowAnatomy.ethos.',
             '{',
             ' { ; Anatomy: the models, then the impersonation rows',
             '  [']
    for model_id, name, harness, temperament, window, path, heading in MODELS:
        lines.append('   { %s %s %s %s %s { %s %s } }'
                     % (q(model_id), q(name), harness, temperament, window, q(path), q(heading)))
    lines.append('  ]')
    lines.append('  [')
    for role, model_id, note, path, heading in IMPERSONATIONS:
        lines.append('   { %s %s %s { %s %s } }' % (role, q(model_id), q(note), q(path), q(heading)))
    lines.append('  ] }')
    lines.append(' [ ; the modules')
    lines.extend(' ' + row for row in module_rows())
    lines.append(' ]')
    lines.append(' [ ; the compositions, per role and harness')
    for role, harness, names in compositions():
        lines.append('  { %s %s [' % (role, harness))
        for name in names:
            lines.append('   %s' % q(name))
        lines.append('  ] }')
    lines.append(' ]')
    lines.append(' [ ; how each harness installs a composed base')
    for harness, flag, effect, stratum, note in INSTALLS:
        lines.append('  { %s %s %s %s %s }' % (harness, q(flag), effect, stratum, q(note)))
    lines.append(' ] }')
    (ROOT / 'index.datom').write_text('\n'.join(lines) + '\n')
    print('index.datom written: %d modules, %d compositions'
          % (len(module_rows()), len(compositions())))


def main(argv) -> int:
    if len(argv) == 3 and argv[1] == '--extract':
        extract(Path(argv[2]).resolve())
        return 0
    if len(argv) == 2 and argv[1] == '--index':
        write_index()
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
