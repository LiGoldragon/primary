import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import { checkup, failureEpisode, livenessFromAgents, thinSummary } from './core-checkup.mjs';

test('restarts an owned failed unit only once during a continuing episode', async () => {
  const calls = [];
  const run = async argv => { calls.push(argv); return { code: argv.includes('restart') || argv.includes('is-failed') ? 0 : 3 }; };
  const input = { run, units: [{ name: 'owned.service', scope: 'user', owned: true, allowRestart: true }], liveness: [], endpoints: [], allowRepair: true, now: () => '2026-09-15T00:00:00Z' };
  const first = await checkup({ ...input, state: {} });
  assert.equal(first.events.find(event => event.kind === 'repair').action, 'restart-attempted');
  const second = await checkup({ ...input, state: first.state });
  assert.equal(second.events.some(event => event.kind === 'repair'), false);
  assert.equal(failureEpisode(true, 'active'), false);
});

test('wake is reported as undelivered and never repairs a service', async () => {
  const result = await checkup({ run: async () => ({ code: 0 }), endpoints: [], units: [], liveness: [{ name: 'primary', status: 'idle', idleMinutes: 91, openWork: true }], wake: { enabled: true, send: async () => ({ accepted: false }) } });
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


test('fresh Claude status retains an unknown idle duration and suppresses completed work', () => {
  const result = livenessFromAgents(
    [{ name: 'primary', id: '840e42bb', openWork: true }, { name: 'secondary', id: '57a7aa02', openWork: true }],
    [{ id: '840e42bb', status: 'waiting', state: 'blocked' }, { id: '57a7aa02', status: 'idle', state: 'done' }],
  );
  assert.deepEqual(result, [
    { name: 'primary', status: 'waiting', idleMinutes: null, openWork: true },
    { name: 'secondary', status: 'idle', idleMinutes: null, openWork: false },
  ]);
});

test('a non-applicable legacy unit is recorded without a failed episode', async () => {
  const result = await checkup({ run: async () => ({ code: 1 }), endpoints: [], liveness: [], units: [{ name: 'cc-daemon.service', scope: 'user', applicable: false }] });
  assert.equal(result.events[0].status, 'not-applicable');
  assert.equal(result.state.failed['cc-daemon.service'], false);
});


test('missing persistent config emits a thin unhealthy event and fails', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'core-checkup-test-'));
  const eventPath = path.join(directory, 'events.ndjson');
  const result = spawnSync(process.execPath, ['tools/core-checkup.mjs', path.join(directory, 'missing-roster.json'), path.join(directory, 'missing-policy.json'), eventPath, path.join(directory, 'state.json')]);
  assert.notEqual(result.status, 0);
  assert.equal(JSON.parse(fs.readFileSync(eventPath, 'utf8')).status, 'missing');
  fs.rmSync(directory, { recursive: true, force: true });
});

test('Ygg evidence requires the yggTun route as well as reachability', async () => {
  const calls = [];
  const result = await checkup({
    endpoints: [{ name: 'peer', address: '200::1' }], units: [], liveness: [],
    run: async argv => { calls.push(argv); return argv[0] === 'ip' ? { code: 0, stdout: '200::1 dev eth0 src 200::2' } : { code: 0 }; },
  });
  assert.equal(result.events[0].status, 'failed');
  assert.equal(calls.some(argv => argv[0] === 'ping'), false);
});

test('an inactive owned unit is never restarted', async () => {
  const calls = [];
  await checkup({
    endpoints: [], liveness: [], allowRepair: true,
    units: [{ name: 'owned.service', scope: 'user', owned: true, allowRestart: true }],
    run: async argv => { calls.push(argv); return { code: 3 }; },
  });
  assert.equal(calls.some(argv => argv.includes('restart')), false);
});

test('truthy repair and ownership values cannot authorize a restart', async () => {
  const calls = [];
  await checkup({
    endpoints: [], liveness: [], allowRepair: 'true',
    units: [{ name: 'owned.service', scope: 'user', owned: 'true', allowRestart: true }],
    run: async argv => { calls.push(argv); return { code: argv.includes('is-failed') ? 0 : 3 }; },
  });
  assert.equal(calls.some(argv => argv.includes('restart')), false);
});

test('CLI fails closed for corrupt state and an existing state lock', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'core-checkup-test-'));
  const roster = path.join(directory, 'roster.json');
  const policy = path.join(directory, 'policy.json');
  const events = path.join(directory, 'events.ndjson');
  const state = path.join(directory, 'state.json');
  fs.writeFileSync(roster, JSON.stringify({ endpoints: [], units: [], allowRestart: false }));
  fs.writeFileSync(policy, JSON.stringify({ eventLog: { retention: 'test' }, allowRepair: false, luna: false, wake: { enabled: false }, units: [] }));
  fs.writeFileSync(state, '{');
  assert.notEqual(spawnSync(process.execPath, ['tools/core-checkup.mjs', roster, policy, events, state]).status, 0);
  assert.match(fs.readFileSync(events, 'utf8'), /"kind":"state","name":"core-checkup","status":"corrupt"/);
  fs.writeFileSync(state, '{}');
  fs.writeFileSync(`${state}.lock`, 'claimed');
  assert.notEqual(spawnSync(process.execPath, ['tools/core-checkup.mjs', roster, policy, events, state]).status, 0);
  assert.match(fs.readFileSync(events, 'utf8'), /"kind":"state","name":"core-checkup","status":"locked"/);
  fs.rmSync(directory, { recursive: true, force: true });
});

test('quota windows preserve used semantics and label derived remaining separately', async () => {
  const quota = [{ kind: 'quota', name: 'account.primary', status: 'observed', usedPercent: 48, remainingPercent: 52, windowMinutes: 10080, resetsAt: '2026-09-19T15:05:28.000Z', observedAt: '2026-09-16T00:27:33.000Z' }];
  const result = await checkup({ run: async () => ({ code: 0 }), endpoints: [], units: [], liveness: [], quota });
  assert.deepEqual(result.events.find(event => event.name === 'account.primary'), { schema: 'core-checkup/v1', at: result.events.find(event => event.name === 'account.primary').at, ...quota[0] });
  assert.equal(result.events.find(event => event.name === 'claude').status, 'unknown');
});
