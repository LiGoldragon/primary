#!/usr/bin/env node
import fs from 'node:fs';
const phrase = 'HOOK_ORDERING_SYNTHETIC_PROBE_34D94E';
const output = process.env.HOOK_WITNESS_OUTPUT;
let input = '', event = {};
process.stdin.setEncoding('utf8');
process.stdin.on('data', c => input += c);
process.stdin.on('end', () => {
  try { event = JSON.parse(input); } catch { event = {}; }
  const transcript = event.transcript_path;
  const records = [];
  if (transcript && fs.existsSync(transcript)) {
    for (const line of fs.readFileSync(transcript, 'utf8').split('\n')) {
      try { const record = JSON.parse(line); if (record.type === 'user' && JSON.stringify(record).includes(phrase)) records.push({uuid: record.uuid ?? record.message?.id ?? null, promptId: record.promptId ?? record.prompt_id ?? null, rawTextComparison: JSON.stringify(record).includes(phrase), metadata: Object.keys(record).sort()}); } catch {}
    }
  }
  const witness = {schema: 'hook-ordering-witness/v1', hookEvent: event.hook_event_name ?? null, inputKeys: Object.keys(event).sort(), transcriptPathPresent: Boolean(transcript), matchingUserRecordsAtHookTime: records, syntheticProbePhrase: phrase, observedAtHookTime: true, modelCall: false};
  if (output) { fs.writeFileSync(output, JSON.stringify(witness, null, 2) + '\n', {mode: 0o600}); fs.chmodSync(output, 0o600); }
  process.exitCode = 2;
});
