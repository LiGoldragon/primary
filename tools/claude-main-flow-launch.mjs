#!/usr/bin/env node
/* Start one Claude Code main-flow seat in Herdr: the Claude twin of
   codex-main-flow-launch.mjs.

   node tools/claude-main-flow-launch.mjs --model claude-opus-5-5 --brief FILE
        [--aspect Psyche|Mind|Field] [--workspace /home/li/primary] [--herdr-session default]
        [--herdr-workspace-label LABEL] [--compose-only]

   The session UUID is chosen here, so the Flow ID is claimed before start and
   the canonical title is given as the session's name.  The first prompt is
   Claude's own start argument: the birth skills as slash commands at its head,
   then the brief as their argument.  It is given once and never retried; the
   native transcript proves that one prompt was accepted and main-flow expanded
   as its leading block.  Remote control is on.  CLAUDE_CODE_CHILD_SESSION and
   CLAUDE_JOB_DIR are unset for the seat. */
import {execFileSync} from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {requireModelTitle} from './model-display-name.mjs';
import {canonicalTitleFor} from './native-seat-launch.mjs';
import {pickWorkspace} from './codex-main-flow-launch.mjs';

// Birth skills: main-flow leads, then spirit and what main-flow depends on.
// The harness loads the head command and up to five more from the start argument.
export const BIRTH_SKILLS = ['main-flow', 'spirit', 'psyche', 'psyche-interraction', 'vocabulary', 'edit-coordination'];
export const ASPECTS = ['Psyche', 'Mind', 'Field'];
// Session variables a parent Claude leaves behind; the seat is nobody's child.
export const UNSET_ENV = ['CLAUDE_CODE_CHILD_SESSION', 'CLAUDE_JOB_DIR', 'CLAUDE_CODE_SESSION_KIND', 'CLAUDE_CODE_SESSION_ID', 'CLISESSIONID'];

export function parseArgs(argv) {
  const known = new Set(['--model', '--brief', '--aspect', '--workspace', '--herdr-session', '--herdr-workspace-label']);
  const o = {aspect: 'Psyche', workspace: '/home/li/primary', herdrSession: 'default', herdrWorkspaceLabel: undefined, composeOnly: false};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--compose-only') { o.composeOnly = true; continue; }
    if (!known.has(a) || argv[i + 1] === undefined || argv[i + 1].startsWith('--')) throw new Error(`bad argument: ${a}`);
    o[a.slice(2).replace(/-(\w)/g, (_, c) => c.toUpperCase())] = argv[++i];
  }
  if (!o.model || !o.brief) throw new Error('--model and --brief are required');
  if (!ASPECTS.includes(o.aspect)) throw new Error(`no such aspect: ${o.aspect}`);
  if (!/^claude-/.test(o.model)) throw new Error(`not a Claude model: ${o.model}`);
  requireModelTitle(o.model);
  o.workspace = path.resolve(o.workspace);
  return o;
}

// Every birth skill must exist on main in the Claude tree.
export const mainSkillExists = workspace => name => {
  try { return execFileSync('jj', ['-R', workspace, 'file', 'show', '-r', 'main', `root:.claude/skills/${name}/SKILL.md`], {encoding: 'utf8'}).trim().length > 0; }
  catch { return false; }
};

export function composeFirstPrompt({brief, exists}) {
  for (const name of BIRTH_SKILLS) if (!exists(name)) throw new Error(`skill missing on main: ${name}`);
  if (!brief.trim()) throw new Error('launch brief is empty');
  const prompt = `${BIRTH_SKILLS.map(n => `/${n}`).join(' ')} # Launch brief\n\n${brief.trim()}\n`;
  if (Buffer.byteLength(prompt) >= 120 * 1024) throw new Error('first prompt exceeds one argument (120 KiB)');
  return prompt;
}

export function claimFlow(flowsRoot, sessionId) {
  const id = execFileSync('flow-id', ['claude', '--flows-root', flowsRoot, '--parent-session', sessionId], {encoding: 'utf8'}).trim();
  if (!/^[0-9a-f]{6,}$/.test(id) || !fs.statSync(path.join(flowsRoot, id)).isDirectory()) throw new Error(`flow-id returned no flow directory: ${id}`);
  return id;
}

export const transcriptPath = (workspace, sessionId) =>
  path.join(os.homedir(), '.claude', 'projects', `-${workspace.replace(/^\/+/, '').replaceAll('/', '-')}`, `${sessionId}.jsonl`);

const textOf = r => { const c = r.message?.content; return typeof c === 'string' ? c : (c ?? []).map(x => x.type === 'text' ? x.text : '').join(''); };

// The first prompt as the transcript holds it: the prompt ids of accepted user
// prompts, the commands of the first in order, and the skill bodies expanded.
export function readFirstPrompt(rows) {
  const users = rows.filter(r => r.type === 'user' && !r.isMeta && !(Array.isArray(r.message?.content) && r.message.content.some(x => x.type === 'tool_result')));
  const promptIds = [...new Set(users.map(r => r.promptId ?? r.uuid))];
  const first = promptIds[0];
  const turn = rows.filter(r => r.type === 'user' && (r.promptId ?? r.uuid) === first);
  const commands = turn.map(textOf).flatMap(t => [...t.matchAll(/<command-name>\/([^<]+)<\/command-name>/g)].map(m => m[1]));
  const expanded = turn.filter(r => r.isMeta).map(textOf).flatMap(t => { const m = /^Base directory for this skill: \S*\/skills\/([^\s/]+)/.exec(t); return m ? [m[1]] : []; });
  const args = turn.map(textOf).map(t => /<command-args>([\s\S]*?)<\/command-args>/.exec(t)?.[1]).find(Boolean) ?? '';
  return {promptIds, commands, expanded, args};
}

export function titleRecords(rows, sessionId) {
  return rows.filter(r => (r.type === 'custom-title' || r.type === 'agent-name') && (!r.sessionId || r.sessionId === sessionId)).map(r => r.customTitle ?? r.agentName);
}

const sh = s => `'${s.replaceAll("'", `'\\''`)}'`;
const herdr = (session, ...args) => JSON.parse(execFileSync('herdr', ['--session', session, ...args], {encoding: 'utf8', timeout: 15000})).result;
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function poll(what, seconds, probe) {
  for (let i = 0; i < seconds; i++) { const v = probe(); if (v) return v; await sleep(1000); }
  throw new Error(`timed out waiting for ${what}`);
}
const rows = file => fs.existsSync(file) ? fs.readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap(l => { try { return [JSON.parse(l)]; } catch { return []; } }) : [];

async function launch(o) {
  let step = 'workspace';
  const done = (msg) => console.log(`${step}: ${msg}`);
  try {
    if (!fs.statSync(path.join(o.workspace, '.jj', 'repo')).isDirectory()) throw new Error('not the jj default workspace');
    const atMain = execFileSync('jj', ['-R', o.workspace, 'log', '--no-graph', '-r', 'main & ::@', '-T', 'commit_id'], {encoding: 'utf8'}).trim();
    if (!atMain) throw new Error(`main is not an ancestor of @ in ${o.workspace}`);
    done(`${o.workspace} is the default workspace and holds main`);

    step = 'prompt';
    const prompt = composeFirstPrompt({brief: fs.readFileSync(o.brief, 'utf8'), exists: mainSkillExists(o.workspace)});
    const promptFile = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'claude-main-flow-launch-')), 'first-prompt.md');
    fs.writeFileSync(promptFile, prompt);
    done(`composed ${Buffer.byteLength(prompt)} bytes into ${promptFile}; head ${BIRTH_SKILLS.map(n => `/${n}`).join(' ')}`);

    step = 'flow';
    const sessionId = crypto.randomUUID();
    const flowId = claimFlow(path.join(o.workspace, 'flows'), sessionId);
    const title = canonicalTitleFor(o.aspect, o.model, flowId);
    done(`Flow ID ${flowId} for session ${sessionId}, directory ${path.join(o.workspace, 'flows', flowId)}`);

    step = 'pane';
    const ws = pickWorkspace(herdr(o.herdrSession, 'workspace', 'list').workspaces, o.herdrWorkspaceLabel);
    const created = herdr(o.herdrSession, 'tab', 'create', '--workspace', ws.workspace_id, '--cwd', o.workspace, '--label', `${o.aspect} ${requireModelTitle(o.model)}`, '--no-focus');
    const tabId = created.tab?.tab_id ?? created.tab_id;
    const panes = herdr(o.herdrSession, 'pane', 'list').panes.filter(p => p.tab_id === tabId);
    if (!tabId || panes.length !== 1) throw new Error('new tab has no single pane');
    const paneId = panes[0].pane_id;
    done(`${paneId} in tab ${tabId} of workspace ${ws.workspace_id}, cwd ${o.workspace}`);

    step = 'harness';
    const transcript = transcriptPath(o.workspace, sessionId);
    if (fs.existsSync(transcript)) throw new Error(`transcript already exists: ${transcript}`);
    const unset = UNSET_ENV.map(v => `-u ${v}`).join(' ');
    const command = `cd ${sh(o.workspace)} && exec env ${unset} claude --session-id ${sessionId} --model ${sh(o.model)} --effort medium --name ${sh(title)} --remote-control --dangerously-skip-permissions "$(cat ${sh(promptFile)})"`;
    execFileSync('herdr', ['--session', o.herdrSession, 'pane', 'run', paneId, command], {encoding: 'utf8', timeout: 15000});
    await poll('the native transcript', 120, () => fs.existsSync(transcript));
    done(`claude session ${sessionId}, transcript ${transcript}`);

    step = 'first prompt';
    await poll('the first prompt in the transcript', 120, () => readFirstPrompt(rows(transcript)).expanded.length > 0);
    await sleep(3000);
    const fp = readFirstPrompt(rows(transcript));
    const loaded = `commands [${fp.commands.join(' ')}], expanded [${fp.expanded.join(' ')}], prompts ${fp.promptIds.length}`;
    if (fp.promptIds.length !== 1) throw new Error(`expected one accepted prompt: ${loaded}`);
    if (fp.expanded[0] !== 'main-flow') throw new Error(`main-flow is not the leading block: ${loaded}`);
    if (fp.expanded.join(' ') !== BIRTH_SKILLS.join(' ')) throw new Error(`not every birth skill loaded (nothing is resent): ${loaded}`);
    if (!fp.args.includes('# Launch brief')) throw new Error(`the brief is not the commands' argument: ${loaded}`);
    done(`accepted once; ${loaded}; the brief is the argument`);

    step = 'harness settings';
    const assistant = await poll('the first assistant record', 180, () => rows(transcript).find(r => r.type === 'assistant' && r.message?.model));
    if (assistant.message.model !== o.model) throw new Error(`native model differs: ${assistant.message.model}`);
    done(`model ${assistant.message.model}, effort medium and remote control as started`);

    step = 'title';
    const named = await poll('the session name in the transcript', 60, () => titleRecords(rows(transcript), sessionId).find(t => t === title));
    const terminal = herdr(o.herdrSession, 'pane', 'list').panes.find(p => p.pane_id === paneId)?.terminal_title_stripped;
    done(`read back "${named}"; terminal title "${terminal}"`);

    step = 'herdr agent';
    const name = `${o.aspect}_${requireModelTitle(o.model)}_${flowId}`.toLowerCase().replace(/[^a-z0-9_]/g, '_');
    execFileSync('herdr', ['--session', o.herdrSession, 'pane', 'report-agent-session', paneId, '--source', 'herdr:claude', '--agent', 'claude', '--agent-session-id', sessionId, '--session-start-source', 'claude-main-flow-launch'], {encoding: 'utf8', timeout: 15000});
    herdr(o.herdrSession, 'agent', 'rename', paneId, name);
    await poll('an interactive agent bound to the session', 180, () => {
      const a = herdr(o.herdrSession, 'agent', 'get', name).agent;
      return a?.pane_id === paneId && a.interactive_ready && a.agent_session?.value === sessionId;
    });
    done(`${name} on ${paneId}, agent session ${sessionId}`);

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
    process.stdout.write(composeFirstPrompt({brief: fs.readFileSync(o.brief, 'utf8'), exists: mainSkillExists(o.workspace)}));
  } else await launch(o);
}
