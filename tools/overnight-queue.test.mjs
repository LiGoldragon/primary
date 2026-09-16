import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { acquire, catalog, complete, jobKey, readState, release, runOnce, select, validateReceipt, writeState } from './overnight-queue.mjs';

const fixed = catalog['message-idle-idempotence'];
const job = { task: 'message-idle-idempotence', sourceRevision: fixed.sourceBase, outputContract: fixed.outputContract, provider: 'codex', workspace: '/tmp/overnight-fixture', prompt: fixed.prompt, promptHash: fixed.promptHash, model: 'gpt-5.6-luna' };
const quota = { status: 'available', observedAt: new Date().toISOString() };
const fresh = () => { const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'overnight-queue-')); return { dir, state: path.join(dir, 'state.json'), lock: path.join(dir, 'lock') }; };
test('only one claimant acquires the queue lease', () => {
  const f = fresh(), fd = acquire(f.lock);
  assert.deepEqual(runOnce({ statePath: f.state, lockPath: f.lock, jobs: [job] }), { status: 'locked' });
  release(f.lock, fd);
});
test('claim is durable before an interrupted child and allows one retry', () => {
  const f = fresh();
  const first = runOnce({ statePath: f.state, lockPath: f.lock, jobs: [job], codexQuota: quota, spawn: () => ({ status: 1 }) });
  assert.equal(first.status, 'Interrupted');
  const state = readState(f.state), key = jobKey(job);
  assert.equal(state.jobs[key].attempts, 1);
  const second = select(state, [job], { codexQuota: quota }); assert.equal(second.runId.length > 10, true);
  assert.equal(state.jobs[key].attempts, 2);
  assert.equal(select(state, [job], { codexQuota: quota }), null);
});
test('success survives restart and cannot be duplicated', () => {
  const f = fresh(), state = readState(f.state), claim = select(state, [job], { codexQuota: quota });
  complete(state, claim.key, claim.runId, { ok: true, outputRef: 'out', outputHash: 'hash' }); writeState(f.state, state);
  assert.equal(runOnce({ statePath: f.state, lockPath: f.lock, jobs: [job], codexQuota: quota }).status, 'idle');
});
test('corrupt state and unavailable Codex quota fail closed', () => {
  const f = fresh(); fs.writeFileSync(f.state, '{');
  assert.throws(() => runOnce({ statePath: f.state, lockPath: f.lock, jobs: [job] }));
  const state = { version: 1, jobs: {}, deadline: null };
  assert.equal(select(state, [job], { codexQuota: { status: 'unavailable', observedAt: new Date().toISOString() } }), null);
});
test('deadline and stale completion are rejected', () => {
  const state = { version: 1, jobs: {}, deadline: '2000-01-01T00:00:00.000Z' };
  assert.equal(select(state, [job], { codexQuota: quota }), null);
  assert.throws(() => complete(state, 'none', 'none', { ok: true }));
});
test('invalid or future quota and mismatched receipt fail closed', () => {
  const state = { version: 1, jobs: {}, deadline: 'not-a-date' };
  assert.equal(select(state, [job], { codexQuota: quota }), null);
  assert.equal(select({ version: 1, jobs: {}, deadline: null }, [job], { now: Date.now(), codexQuota: { status: 'available', observedAt: 'not-a-date' } }), null);
  const claim = { key: jobKey(job), runId: 'run', job };
  assert.equal(validateReceipt({ jobKey: claim.key, runId: 'wrong' }, claim), false);
});
