import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {test} from 'node:test';

test('named JJ commits and a published late squash preserve concurrent and excluded bytes; raced lease refuses', () => {
  // Entirely synthetic repositories, never a clone or operation on Primary.
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'committer-jj-proof-'));
  const repo = path.join(root, 'working');
  const remote = path.join(root, 'origin.git');
  const config = path.join(root, 'jj.toml');
  fs.writeFileSync(config, '[user]\nname = "Synthetic committer"\nemail = "fixture@example.invalid"\n');
  const env = {...process.env, JJ_CONFIG: config, GIT_CONFIG_GLOBAL: '/dev/null', GIT_CONFIG_NOSYSTEM: '1'};
  const transcript = [];
  function run(program, args, cwd = root, expected = 0) {
    const r = spawnSync(program, args, {cwd, env, encoding: 'utf8'});
    transcript.push({program, args, status: r.status, stdout: r.stdout, stderr: r.stderr});
    fs.writeFileSync(path.join(root, 'commands.json'), JSON.stringify(transcript, null, 2));
    assert.equal(r.status, expected, `${program} ${args.join(' ')}\n${r.stderr}\nEvidence: ${root}`);
    return r.stdout.trim();
  }
  const jj = (...args) => run('jj', args, repo);
  const git = (...args) => run('git', args, repo);
  const write = (name, body) => { const f = path.join(repo, name); fs.mkdirSync(path.dirname(f), {recursive: true}); fs.writeFileSync(f, body); };
  run('git', ['init', '--bare', remote]);
  run('jj', ['git', 'init', '--colocate', repo]);
  jj('git', 'remote', 'add', 'origin', remote);
  write('base.txt', 'base\n');
  jj('commit', '-m', 'base fixture', 'base.txt');
  jj('bookmark', 'set', 'main', '-r', '@-');
  jj('git', 'push', '--remote', 'origin', '--bookmark', 'main');
  write('flows/aaaaaa/work.md', 'A first\n');
  write('flows/bbbbbb/work.md', 'B concurrent\n');
  write('.agents/fixture.md', 'excluded generated fixture\n');
  jj('commit', '-m', 'aaaaaa: first work', 'flows/aaaaaa/work.md');
  const a = jj('log', '-r', '@-', '--no-graph', '-T', 'change_id');
  assert.equal(fs.readFileSync(path.join(repo, 'flows/bbbbbb/work.md'), 'utf8'), 'B concurrent\n');
  jj('bookmark', 'set', 'main', '-r', '@-');
  jj('git', 'push', '--remote', 'origin', '--bookmark', 'main');
  assert.equal(run('git', ['--git-dir', remote, 'ls-tree', '-r', '--name-only', 'main']), 'base.txt\nflows/aaaaaa/work.md');
  jj('commit', '-m', 'bbbbbb: concurrent work', 'flows/bbbbbb/work.md');
  jj('bookmark', 'set', 'main', '-r', '@-');
  jj('git', 'push', '--remote', 'origin', '--bookmark', 'main');
  const before = run('git', ['--git-dir', remote, 'rev-parse', 'main']);
  write('flows/aaaaaa/work.md', 'A first\nA late correction\n');
  // Explicitly authorized published-history rewrite, scoped to this command.
  jj('--ignore-immutable', 'squash', '--into', a, '--use-destination-message', 'flows/aaaaaa/work.md');
  const after = jj('log', '-r', 'main', '--no-graph', '-T', 'commit_id');
  assert.notEqual(after, before);
  git('push', 'origin', `${after}:refs/heads/main`, `--force-with-lease=refs/heads/main:${before}`);
  assert.equal(run('git', ['--git-dir', remote, 'show', 'main:flows/aaaaaa/work.md']), 'A first\nA late correction');
  assert.equal(run('git', ['--git-dir', remote, 'show', 'main:flows/bbbbbb/work.md']), 'B concurrent');
  assert.equal(fs.readFileSync(path.join(repo, '.agents/fixture.md'), 'utf8'), 'excluded generated fixture\n');
  assert.ok(!run('git', ['--git-dir', remote, 'ls-tree', '-r', '--name-only', 'main']).includes('.agents'));
  // A foreign remote advance is simulated without another checkout.
  const tree = git('rev-parse', `${after}^{tree}`);
  const foreign = run('git', ['-c', 'user.name=Foreign fixture', '-c', 'user.email=foreign@example.invalid', 'commit-tree', tree, '-p', after, '-m', 'unexpected remote writer'], repo);
  git('push', 'origin', `${foreign}:refs/heads/main`);
  const refusal = spawnSync('git', ['push', 'origin', `${after}:refs/heads/main`, `--force-with-lease=refs/heads/main:${after}`], {cwd: repo, env, encoding: 'utf8'});
  assert.notEqual(refusal.status, 0);
  assert.match(refusal.stderr, /stale info/);
  assert.equal(run('git', ['--git-dir', remote, 'rev-parse', 'main']), foreign);
  assert.equal(fs.readFileSync(path.join(repo, '.agents/fixture.md'), 'utf8'), 'excluded generated fixture\n');
  console.log(`Synthetic JJ evidence: ${root}`);
});
