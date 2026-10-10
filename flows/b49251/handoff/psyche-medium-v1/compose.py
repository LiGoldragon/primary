#!/usr/bin/env python3
"""Compose the base context of one role on one harness.

    compose.py 'Compose.{ primary-main claude «/tmp/base.md» }'
    compose.py 'Verify'
    compose.py 'Roles'

One inline datom value, no flags, as a datom-speaking CLI takes. The output is
an enum, always: Composed, Verified, Roles or Refused.

The composition is read from index.datom; nothing is hand-assembled. A role
with no composition, an unknown harness, a missing module and a module whose
bytes no longer hash to the recorded sha256 each refuse with a typed Refusal.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import datom_read as dr          # noqa: E402
import index_read as ir          # noqa: E402

ROOT = Path(__file__).resolve().parent


class Refused(Exception):
    def __init__(self, datom_text: str):
        super().__init__(datom_text)
        self.datom_text = datom_text


def _quote(text: str) -> str:
    return '«' + text.replace('»', '\\»') + '»'


def load_index(root: Path = ROOT) -> ir.Index:
    return ir.read((root / 'index.datom').read_text())


def module_body(module: ir.Module, root: Path = ROOT) -> str:
    path = root / module.module_path
    if not path.is_file():
        raise Refused('Refused.MissingModule.{ %s %s }'
                      % (_quote(module.module_name), _quote(module.module_path)))
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != module.sha256:
        raise Refused('Refused.HashMismatch.{ %s %s %s }'
                      % (_quote(module.module_name), module.sha256, actual))
    text = raw.decode('utf-8')
    return text.rstrip('\n') if module.wrap == 'Bare' else text


def compose(index: ir.Index, role: ir.Role, harness: str, root: Path = ROOT) -> str:
    """Emit the composed base text for one role and harness."""
    by_name = {m.module_name: m for m in index.modules}
    composition = next((c for c in index.compositions
                        if c.role == role and c.harness == harness), None)
    if composition is None:
        raise Refused('Refused.NoComposition.{ %s %s }' % (role.datom(), harness))

    pieces, bare_run = [], []

    def flush():
        if bare_run:
            pieces.append('\n\n'.join(bare_run) + '\n')
            bare_run.clear()

    for name in composition.module_names:
        module = by_name.get(name)
        if module is None:
            raise Refused('Refused.UnknownModule.{ %s %s }'
                          % (role.datom(), _quote(name)))
        body = module_body(module, root)
        if module.wrap == 'Bare':
            bare_run.append(body)
        elif module.wrap == 'Source':
            flush()
            pieces.append('\n<source path="%s" sha256="%s">\n%s\n</source>\n'
                          % (module.emitted_path, module.sha256, body))
        else:
            flush()
            pieces.append('\n<skill name="%s" location="%s">\n%s\n</skill>\n'
                          % (module.skill[0], module.skill[1], body))
    flush()
    return ''.join(pieces)


def _request(text: str):
    form = dr.parse(text)
    head = dr.variant(form, ('Compose', 'Verify', 'Roles'), 'Request')
    return head


def run(argv) -> str:
    if len(argv) != 2:
        return 'Refused.UnknownRole.«usage: compose.py \'Compose.{ <role> <harness> <out> }\'»'
    try:
        head = _request(argv[1])
    except dr.DatomError as error:
        return 'Refused.UnknownRole.%s' % _quote(str(error))

    index = load_index()

    if head.text == 'Roles':
        names = sorted({c.role.name for c in index.compositions})
        return 'Roles.[ %s ]' % ' '.join(names)

    if head.text == 'Verify':
        for module in index.modules:
            module_body(module)
        return 'Verified.%d' % len(index.modules)

    role_name, harness_name, out_path = dr.struct(head.payload, 3, 'Compose')
    role = ir.role_by_name(dr.string(role_name, 'RoleName'))
    if role is None:
        raise Refused('Refused.UnknownRole.%s' % _quote(dr.string(role_name, 'RoleName')))
    harness = ir.harness_by_name(dr.string(harness_name, 'HarnessName'))
    if harness is None:
        raise Refused('Refused.UnknownHarness.%s'
                      % _quote(dr.string(harness_name, 'HarnessName')))
    out = Path(dr.string(out_path, 'OutPath'))
    text = compose(index, role, harness)
    out.write_text(text)
    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return 'Composed.{ %s %s %d %s %s }' % (
        role.datom(), harness, len(text.encode('utf-8')), digest, _quote(str(out)))


def main(argv) -> int:
    try:
        print(run(argv))
        return 0
    except Refused as refusal:
        print(refusal.datom_text)
        return 1
    except dr.DatomError as error:
        print('Refused.UnknownRole.%s' % _quote(str(error)))
        return 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
