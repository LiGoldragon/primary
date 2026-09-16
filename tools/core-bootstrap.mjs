#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

const root = '/home/li/primary';
const sources = [
  `${root}/flows/05c604/vision/layers.md`,
  ...fs.readdirSync(`${root}/Intent`).filter(name => name.endsWith('.md')).sort().map(name => `${root}/Intent/${name}`),
  ...fs.readdirSync(`${root}/design/Spirit`).filter(name => name.endsWith('.md')).sort().map(name => `${root}/design/Spirit/${name}`),
];
const sha = text => crypto.createHash('sha256').update(text, 'utf8').digest('hex');
const records = sources.map(sourcePath => { const text = fs.readFileSync(sourcePath, 'utf8'); return { path: sourcePath, utf8_bytes: Buffer.byteLength(text), sha256: sha(text), text }; });
const base = `You are CORE, a distinct core main for flow cf7879. Root cf7879 remains the primary and you are not a successor. Spirit and Intent records supplied below govern you. Vision is available for consideration only and is not authoritative for CORE. Work as a read-only, bounded first turn: state your runtime identity, restate the authority boundary, and provide readiness to coordinate with the primary and the separate core-checkup worker. Do not create a recursive work loop, deliver messages, deploy, edit files, change network state, or decide actions. Approval-wait is never idle. Checkups use Luna and may only read state; any optional restart is once for one owned failed unit and requires the checkup worker's explicit policy. Return a concise JSON object with runtime_identity, authority_boundary, readiness, and limitations.`;
const manifest = { kind: 'core-bootstrap-source-manifest', core_role: 'distinct-core-main', primary_flow_identifier: 'cf7879', model: 'gpt-6-astra', base_instructions: { utf8_bytes: Buffer.byteLength(base), sha256: sha(base) }, sources: records.map(({ text, ...record }) => record) };

// This ordering is deliberate. Earlier CORE e43002 is preserved as a late-claim
// historical receipt; this procedure applies only to future launches.
export const bootstrapPhasePlan = () => ['thread/start', 'flow-id claim', 'lane creation', 'index registration', 'turn/start readiness'];
const readinessInput = ({ flowIdentifier, laneDirectory }) => JSON.stringify({
  task: 'Establish CORE readiness from supplied authoritative records.',
  flow_identifier: flowIdentifier,
  lane_directory: laneDirectory,
  source_manifest: records.map(({ text, ...record }) => record),
  records,
});

const claimFlow = ({ threadId, flowsRoot }) => {
  const result = spawnSync('flow-id', ['codex', '--flows-root', flowsRoot], { encoding: 'utf8', env: { ...process.env, CODEX_SESSION_ID: threadId } });
  if (result.status !== 0) throw new Error(`flow-id claim failed: ${result.stderr.trim()}`);
  const flowIdentifier = result.stdout.trim();
  if (!/^[0-9a-f]+$/i.test(flowIdentifier)) throw new Error('flow-id returned an invalid Flow identifier');
  return flowIdentifier;
};

const createAndRegisterLane = ({ workspace, flowIdentifier, threadId }) => {
  const laneDirectory = path.join(workspace, 'flows', flowIdentifier);
  if (!fs.statSync(laneDirectory).isDirectory()) throw new Error('flow-id did not create the claimed lane');
  const logPath = path.join(laneDirectory, 'log.md');
  if (!fs.existsSync(logPath)) fs.writeFileSync(logPath, `# CORE flow ${flowIdentifier}\n\nClaimed before the first readiness turn. Thread: \`${threadId}\`. Root primary remains \`cf7879\`.\n`);
  const indexPath = path.join(workspace, 'flows', 'index.md');
  const index = fs.readFileSync(indexPath, 'utf8');
  if (!index.includes(`, ${flowIdentifier},`)) fs.appendFileSync(indexPath, `\ncore, ${flowIdentifier}, DISTINCT CORE main; own lane \`${laneDirectory}\`; actual Codex thread \`${threadId}\`; readiness turn pending.\n`);
  return laneDirectory;
};

export const launch = async ({ workspace = process.cwd() } = {}) => {
  const { createUnixWebSocketTransport } = await import(pathToFileURL('/home/li/wt/primary-5f4fea/tools/codex-app-server-client.mjs').href);
  const t = createUnixWebSocketTransport('/home/li/.codex/app-server-control/app-server-control.sock');
  try {
    await t.request('initialize', { clientInfo: { name: 'core-bootstrap', version: '2' }, capabilities: {} });
    await t.notify('initialized', {});
    const models = await t.request('model/list', {});
    const availableModels = models.data?.map(entry => entry.model) ?? [];
    if (!availableModels.includes('gpt-6-astra')) throw new Error('gpt-6-astra not exposed');
    const started = await t.request('thread/start', { model: 'gpt-6-astra', sandbox: 'read-only', ephemeral: false, baseInstructions: base, developerInstructions: null, cwd: workspace, threadSource: 'subAgentOther' });
    const threadId = started.thread.id;
    const flowIdentifier = claimFlow({ threadId, flowsRoot: path.join(workspace, 'flows') });
    const laneDirectory = createAndRegisterLane({ workspace, flowIdentifier, threadId });
    const turn = await t.request('turn/start', { threadId, input: [{ type: 'text', text: readinessInput({ flowIdentifier, laneDirectory }) }] });
    return { ...manifest, available_models: availableModels, core_thread_identifier: threadId, flow_identifier: flowIdentifier, lane_directory: laneDirectory, core_turn_identifier: turn.turn?.id ?? null, turn_status: turn.turn?.status ?? null, phases: bootstrapPhasePlan() };
  } finally { t.close(); }
};

if (process.argv.includes('--manifest')) console.log(JSON.stringify({ ...manifest, phases: bootstrapPhasePlan() }));
else if (process.argv[1] && new URL(import.meta.url).pathname === process.argv[1]) launch().then(result => console.log(JSON.stringify(result)));
