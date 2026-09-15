import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const tool = path.join(import.meta.dirname, 'claude-user-prompt-submit.mjs');
const lane = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-prompt-hook-'));
const run = (event, env = {}) => spawnSync(process.execPath, [tool], {
  input: JSON.stringify(event), encoding: 'utf8', env: { ...process.env, CLUSTERRELAY_FLOW_LANE: lane, ...env },
});
const event = prompt => ({
  hook_event_name: 'UserPromptSubmit',
  session_id: 'fba65fcb-092d-494a-9225-f72bca842186',
  prompt_id: 'aa0e5aaa-0a2c-4b10-b11a-24eeff54e01c',
  transcript_path: '/tmp/witness.jsonl',
  prompt,
});

const text = 'one two three four five six seven eight nine';
let result = run(event(text));
assert.equal(result.status, 0);
assert.equal(JSON.parse(result.stdout).kind, 'recorded');
const ledger = path.join(lane, 'claude-user-prompt-submit.jsonl');
const record = JSON.parse(fs.readFileSync(ledger, 'utf8'));
assert.equal(record.source_origin, 'unclassified-claude-user-prompt-submit');
assert.equal(record.sha256_utf8, crypto.createHash('sha256').update(text, 'utf8').digest('hex'));
assert.deepEqual(record.first_six_words, ['one', 'two', 'three', 'four', 'five', 'six']);
assert.deepEqual(record.last_six_words, ['four', 'five', 'six', 'seven', 'eight', 'nine']);
assert.equal(JSON.stringify(record).includes(text), false, 'ledger must not retain prompt body');

result = run(event('[PEER other] one two three'));
assert.equal(result.status, 0);
assert.equal(JSON.parse(result.stdout).kind, 'ignored-relayed-prompt');
result = run(event('{"provenance":{"source_message_id":"one"}}\n\npeer body'));
assert.equal(result.status, 0);
assert.equal(JSON.parse(result.stdout).kind, 'ignored-relayed-prompt');
result = run(event('Relay.{ «typed source» }\n\npeer body'));
assert.equal(result.status, 0);
assert.equal(JSON.parse(result.stdout).kind, 'ignored-relayed-prompt');
assert.equal(fs.readFileSync(ledger, 'utf8').trim().split('\n').length, 1);

result = run({ ...event('x'), hook_event_name: 'Stop' });
assert.equal(result.status, 2);
assert.match(result.stdout, /unexpected hook event/);
result = run(event('x'), { CLUSTERRELAY_FLOW_LANE: 'relative' });
assert.equal(result.status, 2);
assert.match(result.stdout, /absolute flow lane/);
console.log('claude prompt submit fixtures passed');
