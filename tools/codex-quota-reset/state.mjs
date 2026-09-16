/* The append-only ndjson record of every observation and decision.
   $XDG_STATE_HOME/codex-quota-reset/log.ndjson, else ~/.local/state/codex-quota-reset/log.ndjson. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';

export function logPath(env = process.env) {
  const base = env.XDG_STATE_HOME && env.XDG_STATE_HOME.length > 0 ? env.XDG_STATE_HOME : path.join(os.homedir(), '.local', 'state');
  return path.join(base, 'codex-quota-reset', 'log.ndjson');
}

export function append(record, env = process.env) {
  const file = logPath(env);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, `${JSON.stringify({ at: new Date().toISOString(), ...record })}\n`, { flag: 'a' });
}

export function records(env = process.env) {
  const file = logPath(env);
  if (!fs.existsSync(file)) return [];
  return fs
    .readFileSync(file, 'utf8')
    .split('\n')
    .filter(Boolean)
    .map(line => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    })
    .filter(Boolean);
}

/* One logical reset attempt per rate-limit window: the key is the window's own reset instant.
   A rerun against the same window therefore reuses the key, so a resend is one attempt, not two. */
export function idempotencyKey(resetsAt) {
  const digest = crypto.createHash('sha256').update(`codex-quota-reset/window/${resetsAt}`, 'utf8').digest();
  const bytes = Buffer.from(digest.subarray(0, 16));
  bytes[6] = (bytes[6] & 0x0f) | 0x50;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  const hex = bytes.toString('hex');
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}

/* What the log already says about this window's one logical attempt.
   `consumed` is the only state that stops a call: a bare `ResetAttempted` means a consume was
   sent and no outcome was ever recorded, which the same idempotency key is built to resend. */
export function windowAttempt(key, env = process.env) {
  let attempted = null;
  for (const record of records(env)) {
    if (record.idempotencyKey !== key) continue;
    if (record.kind === 'ResetConsumed') return { status: 'consumed', creditId: record.creditId ?? null };
    if (record.kind === 'ResetAttempted') attempted = record;
  }
  return attempted === null ? { status: 'fresh', creditId: null } : { status: 'attempted', creditId: attempted.creditId ?? null };
}
