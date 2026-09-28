#!/usr/bin/env node
/* Start one Codex main-flow seat in Herdr, without the Flow Nexus.

   node tools/codex-main-flow-launch.mjs --model gpt-6-astra --brief FILE
        [--aspect Mind|Field] [--workspace /home/li/primary] [--herdr-session default]
        [--herdr-workspace-label LABEL] [--compose-only]

   The seat opens in Herdr's only workspace; the label chooses one only when
   Herdr holds several.

   One line per step; the first failure stops the launch and names its step.
   The first prompt is given once, as Codex's own PROMPT argument, and is never
   retried.  The Flow ID is the native thread's alias, so it is claimed as soon
   as the thread exists, before the title and the registration. */
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {requireModelTitle} from './model-display-name.mjs';
import {canonicalTitleFor, clientForModel, herdrSessionReportArgs, setAndReadNativeTitle, withRpc} from './native-seat-launch.mjs';

// Startup skills per aspect, after main-flow: spirit, then what main-flow depends on.
// Every other skill is loaded through the skill interface when the work calls for it.
export const ASPECT_SKILLS = {
  Mind: ['spirit', 'psyche', 'psyche-interraction', 'vocabulary', 'edit-coordination'],
  Field: ['spirit', 'psyche', 'psyche-interraction', 'vocabulary', 'edit-coordination'],
};

export function parseArgs(argv) {
  const known = new Set(['--model', '--brief', '--aspect', '--workspace', '--herdr-session', '--herdr-workspace-label']);
  const o = {aspect: 'Mind', workspace: '/home/li/primary', herdrSession: 'default', herdrWorkspaceLabel: undefined, composeOnly: false};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--compose-only') { o.composeOnly = true; continue; }
    if (!known.has(a) || argv[i + 1] === undefined || argv[i + 1].startsWith('--')) throw new Error(`bad argument: ${a}`);
    o[a.slice(2).replace(/-(\w)/g, (_, c) => c.toUpperCase())] = argv[++i];
  }
  if (!o.model || !o.brief) throw new Error('--model and --brief are required');
  if (!ASPECT_SKILLS[o.aspect]) throw new Error(`no startup skill set for aspect ${o.aspect}`);
  if (!/^gpt-/.test(o.model)) throw new Error(`not a Codex model: ${o.model}`);
  requireModelTitle(o.model);
  o.workspace = path.resolve(o.workspace);
  return o;
}

// Skill text as it stands on main, from the generated Codex tree.
export const mainSkillReader = workspace => name =>
  execFileSync('jj', ['-R', workspace, 'file', 'show', '-r', 'main', `.agents/skills/${name}/SKILL.md`], {encoding: 'utf8'});

export const skillBlock = (workspace, name, text) =>
  `Base directory for this skill: ${path.join(workspace, '.agents', 'skills', name)}\n\n${text.trim()}\n`;

export function composeFirstPrompt({workspace, aspect, brief, read}) {
  const blocks = ['main-flow', ...ASPECT_SKILLS[aspect]].map(name => {
    const text = read(name);
    if (!text || !text.trim()) throw new Error(`skill missing on main: ${name}`);
    return skillBlock(workspace, name, text);
  });
  if (!brief.trim()) throw new Error('launch brief is empty');
  const prompt = `${blocks.join('\n')}\n# Launch brief\n\n${brief.trim()}\n`;
  if (Buffer.byteLength(prompt) >= 120 * 1024) throw new Error('first prompt exceeds one argument (120 KiB)');
  return {prompt, leading: blocks[0]};
}

export function pickWorkspace(workspaces, label) {
  if (workspaces.length === 1) return workspaces[0];
  if (!label) throw new Error(`Herdr holds ${workspaces.length} workspaces; name one with --herdr-workspace-label`);
  const found = workspaces.filter(w => w.label === label);
  if (found.length !== 1) throw new Error(`expected one Herdr workspace labelled ${label}, found ${found.length}`);
  return found[0];
}

export function claimFlow(flowsRoot, threadId) {
  const id = execFileSync('flow-id', ['codex', '--flows-root', flowsRoot], {encoding: 'utf8', env: {...process.env, CODEX_SESSION_ID: threadId}}).trim();
  if (!/^[0-9a-f]{6,}$/.test(id) || !fs.statSync(path.join(flowsRoot, id)).isDirectory()) throw new Error(`flow-id returned no flow directory: ${id}`);
  return id;
}

const sh = s => `'${s.replaceAll("'", `'\\''`)}'`;
const herdr = (session, ...args) => JSON.parse(execFileSync('herdr', ['--session', session, ...args], {encoding: 'utf8', timeout: 15000})).result;
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function poll(what, seconds, probe) {
  for (let i = 0; i < seconds; i++) { const v = probe(); if (v) return v; await sleep(1000); }
  throw new Error(`timed out waiting for ${what}`);
}
function rolloutFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, {recursive: true}).filter(f => /rollout-.*\.jsonl$/.test(f)).map(f => path.join(dir, f));
}
const rows = file => fs.readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap(l => { try { return [JSON.parse(l)]; } catch { return []; } });

async function launch(o) {
  let step = 'workspace';
  const done = (msg) => console.log(`${step}: ${msg}`);
  try {
    if (!fs.statSync(path.join(o.workspace, '.jj', 'repo')).isDirectory()) throw new Error('not the jj default workspace');
    const atMain = execFileSync('jj', ['-R', o.workspace, 'log', '--no-graph', '-r', 'main & ::@', '-T', 'commit_id'], {encoding: 'utf8'}).trim();
    if (!atMain) throw new Error(`main is not an ancestor of @ in ${o.workspace}`);
    done(`${o.workspace} is the default workspace and holds main`);

    step = 'prompt';
    const {prompt, leading} = composeFirstPrompt({workspace: o.workspace, aspect: o.aspect, brief: fs.readFileSync(o.brief, 'utf8'), read: mainSkillReader(o.workspace)});
    const promptFile = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'codex-main-flow-launch-')), 'first-prompt.md');
    fs.writeFileSync(promptFile, prompt);
    done(`composed ${Buffer.byteLength(prompt)} bytes from main into ${promptFile}`);

    step = 'pane';
    const client = clientForModel(o.model);
    const sessions = path.join(path.dirname(path.dirname(client.endpoint)), 'sessions');
    const ws = [pickWorkspace(herdr(o.herdrSession, 'workspace', 'list').workspaces, o.herdrWorkspaceLabel)];
    const label = `${o.aspect} ${requireModelTitle(o.model)}`;
    const created = herdr(o.herdrSession, 'tab', 'create', '--workspace', ws[0].workspace_id, '--cwd', o.workspace, '--label', label, '--no-focus');
    const tabId = created.tab?.tab_id ?? created.tab_id;
    const panes = herdr(o.herdrSession, 'pane', 'list').panes.filter(p => p.tab_id === tabId);
    if (!tabId || panes.length !== 1) throw new Error('new tab has no single pane');
    const paneId = panes[0].pane_id;
    done(`${paneId} in tab ${tabId} of workspace ${ws[0].workspace_id}, cwd ${o.workspace}`);

    step = 'harness';
    const before = new Set(rolloutFiles(sessions));
    const command = `exec ${client.command} -m ${sh(o.model)} -c 'model_reasoning_effort="medium"' --dangerously-bypass-approvals-and-sandbox -C ${sh(o.workspace)} "$(cat ${sh(promptFile)})"`;
    execFileSync('herdr', ['--session', o.herdrSession, 'pane', 'run', paneId, command], {encoding: 'utf8', timeout: 15000});
    const rollout = await poll('the native rollout', 120, () => {
      const fresh = rolloutFiles(sessions).filter(f => !before.has(f) && rows(f)[0]?.payload?.cwd === o.workspace);
      if (fresh.length > 1) throw new Error('more than one new native thread in this workspace');
      return fresh[0];
    });
    const threadId = rows(rollout)[0].payload.id;
    const ctx = await poll('the first turn context', 120, () => rows(rollout).find(r => r.type === 'turn_context')?.payload);
    if (ctx.model !== o.model || ctx.effort !== 'medium' || ctx.approval_policy !== 'never' || ctx.sandbox_policy?.type !== 'danger-full-access')
      throw new Error(`native settings differ: ${ctx.model} ${ctx.effort} ${ctx.approval_policy} ${ctx.sandbox_policy?.type}`);
    done(`${client.command} thread ${threadId}: ${ctx.model}, effort ${ctx.effort}, approval never, no sandbox`);

    step = 'first prompt';
    const texts = r => (r.type === 'response_item' && r.payload?.role === 'user' ? r.payload.content ?? [] : []).map(c => c.text ?? '');
    await poll('the first prompt in the rollout', 60, () => rows(rollout).flatMap(texts).some(t => t.startsWith(leading)));
    done('accepted once; leading block is main-flow as on main');

    step = 'flow';
    const flowId = claimFlow(path.join(o.workspace, 'flows'), threadId);
    done(`Flow ID ${flowId}, directory ${path.join(o.workspace, 'flows', flowId)}`);

    step = 'title';
    const title = canonicalTitleFor(o.aspect, o.model, flowId);
    const thread = await withRpc(client.endpoint, call => setAndReadNativeTitle(call, threadId, title));
    done(`read back "${thread.name}"`);

    step = 'herdr agent';
    const name = `${o.aspect}_${requireModelTitle(o.model)}_${flowId}`.toLowerCase().replace(/[^a-z0-9_]/g, '_');
    execFileSync('herdr', herdrSessionReportArgs({session: o.herdrSession, paneId}, threadId), {encoding: 'utf8', timeout: 15000});
    herdr(o.herdrSession, 'agent', 'rename', paneId, name);
    await poll('an interactive agent bound to the thread', 120, () => {
      const a = herdr(o.herdrSession, 'agent', 'get', name).agent;
      return a?.pane_id === paneId && a.interactive_ready && a.agent_session?.value === threadId;
    });
    done(`${name} on ${paneId}, agent session ${threadId}`);

    step = 'register';
    done(execFileSync('hm-register', [flowId, name, '--session', o.herdrSession, '--native-thread', threadId], {encoding: 'utf8', timeout: 60000}).trim());
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
    process.stdout.write(composeFirstPrompt({workspace: o.workspace, aspect: o.aspect, brief: fs.readFileSync(o.brief, 'utf8'), read: mainSkillReader(o.workspace)}).prompt);
  } else await launch(o);
}
