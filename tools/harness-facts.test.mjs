import assert from 'node:assert/strict';
import test from 'node:test';
import { collectHarnessFacts } from './harness-facts.mjs';

const now = () => 1_800_000;
const codexTarget = { identifier: 'core-e43002', threadId: 'thread-core', socketPath: '/socket', openWork: true };
const claudeTarget = { identifier: 'primary-840e42', sessionId: '840e42bb-b2cd-42eb-a9ec-7659a5b13ded', transcriptPath: '/primary.jsonl', openWork: true };
const adapterCalls = [];
const adapters = {
  readFlowIdleness: async input => { adapterCalls.push(['codex', input.threadId, input.operationalState]); return { state: 'idle', idleMinutes: 91, eligible: true, source: 'codex-app-server/thread/turns/list', turnId: 'turn-1' }; },
  deriveClaudeFlowIdleness: input => { adapterCalls.push(['claude', input.sessionId, input.rosterEntry.status]); return { state: 'idle', idleMinutes: 92, eligible: true, source: 'claude-transcript/system.turn_duration', completionEventId: 'duration-1' }; },
};
const transport = () => ({ request: async (method, params) => method === 'thread/read' ? { thread: { id: params.threadId, status: { type: 'idle' } } } : {}, notify: async () => {}, close: () => {} });

test('collects separate bounded Codex and Claude facts through the supplied adapters once', async () => {
  adapterCalls.length = 0;
  const facts = await collectHarnessFacts({ codexTargets: [codexTarget], claudeTargets: [claudeTarget], createTransport: transport, claudeAgents: () => [{ sessionId: claudeTarget.sessionId, status: 'idle' }], readText: () => JSON.stringify({ type: 'system' }) + '\n', adapters, now });
  assert.deepEqual(facts, [
    { targetIdentifier: 'core-e43002', harness: 'codex', openWork: true, state: 'idle', idleMinutes: 91, sourceEvent: { kind: 'codex-app-server/thread/turns/list', identifier: 'turn-1' }, unknownReason: null },
    { targetIdentifier: 'primary-840e42', harness: 'claude', openWork: true, state: 'idle', idleMinutes: 92, sourceEvent: { kind: 'claude-transcript/system.turn_duration', identifier: 'duration-1' }, unknownReason: null },
  ]);
  assert.deepEqual(adapterCalls, [['codex', 'thread-core', 'idle'], ['claude', claudeTarget.sessionId, 'idle']]);
});

test('rejects mismatched Codex metadata and ambiguous exact-session Claude roster entries', async () => {
  const facts = await collectHarnessFacts({ codexTargets: [codexTarget], claudeTargets: [claudeTarget], createTransport: () => ({ request: async method => method === 'thread/read' ? { thread: { id: 'other', status: { type: 'idle' } } } : {}, notify: async () => {}, close: () => {} }), claudeAgents: () => [{ sessionId: claudeTarget.sessionId }, { sessionId: claudeTarget.sessionId }], adapters, now });
  assert.equal(facts[0].unknownReason, 'thread-identity-mismatch');
  assert.equal(facts[1].unknownReason, 'roster-session-ambiguous');
});

test('timeout preserves unknown rather than fabricating idleness', async () => {
  const facts = await collectHarnessFacts({ codexTargets: [codexTarget], claudeTargets: [], createTransport: () => ({ request: () => new Promise(() => {}), notify: () => Promise.resolve(), close: () => {} }), adapters, now, timeoutMs: 5 });
  assert.deepEqual(facts[0], { targetIdentifier: 'core-e43002', harness: 'codex', openWork: true, state: 'unknown', idleMinutes: null, sourceEvent: null, unknownReason: 'timeout' });
});
