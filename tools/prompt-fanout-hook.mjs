#!/usr/bin/env node
import fs from 'node:fs';
import { createUnixWebSocketTransport } from './codex-app-server-client.mjs';

const text = value => typeof value === 'string'
  ? value
  : Array.isArray(value) && value.every(part => part?.type === 'text' && typeof part.text === 'string')
    ? value.map(part => part.text).join('')
    : null;

const receipt = value => {
  const destination = process.env.FLOW_FANOUT_RECEIPT;
  if (destination) fs.writeFileSync(destination, `${JSON.stringify(value)}\n`, { mode: 0o600 });
};

const fail = error => {
  receipt({ kind: 'fanout-hook', status: 'refused', error });
  process.exitCode = 2;
};

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', async () => {
  try {
    const event = JSON.parse(input);
    const session = process.env.FLOW_FANOUT_SESSION || (process.env.FLOW_FANOUT_SESSION_RECORD && JSON.parse(fs.readFileSync(process.env.FLOW_FANOUT_SESSION_RECORD, 'utf8')).session_id);
    const thread = process.env.FLOW_FANOUT_CODEX_THREAD;
    if (!session || !thread) throw new Error('test session and Codex thread must be explicit');
    if (event.hook_event_name !== 'Stop' || event.session_id !== session) throw new Error('event is outside the named flow');
    if (!event.transcript_path || !fs.existsSync(event.transcript_path)) throw new Error('Stop event has no readable transcript');
    const assistants = fs.readFileSync(event.transcript_path, 'utf8').split('\n').filter(Boolean)
      .flatMap(line => { try { return [JSON.parse(line)]; } catch { return []; } })
      .filter(record => record.type === 'assistant' && record.message?.role === 'assistant')
      .map(record => ({ id: record.uuid, body: text(record.message.content) }))
      .filter(record => record.id && record.body !== null);
    const marker = `Send.{ Codex.${thread} }`;
    const source = assistants.filter(record => record.body.includes(marker)).at(-1);
    if (!source) throw new Error('transcript contains no addressed Send marker');
    const start = source.body.indexOf(marker);
    const body = source.body.slice(start + marker.length).replace(/^\r?\n/, '');
    if (!body) throw new Error('addressed Send section is empty');
    const transport = createUnixWebSocketTransport(process.env.FLOW_FANOUT_CODEX_SOCKET || `${process.env.HOME}/.codex/app-server-control/app-server-control.sock`);
    await transport.request('initialize', { clientInfo: { name: 'flow-fanout-hook', version: '1' } });
    await transport.notify('initialized', {});
    await transport.request('thread/resume', { threadId: thread, excludeTurns: true });
    const result = await transport.request('turn/start', { threadId: thread, input: [{ type: 'text', text: body }] });
    transport.close();
    receipt({ kind: 'fanout-hook', status: 'delivered', source_message_id: source.id, source_bytes: Buffer.byteLength(body), turn_id: result.turn?.id ?? result.result?.turn?.id ?? null });
  } catch (error) { fail(error.message); }
});
