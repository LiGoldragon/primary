import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { captureOne, enrolledBinding, publish } from './primary-publish.mjs';

const run = (cwd, args) => execFileSync('git', args, { cwd, encoding: 'utf8' }).trim();
const ownIdentity = () => {
  const fields = fs.readFileSync(`/proc/${process.pid}/stat`, 'utf8').trim().split(' ');
  return { pid: process.pid, startTicks: fields[21], bootId: fs.readFileSync('/proc/sys/kernel/random/boot_id', 'utf8').trim() };
};
function fixture() {
  const home = fs.mkdtempSync(path.join(os.tmpdir(), 'primary-publish-'));
  const remote = path.join(home, 'remote.git'), root = path.join(home, 'primary');
  run(home, ['init', '--bare', remote]); run(home, ['init', root]);
  run(root, ['config', 'user.email', 'fixture@example.test']); run(root, ['config', 'user.name', 'fixture']);
  fs.writeFileSync(path.join(root, 'unowned.txt'), 'remote stays\n');
  fs.writeFileSync(path.join(root, 'lane.txt'), 'baseline\n');
  run(root, ['add', '.']); run(root, ['commit', '-m', 'initial']); run(root, ['branch', '-M', 'main']); run(root, ['remote', 'add', 'origin', remote]); run(root, ['push', '-u', 'origin', 'main']); run(root, ['fetch', 'origin', 'main']);
  const identity = ownIdentity(), authorityFile = path.join(home, 'authority.json'), stateFile = path.join(home, 'state', 'state.json');
  const authority = { version: 1, bindings: [{ bindingId: 'fixture-binding', ...identity, laneRoot: root, allowedRelativePrefixes: ['lane.txt', 'new.txt', 'gone.txt', 'links', 'bin.dat', 'run.sh', 'link'], excludedRelativePrefixes: [], enabled: true }] };
  fs.writeFileSync(authorityFile, JSON.stringify(authority), { mode: 0o600 }); fs.chmodSync(authorityFile, 0o600);
  const entry = relativePath => { const row = run(root, ['ls-tree', 'origin/main', '--', relativePath]); if (!row) return { present: false, mode: null, blobOid: null }; const match = /^(\d+) \w+ ([0-9a-f]+)\t/.exec(row); return { present: true, mode: match[1], blobOid: match[2] }; };
  const state = { version: 1, repository: { root, remote: 'origin', branch: 'main' }, lanes: { 'fixture-binding': { baseline: { 'lane.txt': entry('lane.txt') } } }, requests: {}, receipts: {} };
  fs.mkdirSync(path.dirname(stateFile), { recursive: true }); fs.writeFileSync(stateFile, JSON.stringify(state));
  return { home, remote, root, authorityFile, stateFile, identity, state, entry };
}
function request(id, paths, description = 'fixture publish') { return { requestId: id, paths, description }; }
function invoke(fixture, value, options = {}) { return publish(value, { authorityFile: fixture.authorityFile, stateFile: fixture.stateFile, processChain: [fixture.identity], ...options }); }
function advanceRemote(fixture, relative = 'unowned.txt', content = 'remote advance\n') {
  const other = path.join(fixture.home, `other-${crypto.randomUUID()}`); run(fixture.home, ['clone', fixture.remote, other]);
  run(other, ['config', 'user.email', 'other@example.test']); run(other, ['config', 'user.name', 'other']);
  fs.writeFileSync(path.join(other, relative), content); run(other, ['add', relative]); run(other, ['commit', '-m', 'advance']); run(other, ['push']);
}

test('enrolled authority accepts only the exact controller process tuple', () => {
  const f = fixture();
  assert.equal(enrolledBinding(JSON.parse(fs.readFileSync(f.authorityFile)), [f.identity]).bindingId, 'fixture-binding');
  assert.throws(() => enrolledBinding(JSON.parse(fs.readFileSync(f.authorityFile)), [{ ...f.identity, startTicks: 'wrong' }]), /not enrolled/);
});

test('authority must be a controller-owned regular 0600 file before it is parsed', () => {
  const f = fixture(); fs.chmodSync(f.authorityFile, 0o644);
  assert.throws(() => invoke(f, request('r-open-authority', [{ path: 'lane.txt' }])), /private controller file/);
  fs.chmodSync(f.authorityFile, 0o600);
});

test('private-index publication changes an owned capture and preserves live and remote unowned bytes', () => {
  const f = fixture();
  fs.writeFileSync(path.join(f.root, 'lane.txt'), 'captured\n');
  const outcome = invoke(f, request('r-owned', [{ path: 'lane.txt' }]));
  assert.deepEqual(outcome, { outcome: 'published', paths: ['lane.txt'], capturedSnapshot: true, observedPostCaptureChange: 'unknown' });
  assert.equal(fs.readFileSync(path.join(f.root, 'lane.txt'), 'utf8'), 'captured\n');
  assert.equal(run(f.root, ['show', 'origin/main:lane.txt']), 'captured');
  assert.equal(run(f.root, ['show', 'origin/main:unowned.txt']), 'remote stays');
  const state = JSON.parse(fs.readFileSync(f.stateFile));
  assert.equal(state.receipts['r-owned'].outcome, 'published');
  assert.equal(state.requests['r-owned'].phase, 'published');
});

test('new remote-absent file may establish its first baseline, but no pre-existing missing baseline may overwrite', () => {
  const f = fixture(); fs.writeFileSync(path.join(f.root, 'new.txt'), 'new bytes\n');
  assert.equal(invoke(f, request('r-new', [{ path: 'new.txt' }])).outcome, 'published');
  const second = fixture();
  fs.writeFileSync(path.join(second.root, 'lane.txt'), 'overwrite attempt\n');
  second.state.lanes['fixture-binding'].baseline = {}; fs.writeFileSync(second.stateFile, JSON.stringify(second.state));
  assert.equal(invoke(second, request('r-missing', [{ path: 'lane.txt' }])).outcome, 'refused');
  assert.equal(JSON.parse(fs.readFileSync(second.stateFile)).requests['r-missing'].phase, 'refused');
});

test('remote changes to an owned baseline refuse without changing main', () => {
  const f = fixture();
  const other = path.join(f.home, 'other'); run(f.home, ['clone', f.remote, other]); run(other, ['config', 'user.email', 'other@example.test']); run(other, ['config', 'user.name', 'other']);
  fs.writeFileSync(path.join(other, 'lane.txt'), 'other change\n'); run(other, ['add', 'lane.txt']); run(other, ['commit', '-m', 'other']); run(other, ['push']);
  const before = run(f.root, ['ls-remote', '--refs', 'origin', 'refs/heads/main']); fs.writeFileSync(path.join(f.root, 'lane.txt'), 'ours\n');
  assert.equal(invoke(f, request('r-conflict', [{ path: 'lane.txt' }])).outcome, 'refused');
  assert.equal(run(f.root, ['ls-remote', '--refs', 'origin', 'refs/heads/main']), before);
});

test('a remote path already equal to the capture records an atomic current baseline', () => {
  const f = fixture();
  const other = path.join(f.home, 'other'); run(f.home, ['clone', f.remote, other]); run(other, ['config', 'user.email', 'other@example.test']); run(other, ['config', 'user.name', 'other']);
  fs.writeFileSync(path.join(other, 'lane.txt'), 'captured elsewhere\n'); run(other, ['add', 'lane.txt']); run(other, ['commit', '-m', 'elsewhere']); run(other, ['push']);
  fs.writeFileSync(path.join(f.root, 'lane.txt'), 'captured elsewhere\n');
  const result = invoke(f, request('r-current', [{ path: 'lane.txt' }]));
  assert.equal(result.outcome, 'already-current');
  const state = JSON.parse(fs.readFileSync(f.stateFile));
  assert.equal(state.requests['r-current'].phase, 'published');
  assert.equal(state.lanes['fixture-binding'].baseline['lane.txt'].blobOid, f.entry('lane.txt').blobOid);
});

test('deletion requires explicit intent and a matching enrolled baseline', () => {
  const f = fixture(); fs.unlinkSync(path.join(f.root, 'lane.txt'));
  assert.throws(() => invoke(f, request('r-implicit-delete', [{ path: 'lane.txt' }])), /ENOENT|unsupported/);
  assert.equal(invoke(f, request('r-delete', [{ path: 'lane.txt', delete: true }])).outcome, 'published');
  assert.throws(() => run(f.root, ['show', 'origin/main:lane.txt']));
});

test('a deletion recreated after capture remains refused instead of silently deleting its remote path', () => {
  const f = fixture(); fs.unlinkSync(path.join(f.root, 'lane.txt'));
  const result = invoke(f, request('r-delete-recreated', [{ path: 'lane.txt', delete: true }]), { hooks: { afterCapture: () => fs.writeFileSync(path.join(f.root, 'lane.txt'), 'later edit\n') } });
  assert.equal(result.outcome, 'refused'); assert.equal(run(f.root, ['show', 'origin/main:lane.txt']), 'baseline');
});

test('capture never follows a symlink ancestor', () => {
  const f = fixture(); fs.mkdirSync(path.join(f.root, 'outside')); fs.writeFileSync(path.join(f.root, 'outside', 'x'), 'x'); fs.symlinkSync('outside', path.join(f.root, 'links'));
  assert.throws(() => captureOne(f.root, { path: 'links/x' }), /symlink ancestor/);
});

test('private exclusions and repository internals deny before capture even when their prefix is allowed', () => {
  const f = fixture(); const authority = JSON.parse(fs.readFileSync(f.authorityFile));
  authority.bindings[0].allowedRelativePrefixes.push('private', '.git'); authority.bindings[0].excludedRelativePrefixes = ['private'];
  fs.mkdirSync(path.join(f.root, 'private')); fs.writeFileSync(path.join(f.root, 'private', 'secret'), 'no read'); fs.writeFileSync(f.authorityFile, JSON.stringify(authority));
  assert.throws(() => invoke(f, request('r-private', [{ path: 'private/secret' }])), /private path refused/);
  assert.throws(() => invoke(f, request('r-internal', [{ path: '.git/config' }])), /internal path refused/);
});

test('binary, executable, and leaf symlink snapshots preserve Git modes without following the link', () => {
  const f = fixture(); const binary = Buffer.from([0, 255, 7, 0, 99]);
  fs.writeFileSync(path.join(f.root, 'bin.dat'), binary); fs.writeFileSync(path.join(f.root, 'run.sh'), '#!/bin/sh\necho fixture\n'); fs.chmodSync(path.join(f.root, 'run.sh'), 0o755); fs.symlinkSync('bin.dat', path.join(f.root, 'link'));
  assert.equal(invoke(f, request('r-modes', [{ path: 'bin.dat' }, { path: 'run.sh' }, { path: 'link' }])).outcome, 'published');
  assert.match(run(f.root, ['ls-tree', 'origin/main', '--', 'run.sh']), /^100755 /);
  assert.match(run(f.root, ['ls-tree', 'origin/main', '--', 'link']), /^120000 /);
  assert.deepEqual(execFileSync('git', ['show', 'origin/main:bin.dat'], { cwd: f.root }), binary);
  assert.equal(run(f.root, ['show', 'origin/main:link']), 'bin.dat');
});

test('a file changed between anchored read and second lstat is refused as busy', () => {
  const f = fixture(), target = path.join(f.root, 'lane.txt'), original = fs.realpathSync; let changed = false;
  fs.realpathSync = function(file, ...rest) {
    const resolved = original.call(this, file, ...rest);
    if (String(file).startsWith('/proc/self/fd/') && !changed) { changed = true; fs.writeFileSync(target, 'changed after read\n'); }
    return resolved;
  };
  try { assert.throws(() => captureOne(f.root, { path: 'lane.txt' }), /busy editing/); }
  finally { fs.realpathSync = original; }
});

test('a remote advance after admission retries against fresh owned-path checks', () => {
  const f = fixture(); fs.writeFileSync(path.join(f.root, 'lane.txt'), 'ours after race\n'); let raced = false;
  const result = invoke(f, request('r-race', [{ path: 'lane.txt' }]), { hooks: { beforePush: () => { if (!raced) { raced = true; advanceRemote(f); } } } });
  assert.equal(raced, true); assert.equal(result.outcome, 'published'); assert.equal(run(f.root, ['show', 'origin/main:lane.txt']), 'ours after race');
});

test('a crash after a successful push reconciles remote content before atomically recording baseline and receipt', () => {
  const f = fixture(); fs.writeFileSync(path.join(f.root, 'lane.txt'), 'recover me\n');
  const first = invoke(f, request('r-crash', [{ path: 'lane.txt' }]), { hooks: { afterPush: () => { throw new Error('fixture crash'); } } });
  assert.equal(first.outcome, 'push-uncertain');
  const pushed = run(f.root, ['ls-remote', '--refs', 'origin', 'refs/heads/main']);
  const second = invoke(f, request('r-crash', [{ path: 'lane.txt' }]));
  assert.equal(second.outcome, 'published'); assert.equal(run(f.root, ['ls-remote', '--refs', 'origin', 'refs/heads/main']), pushed);
  const state = JSON.parse(fs.readFileSync(f.stateFile)); assert.equal(state.requests['r-crash'].phase, 'published'); assert.equal(state.receipts['r-crash'].outcome, 'published');
});

test('a validated dead lock owner is recovered, while a malformed lock would require controller recovery', () => {
  const f = fixture(), lock = `${f.stateFile}.lock`; fs.mkdirSync(lock); fs.writeFileSync(path.join(lock, 'owner.json'), JSON.stringify({ pid: 999999, startTicks: '0', bootId: f.identity.bootId, token: 'dead', path: lock }));
  fs.writeFileSync(path.join(f.root, 'lane.txt'), 'after dead lock\n'); assert.equal(invoke(f, request('r-dead-lock', [{ path: 'lane.txt' }])).outcome, 'published');
  fs.mkdirSync(lock); fs.writeFileSync(path.join(lock, 'owner.json'), '{bad'); assert.throws(() => invoke(f, request('r-bad-lock', [{ path: 'lane.txt' }])), /needs controller recovery/);
});
