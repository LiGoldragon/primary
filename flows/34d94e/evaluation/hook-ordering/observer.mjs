#!/usr/bin/env node
import fs from 'node:fs';
const phrase = process.env.HOOK_PROBE_PHRASE || 'HOOK_ORDERING_SYNTHETIC_REPLAY_34D94E';
const output = process.env.HOOK_WITNESS_OUTPUT;
const textOf = value => typeof value === 'string' ? value : Array.isArray(value) ? value.map(item => item?.text ?? '').join('') : '';
let input = '', event = {};
process.stdin.setEncoding('utf8');
process.stdin.on('data', c => input += c);
process.stdin.on('end', () => {
  try { event = JSON.parse(input); } catch { event = {}; }
  const transcript = event.transcript_path;
  const records = [];
  if (transcript && fs.existsSync(transcript)) {
    for (const line of fs.readFileSync(transcript, 'utf8').split('\n')) {
      try { const record = JSON.parse(line); const recordText = textOf(record.message?.content ?? record.content ?? record.prompt); if (record.type === 'user' && recordText === event.prompt) records.push({uuid: record.uuid ?? record.message?.id ?? null, promptId: record.promptId ?? record.prompt_id ?? null, rawTextComparison: recordText === event.prompt, metadata: Object.keys(record).sort()}); } catch {}
    }
  }
  const witness = {schema: 'hook-ordering-witness/v1', hookEvent: event.hook_event_name ?? null, inputKeys: Object.keys(event).sort(), promptId: event.prompt_id ?? null, sessionId: event.session_id ?? null, promptExact: event.prompt === phrase, transcriptFileExists: Boolean(transcript && fs.existsSync(transcript)), matchingUserRecordsAtHookTime: records, syntheticProbePhrase: phrase, observedAtHookTime: true};
  if (process.env.HOOK_REPLAY_LOG) { fs.appendFileSync(process.env.HOOK_REPLAY_LOG, JSON.stringify(witness) + '\n', {mode: 0o600}); } else if (output) { fs.writeFileSync(output, JSON.stringify(witness, null, 2) + '\n', {mode: 0o600}); fs.chmodSync(output, 0o600); }
  process.exitCode = 2;
});
