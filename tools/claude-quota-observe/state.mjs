/* The append-only ndjson record of every observation.
   $XDG_STATE_HOME/claude-quota-observe/log.ndjson, else
   ~/.local/state/claude-quota-observe/log.ndjson. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

export function logPath(env = process.env) {
  const base = env.XDG_STATE_HOME && env.XDG_STATE_HOME.length > 0 ? env.XDG_STATE_HOME : path.join(os.homedir(), '.local', 'state');
  return path.join(base, 'claude-quota-observe', 'log.ndjson');
}

export function append(record, env = process.env) {
  const file = logPath(env);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, `${JSON.stringify({ at: new Date().toISOString(), ...record })}\n`, { flag: 'a' });
}
