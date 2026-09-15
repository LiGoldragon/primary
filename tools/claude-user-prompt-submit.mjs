#!/usr/bin/env node
/*
 * Scoped Claude UserPromptSubmit hook.
 *
 * Configuration supplies CLUSTERRELAY_FLOW_LANE for the one flow which owns
 * this hook. The handler records an unclassified source event and never
 * records the prompt body. A relay/provenance-shaped prompt is ignored to
 * avoid feeding an injected peer turn back into the relay.
 */
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const lane = process.env.CLUSTERRELAY_FLOW_LANE;
const fail = message => {
  process.stdout.write(JSON.stringify({ kind: 'refused', error: message }) + '\n');
  process.exitCode = 2;
};
const sha256 = text => crypto.createHash('sha256').update(text, 'utf8').digest('hex');
const words = text => text.trim() ? text.trim().split(/\s+/u) : [];

function isRelayed(text) {
  const trimmed = text.trimStart();
  if (trimmed.startsWith('[PEER ') || trimmed.startsWith('[RELAY ')) return true;
  const firstLine = trimmed.split(/\r?\n/, 1)[0];
  try {
    return Boolean(JSON.parse(firstLine)?.provenance);
  } catch {
    return false;
  }
}

let raw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { raw += chunk; });
process.stdin.on('end', () => {
  let event;
  try { event = JSON.parse(raw); } catch { return fail('hook input is not JSON'); }
  if (event?.hook_event_name !== 'UserPromptSubmit') return fail('unexpected hook event');
  if (typeof event.prompt !== 'string') return fail('hook input has no prompt');
  if (typeof event.session_id !== 'string' || !event.session_id) return fail('hook input has no session_id');
  if (typeof event.prompt_id !== 'string' || !event.prompt_id) return fail('hook input has no prompt_id');
  if (!lane || !path.isAbsolute(lane)) return fail('CLUSTERRELAY_FLOW_LANE must be an absolute flow lane');

  if (isRelayed(event.prompt)) {
    process.stdout.write(JSON.stringify({ kind: 'ignored-relayed-prompt', session_id: event.session_id, prompt_id: event.prompt_id }) + '\n');
    return;
  }

  const output = path.join(path.resolve(lane), 'claude-user-prompt-submit.jsonl');
  const tokens = words(event.prompt);
  const record = {
    schema: 'claude-user-prompt-submit/v1',
    observed_at: new Date().toISOString(),
    source_origin: 'unclassified-claude-user-prompt-submit',
    session_id: event.session_id,
    prompt_id: event.prompt_id,
    transcript_path: typeof event.transcript_path === 'string' ? event.transcript_path : null,
    sha256_utf8: sha256(event.prompt),
    first_six_words: tokens.slice(0, 6),
    last_six_words: tokens.slice(-6),
    word_count: tokens.length,
  };
  fs.mkdirSync(path.dirname(output), { recursive: true, mode: 0o700 });
  fs.appendFileSync(output, JSON.stringify(record) + '\n', { encoding: 'utf8', mode: 0o600 });
  process.stdout.write(JSON.stringify({ kind: 'recorded', session_id: record.session_id, prompt_id: record.prompt_id, sha256_utf8: record.sha256_utf8 }) + '\n');
});
