#!/usr/bin/env node
/* Launch one native Codex Terra worker with typed skill inputs and verify its rollout. */
import crypto from 'node:crypto';
import fs from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';

const MODEL = 'gpt-5.6-terra';
const args = process.argv.slice(2);
const values = name => args.flatMap((value, index) => value === name ? [args[index + 1]] : []);
const value = name => values(name).at(-1);
const has = name => args.includes(name);
const fail = message => { throw new Error(message); };
const digest = body => crypto.createHash('sha256').update(body).digest('hex');
const sleep = milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds));

function usage() {
  return `usage: native-worker-launch.mjs --parent-flow-id FLOW_ID --parent-flow-directory DIR --brief-file FILE --skill NAME [--skill NAME ...] --receipt FILE [--cwd DIR] [--effort low|medium] [--socket FILE] [--sessions-root DIR] [--wait-seconds N] --launch

Launches a new native ${MODEL} implementation worker through the current Codex app-server. The launcher sends one initial turn containing typed skill items followed by one text brief. It does not assign a main Flow identity or title.

The brief begins with the exact parent identity line:
  $subflow FLOW_ID=<FLOW_ID> FLOW_DIRECTORY=<FLOW_DIRECTORY>

The required skill list must explicitly include subflow. The receipt path must be new; its exclusive reservation prevents an accidental second launch.`;
}

function parseOptions() {
  if (has('--help')) return { help: true };
  const cwd = path.resolve(value('--cwd') ?? process.cwd());
  const parentFlowId = value('--parent-flow-id');
  const parentFlowDirectory = value('--parent-flow-directory');
  const briefFile = value('--brief-file');
  const receiptFile = value('--receipt');
  const effort = value('--effort') ?? 'medium';
  const socket = path.resolve(value('--socket') ?? path.join(os.homedir(), '.codex/app-server-control/app-server-control.sock'));
  const sessionsRoot = path.resolve(value('--sessions-root') ?? path.join(os.homedir(), '.codex/sessions'));
  const waitSeconds = Number(value('--wait-seconds') ?? 180);
  const skills = values('--skill');
  if (!has('--launch')) fail('refusing to start a worker without --launch');
  if (!fs.existsSync(cwd) || !fs.statSync(cwd).isDirectory()) fail('worker cwd is missing');
  if (!/^[a-f0-9]{6}$/.test(parentFlowId ?? '')) fail('parent Flow ID must be six lowercase hexadecimal characters');
  if (!parentFlowDirectory || !path.isAbsolute(parentFlowDirectory)) fail('parent Flow directory must be absolute');
  if (path.basename(path.resolve(parentFlowDirectory)) !== parentFlowId) fail('parent Flow directory basename must equal parent Flow ID');
  if (!fs.existsSync(parentFlowDirectory) || !fs.statSync(parentFlowDirectory).isDirectory()) fail('parent Flow directory is missing');
  if (!briefFile || !fs.existsSync(briefFile) || !fs.statSync(briefFile).isFile()) fail('brief file is missing');
  if (!receiptFile || !path.isAbsolute(receiptFile)) fail('receipt path must be explicit and absolute');
  if (!['low', 'medium'].includes(effort)) fail('Terra effort must be low or medium');
  if (!Number.isInteger(waitSeconds) || waitSeconds < 1 || waitSeconds > 900) fail('wait seconds must be an integer from 1 through 900');
  if (!skills.length || !skills.includes('subflow')) fail('required skills must explicitly include subflow');
  if (skills.some(name => !/^[a-z][a-z0-9-]*$/.test(name)) || new Set(skills).size !== skills.length) fail('skill names must be unique lowercase names');
  if (!fs.existsSync(socket) || !fs.statSync(socket).isSocket()) fail(`Codex app-server socket is missing: ${socket}`);
  if (!fs.existsSync(sessionsRoot) || !fs.statSync(sessionsRoot).isDirectory()) fail(`Codex sessions root is missing: ${sessionsRoot}`);
  if (fs.existsSync(receiptFile)) fail(`receipt already exists; refusing duplicate startup: ${receiptFile}`);
  const brief = fs.readFileSync(briefFile, 'utf8');
  if (!brief.trim()) fail('brief file is empty');
  return { cwd, parentFlowId, parentFlowDirectory: path.resolve(parentFlowDirectory), briefFile: path.resolve(briefFile), receiptFile, effort, socket, sessionsRoot, waitSeconds, skills, brief };
}

function reserveReceipt(options) {
  fs.mkdirSync(path.dirname(options.receiptFile), { recursive: true });
  const initial = {
    version: 1,
    status: 'reserved',
    model: MODEL,
    effort: options.effort,
    parentFlowId: options.parentFlowId,
    parentFlowDirectory: options.parentFlowDirectory,
    endpoint: options.socket,
    requiredSkillNames: options.skills,
    reservedAt: new Date().toISOString(),
  };
  fs.writeFileSync(options.receiptFile, `${JSON.stringify(initial, null, 2)}\n`, { flag: 'wx', mode: 0o600 });
  return initial;
}

function writeReceipt(file, receipt) {
  const temporary = `${file}.tmp-${process.pid}`;
  fs.writeFileSync(temporary, `${JSON.stringify(receipt, null, 2)}\n`, { mode: 0o600 });
  fs.renameSync(temporary, file);
}

function catalogRows(reply) {
  const available = reply?.skills ?? reply?.data?.skills ?? reply?.data?.items ?? reply?.data ?? reply?.result?.skills ?? reply;
  if (!Array.isArray(available)) fail('skills/list did not return an array');
  return available.flatMap(item => item?.skills ?? [item?.skill ?? item]);
}

function resolveSkills(reply, requiredNames) {
  const catalog = new Map(catalogRows(reply).filter(Boolean).map(skill => [skill.name, skill]));
  return requiredNames.map(name => {
    const entry = catalog.get(name);
    if (!entry?.path || !path.isAbsolute(entry.path)) fail(`required native skill unavailable: ${name}`);
    if (!fs.existsSync(entry.path) || !fs.statSync(entry.path).isFile()) fail(`catalog path is missing for required native skill: ${name}`);
    const source = fs.readFileSync(entry.path, 'utf8');
    if (!source.trim()) fail(`catalog source is empty for required native skill: ${name}`);
    return { name, path: entry.path, source, sha256: digest(source) };
  });
}

function promptText(options) {
  return `$subflow FLOW_ID=${options.parentFlowId} FLOW_DIRECTORY=${options.parentFlowDirectory}\n\nYou are a native ${MODEL} implementation worker and a subflow of the parent above. Do not claim a new Flow ID or set a main Flow title. Do not spawn a Sol collaboration child. Work only within this brief and return evidence to the parent.\n\n${options.brief.trim()}\n`;
}

function frame(payload, opcode = 1) {
  const body = Buffer.from(payload), mask = crypto.randomBytes(4);
  let header;
  if (body.length < 126) header = Buffer.from([128 | opcode, 128 | body.length]);
  else if (body.length <= 65535) { header = Buffer.alloc(4); header[0] = 128 | opcode; header[1] = 254; header.writeUInt16BE(body.length, 2); }
  else { header = Buffer.alloc(10); header[0] = 128 | opcode; header[1] = 255; header.writeBigUInt64BE(BigInt(body.length), 2); }
  const encrypted = Buffer.alloc(body.length);
  for (let index = 0; index < body.length; index++) encrypted[index] = body[index] ^ mask[index % 4];
  return Buffer.concat([header, mask, encrypted]);
}

async function withRpc(socketPath, operation) {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection(socketPath);
    let buffer = Buffer.alloc(0), upgraded = false, requestId = 0, fragment = null, settled = false;
    const pending = new Map();
    const finish = (error, result) => {
      if (settled) return;
      settled = true;
      for (const waiter of pending.values()) clearTimeout(waiter.timer);
      pending.clear();
      socket.destroy();
      error ? reject(error) : resolve(result);
    };
    const call = (method, params) => new Promise((accept, rejectCall) => {
      const id = ++requestId;
      const timer = setTimeout(() => { pending.delete(id); rejectCall(new Error(`RPC timeout: ${method}`)); }, 15000);
      pending.set(id, { accept, rejectCall, timer });
      socket.write(frame(JSON.stringify({ jsonrpc: '2.0', id, method, params })));
    });
    const parse = () => {
      while (buffer.length >= 2) {
        const fin = Boolean(buffer[0] & 128), opcode = buffer[0] & 15;
        let length = buffer[1] & 127, offset = 2;
        if (length === 126) { if (buffer.length < 4) return; length = buffer.readUInt16BE(2); offset = 4; }
        else if (length === 127) { if (buffer.length < 10) return; length = Number(buffer.readBigUInt64BE(2)); offset = 10; }
        if (buffer.length < offset + length) return;
        const body = buffer.subarray(offset, offset + length); buffer = buffer.subarray(offset + length);
        if (opcode === 9) { socket.write(frame(body, 10)); continue; }
        if (opcode === 1) fragment = body;
        else if (opcode === 0 && fragment) fragment = Buffer.concat([fragment, body]);
        else continue;
        if (!fin) continue;
        let message;
        try { message = JSON.parse(fragment); } catch (error) { return finish(error); }
        fragment = null;
        const waiter = pending.get(message.id);
        if (!waiter) continue;
        pending.delete(message.id); clearTimeout(waiter.timer);
        message.error ? waiter.rejectCall(new Error(JSON.stringify(message.error))) : waiter.accept(message.result);
      }
    };
    socket.on('error', error => finish(error));
    socket.on('connect', () => socket.write('GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n'));
    socket.on('data', data => {
      buffer = Buffer.concat([buffer, data]);
      if (!upgraded) {
        const end = buffer.indexOf('\r\n\r\n');
        if (end < 0) return;
        if (!buffer.subarray(0, end).toString().startsWith('HTTP/1.1 101')) return finish(new Error('websocket upgrade refused'));
        buffer = buffer.subarray(end + 4); upgraded = true;
        void (async () => {
          try {
            await call('initialize', { clientInfo: { name: 'native-worker-launch', version: '1' } });
            socket.write(frame(JSON.stringify({ jsonrpc: '2.0', method: 'initialized', params: {} })));
            finish(null, await operation(call));
          } catch (error) { finish(error); }
        })();
      }
      parse();
    });
  });
}

function walk(directory, match, found = []) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const candidate = path.join(directory, entry.name);
    if (entry.isDirectory()) walk(candidate, match, found);
    else if (entry.isFile() && match(entry.name)) found.push(candidate);
  }
  return found;
}

function findRollout(sessionsRoot, threadId) {
  const matches = walk(sessionsRoot, name => name.startsWith('rollout-') && name.endsWith(`-${threadId}.jsonl`));
  if (matches.length > 1) fail(`multiple rollout files found for native thread ${threadId}`);
  return matches[0] ?? null;
}

function parseRows(file) {
  return fs.readFileSync(file, 'utf8').trim().split('\n').filter(Boolean).map(line => JSON.parse(line));
}

function verifyRollout(file, pending) {
  const body = fs.readFileSync(file, 'utf8'), rows = parseRows(file);
  const session = rows.find(row => row.type === 'session_meta')?.payload;
  if (session?.id !== pending.threadId || path.resolve(session?.cwd ?? '') !== pending.cwd) fail('rollout session identity or cwd differs');
  const contexts = rows.filter(row => row.type === 'turn_context' && row.payload?.turn_id === pending.turnId);
  if (contexts.length !== 1 || contexts[0].payload.model !== MODEL || contexts[0].payload.effort !== pending.effort) fail('rollout lacks one exact Terra model/effort context');
  const userMessages = rows.filter(row => row.type === 'event_msg' && row.payload?.thread_id === pending.threadId && row.payload?.item?.type === 'UserMessage');
  if (userMessages.length !== 1 || userMessages[0].payload?.turn_id !== pending.turnId) fail('rollout does not contain exactly one startup user message');
  const content = userMessages[0].payload.item.content ?? [];
  const typed = content.filter(item => item.type === 'skill');
  const texts = content.filter(item => item.type === 'text');
  if (texts.length !== 1 || digest(texts[0].text ?? '') !== pending.firstPromptSha256) fail('rollout first text brief differs from receipt');
  if (typed.length !== pending.skillManifest.length) fail('rollout typed skill count differs from receipt');
  for (const expected of pending.skillManifest) {
    if (!typed.some(item => item.name === expected.name && item.path === expected.path)) fail(`rollout lacks typed skill item: ${expected.name}`);
    const prefix = `<skill>\n<name>${expected.name}</name>\n<path>${expected.path}</path>\n`;
    const expanded = rows.filter(row => row.type === 'response_item' && row.payload?.role === 'user').flatMap(row => row.payload?.content ?? []).map(item => item.text ?? '');
    if (!expanded.some(text => text.startsWith(prefix) && text.includes(expected.source) && text.trimEnd().endsWith('</skill>'))) fail(`rollout lacks expanded skill source: ${expected.name}`);
  }
  const response = rows.find(row => row.type === 'event_msg' && row.payload?.thread_id === pending.threadId && row.payload?.turn_id === pending.turnId && row.payload?.item?.type === 'AgentMessage');
  if (!response) return null;
  return { rollout: file, rolloutSha256: digest(body), responseObserved: true };
}

async function awaitVerifiedRollout(options, pending) {
  const deadline = Date.now() + options.waitSeconds * 1000;
  let lastError = null;
  while (Date.now() < deadline) {
    const file = findRollout(options.sessionsRoot, pending.threadId);
    if (file) {
      try {
        const verified = verifyRollout(file, pending);
        if (verified) return verified;
      } catch (error) { lastError = error; }
    }
    await sleep(250);
  }
  if (lastError) throw lastError;
  fail(`timed out waiting for verified native rollout after ${options.waitSeconds} seconds`);
}

async function launch(options) {
  const reserved = reserveReceipt(options);
  let current = reserved;
  try {
    const result = await withRpc(options.socket, async call => {
      const catalog = await call('skills/list', { cwds: [options.cwd] });
      const skillManifest = resolveSkills(catalog, options.skills);
      const prompt = promptText(options);
      const started = await call('thread/start', { model: MODEL, cwd: options.cwd, approvalPolicy: 'never', sandbox: 'danger-full-access' });
      const threadId = started?.thread?.id ?? started?.id;
      if (!threadId) fail('thread/start returned no native thread ID');
      current = { ...reserved, status: 'thread-created', cwd: options.cwd, threadId, skillManifest, firstPromptSha256: digest(prompt), createdAt: new Date().toISOString() };
      writeReceipt(options.receiptFile, current);
      const input = [...skillManifest.map(skill => ({ type: 'skill', name: skill.name, path: skill.path })), { type: 'text', text: prompt, text_elements: [] }];
      const turn = await call('turn/start', { threadId, effort: options.effort, input });
      const turnId = turn?.turn?.id ?? turn?.id;
      if (!turnId) fail('turn/start returned no native turn ID');
      current = { ...current, status: 'pending-verification', turnId, generationId: turn?.turn?.generationId ?? turn?.generationId ?? turn?.generation?.id ?? null, submittedAt: new Date().toISOString() };
      writeReceipt(options.receiptFile, current);
      return current;
    });
    const verified = await awaitVerifiedRollout(options, result);
    current = { ...result, status: 'verified', verifiedAt: new Date().toISOString(), rolloutEvidence: { path: verified.rollout, sha256: verified.rolloutSha256 }, oneStartupPrompt: true, mainFlowIdentityCreated: false, nativeTitleAssigned: false };
    writeReceipt(options.receiptFile, current);
    return current;
  } catch (error) {
    writeReceipt(options.receiptFile, { ...current, status: 'failed', failedAt: new Date().toISOString(), failure: String(error) });
    throw error;
  }
}

const invokedDirectly = Boolean(process.argv[1]) && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname);
if (invokedDirectly) {
  try {
    const options = parseOptions();
    if (options.help) console.log(usage());
    else console.log(JSON.stringify(await launch(options)));
  } catch (error) {
    console.error(error.message ?? String(error));
    process.exitCode = 1;
  }
}

export { MODEL, findRollout, promptText, resolveSkills, verifyRollout };
