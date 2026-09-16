/**
 * Claude Flow lifecycle adapter. It reads a native transcript as a record
 * stream and accepts only the CLI's terminal `system/turn_duration` record
 * directly parented by a same-session assistant `end_turn` record. The caller
 * supplies one fresh `claude agents --json` entry; this module owns no roster.
 */
const MINUTE_MS = 60_000;
const timestampMs = value => typeof value === 'string' && Number.isSafeInteger(Date.parse(value)) ? Date.parse(value) : null;
const isUserInput = record => record?.type === 'user' && record?.message?.role === 'user';

export const deriveClaudeFlowIdleness = ({ sessionId, records, rosterEntry, observedAtMs }) => {
  if (typeof sessionId !== 'string' || sessionId.length === 0) throw new Error('sessionId is required');
  if (!Array.isArray(records)) throw new Error('records must be an array');
  if (!Number.isSafeInteger(observedAtMs) || observedAtMs < 0) throw new Error('observedAtMs is required');
  const base = { sessionId, observedAtMs, source: 'claude-transcript/system.turn_duration', idleSinceMs: null, idleMinutes: null, eligible: false };
  // A full, fresh session match prevents a prefix collision. WaitingFor wins
  // even if a stale roster status says idle: a genuine approval dialog owns the
  // terminal and is never safely wakeable.
  if (!rosterEntry || rosterEntry.sessionId !== sessionId) return { ...base, state: 'unknown', reason: 'roster-session-not-exact' };
  if (rosterEntry.waitingFor) return { ...base, state: 'approval-wait', reason: 'approval-pending' };
  if (rosterEntry.status !== 'idle') return { ...base, state: rosterEntry.status === 'active' ? 'busy' : 'unknown', reason: 'roster-not-idle' };

  const indexed = records.map((record, index) => ({ record, index }));
  const completions = indexed.filter(({ record, index }) => {
    if (record?.type !== 'system' || record?.subtype !== 'turn_duration' || record?.sessionId !== sessionId) return false;
    if (!Number.isInteger(record.durationMs) || record.durationMs < 0 || timestampMs(record.timestamp) === null) return false;
    const parent = indexed.find(({ record: candidate }) => candidate?.uuid === record.parentUuid)?.record;
    return parent?.type === 'assistant' && parent?.sessionId === sessionId && parent?.message?.role === 'assistant' && parent?.message?.stop_reason === 'end_turn';
  });
  const completion = completions.at(-1);
  if (!completion) return { ...base, state: 'unknown', reason: 'no-linked-completed-turn' };
  if (completion.record.pendingBackgroundAgentCount > 0) return { ...base, state: 'busy', reason: 'background-work-pending' };
  if (indexed.slice(completion.index + 1).some(({ record }) => isUserInput(record) && record.sessionId === sessionId)) return { ...base, state: 'busy', reason: 'later-user-input' };
  const idleSinceMs = timestampMs(completion.record.timestamp);
  if (idleSinceMs > observedAtMs) return { ...base, state: 'unknown', reason: 'completion-time-future' };
  return { ...base, state: 'idle', idleSinceMs, idleMinutes: Math.floor((observedAtMs - idleSinceMs) / MINUTE_MS), eligible: true, completionEventId: completion.record.uuid };
};
