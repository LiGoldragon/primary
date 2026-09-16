#!/usr/bin/env python3
"""Tests for the model and flow anatomy composer.

Run: python3 anatomy/compose.test.py

Every test runs the composer as the CLI runs it, over the committed module
tree. The expected bytes of the primary-main base come from a fixture file
recorded from the launched v6 base, outside the code under test.
"""

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMPOSE = ROOT / 'compose.py'
FIXTURES = ROOT / 'tests' / 'fixtures'

FAILURES = []


def check(name: str, condition: bool, detail: str = '') -> None:
    if condition:
        print('ok   %s' % name)
    else:
        print('FAIL %s %s' % (name, detail))
        FAILURES.append(name)


def writable_copy(tmp: Path, name: str) -> Path:
    """Copy the anatomy tree somewhere writable; the source may be read-only."""
    copy = tmp / name
    shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('__pycache__'))
    for path in copy.rglob('*'):
        path.chmod(path.stat().st_mode | 0o200)
    return copy


def run(request: str, root: Path = ROOT):
    proc = subprocess.run([sys.executable, str(root / 'compose.py'), request],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def roles():
    code, out, _ = run('Roles')
    assert code == 0, out
    return out[len('Roles.[ '):-len(' ]')].split()


def test_every_role_composes_distinctly(tmp: Path) -> None:
    digests = {}
    pairs = [(role, 'claude') for role in roles()] + \
            [(role, 'codex') for role in
             ('primary-main', 'secondary-main', 'tertiary-main', 'quaternary-main')]
    for role, harness in pairs:
        out = tmp / ('%s-%s.md' % (role, harness))
        code, line, err = run('Compose.{ %s %s «%s» }' % (role, harness, out))
        if code != 0:
            check('composes %s/%s' % (role, harness), False, line + err)
            continue
        digest = hashlib.sha256(out.read_bytes()).hexdigest()
        check('composes %s/%s' % (role, harness), out.is_file() and out.stat().st_size > 0)
        check('distinct %s/%s' % (role, harness), digest not in digests,
              'collides with %s' % digests.get(digest))
        digests[digest] = '%s/%s' % (role, harness)
    check('every composition distinct', len(digests) == len(pairs),
          '%d digests for %d compositions' % (len(digests), len(pairs)))


def test_primary_main_reproduces_v6(tmp: Path) -> None:
    expected_bytes, expected_sha = FIXTURES.joinpath('v6-claude-base.expected').read_text().split()
    out = tmp / 'v6.md'
    code, line, _ = run('Compose.{ primary-main claude «%s» }' % out)
    raw = out.read_bytes()
    check('v6 reproduction: exit 0', code == 0, line)
    check('v6 reproduction: byte count', len(raw) == int(expected_bytes),
          '%d != %s' % (len(raw), expected_bytes))
    check('v6 reproduction: sha256', hashlib.sha256(raw).hexdigest() == expected_sha,
          hashlib.sha256(raw).hexdigest())
    check('v6 reproduction: reported in the outcome',
          expected_sha in line and expected_bytes in line, line)


def test_refusals(tmp: Path) -> None:
    code, line, _ = run('Compose.{ quinary-main claude «%s» }' % (tmp / 'x.md'))
    check('unknown role refuses', code == 1 and line == 'Refused.UnknownRole.«quinary-main»', line)

    code, line, _ = run('Compose.{ primary-main deepseek «%s» }' % (tmp / 'x.md'))
    check('unknown harness refuses',
          code == 1 and line == 'Refused.UnknownHarness.«deepseek»', line)

    code, line, _ = run('Compose.{ subflow-checkup codex «%s» }' % (tmp / 'x.md'))
    check('role with no composition on that harness refuses',
          code == 1 and line == 'Refused.NoComposition.{ Sub.Checkup Codex }', line)

    code, line, _ = run('Compose.{ primary-main claude }')
    check('wrong arity refuses', code == 1 and line.startswith('Refused.'), line)


def test_tampered_module_refuses(tmp: Path) -> None:
    copy = writable_copy(tmp, 'tampered')
    target = copy / 'modules' / 'header' / 'authority.md'
    target.write_text(target.read_text() + '\nan added line no index records\n')
    code, line, _ = run('Compose.{ primary-main claude «%s» }' % (tmp / 'y.md'), copy)
    check('tampered module refuses',
          code == 1 and line.startswith('Refused.HashMismatch.{ «header/authority»'), line)
    code, line, _ = run('Verify', copy)
    check('Verify catches the tampered module',
          code == 1 and line.startswith('Refused.HashMismatch.'), line)


def test_missing_module_refuses(tmp: Path) -> None:
    copy = writable_copy(tmp, 'missing')
    (copy / 'modules' / 'header' / 'quota.md').unlink()
    code, line, _ = run('Compose.{ primary-main claude «%s» }' % (tmp / 'z.md'), copy)
    check('missing module refuses',
          code == 1 and line.startswith('Refused.MissingModule.{ «header/quota»'), line)


def test_verify_covers_every_module() -> None:
    code, line, _ = run('Verify')
    check('Verify passes over the committed tree', code == 0 and line.startswith('Verified.'),
          line)


def test_index_is_its_plan(tmp: Path) -> None:
    copy = writable_copy(tmp, 'reseed')
    before = (copy / 'index.datom').read_bytes()
    proc = subprocess.run([sys.executable, str(copy / 'seed.py'), '--index'],
                          capture_output=True, text=True)
    after = (copy / 'index.datom').read_bytes()
    check('seed.py --index reproduces the committed index',
          proc.returncode == 0 and before == after, proc.stdout + proc.stderr)


def main() -> int:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        test_every_role_composes_distinctly(tmp)
        test_primary_main_reproduces_v6(tmp)
        test_refusals(tmp)
        test_tampered_module_refuses(tmp)
        test_missing_module_refuses(tmp)
        test_verify_covers_every_module()
        test_index_is_its_plan(tmp)
    if FAILURES:
        print('\n%d failing: %s' % (len(FAILURES), ', '.join(FAILURES)))
        return 1
    print('\nall green')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
