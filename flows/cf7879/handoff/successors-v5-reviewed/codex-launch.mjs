import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {createUnixWebSocketTransport} from './client/codex-app-server-client.mjs';

const root = path.dirname(fileURLToPath(import.meta.url));
const opt = name => { const i = process.argv.indexOf(name); return i < 0 ? null : process.argv[i + 1]; };
for (const [name, digest] of Object.entries(JSON.parse(fs.readFileSync(path.join(root, 'artifact-manifest.json'))))) {
  if (crypto.createHash('sha256').update(fs.readFileSync(path.join(root, name))).digest('hex') !== digest) throw new Error(`hash mismatch: ${name}`);
}
const cwd = fs.realpathSync(opt('--cwd') ?? root);
const baseInstructions = fs.readFileSync(path.join(root, 'codex-base.md'), 'utf8');
const first = fs.readFileSync(path.join(root, 'first-prompt.md'), 'utf8');
if (Buffer.byteLength(first) >= 100000) throw new Error('first prompt too large');
const params = {cwd, model: 'gpt-6-astra', baseInstructions, ephemeral: false};
if (!process.argv.includes('--launch')) {
  console.log(JSON.stringify({dryRun: true, replacementField: 'baseInstructions', baseBytes: Buffer.byteLength(baseInstructions), firstPromptBytes: Buffer.byteLength(first), requestBytes: Buffer.byteLength(JSON.stringify(params))}));
} else {
  const repo = path.join(cwd, '.jj/repo');
  if (!fs.lstatSync(repo).isDirectory() || fs.lstatSync(repo).isSymbolicLink()) throw new Error('independent JJ clone root required');
  const socket = opt('--socket');
  if (!socket) throw new Error('explicit connected app-server socket required');
  const t = createUnixWebSocketTransport(socket);
  const timeout = setTimeout(() => {t.close(); process.exit(2);}, 20000);
  try {
    await t.request('initialize', {clientInfo: {name: 'primary-successor-launch', version: '1'}, capabilities: {experimentalApi: true}});
    await t.notify('initialized', {});
    const status = await t.request('remoteControl/status/read', {});
    if (status.status !== 'connected') throw new Error('host remote control is not connected');
    const started = await t.request('thread/start', params);
    const threadId = started.thread.id;
    console.log(JSON.stringify({kind: 'thread-created', threadId, remoteStatus: status.status}));
    await t.request('thread/name/set', {threadId, name: 'Primary Codex successor of cf7879 · readiness pending'});
    const turn = await t.request('turn/start', {threadId, effort: 'medium', input: [{type: 'text', text: first}]});
    console.log(JSON.stringify({kind: 'first-turn-started', threadId, turnId: turn.turn?.id, desktopVisibilityVerified: false}));
  } finally { clearTimeout(timeout); t.close(); }
}
