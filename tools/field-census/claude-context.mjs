/* Passive, bounded Claude Code context observation. Never reads message content. */
import fs from 'node:fs';
import path from 'node:path';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const TAIL_BYTES = 524288;
const STATUS_BYTES = 65536;
const STATUS_MAX_AGE_MS = 300000;
const integer = x => Number.isSafeInteger(x) && x >= 0 ? x : null;
const percent = x => typeof x === 'number' && Number.isFinite(x) && x >= 0 ? x : null;
const iso = x => Number.isFinite(x) ? new Date(x).toISOString() : null;

function readBounded(file, maxBytes, tail = false) {
  const stat = fs.statSync(file);
  if (!stat.isFile()) throw new Error('source is not a regular file');
  if (!tail && stat.size > maxBytes) throw new Error('statusline snapshot exceeds byte limit');
  const bytes = Math.min(stat.size, maxBytes);
  const buffer = Buffer.alloc(bytes);
  const fd = fs.openSync(file, 'r');
  try { fs.readSync(fd, buffer, 0, bytes, tail ? stat.size - bytes : 0); }
  finally { fs.closeSync(fd); }
  return {text: buffer.toString('utf8'), stat, clipped: tail && stat.size > bytes};
}

function quotaWindow(value) {
  if (!value || typeof value !== 'object') return null;
  const usedPct = percent(value.used_percentage);
  const resetsAt = integer(value.resets_at);
  return usedPct === null && resetsAt === null ? null : {usedPct, remainingPct: usedPct === null ? null : 100 - usedPct, resetsAt: resetsAt === null ? null : iso(resetsAt * 1000)};
}

function tokenUsage(value) {
  if (!value || typeof value !== 'object') return null;
  const inputTokens = integer(value.input_tokens);
  const cacheCreationTokens = integer(value.cache_creation_input_tokens);
  const cacheReadTokens = integer(value.cache_read_input_tokens);
  const outputTokens = integer(value.output_tokens);
  const totalInputTokens = [inputTokens, cacheCreationTokens, cacheReadTokens].every(x => x !== null)
    ? inputTokens + cacheCreationTokens + cacheReadTokens : null;
  if ([inputTokens, cacheCreationTokens, cacheReadTokens, outputTokens].every(x => x === null)) return null;
  return {inputTokens, cacheCreationTokens, cacheReadTokens, outputTokens, totalInputTokens};
}

function transcriptObservation(file, nativeThreadId, now, maxTailBytes) {
  if (path.basename(file) !== `${nativeThreadId}.jsonl`) throw new Error('transcript identity does not match native thread');
  const bounded = readBounded(file, maxTailBytes, true);
  let lines = bounded.text.split('\n');
  if (bounded.clipped) lines = lines.slice(1);
  if (lines.at(-1) === '') lines.pop();
  let partial = false;
  let last = null, superseded = false, eventAt = null, model = null, mismatches = 0;
  for (const line of lines) {
    let record;
    try { record = JSON.parse(line); } catch { partial = true; continue; }
    if (!record.sessionId) continue;
    if (record.sessionId !== nativeThreadId) { mismatches++; continue; }
    if (record.type === 'assistant') {
      const next = tokenUsage(record.message?.usage);
      if (next) {
        last = next; eventAt = typeof record.timestamp === 'string' ? record.timestamp : null;
        model = typeof record.message?.model === 'string' ? record.message.model : null;
        superseded = false;
      }
    } else if (record.type === 'user' || record.type === 'summary' || record.type === 'compact_boundary' ||
      (record.type === 'system' && /compact|clear/i.test(record.subtype || ''))) {
      superseded = true;
    }
  }
  const eventMs = eventAt === null ? NaN : Date.parse(eventAt);
  return {last, eventAt, model, usedTokens: last && !superseded && !partial ? last.totalInputTokens : null,
    state: partial ? 'partial' : superseded ? 'superseded' : last ? 'response-observed' : 'unknown',
    ageMs: Number.isFinite(eventMs) ? Math.max(0, now - eventMs) : null,
    clipped: bounded.clipped, mismatches, fileMtime: iso(bounded.stat.mtimeMs)};
}

function statusObservation(file, nativeThreadId, now, maxStatusBytes) {
  const bounded = readBounded(file, maxStatusBytes);
  const value = JSON.parse(bounded.text);
  if (value.session_id !== nativeThreadId) throw new Error('statusline identity does not match native thread');
  const ageMs = Math.max(0, now - bounded.stat.mtimeMs);
  if (ageMs > STATUS_MAX_AGE_MS) throw new Error('statusline snapshot is stale');
  const context = value.context_window || {};
  const usedTokens = context.current_usage == null && context.used_percentage == null
    ? null : integer(context.total_input_tokens);
  const windowTokens = integer(context.context_window_size);
  const usedPct = percent(context.used_percentage);
  const remainingPct = percent(context.remaining_percentage);
  const quota = value.rate_limits && {
    fiveHour: quotaWindow(value.rate_limits.five_hour),
    sevenDay: quotaWindow(value.rate_limits.seven_day),
    spendLimit: quotaWindow(value.rate_limits.spend_limit),
  };
  return {usedTokens, windowTokens, usedPct, remainingPct,
    last: tokenUsage(context.current_usage),
    quota: quota && Object.values(quota).some(Boolean) ? quota : null,
    model: typeof value.model?.id === 'string' ? value.model.id : null,
    ageMs, eventAt: iso(bounded.stat.mtimeMs)};
}

export async function collectClaudeContext({nativeThreadId, transcriptPath = null, statuslinePath = null,
  now = Date.now(), maxTailBytes = TAIL_BYTES, maxStatusBytes = STATUS_BYTES} = {}) {
  const observedAt = iso(now);
  const result = {source: 'claude', method: 'unavailable', observedAt, eventAt: null, nativeThreadId: nativeThreadId ?? null,
    model: null,
    occupancy: {status: 'unknown', usedTokens: null, windowTokens: null, usedPct: null, remainingPct: null},
    usage: {scope: 'last-request', inputTokens: null, cacheCreationTokens: null, cacheReadTokens: null, outputTokens: null, totalInputTokens: null},
    quota: null, freshness: {state: 'unknown', ageMs: null}, errors: []};
  if (!UUID.test(nativeThreadId || '')) { result.errors.push('invalid native thread identity'); return result; }
  if (statuslinePath) {
    try {
      const x = statusObservation(statuslinePath, nativeThreadId, now, maxStatusBytes);
      result.source = 'claude-statusline'; result.method = 'exact-session-statusline-snapshot';
      result.eventAt = x.eventAt; result.model = x.model;
      result.occupancy = {status: x.usedPct !== null ? 'exact' : x.usedTokens !== null ? 'observed' : 'unknown',
        usedTokens: x.usedTokens, windowTokens: x.windowTokens, usedPct: x.usedPct, remainingPct: x.remainingPct};
      result.usage = {scope: 'last-request', ...(x.last || result.usage)};
      result.quota = x.quota;
      result.freshness = {state: 'current-snapshot', ageMs: x.ageMs};
      return result;
    } catch (error) { result.errors.push(String(error.message || error)); }
  }
  if (transcriptPath) {
    try {
      const x = transcriptObservation(transcriptPath, nativeThreadId, now, maxTailBytes);
      result.source = 'claude-transcript'; result.method = 'bounded-exact-session-jsonl-tail';
      result.eventAt = x.eventAt; result.model = x.model;
      result.occupancy = {...result.occupancy, status: x.usedTokens === null ? 'unknown' : 'proxy', usedTokens: x.usedTokens};
      result.usage = {scope: 'last-request', ...(x.last || result.usage)};
      result.freshness = {state: x.state, ageMs: x.ageMs, fileMtime: x.fileMtime, clipped: x.clipped};
      if (x.mismatches) result.errors.push(`${x.mismatches} transcript records had a different session identity`);
    } catch (error) { result.errors.push(String(error.message || error)); }
  }
  return result;
}
