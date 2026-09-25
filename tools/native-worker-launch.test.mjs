#!/usr/bin/env node
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';

const tool = path.join(import.meta.dirname, 'native-worker-launch.mjs');
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'native-worker-launch-'));
const flow = path.join(temporary, 'flows', '00f95a');
const sessions = path.join(temporary, 'sessions');
const skills = path.join(temporary, 'skills');
const brief = path.join(temporary, 'brief.md');
fs.mkdirSync(flow, { recursive: true }); fs.mkdirSync(sessions); fs.mkdirSync(skills);
fs.writeFileSync(brief, 'Inspect the fixture and report success.');
for (const name of ['subflow', 'testing']) { const directory = path.join(skills, name); fs.mkdirSync(directory); fs.writeFileSync(path.join(directory, 'SKILL.md'), `# ${name}\nfixture body\n`); }

function serverFrame(payload, opcode = 1) {
  const body = Buffer.from(payload); let header;
  if (body.length < 126) header = Buffer.from([128 | opcode, body.length]);
  else { header = Buffer.alloc(4); header[0] = 128 | opcode; header[1] = 126; header.writeUInt16BE(body.length, 2); }
  return Buffer.concat([header, body]);
}

function fakeServer(socketPath, mutate = () => {}) {
  const calls = [];
  const server = net.createServer(socket => {
    let raw = Buffer.alloc(0), upgraded = false;
    const reply = (id, result) => socket.write(serverFrame(JSON.stringify({ jsonrpc: '2.0', id, result })));
    socket.on('data', data => {
      raw = Buffer.concat([raw, data]);
      if (!upgraded) {
        const end = raw.indexOf('\r\n\r\n'); if (end < 0) return;
        raw = raw.subarray(end + 4); upgraded = true;
        socket.write('HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n');
      }
      while (raw.length >= 2) {
        let length = raw[1] & 127, offset = 2;
        if (length === 126) { if (raw.length < 4) return; length = raw.readUInt16BE(2); offset = 4; }
        if (raw.length < offset + 4 + length) return;
        const mask = raw.subarray(offset, offset + 4), body = Buffer.alloc(length);
        for (let index = 0; index < length; index++) body[index] = raw[offset + 4 + index] ^ mask[index % 4];
        raw = raw.subarray(offset + 4 + length);
        const request = JSON.parse(body); if (!request.id) continue;
        calls.push(request);
        if (request.method === 'initialize') reply(request.id, {});
        else if (request.method === 'skills/list') reply(request.id, ['subflow', 'testing'].map(name => ({ name, path: path.join(skills, name, 'SKILL.md') })));
        else if (request.method === 'thread/start') reply(request.id, { thread: { id: '00000000-1111-4222-8333-444444444444' } });
        else if (request.method === 'turn/start') {
          const turnId = 'turn-one', threadId = request.params.threadId;
          const typed = request.params.input.filter(item => item.type === 'skill');
          const rows = [
            { type: 'session_meta', payload: { id: threadId, cwd: temporary } },
            { type: 'turn_context', payload: { turn_id: turnId, model: 'gpt-5.6-terra', effort: 'medium' } },
            { type: 'event_msg', payload: { thread_id: threadId, turn_id: turnId, item: { type: 'UserMessage', content: request.params.input } } },
            ...typed.map(item => ({ type: 'response_item', payload: { role: 'user', content: [{ text: `<skill>\n<name>${item.name}</name>\n<path>${item.path}</path>\n${fs.readFileSync(item.path, 'utf8')}\n</skill>` }] } })),
            { type: 'event_msg', payload: { thread_id: threadId, turn_id: turnId, item: { type: 'AgentMessage', content: [{ type: 'Text', text: 'Fixture complete.' }] } } },
          ];
          mutate(rows);
          const directory = path.join(sessions, '2026', '09', '25'); fs.mkdirSync(directory, { recursive: true });
          fs.writeFileSync(path.join(directory, `rollout-fixture-${threadId}.jsonl`), `${rows.map(row => JSON.stringify(row)).join('\n')}\n`);
          reply(request.id, { turn: { id: turnId, generationId: 'generation-one' } });
        }
      }
    });
  });
  return { server, calls };
}

function run(arguments_, socketPath, receipt) {
  return new Promise(resolve => {
    const child = spawn(process.execPath, [tool, '--parent-flow-id', '00f95a', '--parent-flow-directory', flow, '--brief-file', brief, '--skill', 'subflow', '--skill', 'testing', '--receipt', receipt, '--cwd', temporary, '--socket', socketPath, '--sessions-root', sessions, '--wait-seconds', '2', '--launch', ...arguments_]);
    let stdout = '', stderr = ''; child.stdout.on('data', data => stdout += data); child.stderr.on('data', data => stderr += data);
    child.on('exit', code => resolve({ code, stdout, stderr }));
  });
}

function runRaw(arguments_) {
  return new Promise(resolve => {
    const child = spawn(process.execPath, [tool, ...arguments_]);
    let stdout = '', stderr = ''; child.stdout.on('data', data => stdout += data); child.stderr.on('data', data => stderr += data);
    child.on('exit', code => resolve({ code, stdout, stderr }));
  });
}

const socketPath = path.join(temporary, 'app-server.sock'), receipt = path.join(temporary, 'receipt.json');
const fixture = fakeServer(socketPath); await new Promise(resolve => fixture.server.listen(socketPath, resolve));
const launched = await run([], socketPath, receipt);
assert.equal(launched.code, 0, launched.stderr);
const parsed = JSON.parse(launched.stdout), stored = JSON.parse(fs.readFileSync(receipt));
assert.equal(parsed.status, 'verified'); assert.equal(stored.model, 'gpt-5.6-terra'); assert.equal(stored.effort, 'medium');
assert.equal(stored.oneStartupPrompt, true); assert.equal(stored.mainFlowIdentityCreated, false); assert.equal(stored.nativeTitleAssigned, false);
assert.deepEqual(fixture.calls.map(call => call.method), ['initialize', 'skills/list', 'thread/start', 'turn/start']);
const first = fixture.calls.find(call => call.method === 'turn/start');
assert.deepEqual(first.params.input.slice(0, 2).map(item => item.type), ['skill', 'skill']);
assert.match(first.params.input.at(-1).text, /^\$subflow FLOW_ID=00f95a FLOW_DIRECTORY=/);
assert.equal(first.params.input.filter(item => item.type === 'text').length, 1);

const duplicate = await run([], socketPath, receipt);
assert.notEqual(duplicate.code, 0); assert.match(duplicate.stderr, /receipt already exists; refusing duplicate startup/);
assert.equal(fixture.calls.filter(call => call.method === 'thread/start').length, 1);
fixture.server.close();

const missingReceipt = await runRaw(['--parent-flow-id', '00f95a', '--parent-flow-directory', flow, '--brief-file', brief, '--skill', 'subflow', '--cwd', temporary, '--socket', socketPath, '--sessions-root', sessions, '--launch']);
assert.notEqual(missingReceipt.code, 0); assert.match(missingReceipt.stderr, /receipt path must be explicit and absolute/);

const noHostReceipt = path.join(temporary, 'no-host.json');
const noHost = await run([], path.join(temporary, 'missing.sock'), noHostReceipt);
assert.notEqual(noHost.code, 0); assert.match(noHost.stderr, /app-server socket is missing/); assert.equal(fs.existsSync(noHostReceipt), false);

const badSocket = path.join(temporary, 'bad.sock'), badReceipt = path.join(temporary, 'bad.json');
const bad = fakeServer(badSocket, rows => { rows.find(row => row.type === 'turn_context').payload.model = 'gpt-6-sol'; });
await new Promise(resolve => bad.server.listen(badSocket, resolve));
const refused = await run([], badSocket, badReceipt);
assert.notEqual(refused.code, 0); assert.match(refused.stderr, /exact Terra model\/effort context/);
assert.equal(JSON.parse(fs.readFileSync(badReceipt)).status, 'failed');
bad.server.close();

const missingSkillSocket = path.join(temporary, 'missing-skill.sock'), missingSkillReceipt = path.join(temporary, 'missing-skill.json');
const missingSkillServer = fakeServer(missingSkillSocket); await new Promise(resolve => missingSkillServer.server.listen(missingSkillSocket, resolve));
const missingSkill = await run(['--skill', 'not-catalogued'], missingSkillSocket, missingSkillReceipt);
assert.notEqual(missingSkill.code, 0); assert.match(missingSkill.stderr, /required native skill unavailable: not-catalogued/);
assert.equal(missingSkillServer.calls.some(call => call.method === 'thread/start'), false);
assert.equal(JSON.parse(fs.readFileSync(missingSkillReceipt)).status, 'failed');
missingSkillServer.server.close();

assert.equal(crypto.createHash('sha256').update(fs.readFileSync(receipt)).digest('hex').length, 64);
console.log('native-worker-launch tests passed');
