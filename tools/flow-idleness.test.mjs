import assert from 'node:assert/strict';
import test from 'node:test';
import { deriveIdleObservation, readFlowIdleness } from './flow-idleness.mjs';

const observedAtMs = 1_800_000;
const completed = { id: 'turn-1', status: 'completed', completedAt: 1_680 };

test('derives duration only from a completed app-server turn while collector says idle', () => {
  const actual = deriveIdleObservation({ threadId: 'flow-thread', observedAtMs, operationalState: 'idle', turn: completed });
  assert.deepEqual(actual, { threadId: 'flow-thread', observedAtMs, source: 'codex-app-server/thread/turns/list', idleSinceMs: 1_680_000, idleMinutes: 2, eligible: true, state: 'idle', turnId: 'turn-1' });
});

test('approval wait stays ineligible even if the last turn completed long ago', () => {
  const actual = deriveIdleObservation({ threadId: 'flow-thread', observedAtMs, operationalState: 'approval-wait', turn: completed });
  assert.equal(actual.eligible, false); assert.equal(actual.idleMinutes, null); assert.equal(actual.reason, 'operational-state-not-idle');
});

test('busy and unknown states never infer a duration', () => {
  for (const operationalState of ['busy', 'unknown', null]) {
    const actual = deriveIdleObservation({ threadId: 'flow-thread', observedAtMs, operationalState, turn: completed });
    assert.equal(actual.eligible, false); assert.equal(actual.idleSinceMs, null);
  }
});

test('uses the supported latest-turn metadata call with no item hydration', async () => {
  const calls = []; const transport = { request: async (method, params) => { calls.push({ method, params }); return { data: [completed] }; } };
  const actual = await readFlowIdleness({ transport, threadId: 'flow-thread', operationalState: 'idle', now: () => observedAtMs });
  assert.equal(actual.idleMinutes, 2);
  assert.deepEqual(calls, [{ method: 'thread/turns/list', params: { threadId: 'flow-thread', limit: 1, sortDirection: 'desc', itemsView: 'notLoaded' } }]);
});
