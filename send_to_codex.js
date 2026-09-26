#!/usr/bin/env node
import fs from 'node:fs';
import net from 'node:net';
import crypto from 'node:crypto';

const socketPath = '/home/li/.codex/app-server-control/app-server-control.sock';
const threadId = '01a0a715-2d5d-7342-b278-1dbcf78795bd';
const sha256Hash = 'b747be9d249d19445e523815e9567e79a8941831ffc414e872be52a957865b1f';

// The extracted text
const extractedText = `You should set up a layer, a core layer: a codex, or a pair, but it's codex-heavy in that the codex runs these checkup Luna jobs to see if things are going okay. It checks if the system hasn't paralyzed into some kind of weird self-update failure thing or some catastrophic network sandboxing problem or whatever. It can fix it and bring the system back online.

If nobody's doing anything, it can maybe message primary and say, "Hey, did you fall asleep? Do you want to get back to work? Maybe on this and this, crucial things: why did you fall asleep? Is the quota low? Did I not see that?" You start talking to yourself about whether I should be working and on what, or should I message the Living, right? Then wait for my answer. If I'm not answering, then ask yourself what the Living would probably want us to do, or should we save our thing and wake back up in a bit?

That would be the core layer's job, and for now, let's use Codex mostly for the wake-up. `;

// Construct the full message
const peerMessage = `[PEER primary-claude 840e42] Item 49, build now, from the words above: the core layer, Codex-heavy, as a stopgap until Persona keeps it. (1) A core Codex main: a thread launched per the living's layers vision (flows/05c604/vision/layers.md: core is core programming and the soul; Spirit and Intent whole in its prompt, Vision considered, not authoritative), registered in flows/index.md as core with its own lane. (2) A checkup job: a systemd user timer on ouranos, every 30 minutes, running a bounded non-interactive codex job with a read-only checklist: hosts answer over Yggdrasil (ouranos, prometheus, zeus); our units healthy (orchestrate-nexus, lojix, message, codex-remote-control, cc-daemon); the primary and secondary Claude sessions and the Codex main alive, with idle times; quota of both providers. Repairs allowed: restart one of our own failed units, once, reported; everything else reported only. (3) The wake-up: when the primary has been idle beyond a threshold you propose (default 90 minutes) with open items, the job sends it a wake message by the route that works (cross-session message to "primary-claude-pending [eafe83]", or prompt-relay when idle) carrying the checkup summary and the questions "why idle; is quota low; which crucial items", and the primary answers itself or the living per the words. (4) Its thin event log per item 45. Report the anatomy and the witness of one timer run whole to flows/cf7879/reports/to-840e42.md with a pointer by cross-session message. Order: 50, 31 (with 45), 49, 47 (with 48), 35, 34, 40, 37, 46, 42, 43, 32, 36, 44, 38, 41, 39.`;

const messageBody = `[RELAY through primary Claude 840e42; the living's words, verbatim; session 840e42bb; sha256 ${sha256Hash}]
${extractedText}

${peerMessage}`;

function websocketFrame(payload, opcode = 0x1) {
  const body = Buffer.isBuffer(payload) ? payload : Buffer.from(payload);
  const mask = crypto.randomBytes(4);
  let header;
  if (body.length < 126) header = Buffer.from([0x80 | opcode, 0x80 | body.length]);
  else if (body.length < 65536) header = Buffer.from([0x80 | opcode, 0xfe, body.length >> 8, body.length & 255]);
  else {
    header = Buffer.alloc(10);
    header[0] = 0x80 | opcode;
    header[1] = 0xff;
    header.writeBigUInt64BE(BigInt(body.length), 2);
  }
  const out = Buffer.alloc(body.length);
  for (let i = 0; i < body.length; i++) out[i] = body[i] ^ mask[i % 4];
  return Buffer.concat([header, mask, out]);
}

const socket = net.createConnection(socketPath);
let buffer = Buffer.alloc(0), upgraded = false, sequence = 0;
const pending = new Map();

const fail = error => { socket.destroy(); console.error('ERROR:', error.message); process.exit(1); };
const call = (method, params) => new Promise((ok, no) => {
  const id = ++sequence;
  const timer = setTimeout(() => { pending.delete(id); no(new Error(`Codex RPC timeout: ${method}`)); }, 10_000);
  pending.set(id, { ok, no, timer });
  socket.write(websocketFrame(JSON.stringify({ jsonrpc: '2.0', id, method, params })));
});

const frame = (fin, opcode, body) => {
  if (opcode === 0x9) { socket.write(websocketFrame(body, 0xa)); return; }
  if (opcode === 0x8) return fail(new Error('Codex websocket closed'));
  if (opcode === 0x1) fragment = body;
  else if (opcode === 0x0 && fragment) fragment = Buffer.concat([fragment, body]);
  else return;
  if (!fin) return;
  const message = JSON.parse(fragment.toString());
  fragment = null;
  const waiter = pending.get(message.id);
  if (waiter) {
    pending.delete(message.id);
    clearTimeout(waiter.timer);
    message.error ? waiter.no(new Error(JSON.stringify(message.error))) : waiter.ok(message.result ?? message);
  }
};

let fragment = null;
const parse = () => {
  while (buffer.length >= 2) {
    const fin = Boolean(buffer[0] & 128), opcode = buffer[0] & 15;
    let length = buffer[1] & 127, offset = 2;
    if (length === 126) {
      if (buffer.length < 4) return;
      length = buffer.readUInt16BE(2);
      offset = 4;
    } else if (length === 127) {
      if (buffer.length < 10) return;
      const big = buffer.readBigUInt64BE(2);
      if (big > BigInt(Number.MAX_SAFE_INTEGER)) return fail(new Error('Codex frame too large'));
      length = Number(big);
      offset = 10;
    }
    if (buffer.length < offset + length) return;
    const body = buffer.subarray(offset, offset + length);
    buffer = buffer.subarray(offset + length);
    frame(fin, opcode, body);
  }
};

const start = async () => {
  try {
    await call('initialize', { clientInfo: { name: 'fable-840e42', version: '1' } });
    socket.write(websocketFrame(JSON.stringify({ jsonrpc: '2.0', method: 'initialized', params: {} })));
    await call('thread/resume', { threadId, excludeTurns: true });
    const result = await call('turn/start', { threadId, input: [{ type: 'text', text: messageBody }] });
    const turn = result.turn ?? result.result?.turn ?? {};
    console.log(JSON.stringify({ sha256: sha256Hash, turn_id: turn.id ?? null, status: turn.status ?? null }));
    socket.end();
  } catch (error) {
    fail(error);
  }
};

socket.setTimeout(10_000, () => fail(new Error('Codex socket timeout')));
socket.on('error', fail);
socket.on('connect', () => socket.write('GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n'));
socket.on('data', data => {
  buffer = Buffer.concat([buffer, data]);
  if (!upgraded) {
    const end = buffer.indexOf('\r\n\r\n');
    if (end < 0) return;
    const header = buffer.subarray(0, end).toString();
    const accept = header.match(/sec-websocket-accept:\s*([^\r\n]+)/i)?.[1]?.trim();
    const expected = crypto.createHash('sha1').update('dGhlIHNhbXBsZSBub25jZQ==258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest('base64');
    if (!header.startsWith('HTTP/1.1 101') || !/upgrade:\s*websocket/i.test(header) || accept !== expected) return fail(new Error('Codex websocket upgrade refused'));
    buffer = buffer.subarray(end + 4);
    upgraded = true;
    void start();
  }
  parse();
});
