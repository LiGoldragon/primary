/**
 * Codex app-server lifecycle adapter.  It owns no roster or state: the caller
 * supplies the independently observed operational state and this module reads
 * exactly one latest turn from the named Codex Flow/thread.
 */
const MINUTE_MS = 60_000;

const unixSecondsToMs = value => Number.isInteger(value) && value >= 0 ? value * 1_000 : null;

export const deriveIdleObservation = ({ threadId, observedAtMs, operationalState, turn }) => {
  if (typeof threadId !== 'string' || threadId.length === 0) throw new Error('threadId is required');
  if (!Number.isSafeInteger(observedAtMs) || observedAtMs < 0) throw new Error('observedAtMs is required');
  const base = { threadId, observedAtMs, source: 'codex-app-server/thread/turns/list', idleSinceMs: null, idleMinutes: null, eligible: false };
  // An external state wins. Completion timestamps do not erase approval-wait,
  // and a concurrent/busy or unknown state cannot establish idle time.
  if (operationalState !== 'idle') return { ...base, state: operationalState ?? 'unknown', reason: 'operational-state-not-idle' };
  if (!turn || turn.status !== 'completed') return { ...base, state: 'busy', reason: 'latest-turn-not-completed' };
  const completedAtMs = unixSecondsToMs(turn.completedAt);
  if (completedAtMs === null || completedAtMs > observedAtMs) return { ...base, state: 'unknown', reason: 'completion-time-unavailable-or-future' };
  return { ...base, state: 'idle', idleSinceMs: completedAtMs, idleMinutes: Math.floor((observedAtMs - completedAtMs) / MINUTE_MS), eligible: true, turnId: turn.id };
};

export const readFlowIdleness = async ({ transport, threadId, operationalState, now = () => Date.now() }) => {
  if (!transport || typeof transport.request !== 'function') throw new Error('app-server request transport is required');
  const response = await transport.request('thread/turns/list', { threadId, limit: 1, sortDirection: 'desc', itemsView: 'notLoaded' });
  return deriveIdleObservation({ threadId, observedAtMs: now(), operationalState, turn: response?.data?.[0] ?? null });
};
