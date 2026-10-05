#!/usr/bin/env python3
"""Cut the texts the designer's rulings name into flows/aa887c/scripts/splits/
and record each in splits/index.tsv with its source's sha256.

Texts are copied by line range, never reworded. The only transformations are
the ones the rulings name and the index records:
  - a Markdown quotation prefix ("> ") is removed from book quotations;
  - a `type:` line is dropped from a proposed frontmatter (ruling 1);
  - a line replaced or added by a named proposal is replaced or added.
Every cut asserts its first words, so a changed book refuses here.

vision-raw/ (ruling 6): a record is a `## ` section of a file (the text before
the first `## `, less a leading `# ` title line, is a record of its own). A
provenance line is a line beginning `— psyche` or `-- psyche` (with its
parenthesis continued onto the next lines). A record whose provenance lines name
exactly one flow (`session <id>` or `flow <id>`) and no unnamed source goes to
that flow; a record naming none goes to legacy; any other record is ambiguous
and is listed in splits/vision-raw/ambiguous.tsv, where the migration refuses
until its `ruled_flow` column is filled. A file whose records all go one way is
copied whole by the migration; a file whose records go several ways is cut per
record here, each part carrying the file's `# ` title line.
"""
import hashlib, os, re, sys

PRI = '/home/li/primary'
CUR = '/git/github.com/LiGoldragon/Curriculum'
SPL = PRI + '/flows/aa887c/scripts/splits'
B15 = PRI + '/flows/bad807/books/15-context-modules.md'
B17 = PRI + '/flows/bad807/books/17-workspace.md'
ROLES = CUR + '/roles.datom'
GEN_PREFIXES = ('books/', 'roles/', 'readme/', 'field/', 'vision-raw/')

def sha(b): return hashlib.sha256(b).hexdigest()
def fsha(p): return sha(open(p, 'rb').read())
def lines(p): return open(p, encoding='utf-8').read().split('\n')

def rng(p, a, b, first, unquote=False):
    """Lines a..b (1-based, inclusive) of p; asserts the first line starts with `first`."""
    L = lines(p)[a - 1:b]
    if unquote:
        L = [re.sub(r'^> ?', '', l) for l in L]
    if not L or not L[0].startswith(first):
        sys.exit(f'refused: {p} l.{a} does not start with {first!r}: {L[:1]}')
    return L

def write(rel, text):
    p = f'{SPL}/{rel}'
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)
    return sha(text.encode())

rows = []   # part source sha256 section cut_sha256 edited_sha256 edit
def add(rel, text, src, section, edit='-'):
    rows.append([rel, src, fsha(src), section, write(rel, text), '-', edit])

# Ruling 3: psyche-primary, Proposal 7 whole, `type:` line dropped.
p7 = rng(B15, 181, 190, '---')
assert p7[1] == 'type: Operation', p7[1]
add('books/mind-operation-psyche-primary.md', '\n'.join(p7[:1] + p7[2:]) + '\n', B15,
    'Proposal 7 (l.181-190), the type: line l.182 dropped')

# Ruling 4: three inline role modules, bodies verbatim from roles.datom.
rd = open(ROLES, encoding='utf-8').read()
ROLE_DESC = {'general-instructions': 'A subagent begins on its brief.',
             'codex-skill-loading': 'A Codex subagent is handed a pasted skill.',
             'subflow-role': 'A subflow starts inside a flow\'s lane.'}
for name in ('general-instructions', 'codex-skill-loading', 'subflow-role'):
    m = re.search(r'\{ ' + re.escape(name) + r' «([^»]*)» \}', rd)
    if not m: sys.exit(f'refused: {name} not found in {ROLES}')
    add(f'roles/mind-operation-{name}.md', '---\ndescription: ' + ROLE_DESC[name] + '\n---\n\n' + m.group(1) + '\n', ROLES,
        f'inline module {name}, the text between « and »; frontmatter description by ruling C3')

# Ruling 5: main-flow head, Proposal 6: the fifteen lines of the system prompt.
smp = PRI + '/tools/main-flow-mode/system-prompt.md'
sp = lines(smp)
assert sp[0].startswith('You are a main flow:') and len([l for l in sp[:15]]) == 15
add('books/mind-operation-main-flow.head.md', '\n'.join(sp[:15]) + '\n', smp,
    'Proposal 6 of 15-context-modules.md: the fifteen lines, placed after the frontmatter of main-flow')

# Ruling 5: the context-modules Vision module, Proposal 1 body under its heading;
# the frontmatter description is Proposal 3's (l.80), its type: and name: lines dropped.
p1 = rng(B15, 33, 56, '**A context module is one file', unquote=True)
p3 = rng(B15, 80, 80, 'description: A context module')
add('books/psyche-vision-contextModules.md', '---\n' + p3[0] + '\n---\n\n' + '\n'.join(p1) + '\n', B15,
    'Proposal 1 body (l.33-56, quotation prefix removed); frontmatter: Proposal 3 description (l.80)')

# Ruling 5: Proposal 10, Line 1, Line 2, Proposal 11 as parts of their own.
p10 = rng(B15, 244, 248, 'A skill is a context module', unquote=True)
add('books/p10-skill-types.md', '\n'.join(p10) + '\n', B15, 'Proposal 10 (l.244-248, quotation prefix removed)')
l1 = rng(B17, 199, 200, '"Psyche" alone means')
add('books/line1-psyche.md', '\n'.join(l1) + '\n', B17, 'Line 1, Proposed (l.199-200)')
l2 = rng(B17, 212, 212, "A seat's identity module")
add('books/line2-skill-designing.md', '\n'.join(l2) + '\n', B17, 'Line 2, Proposed (l.212)')
p11 = rng(B15, 257, 258, 'A proposal is small', unquote=True)
add('books/p11-distillation.md', '\n'.join(p11) + '\n', B15, 'Proposal 11 (l.257-258, quotation prefix removed)')

# Ruling 5: READMEs, "<Aspect> is in charge of this repository." and the aspect's
# sentence from the rule of belonging (Proposal 1 of 17-workspace.md).
psy = rng(B17, 62, 62, 'Psyche answers')[0]
mnd = rng(B17, 63, 63, 'Mind answers')[0]
fld = ' '.join(rng(B17, 64, 65, 'Field answers'))
for repo, aspect, s, sec in (('psyche-skills', 'Psyche', psy, 'l.62'), ('mind-skills', 'Mind', mnd, 'l.63'),
                             ('field-skills', 'Field', fld, 'l.64-65, the one sentence its two lines carry, joined by one space')):
    add(f'readme/{repo}.README.md', f'{aspect} is in charge of this repository.\n{s}\n', B17,
        f'line 1 by ruling 5; line 2 Proposal 1 {sec}')

# Ruling 5: SKILL_VARIABLES.md as field/knowledge/setup-variables.
sv = PRI + '/SKILL_VARIABLES.md'
add('field/field-knowledge-setup-variables.md',
    '---\ndescription: A value that differs between setups is needed.\n---\n\n# Setup variables\n\n' + open(sv, encoding='utf-8').read(),
    sv, 'whole file, after the frontmatter and heading given by ruling 5')

# Edits of parts already cut (ruling 5): Line 1, Proposal 10 with Line 2, Proposal 11.
EDITS = {
    '02-psyche/vision-psyche.body.md': (
        lambda L: L[:18] + l1 + L[21:],
        lambda L: L[18].startswith('"Psyche" alone means the written psyche, the records named under') and L[20].startswith('the living psyche is always'),
        'psyche.md l.24-26 replaced by Line 1 of 17-workspace.md (books/line1-psyche.md)'),
    '10-skill-designing/psyche-skills.md': (
        lambda L: L[:2] + p10[:4] + L[7:8] + l2 + L[10:],
        lambda L: L[2] == "A skill's kind says who stands behind it." and L[8].startswith('A role skill carries'),
        'skill-designing.md l.55-59 replaced by Proposal 10 lines 1-4 (books/p10-skill-types.md); l.66-67 replaced by Line 2 of 17-workspace.md (books/line2-skill-designing.md); Proposal 10 line 5 not placed: Line 2 replaces the same lines'),
    '08-psyche-distillation/vision-distillation.add.md': (
        lambda L: L[:1] + p11 + L[1:],
        lambda L: L[0].startswith('A distilled statement carries what the psyche said'),
        'Proposal 11 added after psyche-distillation.md l.25 (books/p11-distillation.md)'),
}

# vision-raw cuts (ruling 6).
flows = set(os.listdir(PRI + '/flows'))
prov = re.compile(r'^\s*(—|--)\s*(the\s+)?psyche\b', re.I)
idre = re.compile(r'\b(?:session|flow)\s+`?([0-9a-f]{6,8})\b')
plan, amb = [], []
RULED = {}
_ap = f'{SPL}/vision-raw/ambiguous.tsv'
if os.path.exists(_ap):
    for _l in open(_ap, encoding='utf-8').read().rstrip('\n').split('\n')[1:]:
        _c = _l.split('\t')
        if len(_c) == 5 and _c[4]: RULED[(_c[0], _c[1])] = _c[4]
vr = PRI + '/vision-raw'
for name in sorted(os.listdir(vr)):
    src = f'{vr}/{name}'
    raw = open(src, encoding='utf-8').read()
    L = raw.split('\n')
    title = [L[0]] if L and L[0].startswith('# ') else []
    body_start = len(title)
    recs, cur, start = [], [], body_start
    for i in range(body_start, len(L)):
        if L[i].startswith('## ') and cur:
            recs.append((start, cur)); cur, start = [], i
        cur.append(L[i])
    recs.append((start, cur))
    if recs and not any(x.strip() for x in recs[0][1]) and len(recs) > 1:
        title += recs.pop(0)[1]          # blank lines after the title travel with it
    dest = []
    for s, r in recs:
        ids, unnamed = set(), 0
        for j, l in enumerate(r):
            if prov.match(l):
                t, k = l, j
                while t.count('(') > t.count(')') and k + 1 < len(r) and r[k + 1].strip():
                    k += 1; t += ' ' + r[k]
                f = set(idre.findall(t))
                ids |= f
                unnamed += 0 if f else 1
        if not any(x.strip() for x in r):
            d = None                       # blank remainder: travels with the text before it
        elif len(ids) == 1 and not unnamed:
            d = ids.pop()
        elif not ids:
            d = 'legacy'
        elif (name, f'l.{s + 1}-{s + len(r)}') in RULED:
            d = RULED[(name, f'l.{s + 1}-{s + len(r)}')]
            amb.append([name, f'l.{s + 1}-{s + len(r)}', ' '.join(sorted(ids)) + (f' +{unnamed} unnamed' if unnamed else ''), next((x for x in r if x.strip()), '')[:100], d])
        else:
            d = '?'
            amb.append([name, f'l.{s + 1}-{s + len(r)}', ' '.join(sorted(ids)) + (f' +{unnamed} unnamed' if unnamed else ''), next((x for x in r if x.strip()), '')[:100], ''])
        dest.append(d)
    ds = {d for d in dest if d}
    if len(ds) <= 1 and '?' not in ds:
        d = ds.pop() if ds else 'legacy'
        plan.append([f'{d}/vision/{name}', 'whole', src, ''])
        continue
    # several destinations: cut per record, each part with the title line.
    groups, last = {}, None
    for (s, r), d in zip(recs, dest):
        d = d or last
        last = d
        groups.setdefault(d, []).append((s, r))
    for d, parts in groups.items():
        if d == '?':
            continue
        text = '\n'.join(title + [l for _, r in parts for l in r])
        if not text.endswith('\n'): text += '\n'
        secs = ', '.join(f'l.{s + 1}-{s + len(r)}' for s, r in parts)
        rel = f'vision-raw/{d}/{name}'
        add(rel, text, src, f'records {secs}' + (', with title l.1' if title else ''))
        plan.append([f'{d}/vision/{name}', 'cut', f'{SPL}/{rel}', secs])
    # verbatim proof: the cut records (and ambiguous ones) reassemble the source.
    back = '\n'.join(title + [l for (s, r) in recs for l in r])
    assert back == raw, f'reassembly failed for {name}'

def main():
    idx = f'{SPL}/index.tsv'
    old = [l.split('\t') for l in open(idx, encoding='utf-8').read().rstrip('\n').split('\n')]
    head, body = old[0], [r for r in old[1:] if not r[0].startswith(GEN_PREFIXES)]
    for r in body:
        if r[0] in EDITS:
            fn, ok, note = EDITS[r[0]]
            p = f'{SPL}/{r[0]}'
            cur = open(p, encoding='utf-8').read()
            if fsha(p) == r[4]:
                L = cur.split('\n')
                if not ok(L): sys.exit(f'refused: {r[0]} not as expected for its edit')
                new = '\n'.join(fn(L))
                with open(p, 'w', encoding='utf-8') as f: f.write(new)
                r[5], r[6] = sha(new.encode()), note
            elif r[5] != '-' and fsha(p) == r[5]:
                pass
            else:
                sys.exit(f'refused: {r[0]} is neither as cut nor as edited')
    with open(idx, 'w', encoding='utf-8') as f:
        for r in [head] + body + rows:
            f.write('\t'.join(r) + '\n')
    os.makedirs(f'{SPL}/vision-raw', exist_ok=True)
    with open(f'{SPL}/vision-raw/plan.tsv', 'w', encoding='utf-8') as f:
        f.write('target\tkind\tsource\trecords\n')
        for r in plan: f.write('\t'.join(r) + '\n')
    ap = f'{SPL}/vision-raw/ambiguous.tsv'
    with open(ap, 'w', encoding='utf-8') as f:
        f.write('file\tlines\tnamed\tfirst_line\truled_flow\n')
        for r in amb:
            f.write('\t'.join(r) + '\n')
    print(f'parts {len(rows)}; vision-raw plan {len(plan)}; ambiguous {len(amb)}')

main()
