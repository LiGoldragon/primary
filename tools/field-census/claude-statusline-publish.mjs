#!/usr/bin/env node
/* Optional Claude Code statusLine command: save metadata, then render the existing status line. */
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

const [directory, displayScript] = process.argv.slice(2);
const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
if (!directory || !displayScript) process.exit(2);
let input = '';
for await (const chunk of process.stdin) {
  input += chunk;
  if (Buffer.byteLength(input) > 65536) process.exit(2);
}
try {
  const value = JSON.parse(input);
  if (!uuid.test(value.session_id || '')) throw new Error('invalid session ID');
  const metadata = {
    session_id: value.session_id,
    model: {id: value.model?.id ?? null},
    context_window: value.context_window ?? null,
    rate_limits: value.rate_limits ?? null,
  };
  fs.mkdirSync(directory, {recursive: true, mode: 0o700});
  const target = path.join(directory, `${value.session_id}.json`);
  const temporary = `${target}.${process.pid}.tmp`;
  fs.writeFileSync(temporary, JSON.stringify(metadata), {mode: 0o600});
  fs.renameSync(temporary, target);
} catch {
  // A malformed status update must not hide the display line.
}
const child = spawnSync(displayScript, [], {input, encoding: 'utf8', timeout: 2000, maxBuffer: 65536});
if (child.stdout) process.stdout.write(child.stdout);
