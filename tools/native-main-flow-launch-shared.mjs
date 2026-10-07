import crypto from 'node:crypto';
import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import net from 'node:net';
import path from 'node:path';

export const FLOW_ID = /^[0-9a-f]{6,}$/;
export const LAYER = /^(Primary|Secondary|Tertiary|Quaternary)$/;
export const CONTINUATION_RECORD = 'continuation.json';

// A native voice is identified by its aspect, layer, and durable Flow ID.
// Model correspondence stays in the profile table and is deliberately absent.
export function canonicalTitleFor(aspect, _model, flowId, layer) {
  if (!/^(Psyche|Mind|Field)$/.test(aspect ?? '')) throw new Error('canonical native title requires an exact aspect');
  if (!LAYER.test(layer ?? '')) throw new Error('canonical native title requires an exact layer');
  if (!FLOW_ID.test(flowId ?? '')) throw new Error('canonical native title requires the exact short Flow ID');
  return `{ ${aspect} ${layer} ${flowId} }`;
}

function readMetaflowSource(file) {
  if (!file || !path.isAbsolute(file) || !fs.statSync(file).isFile()) throw new Error('root launch requires a readable absolute --metaflow source file');
  const metaflow = fs.readFileSync(file, 'utf8');
  if (!metaflow.trim()) throw new Error('root launch metaflow source is empty');
  return metaflow;
}

export function continuationForLaunch({flowsRoot, root = false, predecessor, metaflowFile}) {
  if (root === Boolean(predecessor)) throw new Error('choose exactly one of --root or --predecessor');
  if (!path.isAbsolute(flowsRoot)) throw new Error('continuation requires an absolute flows root');
  if (root) {
    if (predecessor !== undefined) throw new Error('root launch cannot name a predecessor');
    return {predecessor: null, metaflow: readMetaflowSource(metaflowFile)};
  }
  if (!FLOW_ID.test(predecessor ?? '')) throw new Error('continuation predecessor must be an exact Flow ID');
  if (metaflowFile !== undefined) throw new Error('continuation inherits metaflow; --metaflow is only valid with --root');
  const recordPath = path.join(flowsRoot, predecessor, CONTINUATION_RECORD);
  let record;
  try { record = JSON.parse(fs.readFileSync(recordPath, 'utf8')); }
  catch { throw new Error(`continuation predecessor record is unavailable: ${recordPath}`); }
  if (!record || record.flowId !== predecessor || typeof record.metaflow !== 'string' || !record.metaflow.trim())
    throw new Error(`continuation predecessor record is invalid: ${recordPath}`);
  return {predecessor, metaflow: record.metaflow};
}

export function writeContinuationRecord(flowsRoot, flowId, continuation) {
  if (!FLOW_ID.test(flowId ?? '')) throw new Error('continuation record requires the exact new Flow ID');
  if (!continuation || (continuation.predecessor !== null && !FLOW_ID.test(continuation.predecessor)) || typeof continuation.metaflow !== 'string' || !continuation.metaflow.trim())
    throw new Error('continuation record has invalid lineage');
  const recordPath = path.join(flowsRoot, flowId, CONTINUATION_RECORD);
  const record = {flowId, predecessor: continuation.predecessor, metaflow: continuation.metaflow};
  fs.writeFileSync(recordPath, `${JSON.stringify(record)}\n`, {encoding: 'utf8', flag: 'wx', mode: 0o600});
  const readback = JSON.parse(fs.readFileSync(recordPath, 'utf8'));
  if (readback.flowId !== record.flowId || readback.predecessor !== record.predecessor || readback.metaflow !== record.metaflow)
    throw new Error('continuation record readback differs');
  return {recordPath, record: readback};
}

export function clientForModel(model, home = process.env.HOME) {
  if (!home || !path.isAbsolute(home)) throw new Error('absolute home required for Codex endpoint selection');
  const next = ['gpt-6-astra', 'gpt-6-sol', 'gpt-6.1-sol', 'gpt-6-luna'].includes(model);
  const command = next ? 'codex-next' : 'codex';
  const expectedPath = path.join(home, '.nix-profile', 'bin', command);
  if (!next) return {command, expectedPath, endpoint: path.join(home, '.codex', 'app-server-control', 'app-server-control.sock')};
  // The installed wrapper owns the remote/home tuple; a generation name is
  // not its endpoint (candidate homes can have an immutable suffix).
  const wrapper = fs.readFileSync(expectedPath, 'utf8');
  const remotes = [...wrapper.matchAll(/--remote\s+unix:\/\/(\/[^\s"']+)/g)].map(match => match[1]);
  const homes = [...wrapper.matchAll(/(?:export\s+)?CODEX_HOME=(\/[^\s;"']+)/g)].map(match => match[1]);
  if (remotes.length !== 1 || homes.length !== 1 || remotes[0] !== path.join(homes[0], 'app-server-control', 'app-server-control.sock'))
    throw new Error('installed Codex Next wrapper must declare one matching literal remote/home tuple');
  return {command, expectedPath, endpoint: remotes[0]};
}

function frame(payload, opcode = 1) {
  const body = Buffer.from(payload), mask = crypto.randomBytes(4);
  let header;
  if (body.length < 126) header = Buffer.from([128 | opcode, 128 | body.length]);
  else if (body.length <= 65535) { header = Buffer.alloc(4); header[0] = 128 | opcode; header[1] = 254; header.writeUInt16BE(body.length, 2); }
  else { header = Buffer.alloc(10); header[0] = 128 | opcode; header[1] = 255; header.writeBigUInt64BE(BigInt(body.length), 2); }
  const encrypted = Buffer.alloc(body.length);
  for (let i = 0; i < body.length; i++) encrypted[i] = body[i] ^ mask[i % 4];
  return Buffer.concat([header, mask, encrypted]);
}

export async function withRpc(socketPath, fn) {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection(socketPath); let buf = Buffer.alloc(0), upgraded = false, next = 0, fragment = null; const pending = new Map();
    const fail = error => { socket.destroy(); reject(error); };
    const call = (method, params) => new Promise((ok, no) => { const id = ++next; const timer = setTimeout(() => { pending.delete(id); no(new Error(`RPC timeout: ${method}`)); }, 15000); pending.set(id, {ok, no, timer}); socket.write(frame(JSON.stringify({jsonrpc: '2.0', id, method, params}))); });
    const parse = () => { while (buf.length >= 2) { const fin = !!(buf[0] & 128), opcode = buf[0] & 15; let length = buf[1] & 127, offset = 2; if (length === 126) { if (buf.length < 4) return; length = buf.readUInt16BE(2); offset = 4; } else if (length === 127) { if (buf.length < 10) return; length = Number(buf.readBigUInt64BE(2)); offset = 10; } if (buf.length < offset + length) return; const body = buf.subarray(offset, offset + length); buf = buf.subarray(offset + length); if (opcode === 9) { socket.write(frame(body, 10)); continue; } if (opcode === 1) fragment = body; else if (opcode === 0 && fragment) fragment = Buffer.concat([fragment, body]); else continue; if (!fin) continue; const message = JSON.parse(fragment); fragment = null; const wait = pending.get(message.id); if (wait) { pending.delete(message.id); clearTimeout(wait.timer); message.error ? wait.no(new Error(JSON.stringify(message.error))) : wait.ok(message.result); } } };
    socket.on('error', fail); socket.on('connect', () => socket.write('GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n'));
    socket.on('data', data => { buf = Buffer.concat([buf, data]); if (!upgraded) { const end = buf.indexOf('\r\n\r\n'); if (end < 0) return; if (!buf.subarray(0, end).toString().startsWith('HTTP/1.1 101')) return fail(new Error('websocket upgrade refused')); buf = buf.subarray(end + 4); upgraded = true; void (async () => { try { await call('initialize', {clientInfo: {name: 'native-main-flow-launch', version: '1'}}); socket.write(frame(JSON.stringify({jsonrpc: '2.0', method: 'initialized', params: {}}))); resolve(await fn(call)); socket.end(); } catch (error) { fail(error); } })(); } parse(); });
  });
}

export async function setAndReadNativeTitle(call, threadId, nativeTitle) {
  await call('thread/name/set', {threadId, name: nativeTitle});
  const read = await call('thread/read', {threadId, includeTurns: false});
  const thread = read?.thread ?? read;
  if (thread?.id !== threadId || thread?.name !== nativeTitle) throw new Error('native title setter readback differs');
  return thread;
}

export function herdrSessionReportArgs(herdr, threadId) {
  return ['--session', herdr.session, 'pane', 'report-agent-session', herdr.paneId, '--source', 'herdr:codex', '--agent', 'codex', '--agent-session-id', threadId, '--session-start-source', 'native-main-flow-launch'];
}

export function pickWorkspace(workspaces, label) {
  if (workspaces.length === 1) return workspaces[0];
  if (!label) throw new Error(`Herdr holds ${workspaces.length} workspaces; name one with --herdr-workspace-label`);
  const found = workspaces.filter(workspace => workspace.label === label);
  if (found.length !== 1) throw new Error(`expected one Herdr workspace labelled ${label}, found ${found.length}`);
  return found[0];
}

export function resolveSkillDependencies(roots, run = request => execFileSync('curriculum', [request], {encoding: 'utf8'})) {
  if (!Array.isArray(roots) || roots.length === 0 || roots.some(name => !/^[A-Za-z0-9_-]+$/.test(name)))
    throw new Error('skill roots must be a nonempty vector of Datom names');
  const request = `ResolveSkills.[ ${roots.join(' ')} ]`;
  let output;
  try { output = run(request); }
  catch (error) { throw new Error(`Curriculum ResolveSkills failed: ${error.message}`, {cause: error}); }
  const match = /^ResolvedSkills\.\[\s*([A-Za-z0-9_-]+(?:\s+[A-Za-z0-9_-]+)*)?\s*\]$/.exec(String(output).trim());
  if (!match) throw new Error('Curriculum returned an invalid ResolvedSkills value');
  const names = match[1] ? match[1].split(/\s+/) : [];
  if (new Set(names).size !== names.length) throw new Error('Curriculum returned duplicate resolved skills');
  const returned = new Set(names);
  const missing = roots.filter(name => !returned.has(name));
  if (missing.length) throw new Error(`Curriculum omitted requested skill roots: ${missing.join(' ')}`);
  return names;
}

export function orderSkillsForPrompt(names, leading = 'operation-main-flow') {
  if (new Set(names).size !== names.length) throw new Error('resolved skill closure contains duplicates');
  return names.includes(leading) ? [leading, ...names.filter(name => name !== leading)] : [...names];
}
