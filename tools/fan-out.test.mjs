import assert from 'node:assert/strict';
import { execFileSync, spawn } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';

const tool = path.join(import.meta.dirname, 'fan-out.mjs');
const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'fan-out-'));
const file = path.join(directory, 'fixture.jsonl');

const run = (...args) => execFileSync(process.execPath, [tool, ...args], { encoding: 'utf8' });
const runChild = (args, env = {}) =>
  new Promise(resolve => {
    const child = spawn(process.execPath, [tool, ...args], { env: { ...process.env, ...env } });
    let stdout = '';
    child.stdout.on('data', d => {
      stdout += d;
    });
    child.on('exit', code => resolve({ code, stdout }));
  });

const user = (id, text) => JSON.stringify({ type: 'user', uuid: id, message: { role: 'user', content: text } });
const codexMessage = (id, text) => JSON.stringify({ item: { id, type: 'message', role: 'user', content: text } });
const codexRollout = (id, text) =>
  JSON.stringify({ type: 'event_msg', payload: { type: 'item_completed', item: { id, type: 'UserMessage', content: [{ type: 'text', text }] } } });

// One source transcript carrying a Claude user message, a Codex message record,
// and a Codex rollout record -- fan-out must pick the one matching --message-id
// and deliver that same extracted text to every endpoint, unchanged.
fs.writeFileSync(
  file,
  [
    user('claude-one', 'Ship the migration notes to the team.'),
    codexMessage('codex-one', 'Different message, must not be picked.'),
    codexRollout('rollout-one', 'Rollout message, also must not be picked.'),
    JSON.stringify({ item: { type: 'message', role: 'assistant', id: 'assistant-one', content: 'not a user message' } }),
  ].join('\n')
);

// --- extraction: exact id match, wrong format ---
{
  let threw = false;
  try {
    run('deliver', '--source', file, '--message-id', 'no-such-id', '--endpoints', '[]');
  } catch (error) {
    threw = true;
    assert.match(error.stdout, /not found in source/);
  }
  assert.ok(threw, 'expected a missing message id to be refused');
}

// --- help / usage ---
{
  const out = run('--help');
  assert.match(out, /usage:/);
}

// --- unsupported endpoint type is reported, not thrown ---
{
  const out = JSON.parse(
    run('deliver', '--source', file, '--message-id', 'claude-one', '--endpoints', JSON.stringify([{ type: 'carrier-pigeon', id: 'p1' }]))
  );
  assert.equal(out.kind, 'fan-out-complete');
  assert.equal(out.message_id, 'claude-one');
  assert.equal(out.results.length, 1);
  assert.equal(out.results[0].status, 'unsupported');
}
// (no fake server involved above, so execFileSync is safe: nothing needs the event loop free)

// --- invalid --endpoints JSON is refused up front ---
{
  let result = await runChild(['deliver', '--source', file, '--message-id', 'claude-one', '--endpoints', 'not-json']);
  assert.equal(result.code, 2);
  assert.match(result.stdout, /must be valid JSON/);
}

// --- websocket frame plumbing shared with the fan-out-to-codex path ---
const frame = (payload, opcode = 1, fin = true) => {
  const body = Buffer.isBuffer(payload) ? payload : Buffer.from(payload);
  const first = (fin ? 0x80 : 0) | opcode;
  if (body.length < 126) return Buffer.concat([Buffer.from([first, body.length]), body]);
  if (body.length < 65536) return Buffer.concat([Buffer.from([first, 126, body.length >> 8, body.length & 255]), body]);
  const head = Buffer.alloc(10);
  head[0] = first;
  head[1] = 127;
  head.writeBigUInt64BE(BigInt(body.length), 2);
  return Buffer.concat([head, body]);
};
function readFrames(state, visit) {
  while (state.raw.length >= 2) {
    let n = state.raw[1] & 127,
      offset = 2;
    if (!(state.raw[1] & 128)) throw new Error('client frame was not masked');
    if (n === 126) {
      if (state.raw.length < 4) return;
      n = state.raw.readUInt16BE(2);
      offset = 4;
    } else if (n === 127) {
      if (state.raw.length < 10) return;
      n = Number(state.raw.readBigUInt64BE(2));
      offset = 10;
    }
    if (state.raw.length < offset + 4 + n) return;
    const mask = state.raw.subarray(offset, offset + 4),
      body = Buffer.alloc(n),
      opcode = state.raw[0] & 15;
    for (let i = 0; i < n; i++) body[i] = state.raw[offset + 4 + i] ^ mask[i % 4];
    state.raw = state.raw.subarray(offset + 4 + n);
    visit(opcode, body);
  }
}
const accept = 's3pPLMBiTxaQ9kYGzzhZRbK+xOo=';
const listen = async (name, behavior) => {
  const server = net.createServer(behavior);
  await new Promise(ok => server.listen(name, ok));
  return server;
};
const upgrade = (socket, value = accept) => socket.write(`HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: ${value}\r\n\r\n`);

function fakeCodexServer(socketPath, { onTurnStart } = {}) {
  const requests = [];
  return listen(socketPath, socket => {
    const state = { raw: Buffer.alloc(0), upgraded: false };
    socket.on('data', data => {
      state.raw = Buffer.concat([state.raw, data]);
      if (!state.upgraded) {
        const end = state.raw.indexOf('\r\n\r\n');
        if (end < 0) return;
        state.raw = state.raw.subarray(end + 4);
        state.upgraded = true;
        upgrade(socket);
      }
      readFrames(state, (opcode, body) => {
        if (opcode !== 1) return;
        const request = JSON.parse(body);
        if (!request.id) return;
        requests.push(request);
        if (request.method === 'turn/start' && onTurnStart) onTurnStart(request);
        const result = request.method === 'turn/start' ? { turn: { id: 'fake-turn', status: 'inProgress' } } : {};
        socket.write(frame(JSON.stringify({ jsonrpc: '2.0', id: request.id, result })));
      });
    });
  }).then(server => ({ server, requests }));
}

// --- deliver the SAME extracted text to two different endpoint kinds in one call ---
{
  const socketA = path.join(directory, 'codex-a.sock');
  const socketB = path.join(directory, 'codex-b.sock');
  const { server: serverA, requests: requestsA } = await fakeCodexServer(socketA);
  const { server: serverB, requests: requestsB } = await fakeCodexServer(socketB);

  const endpoints = [
    { type: 'codex-thread', id: 'thread-a', socket: socketA },
    { type: 'codex-thread', id: 'thread-b', socket: socketB },
  ];
  const result = await runChild(['deliver', '--source', file, '--message-id', 'claude-one', '--endpoints', JSON.stringify(endpoints)]);
  serverA.close();
  serverB.close();
  assert.equal(result.code, 0);
  const out = JSON.parse(result.stdout);

  assert.equal(out.kind, 'fan-out-complete');
  assert.equal(out.endpoints_count, 2);
  assert.deepEqual(
    out.results.map(r => r.status),
    ['delivered', 'delivered']
  );
  const turnStartA = requestsA.find(r => r.method === 'turn/start');
  const turnStartB = requestsB.find(r => r.method === 'turn/start');
  assert.equal(turnStartA.params.input[0].text, 'Ship the migration notes to the team.');
  assert.equal(turnStartB.params.input[0].text, 'Ship the migration notes to the team.');
  // Same extracted text delivered to both endpoints -- one extraction, no duplication.
  assert.equal(turnStartA.params.input[0].text, turnStartB.params.input[0].text);
}

// --- a codex endpoint that refuses the websocket upgrade is reported as failed, not thrown ---
{
  const badPath = path.join(directory, 'bad.sock');
  const bad = await listen(badPath, socket => socket.once('data', () => upgrade(socket, 'wrong')));
  const result = await runChild(['deliver', '--source', file, '--message-id', 'claude-one', '--endpoints', JSON.stringify([{ type: 'codex-thread', id: 'thread-bad', socket: badPath }])]);
  bad.close();
  assert.equal(result.code, 0);
  const out = JSON.parse(result.stdout);
  assert.equal(out.results[0].status, 'failed');
  assert.match(out.results[0].error, /websocket upgrade refused/);
}

// --- deliver to a Claude session over the fake control socket ---
{
  const agent = path.join(directory, 'fake-claude');
  fs.writeFileSync(agent, `#!${process.execPath}\nprocess.stdout.write(process.env.FAN_OUT_FAKE_AGENTS);\n`);
  fs.chmodSync(agent, 0o755);
  const control = path.join(directory, 'claude.sock');
  const key = path.join(directory, 'control.key');
  fs.writeFileSync(key, 'dummy-key\n');
  let attach, pasted;
  const claudeServer = await listen(control, socket => {
    let raw = Buffer.alloc(0);
    socket.on('data', data => {
      raw = Buffer.concat([raw, data]);
      if (!attach) {
        const end = raw.indexOf(10);
        if (end < 0) return;
        attach = JSON.parse(raw.subarray(0, end));
        raw = raw.subarray(end + 1);
        socket.write('{"ok":true}\n');
      }
      if (raw.length) pasted = raw;
    });
  });

  const env = {
    FAN_OUT_CLAUDE_AGENTS: agent,
    FAN_OUT_CLAUDE_CONTROL_SOCKET: control,
    FAN_OUT_CLAUDE_CONTROL_KEY: key,
    FAN_OUT_FAKE_AGENTS: JSON.stringify([{ id: 'full-session-id', status: 'idle' }]),
  };
  const args = [
    'deliver',
    '--source',
    file,
    '--message-id',
    'claude-one',
    '--endpoints',
    JSON.stringify([{ type: 'claude-session', id: 'full-session' }]),
  ];
  const result = await runChild(args, env);
  claudeServer.close();
  assert.equal(result.code, 0);
  const out = JSON.parse(result.stdout);
  assert.equal(out.results[0].status, 'delivered');
  assert.equal(attach.short, 'full-session-id');
  assert.ok(pasted.includes(Buffer.from('Ship the migration notes to the team.')));
  assert.ok(pasted.subarray(0, 6).equals(Buffer.from('\x1b[200~')));
}

// --- fan out to one codex-thread AND one claude-session in the same call: exactly one extraction, two deliveries ---
{
  const socketPath = path.join(directory, 'codex-combo.sock');
  const { server, requests } = await fakeCodexServer(socketPath);

  const agent = path.join(directory, 'fake-claude-combo');
  fs.writeFileSync(agent, `#!${process.execPath}\nprocess.stdout.write(process.env.FAN_OUT_FAKE_AGENTS);\n`);
  fs.chmodSync(agent, 0o755);
  const control = path.join(directory, 'claude-combo.sock');
  const key = path.join(directory, 'control-combo.key');
  fs.writeFileSync(key, 'dummy-key\n');
  let pasted;
  const claudeServer = await listen(control, socket => {
    let raw = Buffer.alloc(0);
    socket.on('data', data => {
      raw = Buffer.concat([raw, data]);
      const end = raw.indexOf(10);
      if (end < 0) return;
      raw = raw.subarray(end + 1);
      socket.write('{"ok":true}\n');
      socket.on('data', d => {
        pasted = d;
      });
    });
  });

  const env = {
    FAN_OUT_CLAUDE_AGENTS: agent,
    FAN_OUT_CLAUDE_CONTROL_SOCKET: control,
    FAN_OUT_CLAUDE_CONTROL_KEY: key,
    FAN_OUT_FAKE_AGENTS: JSON.stringify([{ id: 'combo-session-id', status: 'idle' }]),
  };
  const endpoints = [
    { type: 'codex-thread', id: 'thread-combo', socket: socketPath },
    { type: 'claude-session', id: 'combo-session' },
  ];
  const result = await runChild(['deliver', '--source', file, '--message-id', 'claude-one', '--endpoints', JSON.stringify(endpoints)], env);
  server.close();
  claudeServer.close();

  assert.equal(result.code, 0);
  const out = JSON.parse(result.stdout);
  assert.equal(out.endpoints_count, 2);
  assert.deepEqual(
    out.results.map(r => r.status),
    ['delivered', 'delivered']
  );
  const turnStart = requests.find(r => r.method === 'turn/start');
  assert.equal(turnStart.params.input[0].text, 'Ship the migration notes to the team.');
  assert.ok(pasted && pasted.includes(Buffer.from('Ship the migration notes to the team.')));
}

console.log('fan-out fixtures passed');
