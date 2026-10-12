import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {test} from 'node:test';
import {notifyTurnEnd} from './turn-end.mjs';

test('actual clean/dirty repository: notification only, identity, self suppression and held transport', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'committer-hook-proof-'));
  const primary = path.join(root, 'primary');
  fs.mkdirSync(primary);
  assert.equal(spawnSync('git', ['init', primary]).status, 0);
  const transcript = path.join(root, 'native.jsonl');
  fs.writeFileSync(transcript, '{"fixture":"transcript outside repository"}\n');
  const event = {hook_event_name: 'Stop', session_id: 'actual-fixture-session', transcript_path: transcript};
  const env = {...process.env, FLOW_ID: 'aaaaaa'};
  const sent = [];
  let transport = 'Transported.{ bbbbbb done }';
  const run = (program, args, options) => {
    if (program === 'hm-send') { sent.push({args, ...options}); return transport; }
    assert.equal(program, 'git');
    const result = spawnSync(program, args, {encoding: 'utf8', ...options});
    assert.equal(result.status, 0, result.stderr);
    return result.stdout;
  };
  const invoke = override => notifyTurnEnd({primary, committer: 'bbbbbb', event, env, run, ...override});
  assert.equal(invoke().status, 'clean');
  assert.equal(invoke({env: {...env, FLOW_ID: ''}}).status, 'clean');
  assert.equal(sent.length, 0);
  fs.writeFileSync(path.join(primary, 'owned.txt'), 'uncommitted owner bytes\n');
  assert.equal(invoke().status, 'notified');
  assert.deepEqual(sent[0].args, ['bbbbbb', '--stdin']);
  assert.match(sent[0].input, /"flow_id":"aaaaaa"/);
  assert.ok(sent[0].input.includes(transcript));
  assert.equal(invoke({env: {...env, FLOW_ID: 'bbbbbb'}}).status, 'self');
  assert.equal(sent.length, 1);
  assert.equal(invoke({env: {...env, FLOW_ID: ''}}).status, 'notified');
  assert.match(sent[1].input, /"flow_id":null,"identity_kind":"native_session"/);
  assert.match(sent[1].input, /"session_id":"actual-fixture-session"/);
  assert.equal(sent[1].env.FLOW_ID, '');
  assert.throws(() => invoke({env: {...env, FLOW_ID: 'not-a-claim'}}), /FLOW_ID is malformed/);
  assert.throws(() => invoke({env: {...env, FLOW_ID: ''}, event: {...event, session_id: ''}}), /session_id/);
  assert.throws(() => invoke({event: {...event, transcript_path: null}}), /transcript/);
  transport = 'Held.{ fixture }';
  assert.throws(() => invoke(), /not transported/);
  assert.equal(fs.readFileSync(path.join(primary, 'owned.txt'), 'utf8'), 'uncommitted owner bytes\n');
  assert.equal(spawnSync('git', ['-C', primary, 'rev-parse', '--verify', 'HEAD']).status, 128);
});


test('Primary-own clean boundary ignores nested dirt but detects owned paths, modes and changed gitlinks', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'committer-own-path-proof-'));
  const primary = path.join(root, 'primary');
  const nested = path.join(primary, 'flow');
  fs.mkdirSync(nested, {recursive: true});
  const git = (cwd, ...args) => {
    const result = spawnSync('git', ['-C', cwd, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', ...args], {encoding: 'utf8'});
    assert.equal(result.status, 0, result.stderr);
    return result.stdout;
  };
  git(nested, 'init');
  fs.writeFileSync(path.join(nested, 'source.txt'), 'original nested bytes\n');
  git(nested, 'add', 'source.txt');
  git(nested, 'commit', '-m', 'nested fixture');
  const originalLink = git(nested, 'rev-parse', 'HEAD').trim();
  git(primary, 'init');
  git(primary, 'config', 'core.filemode', 'true');
  fs.writeFileSync(path.join(primary, 'owned.txt'), 'original Primary bytes\n');
  git(primary, 'add', 'owned.txt');
  git(primary, 'update-index', '--add', '--cacheinfo', `160000,${originalLink},flow`);
  git(primary, 'commit', '-m', 'Primary fixture');
  const transcript = path.join(root, 'editor.jsonl');
  fs.writeFileSync(transcript, '{}\n');
  let sends = 0;
  const run = (program, args, options) => {
    if (program === 'hm-send') { sends++; return 'Transported.{ bbbbbb done }'; }
    const result = spawnSync(program, args, {encoding: 'utf8', ...options});
    assert.equal(result.status, 0, result.stderr);
    return result.stdout;
  };
  const invoke = () => notifyTurnEnd({primary, committer: 'bbbbbb', event: {hook_event_name: 'Stop', session_id: 'editor', transcript_path: transcript}, env: {...process.env, FLOW_ID: 'aaaaaa'}, run});
  fs.writeFileSync(path.join(nested, 'source.txt'), 'preserved nested edit\n');
  fs.writeFileSync(path.join(nested, 'untracked.txt'), 'preserved nested untracked\n');
  assert.notEqual(git(primary, 'status', '--porcelain=v1'), '');
  assert.equal(invoke().status, 'clean');
  assert.equal(sends, 0);
  fs.writeFileSync(path.join(primary, 'new.txt'), 'new owned bytes\n');
  assert.equal(invoke().status, 'notified');
  git(primary, 'add', 'new.txt');
  assert.equal(invoke().status, 'notified');
  git(primary, 'commit', '-m', 'new owned path');
  fs.appendFileSync(path.join(primary, 'owned.txt'), 'edited\n');
  assert.equal(invoke().status, 'notified');
  git(primary, 'add', 'owned.txt');
  assert.equal(invoke().status, 'notified');
  git(primary, 'commit', '-m', 'owned edit');
  fs.chmodSync(path.join(primary, 'owned.txt'), 0o755);
  assert.equal(invoke().status, 'notified');
  git(primary, 'add', 'owned.txt');
  git(primary, 'commit', '-m', 'owned mode');
  assert.equal(invoke().status, 'clean');
  git(nested, 'add', 'source.txt');
  git(nested, 'commit', '-m', 'new nested revision');
  assert.notEqual(git(nested, 'rev-parse', 'HEAD').trim(), originalLink);
  assert.equal(invoke().status, 'notified');
  git(primary, 'add', 'flow');
  assert.equal(invoke().status, 'notified');
  assert.equal(fs.readFileSync(path.join(nested, 'source.txt'), 'utf8'), 'preserved nested edit\n');
  assert.equal(fs.readFileSync(path.join(nested, 'untracked.txt'), 'utf8'), 'preserved nested untracked\n');
});


test('restored recipient overrides stale launcher target without settings reload or retired send', () => {
  const primary = fs.mkdtempSync(path.join(os.tmpdir(), 'committer-recipient-proof-'));
  assert.equal(spawnSync('git', ['init', primary]).status, 0);
  const directory = path.join(primary, 'tools', 'primary-committer');
  fs.mkdirSync(directory, {recursive: true});
  const recipient = path.join(directory, 'recipient.json');
  fs.writeFileSync(recipient, JSON.stringify({flow_id: '127d95'}));
  const transcript = path.join(primary, 'editor.jsonl');
  fs.writeFileSync(transcript, '{}\n');
  const sent = [];
  const run = (program, args, options) => {
    if (program === 'hm-send') { sent.push(args[0]); return `Transported.{ ${args[0]} done }`; }
    const result = spawnSync(program, args, {encoding: 'utf8', ...options});
    assert.equal(result.status, 0, result.stderr);
    return result.stdout;
  };
  const invoke = flow => notifyTurnEnd({primary, committer: '8b084b', event: {hook_event_name: 'Stop', session_id: 'actual-fixture-session', transcript_path: transcript}, env: {...process.env, FLOW_ID: flow}, run});
  assert.equal(invoke('6f115e').recipient, '127d95');
  assert.deepEqual(sent, ['127d95']);
  assert.equal(invoke('127d95').status, 'self');
  assert.deepEqual(sent, ['127d95']);
  fs.writeFileSync(recipient, '{bad json');
  assert.throws(() => invoke('6f115e'));
  fs.writeFileSync(recipient, JSON.stringify({flow_id: 'invalid recipient'}));
  assert.throws(() => invoke('6f115e'), /standing committer/);
  assert.deepEqual(sent, ['127d95']);
  fs.writeFileSync(recipient, JSON.stringify({flow_id: 'abcdef'}));
  assert.equal(invoke('6f115e').recipient, 'abcdef');
  assert.deepEqual(sent, ['127d95', 'abcdef']);
  fs.unlinkSync(recipient);
  assert.equal(invoke('6f115e').recipient, '8b084b');
  assert.deepEqual(sent, ['127d95', 'abcdef', '8b084b']);
});
