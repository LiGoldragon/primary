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
