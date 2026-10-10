#!/usr/bin/env node
import fs from 'node:fs';
const output = process.env.HOOK_REPLAY_LOG;
const phrase = process.env.HOOK_PROBE_PHRASE;
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', () => {
  let event = {}; try { event = JSON.parse(input); } catch {}
  const record = { schema: 'hook-replay-observer/v1', hook_event_name: event.hook_event_name ?? null,
    session_id: event.session_id ?? null, prompt_id: event.prompt_id ?? null,
    exact_replay_phrase: event.prompt === phrase, input_keys: Object.keys(event).sort() };
  if (output) fs.appendFileSync(output, JSON.stringify(record) + '\n', { mode: 0o600 });
  process.exitCode = 2;
});
