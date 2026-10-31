import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {test} from 'node:test';
import {publishSelected, validateRequest, verifyLifetime} from './publish-selected.mjs';

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'selected-publisher-proof-'));
  const primary = path.join(root, 'primary');
  const remote = path.join(root, 'origin.git');
  fs.mkdirSync(primary);
  const env = {...process.env, FLOW_ID: 'abcdef', GIT_CONFIG_GLOBAL: '/dev/null', GIT_CONFIG_NOSYSTEM: '1'};
  const git = (...args) => {
    const r = spawnSync('git', ['-C', primary, ...args], {env, encoding: 'utf8'});
    assert.equal(r.status, 0, r.stderr); return r.stdout.trim();
  };
  git('init', '--initial-branch=main');
  git('config', 'user.name', 'Synthetic committer'); git('config', 'user.email', 'fixture@example.invalid');
  git('config', 'core.filemode', 'true');
  git('init', '--bare', remote); git('remote', 'add', 'origin', remote);
  const write = (name, bytes) => { const f = path.join(primary, name); fs.mkdirSync(path.dirname(f), {recursive: true}); fs.writeFileSync(f, bytes); };
  write('tools/primary-committer/recipient.json', '{"flow_id":"abcdef"}\n');
  write('.gitignore', '.jj/\nignored\n');
  write('owned.txt', 'old owner\n'); write('foreign.txt', 'old foreign\n');
  git('add', '.'); git('commit', '-m', 'base'); git('push', '-u', 'origin', 'main');
  write('.jj/working_copy/state', 'foreign JJ state must not change\n');
  const lockSnapshot = `Observed.Locks.[ { 12 PrimaryPublish abcdef [ ${primary}/.PrimaryPublish.lock ] «fixture» } ]`;
  const publish = request => publishSelected(primary, request, {env, lockSnapshot});
  return {root, primary, remote, env, git, write, publish, lockSnapshot};
}

for (const detached of [false, true]) test(`selected publish preserves foreign dirty/staged/untracked/modes and JJ bytes; detached=${detached}`, () => {
  const f = fixture();
  if (detached) f.git('checkout', '--detach', 'HEAD'); // Fixture setup only; never in publisher.
  f.write('foreign.txt', 'foreign staged\n'); f.git('add', 'foreign.txt');
  const staged = f.git('ls-files', '--stage', 'foreign.txt');
  f.write('foreign.txt', 'foreign current, different from staged\n');
  fs.chmodSync(path.join(f.primary, 'foreign.txt'), 0o755);
  f.write('other/new.txt', 'concurrent untracked\n');
  f.write('owned.txt', 'owner completed\n');
  f.write('new-owned.txt', 'new owner path\n');
  const before = f.git('rev-parse', 'HEAD');
  const result = f.publish({paths: ['owned.txt', 'new-owned.txt'], message: 'owner transcript: completed edit'});
  assert.equal(result.status, 'published'); assert.equal(result.parent, before);
  assert.equal(result.workingFilesWritten, 0);
  assert.equal(f.git('ls-remote', 'origin', 'refs/heads/main').split(/\s+/)[0], result.commit);
  assert.equal(f.git('rev-parse', 'HEAD'), result.commit);
  assert.deepEqual(f.git('diff-tree', '--no-commit-id', '--name-only', '-r', result.commit).split('\n'), ['new-owned.txt', 'owned.txt']);
  assert.equal(f.git('ls-files', '--stage', 'foreign.txt'), staged);
  assert.equal(fs.readFileSync(path.join(f.primary, 'foreign.txt'), 'utf8'), 'foreign current, different from staged\n');
  assert.equal(fs.statSync(path.join(f.primary, 'foreign.txt')).mode & 0o777, 0o755);
  assert.equal(fs.readFileSync(path.join(f.primary, 'other/new.txt'), 'utf8'), 'concurrent untracked\n');
  assert.equal(fs.readFileSync(path.join(f.primary, '.jj/working_copy/state'), 'utf8'), 'foreign JJ state must not change\n');
  assert.equal(f.git('diff', '--name-only', '--', 'owned.txt'), '');
  assert.equal(f.git('diff', '--cached', '--name-only', '--', 'owned.txt'), '');
  assert.equal(f.publish({paths: ['owned.txt', 'new-owned.txt'], message: 'no new edit'}).status, 'unchanged');
  fs.writeFileSync(path.join(f.root, 'receipt.json'), JSON.stringify(result, null, 2));
  console.log(`Synthetic publication receipt: ${f.root}/receipt.json`);
});

test('base/revision and unsafe selections refuse before publication; lifetime owner mismatch refuses', () => {
  for (const key of ['base', 'revision', 'parent', 'squash', 'force']) assert.throws(() => validateRequest({paths: ['a'], message: 'x', [key]: 'HEAD'}), /forbidden/);
  for (const name of ['../a', '/tmp/a', '.', '.git/HEAD', '.jj/state', 'flows/*', 'a/../b', 'a\nb']) assert.throws(() => validateRequest({paths: [name], message: 'x'}));
  const f = fixture(); const before = f.git('rev-parse', 'HEAD'); const index = fs.readFileSync(path.join(f.primary, '.git/index'));
  assert.throws(() => verifyLifetime(f.lockSnapshot, 'badbad', `${f.primary}/.PrimaryPublish.lock`), /does not match/);
  assert.throws(() => f.publish({paths: ['tools'], message: 'directory'}), /directory/);
  f.write('ignored', 'excluded'); assert.throws(() => f.publish({paths: ['ignored'], message: 'ignored'}), /ignored/);
  fs.symlinkSync(f.root, path.join(f.primary, 'outside')); assert.throws(() => f.publish({paths: ['outside/file'], message: 'escape'}), /symlink parent/);
  assert.equal(f.git('rev-parse', 'HEAD'), before); assert.ok(fs.readFileSync(path.join(f.primary, '.git/index')).equals(index));
});

test('lifetime lock reasons accept bare and guillemet Datom strings', () => {
  const sentinel = '/home/li/primary/.PrimaryPublish.lock';
  assert.equal(verifyLifetime(`Observed.Locks.[ { 24847 x 9140db [ /x ] x } { 12 PrimaryPublish 6eda8a [ ${sentinel} ] «Lifetime standing committer hold» } ]`, '6eda8a', sentinel), '12');
});

test('divergent selected staged data and an unexpected remote tip are not repaired', () => {
  const f = fixture();
  f.write('owned.txt', 'staged variant\n'); f.git('add', 'owned.txt'); f.write('owned.txt', 'working variant\n');
  const staged = f.git('ls-files', '--stage', 'owned.txt'); const before = f.git('rev-parse', 'HEAD');
  assert.throws(() => f.publish({paths: ['owned.txt'], message: 'ambiguous bytes'}), /staged bytes differ/);
  assert.equal(f.git('ls-files', '--stage', 'owned.txt'), staged);
  const tree = f.git('rev-parse', `${before}^{tree}`);
  const other = f.git('commit-tree', tree, '-p', before, '-m', 'unexpected remote actor');
  f.git('push', 'origin', `${other}:refs/heads/main`);
  assert.throws(() => f.publish({paths: ['owned.txt'], message: 'must refuse'}), /fresh remote differ/);
  assert.equal(f.git('rev-parse', 'HEAD'), before);
  assert.equal(fs.readFileSync(path.join(f.primary, 'owned.txt'), 'utf8'), 'working variant\n');
});

test('intent-to-add is captured without confusing a genuinely staged empty file or changing foreign flags', () => {
  const f = fixture();
  f.write('intent-owned.txt', 'completed owner content\n');
  f.write('intent-foreign.txt', 'foreign unfinished content\n');
  f.git('add', '--intent-to-add', '--', 'intent-owned.txt', 'intent-foreign.txt');
  const foreignFlags = f.git('ls-files', '--debug', '-z', '--', 'intent-foreign.txt');
  const foreignStage = f.git('ls-files', '--stage', '--', 'intent-foreign.txt');
  const result = f.publish({paths: ['intent-owned.txt'], message: 'publish an intended new file'});
  assert.equal(result.status, 'published');
  assert.equal(f.git('show', `${result.commit}:intent-owned.txt`), 'completed owner content');
  assert.equal(f.git('ls-files', '--debug', '-z', '--', 'intent-foreign.txt'), foreignFlags);
  assert.equal(f.git('ls-files', '--stage', '--', 'intent-foreign.txt'), foreignStage);
  assert.equal(fs.readFileSync(path.join(f.primary, 'intent-foreign.txt'), 'utf8'), 'foreign unfinished content\n');
  assert.equal(f.git('status', '--porcelain', '--', 'intent-owned.txt'), '');

  f.write('actually-empty.txt', '');
  f.git('add', '--', 'actually-empty.txt');
  f.write('actually-empty.txt', 'a different working payload\n');
  const index = fs.readFileSync(path.join(f.primary, '.git/index'));
  const before = f.git('rev-parse', 'HEAD');
  assert.throws(() => f.publish({paths: ['actually-empty.txt'], message: 'must retain staged empty payload'}), /staged bytes differ/);
  assert.equal(f.git('rev-parse', 'HEAD'), before);
  assert.ok(fs.readFileSync(path.join(f.primary, '.git/index')).equals(index));
  assert.equal(fs.readFileSync(path.join(f.primary, 'actually-empty.txt'), 'utf8'), 'a different working payload\n');
});

test('pre-push whitespace refusal reports command status and stdout without echoing stdin or environment', () => {
  const f = fixture();
  f.write('owned.txt', 'owner trailing whitespace \n');
  const before = f.git('rev-parse', 'HEAD');
  const index = fs.readFileSync(path.join(f.primary, '.git/index'));
  assert.throws(() => f.publish({paths: ['owned.txt'], message: 'PRIVATE_COMMIT_MESSAGE_SENTINEL'}), error => {
    assert.match(error.message, /"diff" "--check"/);
    assert.match(error.message, /status=2/);
    assert.match(error.message, /stdout=owned\.txt:1: trailing whitespace/);
    assert.match(error.message, /stderr=\(empty\)/);
    assert.ok(!error.message.includes('PRIVATE_COMMIT_MESSAGE_SENTINEL'));
    assert.ok(!error.message.includes('FLOW_ID='));
    return true;
  });
  assert.equal(f.git('rev-parse', 'HEAD'), before);
  assert.equal(f.git('ls-remote', 'origin', 'refs/heads/main').split(/\s+/)[0], before);
  assert.ok(fs.readFileSync(path.join(f.primary, '.git/index')).equals(index));
});
