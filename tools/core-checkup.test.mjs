import assert from 'node:assert/strict';
import test from 'node:test';
import { checkup, failureEpisode, thinSummary } from './core-checkup.mjs';

test('restarts an owned failed unit only once during a continuing episode', async () => {
  const calls = [];
  const run = async argv => { calls.push(argv); return { code: argv.includes('restart') ? 0 : 3 }; };
  const input = { run, units: [{ name: 'owned.service', scope: 'user', owned: true, allowRestart: true }], liveness: [], endpoints: [], allowRepair: true, now: () => '2026-09-15T00:00:00Z' };
  const first = await checkup({ ...input, state: {} });
  assert.equal(first.events.find(event => event.kind === 'repair').action, 'restart-attempted');
  const second = await checkup({ ...input, state: first.state });
  assert.equal(second.events.some(event => event.kind === 'repair'), false);
  assert.equal(failureEpisode(true, 'active'), false);
});

test('wake is reported as undelivered and never repairs a service', async () => {
  const result = await checkup({ run: async () => ({ code: 0 }), endpoints: [], units: [], liveness: [{ name: 'primary', status: 'idle', idleMinutes: 91, openWork: true }], wake: async () => ({ accepted: false }) });
  assert.deepEqual(result.events.at(-1), { schema: 'core-checkup/v1', at: result.events.at(-1).at, kind: 'wake', name: 'primary', status: 'undelivered' });
});

test('Luna receives only thin deterministic observations and its result is an event', async () => {
  let input;
  const result = await checkup({
    run: async () => ({ code: 0 }), endpoints: [], units: [],
    liveness: [{ name: 'primary', status: 'idle', idleMinutes: 4, openWork: false }],
    luna: async summary => { input = summary; return { status: 'attention', findings: ['semantic_health_unverified'] }; },
  });
  assert.deepEqual(input, thinSummary(result.events.slice(0, -1)));
  assert.deepEqual(result.events.at(-1).findings, ['semantic_health_unverified']);
  assert.equal(result.events.at(-1).kind, 'luna');
});
