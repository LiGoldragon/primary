import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { acquire, complete, jobKey, readState, release, runOnce, select, writeState } from './overnight-queue.mjs';

const job = { task: 'fixture', sourceRevision: 'abc', outputContract: 'hash', provider: 'codex', workspace: '/tmp', prompt: 'fixture' };
const fresh = () => { const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'overnight-queue-')); return { dir, state: path.join(dir, 'state.json'), lock: path.join(dir, 'lock') }; };
test('only one claimant acquires the queue lease', () => {
  const f = fresh(), fd = acquire(f.lock);
  assert.deepEqual(runOnce({ statePath: f.state, lockPath: f.lock, jobs: [job] }), { status: 'locked' });
  release(f.lock, fd);
});
test('claim is durable before an interrupted child and allows one retry', () => {
  const f = fresh();
  const first = runOnce({ statePath: f.state, lockPath: f.lock, jobs: [job], spawn: () => ({ status: 1 }) });
  assert.equal(first.status, 'Interrupted');
  const state = readState(f.state), key = jobKey(job);
  assert.equal(state.jobs[key].attempts, 1);
  const second = select(state, [job]); assert.equal(second.runId.length > 10, true);
  assert.equal(state.jobs[key].attempts, 2);
  assert.equal(select(state, [job]), null);
});
test('success survives restart and cannot be duplicated', () => {
  const f = fresh(), state = readState(f.state), claim = select(state, [job]);
  complete(state, claim.key, claim.runId, { ok: true, outputRef: 'out', outputHash: 'hash' }); writeState(f.state, state);
  assert.equal(runOnce({ statePath: f.state, lockPath: f.lock, jobs: [job] }).status, 'idle');
});
test('corrupt state and unavailable Codex quota fail closed', () => {
  const f = fresh(); fs.writeFileSync(f.state, '{');
  assert.throws(() => runOnce({ statePath: f.state, lockPath: f.lock, jobs: [job] }));
  const state = { version: 1, jobs: {}, deadline: null };
  assert.equal(select(state, [job], { codexQuota: 'unavailable' }), null);
});
test('deadline and stale completion are rejected', () => {
  const state = { version: 1, jobs: {}, deadline: '2000-01-01T00:00:00.000Z' };
  assert.equal(select(state, [job]), null);
  assert.throws(() => complete(state, 'none', 'none', { ok: true }));
});
