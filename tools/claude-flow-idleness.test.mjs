import assert from 'node:assert/strict';
import test from 'node:test';
import { deriveClaudeFlowIdleness } from './claude-flow-idleness.mjs';

const sessionId = '840e42bb-b2cd-42eb-a9ec-7659a5b13ded';
const completedAt = '2026-09-16T00:00:00.000Z';
const observedAtMs = Date.parse('2026-09-16T01:31:00.000Z');
const end = { type: 'assistant', uuid: 'assistant-end', sessionId, message: { role: 'assistant', stop_reason: 'end_turn' } };
const duration = { type: 'system', subtype: 'turn_duration', uuid: 'duration-1', parentUuid: 'assistant-end', sessionId, timestamp: completedAt, durationMs: 1000 };
const idleRoster = { id: '840e42bb', sessionId, status: 'idle' };
const observe = ({ records = [end, duration], rosterEntry = idleRoster } = {}) => deriveClaudeFlowIdleness({ sessionId, records, rosterEntry, observedAtMs });

test('uses a same-session turn_duration record linked to end_turn', () => {
  const result = observe();
  assert.equal(result.eligible, true); assert.equal(result.idleMinutes, 91); assert.equal(result.completionEventId, 'duration-1');
});

test('active roster state wins over a completed transcript event', () => {
  const result = observe({ rosterEntry: { ...idleRoster, status: 'active' } });
  assert.equal(result.eligible, false); assert.equal(result.state, 'busy'); assert.equal(result.reason, 'roster-not-idle');
});

test('a genuine pending approval wins even if roster status says idle', () => {
  const result = observe({ rosterEntry: { ...idleRoster, waitingFor: 'permission prompt' } });
  assert.equal(result.eligible, false); assert.equal(result.state, 'approval-wait'); assert.equal(result.reason, 'approval-pending');
});

test('later user input and pending background work invalidate a terminal timestamp', () => {
  let result = observe({ records: [end, duration, { type: 'user', sessionId, message: { role: 'user' } }] });
  assert.equal(result.eligible, false); assert.equal(result.reason, 'later-user-input');
  result = observe({ records: [end, { ...duration, pendingBackgroundAgentCount: 1 }] });
  assert.equal(result.eligible, false); assert.equal(result.reason, 'background-work-pending');
});

test('rejects foreign and unlinked completion lookalikes', () => {
  const result = observe({ records: [{ ...duration, sessionId: 'other' }, { ...duration, parentUuid: 'missing' }] });
  assert.equal(result.eligible, false); assert.equal(result.reason, 'no-linked-completed-turn');
});
