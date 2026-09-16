#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';

const root = '/home/li/primary';
const sources = [
  `${root}/flows/05c604/vision/layers.md`,
  ...fs.readdirSync(`${root}/Intent`).filter(name => name.endsWith('.md')).sort().map(name => `${root}/Intent/${name}`),
  ...fs.readdirSync(`${root}/design/Spirit`).filter(name => name.endsWith('.md')).sort().map(name => `${root}/design/Spirit/${name}`),
];
const sha = text => crypto.createHash('sha256').update(text, 'utf8').digest('hex');
const records = sources.map(path => { const text = fs.readFileSync(path, 'utf8'); return { path, utf8_bytes: Buffer.byteLength(text), sha256: sha(text), text }; });
const base = `You are CORE, a distinct core main for flow cf7879. Root cf7879 remains the primary and you are not a successor. Spirit and Intent records supplied below govern you. Vision is available for consideration only and is not authoritative for CORE. Work as a read-only, bounded first turn: state your runtime identity, restate the authority boundary, and provide readiness to coordinate with the primary and the separate core-checkup worker. Do not create a recursive work loop, deliver messages, deploy, edit files, change network state, or decide actions. Approval-wait is never idle. Checkups use Luna and may only read state; any optional restart is once for one owned failed unit and requires the checkup worker's explicit policy. Return a concise JSON object with runtime_identity, authority_boundary, readiness, and limitations.`;
const input = JSON.stringify({ task: 'Establish CORE readiness from supplied authoritative records.', source_manifest: records.map(({ text, ...record }) => record), records });
const manifest = { kind: 'core-bootstrap-source-manifest', core_role: 'distinct-core-main', primary_flow_identifier: 'cf7879', model: 'gpt-6-astra', base_instructions: { utf8_bytes: Buffer.byteLength(base), sha256: sha(base) }, sources: records.map(({ text, ...record }) => record), input_utf8_bytes: Buffer.byteLength(input) };
if (process.argv.includes('--manifest')) { console.log(JSON.stringify(manifest)); process.exit(0); }
const { createUnixWebSocketTransport } = await import(pathToFileURL('/home/li/wt/primary-5f4fea/tools/codex-app-server-client.mjs').href);
const t = createUnixWebSocketTransport('/home/li/.codex/app-server-control/app-server-control.sock');
try { await t.request('initialize', { clientInfo: { name: 'core-bootstrap', version: '1' }, capabilities: {} }); await t.notify('initialized', {}); const models = await t.request('model/list', {}); const available_models = models.data?.map(x => x.model) ?? []; if (!available_models.includes('gpt-6-astra')) throw new Error('gpt-6-astra not exposed'); const started = await t.request('thread/start', { model: 'gpt-6-astra', sandbox: 'read-only', ephemeral: false, baseInstructions: base, developerInstructions: null, cwd: process.cwd(), threadSource: 'subAgentOther' }); const turn = await t.request('turn/start', { threadId: started.thread.id, input: [{ type: 'text', text: input }] }); console.log(JSON.stringify({ ...manifest, available_models, core_thread_identifier: started.thread.id, core_turn_identifier: turn.turn?.id ?? null, turn_status: turn.turn?.status ?? null })); } finally { t.close(); }
