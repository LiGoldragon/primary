#!/usr/bin/env node
/* Start one OpenCode main-flow seat in Herdr: the OpenCode twin of
   claude-main-flow-launch.mjs and codex-main-flow-launch.mjs.

   node tools/opencode-main-flow-launch.mjs --model criomos-local/qwen3.6-35b-a3b --brief FILE
        [--aspect Psyche|Mind|Field] [--workspace /home/li/primary] [--herdr-session default]
        [--herdr-workspace-label LABEL] [--flow-id ID] [--opencode EXECUTABLE] [--compose-only]

   The seat runs the `main-flow` agent: its system prompt is the main-flow
   text from tools/main-flow-mode, given as the agent's prompt, which
   replaces OpenCode's own.  The first prompt is OpenCode's own start
   argument: the birth skills from the workspace's generated `.opencode`
   tree, main-flow leading, then the brief.  It is given once and never
   retried; `opencode export` proves that one prompt was accepted under that
   agent and model.  The session is bound to the pane by Herdr's own OpenCode
   plugin, which reports it when it starts; the launcher only reads that
   binding.  Permissions are never asked: the Home configuration allows
   every tool.

   A seat claims its Flow ID from its native session.  `--flow-id` instead
   names a flow the seat carries (a subflow witness of that flow): its
   FLOW_ID and FLOW_DIRECTORY are exported into the seat and it is not
   registered a second time.  `--opencode` names the executable the seat
   runs, by absolute path, where the installed `opencode` is not the one
   wanted (a built Home generation not yet deployed). */
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {requireModelTitle} from './model-display-name.mjs';
import {pickWorkspace} from './native-main-flow-launch-shared.mjs';

export const BIRTH_SKILLS = ['main-flow', 'spirit', 'psyche', 'psyche-interraction', 'vocabulary', 'edit-coordination'];
export const ASPECTS = ['Psyche', 'Mind', 'Field'];
export const AGENT = 'main-flow';
const HERDR_SOURCE = 'herdr:opencode';

export function parseArgs(argv) {
  const known = new Set(['--model', '--brief', '--aspect', '--workspace', '--herdr-session', '--herdr-workspace-label', '--flow-id', '--opencode']);
  const o = {aspect: 'Mind', workspace: '/home/li/primary', herdrSession: 'default', herdrWorkspaceLabel: undefined, flowId: undefined, opencode: 'opencode', composeOnly: false};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--compose-only') { o.composeOnly = true; continue; }
    if (!known.has(a) || argv[i + 1] === undefined || argv[i + 1].startsWith('--')) throw new Error(`bad argument: ${a}`);
    o[a.slice(2).replace(/-(\w)/g, (_, c) => c.toUpperCase())] = argv[++i];
  }
  if (!o.model || !o.brief) throw new Error('--model and --brief are required');
  if (!ASPECTS.includes(o.aspect)) throw new Error(`no such aspect: ${o.aspect}`);
  if (!/^[a-z0-9-]+\/[^/\s]+$/.test(o.model)) throw new Error(`not an OpenCode provider/model reference: ${o.model}`);
  requireModelTitle(o.model);
  if (o.flowId !== undefined && !/^[0-9a-f]{6}$/.test(o.flowId)) throw new Error(`not a short Flow ID: ${o.flowId}`);
  if (o.opencode !== 'opencode' && !path.isAbsolute(o.opencode)) throw new Error(`--opencode must be an absolute path: ${o.opencode}`);
  o.workspace = path.resolve(o.workspace);
  return o;
}

// Skill text is read from the generated OpenCode tree the seat itself reads.
export const skillDirectory = (workspace, name) => path.join(workspace, '.opencode', 'skills', name);
export const liveSkillReader = workspace => name => fs.readFileSync(path.join(skillDirectory(workspace, name), 'SKILL.md'), 'utf8');
export const skillBlock = (workspace, name, text) => `Base directory for this skill: ${skillDirectory(workspace, name)}\n\n${text.trim()}\n`;

export function composeFirstPrompt({workspace, brief, read}) {
  const blocks = BIRTH_SKILLS.map(name => {
    const text = read(name);
    if (!text || !text.trim()) throw new Error(`skill input missing or empty: ${name}`);
    return skillBlock(workspace, name, text);
  });
  if (!brief.trim()) throw new Error('launch brief is empty');
  const prompt = `${blocks.join('\n')}\n# Launch brief\n\n${brief.trim()}\n`;
  if (Buffer.byteLength(prompt) >= 120 * 1024) throw new Error('first prompt exceeds one argument (120 KiB)');
  return {prompt, leading: blocks[0]};
}

// The main-flow mode: the agent whose prompt replaces OpenCode's own.
export function seatConfig(systemPrompt, model) {
  if (!systemPrompt.trim()) throw new Error('main-flow system prompt is empty');
  return {agent: {[AGENT]: {description: 'A main flow seat.', mode: 'primary', model, prompt: systemPrompt}}};
}

const sh = s => `'${String(s).replaceAll("'", `'\\''`)}'`;
export const IDENTITIES = ['CODEX_THREAD_ID', 'CODEX_SESSION_ID', 'CLAUDE_CODE_SESSION_ID', 'CLAUDE_SESSION_ID', 'CLAUDE_CODE_CHILD_SESSION', 'CLAUDE_JOB_DIR', 'THREAD_ID', 'FLOW_ID', 'FLOW_DIRECTORY'];
export function opencodeHarnessCommand(o, config, promptFile, carried) {
  // Herdr's pane and socket variables stay; a parent seat's identity does not.
  const flowEnv = carried ? `FLOW_ID=${sh(carried.flowId)} FLOW_DIRECTORY=${sh(carried.directory)} ` : '';
  return `cd ${sh(o.workspace)} && exec env ${IDENTITIES.map(name => `-u ${name}`).join(' ')} ${flowEnv}OPENCODE_CONFIG_CONTENT=${sh(JSON.stringify(config))} ${sh(o.opencode ?? 'opencode')} --model ${sh(o.model)} --agent ${AGENT} --prompt "$(cat ${sh(promptFile)})"`;
}

// The pane's session as Herdr's OpenCode plugin reported it: OpenCode's own
// `ses_` id, twelve lowercase hex of descending time then fourteen base62, the
// one shape `flow-id opencode` accepts.
export const OPENCODE_SESSION = /^ses_[0-9a-f]{12}[0-9A-Za-z]{14}$/;
export function reportedSession(pane) {
  const session = pane?.agent_session;
  return session?.source === HERDR_SOURCE && OPENCODE_SESSION.test(session.value ?? '') ? session.value : undefined;
}

export function hasExactRegistrationBinding(agent, paneId, sessionId) {
  return agent?.pane_id === paneId && agent.agent_session?.value === sessionId;
}

// The first prompt and the turn that answered it, from `opencode export`.
export function readFirstTurn(exported) {
  const messages = exported?.messages ?? [];
  const users = messages.filter(m => m.info?.role === 'user');
  const assistant = messages.find(m => m.info?.role === 'assistant');
  const text = users[0]?.parts?.filter(p => p.type === 'text').map(p => p.text).join('') ?? '';
  return {prompts: users.length, text, agent: users[0]?.info?.agent, model: assistant ? `${assistant.info.providerID}/${assistant.info.modelID}` : undefined};
}

// The seat's Flow ID, claimed by harness `flow-id opencode` from its session.
export function claimFlow(flowsRoot, sessionId, flowIdExecutable = 'flow-id') {
  const id = execFileSync(flowIdExecutable, ['opencode', '--flows-root', flowsRoot, '--parent-session', sessionId], {encoding: 'utf8'}).trim();
  if (!/^[0-9a-f]{6,}$/.test(id) || !fs.statSync(path.join(flowsRoot, id)).isDirectory()) throw new Error(`flow-id returned no flow directory: ${id}`);
  return id;
}

const herdr = (session, ...args) => JSON.parse(execFileSync('herdr', ['--session', session, ...args], {encoding: 'utf8', timeout: 15000})).result;
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function poll(what, seconds, probe) {
  for (let i = 0; i < seconds; i++) { const v = probe(); if (v) return v; await sleep(1000); }
  throw new Error(`timed out waiting for ${what}`);
}
const exportSession = (opencode, workspace, sessionId) => {
  try { return JSON.parse(execFileSync(opencode, ['export', sessionId], {cwd: workspace, encoding: 'utf8', timeout: 60000, stdio: ['ignore', 'pipe', 'ignore']})); }
  catch { return undefined; }
};

async function launch(o) {
  let step = 'workspace';
  const done = (msg) => console.log(`${step}: ${msg}`);
  try {
    if (!fs.statSync(o.workspace).isDirectory()) throw new Error(`workspace is not a directory: ${o.workspace}`);
    fs.accessSync(o.workspace, fs.constants.R_OK | fs.constants.X_OK);
    const carried = o.flowId ? {flowId: o.flowId, directory: path.join(o.workspace, 'flows', o.flowId)} : undefined;
    if (carried && !fs.statSync(carried.directory).isDirectory()) throw new Error(`carried flow has no directory: ${carried.directory}`);
    done(`${o.workspace} is available${carried ? `; carries flow ${carried.flowId}` : ''}`);

    step = 'prompt';
    const {prompt, leading} = composeFirstPrompt({workspace: o.workspace, brief: fs.readFileSync(o.brief, 'utf8'), read: liveSkillReader(o.workspace)});
    const promptFile = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'opencode-main-flow-launch-')), 'first-prompt.md');
    fs.writeFileSync(promptFile, prompt);
    const systemPromptFile = path.join(o.workspace, 'tools', 'main-flow-mode', 'system-prompt.md');
    const config = seatConfig(fs.readFileSync(systemPromptFile, 'utf8'), o.model);
    done(`composed ${Buffer.byteLength(prompt)} bytes into ${promptFile}; agent ${AGENT} prompt from ${systemPromptFile}`);

    step = 'pane';
    const ws = pickWorkspace(herdr(o.herdrSession, 'workspace', 'list').workspaces, o.herdrWorkspaceLabel);
    const created = herdr(o.herdrSession, 'tab', 'create', '--workspace', ws.workspace_id, '--cwd', o.workspace, '--label', `${o.aspect} ${requireModelTitle(o.model)}`, '--no-focus');
    const tabId = created.tab?.tab_id ?? created.tab_id;
    const panes = herdr(o.herdrSession, 'pane', 'list').panes.filter(p => p.tab_id === tabId);
    if (!tabId || panes.length !== 1) throw new Error('new tab has no single pane');
    const paneId = panes[0].pane_id;
    done(`${paneId} in tab ${tabId} of workspace ${ws.workspace_id}, cwd ${o.workspace}`);

    step = 'harness';
    execFileSync('herdr', ['--session', o.herdrSession, 'pane', 'run', paneId, opencodeHarnessCommand(o, config, promptFile, carried)], {encoding: 'utf8', timeout: 15000});
    const sessionId = await poll('the session Herdr\'s OpenCode plugin reports', 180, () =>
      reportedSession(herdr(o.herdrSession, 'pane', 'list').panes.find(p => p.pane_id === paneId)));
    done(`opencode session ${sessionId}, reported to ${paneId} by ${HERDR_SOURCE}`);

    step = 'first prompt';
    const turn = await poll('the first answered turn in the session export', 1800, () => {
      const t = readFirstTurn(exportSession(o.opencode, o.workspace, sessionId));
      return t.model ? t : undefined;
    });
    if (turn.prompts !== 1) throw new Error(`expected one accepted prompt, found ${turn.prompts}`);
    if (!turn.text.startsWith(leading)) throw new Error('main-flow is not the leading block of the first prompt');
    if (turn.agent !== AGENT) throw new Error(`the first prompt ran under agent ${turn.agent}`);
    if (turn.model !== o.model) throw new Error(`native model differs: ${turn.model}`);
    done(`accepted once; leading block is main-flow from the workspace; agent ${turn.agent}, model ${turn.model}`);

    step = 'flow';
    const flowId = carried ? carried.flowId : claimFlow(path.join(o.workspace, 'flows'), sessionId);
    done(carried ? `carries ${flowId}` : `Flow ID ${flowId}, directory ${path.join(o.workspace, 'flows', flowId)}`);

    step = 'herdr agent';
    const name = `${o.aspect}_${requireModelTitle(o.model)}_${flowId}${carried ? `_${sessionId.slice(-6)}` : ''}`.toLowerCase().replace(/[^a-z0-9_]/g, '_');
    herdr(o.herdrSession, 'agent', 'rename', paneId, name);
    await poll('an agent bound to the session', 120, () => hasExactRegistrationBinding(herdr(o.herdrSession, 'agent', 'get', name).agent, paneId, sessionId));
    done(`${name} on ${paneId}, agent session ${sessionId}`);

    if (carried) return;
    step = 'register';
    done(execFileSync('hm-register', [flowId, name, '--session', o.herdrSession, '--native-thread', sessionId], {encoding: 'utf8', timeout: 60000}).trim());
  } catch (error) {
    console.error(`${step}: FAILED: ${error.message}`);
    process.exit(1);
  }
}

const invokedDirectly = process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname);
if (invokedDirectly) {
  let o;
  try { o = parseArgs(process.argv.slice(2)); } catch (e) { console.error(`arguments: FAILED: ${e.message}`); process.exit(2); }
  if (o.composeOnly) {
    process.stdout.write(composeFirstPrompt({workspace: o.workspace, brief: fs.readFileSync(o.brief, 'utf8'), read: liveSkillReader(o.workspace)}).prompt);
  } else await launch(o);
}
