import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { validateConfig, wake } from './wake-adapter.mjs';

const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'wake-adapter-'));
const message = path.join(directory, 'peer.txt');
fs.writeFileSync(message, 'A bounded peer-file wake request.');
const eligible = { status: 'idle', idleMinutes: 90, openWork: true };
const config = { enabled: true, targets: [{ name: 'claude', kind: 'claude', sessionShort: '57a7aa' }, { name: 'codex', kind: 'codex', threadId: 'thread-1' }] };

test('disabled is the default outcome and performs no submission', async () => {
  let calls = 0;
  const result = await wake({ enabled: false, targets: [] }, message, {}, { run: () => { calls++; } });
  assert.equal(result.reason, 'disabled'); assert.equal(calls, 0);
});

test('submits serialized safe argv forms and distinguishes acceptance from delivery', async () => {
  const calls = [];
  const result = await wake(config, message, { claude: eligible, codex: eligible }, { promptRelay: '/published/prompt-relay-6301363e', run: argv => { calls.push(argv); return { status: 0 }; } });
  assert.deepEqual(calls[0], ['/published/prompt-relay-6301363e', 'claude', '--source', message, '--source-format', 'peer-file', '--session-short', '57a7aa']);
  assert.deepEqual(calls[1].slice(0, 5), ['codex', 'queue', '--thread', 'thread-1', '--message']);
  const [header, body] = calls[1][5].split('\n\n');
  const sha256 = crypto.createHash('sha256').update(body, 'utf8').digest('hex');
  assert.deepEqual(JSON.parse(header).provenance, { source_path: message, source_format: 'peer-file', source_message_id: sha256, source_timestamp: null, sha256_utf8: sha256 });
  assert.equal(body, 'A bounded peer-file wake request.');
  assert.equal(result.accepted, true); assert.equal(result.delivery, 'unobserved');
});

test('unknown, approval-wait, and incomplete observations refuse without running', async () => {
  let calls = 0;
  const run = () => { calls++; return { status: 0 }; };
  const result = await wake(config, message, { claude: { status: 'waitingFor permission', idleMinutes: 91, openWork: true }, codex: { status: 'unknown', idleMinutes: null, openWork: true } }, { run });
  assert.equal(calls, 0); assert.equal(result.accepted, false); assert.deepEqual(result.results.map(item => item.reason), ['not-eligible', 'not-eligible']);
  assert.throws(() => validateConfig({ enabled: true, targets: [{ name: 'bad', kind: 'claude', sessionShort: 'x', approvalWait: false }] }), /unsafe wake target/);
});

test('a submission refusal remains distinct from recipient delivery', async () => {
  const result = await wake({ enabled: true, targets: [config.targets[1]] }, message, { codex: eligible }, { run: () => ({ status: 2 }) });
  assert.deepEqual(result.results[0], { name: 'codex', accepted: false, delivery: 'not-accepted', reason: 'submission-refused' });
});


test('timeout and mixed status results refuse without claiming acceptance', async () => {
  const target = { enabled: true, targets: [config.targets[1]] };
  let result = await wake(target, message, { codex: eligible }, { run: () => ({ status: null, error: { code: 'ETIMEDOUT' } }) });
  assert.equal(result.accepted, false); assert.equal(result.results[0].reason, 'submission-refused');
  result = await wake(target, message, { codex: eligible }, { run: () => ({ status: 1, code: 0 }) });
  assert.equal(result.accepted, false);
});
