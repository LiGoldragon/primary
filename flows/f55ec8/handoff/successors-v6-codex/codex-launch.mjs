// v6 Codex launch: the v5 route with the corrected base instructions.
// Dry-run by default; --launch is the live path and needs the living's word.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createUnixWebSocketTransport } from '/home/li/wt/github.com/LiGoldragon/primary/cf7879-report-recovery/flows/cf7879/handoff/successors-v5-reviewed/client/codex-app-server-client.mjs';

const root = path.dirname(fileURLToPath(import.meta.url));
const opt = name => { const i = process.argv.indexOf(name); return i < 0 ? null : process.argv[i + 1]; };
const socket = opt('--socket') ?? `${process.env.HOME}/.codex/app-server-control/app-server-control.sock`;
const cwd = fs.realpathSync(opt('--cwd') ?? (() => { throw new Error('--cwd is required'); })());
const baseInstructions = fs.readFileSync(path.join(root, 'codex-base.md'), 'utf8');
const first = fs.readFileSync(path.join(root, 'first-prompt.md'), 'utf8');
if (Buffer.byteLength(first) >= 100000) throw new Error('first prompt too large');

const repo = path.join(cwd, '.jj/repo');
if (!fs.lstatSync(repo).isDirectory() || fs.lstatSync(repo).isSymbolicLink()) throw new Error('independent JJ clone root required');

const params = { cwd, model: 'gpt-6-astra', baseInstructions, ephemeral: false };
if (!process.argv.includes('--launch')) {
  console.log(JSON.stringify({ dryRun: true, replacementField: 'baseInstructions', baseBytes: Buffer.byteLength(baseInstructions), firstPromptBytes: Buffer.byteLength(first), cwd, socket }));
  process.exit(0);
}

const t = createUnixWebSocketTransport(socket);
const timeout = setTimeout(() => { t.close(); process.exit(2); }, 60000);
try {
  await t.request('initialize', { clientInfo: { name: 'primary-codex-recovery-launch', version: '1' }, capabilities: { experimentalApi: true } });
  await t.notify('initialized', {});
  const status = await t.request('remoteControl/status/read', {});
  if (status.status !== 'connected') throw new Error(`host remote control is not connected: ${status.status}`);
  const started = await t.request('thread/start', params);
  const threadId = started.thread.id;
  console.log(JSON.stringify({ kind: 'thread-created', threadId, remoteStatus: status.status, serverName: status.serverName }));
  await t.request('thread/name/set', { threadId, name: 'Primary Codex, recovery of 2026-09-17 · resets its own usage' });
  const turn = await t.request('turn/start', { threadId, effort: 'medium', input: [{ type: 'text', text: first }] });
  console.log(JSON.stringify({ kind: 'first-turn-started', threadId, turnId: turn.turn?.id }));
} finally { clearTimeout(timeout); t.close(); }
