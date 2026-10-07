#!/usr/bin/env node
/* Start one Claude Code main-flow seat in Herdr: the Claude twin of
   codex-main-flow-launch.mjs.

   node tools/claude-main-flow-launch.mjs --brief FILE --layer LAYER
        [--aspect Psyche|Field] [--layer Primary|Secondary|Tertiary|Quaternary] [--workspace /home/li/primary] [--herdr-session default]
        [--herdr-workspace-label LABEL] [--compose-only]
        [--system-prompt-file FILE] [--effort low|medium|high|xhigh|max]

   The session UUID is chosen here, so the Flow ID is claimed before start and
   the canonical title is given as the session's name. Claude accepts only a
   bounded number of slash commands in one prompt, so resolved skills are
   injected through its native slash-command interface in bounded prompts.
   The launch brief is sent once, after the transcript proves every selected
   skill body was loaded exactly once. Remote control is on.
   CLAUDE_CODE_CHILD_SESSION and
   CLAUDE_JOB_DIR are unset for the seat.  As every main seat, it starts with
   the main-flow text as its system prompt (--system-prompt-file) and with the
   settings whose hook adds the main-flow reminder to the living's prompts
   (--settings), both from tools/main-flow-mode in the workspace; the settings
   are written to the session's job directory under ~/.claude/jobs.
   --system-prompt-file names another system prompt (a path, relative to the
   current directory) in place of tools/main-flow-mode/system-prompt.md; the
   reminder hook then re-adds that file.  --effort defaults to medium. */
import {execFileSync} from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {requireModelTitle} from './model-display-name.mjs';
import {selectVoiceProfile} from './native-voice-profiles.mjs';
import {canonicalTitleFor, orderSkillsForPrompt, pickWorkspace, resolveSkillDependencies} from './native-main-flow-launch-shared.mjs';
import {STANDING_SKILLS} from './standing-skill-selection.mjs';

// Roots are expanded by Curriculum at launch; prompt composition keeps
// operation-main-flow first.
// Claude expands at most six skill commands from one prompt.
export const MAX_SKILLS_PER_PROMPT = 6;
const STARTUP_INSTRUCTION = 'Startup context only: load these skills for the upcoming launch brief. Do not begin that work or write files yet. Reply exactly READY.';
export const BIRTH_SKILLS = [...new Set(['operation-main-flow', ...STANDING_SKILLS, 'knowledge-psyche', 'operation-psyche-interraction', 'knowledge-vocabulary', 'operation-edit-coordination'])];
// Mind runs on Codex only (living ruling 2026-10-05, flows/bfdae1/log.md):
// no Mind seat, at any layer, is launched on Claude.
export const ASPECTS = ['Psyche', 'Field'];
export const LAYERS = ['Primary', 'Secondary', 'Tertiary', 'Quaternary'];
export const EFFORTS = ['low', 'medium', 'high', 'xhigh', 'max'];

// Registration binds the exact native session to the exact Herdr pane.  It
// does not depend on a separate readiness or idleness assertion.
export function hasExactRegistrationBinding(agent, paneId, sessionId) {
  return agent?.pane_id === paneId && agent.agent_session?.value === sessionId;
}

// Session variables a parent Claude leaves behind; the seat is nobody's child.
const sh = s => `'${s.replaceAll("'", `'\\''`)}'`;
export const UNSET_ENV = ['CLAUDE_CODE_CHILD_SESSION', 'CLAUDE_JOB_DIR', 'CLAUDE_CODE_SESSION_KIND', 'CLAUDE_CODE_SESSION_ID', 'CLISESSIONID'];

const SONNET_5_5 = 'claude-sonnet-5-5';
const SONNET_5_5_MINIMUM_CLAUDE_CODE = [2, 1, 284];

export function claudeCodeVersion(versionOutput) {
  const match = /(?:^|\s)(\d+)\.(\d+)\.(\d+)(?:\s|$)/.exec(versionOutput.trim());
  if (!match) throw new Error(`could not read Claude Code version: ${versionOutput.trim()}`);
  return match.slice(1).map(Number);
}

const isOlderThan = (version, minimum) => {
  for (let index = 0; index < minimum.length; index++) {
    if (version[index] !== minimum[index]) return version[index] < minimum[index];
  }
  return false;
};

export function preflightModel(model, readVersion = () => execFileSync('claude', ['--version'], {encoding: 'utf8'})) {
  if (model !== SONNET_5_5) return;
  const installed = claudeCodeVersion(readVersion());
  if (isOlderThan(installed, SONNET_5_5_MINIMUM_CLAUDE_CODE)) {
    throw new Error(`${SONNET_5_5} requires Claude Code ${SONNET_5_5_MINIMUM_CLAUDE_CODE.join('.')} or later; installed ${installed.join('.')}`);
  }
}

export function parseArgs(argv) {
  const known = new Set(['--model', '--brief', '--aspect', '--layer', '--workspace', '--herdr-session', '--herdr-workspace-label', '--system-prompt-file', '--effort']);
  const o = {aspect: 'Psyche', effort: undefined, model: undefined, workspace: '/home/li/primary', herdrSession: 'default', herdrWorkspaceLabel: undefined, composeOnly: false, systemPromptFile: undefined};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--compose-only') { o.composeOnly = true; continue; }
    if (!known.has(a) || argv[i + 1] === undefined || argv[i + 1].startsWith('--')) throw new Error(`bad argument: ${a}`);
    o[a.slice(2).replace(/-(\w)/g, (_, c) => c.toUpperCase())] = argv[++i];
  }
  if (!o.brief) throw new Error('--brief is required');
  if (o.aspect === 'Mind') throw new Error('Mind runs on Codex only; launch it with codex-main-flow-launch.mjs');
  if (!ASPECTS.includes(o.aspect)) throw new Error(`no such aspect: ${o.aspect}`);
  if (o.layer !== undefined && !LAYERS.includes(o.layer)) throw new Error(`no additive layer: ${o.layer}`);
  if (o.model !== undefined && !/^claude-/.test(o.model)) throw new Error(`not a Claude model: ${o.model}`);
  if (o.model !== undefined) requireModelTitle(o.model);
  if (o.effort !== undefined && !EFFORTS.includes(o.effort)) throw new Error(`no such effort: ${o.effort}`);
  if (o.systemPromptFile !== undefined) o.systemPromptFile = path.resolve(o.systemPromptFile);
  o.workspace = path.resolve(o.workspace);
  return o;
}

// Birth skills are the files Claude will receive from this workspace now.
export const liveSkillExists = workspace => name => {
  try { return fs.readFileSync(path.join(workspace, '.claude', 'skills', name, 'SKILL.md'), 'utf8').trim().length > 0; }
  catch { return false; }
};

export const liveSkillReader = workspace => name =>
  fs.readFileSync(path.join(workspace, '.claude', 'skills', name, 'SKILL.md'), 'utf8');

export function composeSkillPrompt({skillNames, exists}) {
  if (!Array.isArray(skillNames) || skillNames.length === 0 || skillNames.length > MAX_SKILLS_PER_PROMPT) throw new Error(`one Claude prompt must contain between one and ${MAX_SKILLS_PER_PROMPT} skills`);
  if (new Set(skillNames).size !== skillNames.length) throw new Error('Claude skill prompt contains duplicate names');
  for (const name of skillNames) if (!exists(name)) throw new Error(`skill input missing or empty: ${name}`);
  return `${skillNames.map(n => `/${n}`).join(' ')} # Startup skills\n\n${STARTUP_INSTRUCTION}\n`;
}

export function composeFirstPrompt({brief, exists, skillNames = BIRTH_SKILLS}) {
  if (!Array.isArray(skillNames) || skillNames.length === 0) throw new Error('resolved skill closure is empty');
  if (new Set(skillNames).size !== skillNames.length) throw new Error('resolved skill closure contains duplicates');
  if (skillNames[0] !== 'operation-main-flow') throw new Error('operation-main-flow must lead the resolved skill closure');
  for (const name of skillNames) if (!exists(name)) throw new Error(`skill input missing or empty: ${name}`);
  if (!brief.trim()) throw new Error('launch brief is empty');
  const skillPrompts = [];
  for (let offset = 0; offset < skillNames.length; offset += MAX_SKILLS_PER_PROMPT) {
    skillPrompts.push(composeSkillPrompt({skillNames: skillNames.slice(offset, offset + MAX_SKILLS_PER_PROMPT), exists}));
  }
  const prompt = `${brief.trim()}\n`;
  if (Buffer.byteLength(prompt) >= 120 * 1024) throw new Error('launch brief exceeds one argument (120 KiB)');
  return {skillPrompts, prompt};
}

// The main-flow mode a main seat starts in: the replacing system prompt, and the
// settings whose UserPromptSubmit hook re-adds the main-flow core.  The hook's
// count lives in the job directory; CLAUDE_JOB_DIR is unset, so it is named.
export function mainFlowMode(workspace, sessionId, home = os.homedir(), systemPromptFile = undefined) {
  const modeDir = path.join(workspace, 'tools', 'main-flow-mode');
  const promptFile = systemPromptFile ?? path.join(modeDir, 'system-prompt.md');
  const jobDir = path.join(home, '.claude', 'jobs', `native-${sessionId}`);
  const hook = ['python3', sh(path.join(modeDir, 'reminder-hook.py')), '--prompt-file', sh(promptFile),
    '--state-dir', sh(path.join(jobDir, 'main-flow-reminder')), '--every', '20'].join(' ');
  const settings = {hooks: {UserPromptSubmit: [{hooks: [{type: 'command', command: hook, timeout: 10}]}]}};
  return {promptFile, settingsFile: path.join(jobDir, 'main-flow-settings.json'), settings};
}

export function writeMainFlowMode(mode) {
  if (!fs.statSync(mode.promptFile).isFile() || !fs.readFileSync(mode.promptFile, 'utf8').trim()) throw new Error(`main-flow system prompt missing or empty: ${mode.promptFile}`);
  fs.mkdirSync(path.dirname(mode.settingsFile), {recursive: true, mode: 0o700});
  fs.writeFileSync(mode.settingsFile, `${JSON.stringify(mode.settings, null, 2)}\n`, {flag: 'wx', mode: 0o600});
}

export function claimFlow(flowsRoot, sessionId) {
  const id = execFileSync('flow-id', ['claude', '--flows-root', flowsRoot, '--parent-session', sessionId], {encoding: 'utf8'}).trim();
  if (!/^[0-9a-f]{6,}$/.test(id) || !fs.statSync(path.join(flowsRoot, id)).isDirectory()) throw new Error(`flow-id returned no flow directory: ${id}`);
  return id;
}

export const transcriptPath = (workspace, sessionId) =>
  path.join(os.homedir(), '.claude', 'projects', `-${workspace.replace(/^\/+/, '').replaceAll('/', '-')}`, `${sessionId}.jsonl`);

const textOf = r => { const c = r.message?.content; return typeof c === 'string' ? c : (c ?? []).map(x => x.type === 'text' ? x.text : '').join(''); };

const withoutFrontmatter = text => text.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '').trim();

export function readLoadedSkillBlocks(rows, workspace) {
  const skillRoot = `${path.join(workspace, '.claude', 'skills')}${path.sep}`;
  return rows.filter(r => r.type === 'user' && r.isMeta).flatMap(row => {
    const text = textOf(row);
    const match = /^Base directory for this skill: ([^\r\n]+)\r?\n\r?\n([\s\S]*)$/.exec(text);
    if (!match) return [];
    if (!match[1].startsWith(skillRoot)) return [];
    const name = match[1].slice(skillRoot.length);
    if (!/^[A-Za-z0-9_-]+$/.test(name)) throw new Error(`invalid skill path in Claude transcript: ${match[1]}`);
    let body = match[2];
    const args = body.indexOf('\n\nARGUMENTS:');
    if (args !== -1) body = body.slice(0, args);
    return [{name, body: withoutFrontmatter(body), promptId: row.promptId ?? row.uuid}];
  });
}

export function validateLoadedSkillBlocks(blocks, skillNames, read) {
  if (blocks.length > skillNames.length) throw new Error(`Claude loaded more skill blocks than selected: ${blocks.map(b => b.name).join(' ')}`);
  const seen = new Set();
  for (let index = 0; index < blocks.length; index++) {
    const {name, body} = blocks[index];
    if (seen.has(name)) throw new Error(`Claude loaded a skill more than once: ${name}`);
    seen.add(name);
    if (name !== skillNames[index]) throw new Error(`Claude skill order differs at ${index}: expected ${skillNames[index]}, got ${name}`);
    const expected = withoutFrontmatter(read(name));
    if (body !== expected) throw new Error(`Claude loaded skill body differs from the generated input: ${name}`);
  }
  return blocks.length;
}

export function readUserPrompts(rows) {
  return rows.filter(r => r.type === 'user' && !r.isMeta && !(Array.isArray(r.message?.content) && r.message.content.some(x => x.type === 'tool_result')))
    .map(row => ({id: row.promptId ?? row.uuid, text: textOf(row)}));
}

export const assistantResponses = rows => rows.filter(r => r.type === 'assistant' && r.message?.model);

export function hasCompletedResponseAfter(rows, previousCount) {
  const responses = assistantResponses(rows);
  return responses.length > previousCount && responses.at(-1).message?.stop_reason === 'end_turn';
}

export function titleRecords(rows, sessionId) {
  return rows.filter(r => (r.type === 'custom-title' || r.type === 'agent-name') && (!r.sessionId || r.sessionId === sessionId)).map(r => r.customTitle ?? r.agentName);
}

const herdr = (session, ...args) => JSON.parse(execFileSync('herdr', ['--session', session, ...args], {encoding: 'utf8', timeout: 15000})).result;
const submitPrompt = (session, paneId, prompt) => {
  execFileSync('herdr', ['--session', session, 'pane', 'send-text', paneId, prompt.trimEnd()], {encoding: 'utf8', timeout: 15000});
  execFileSync('herdr', ['--session', session, 'pane', 'send-keys', paneId, 'Enter'], {encoding: 'utf8', timeout: 15000});
};
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function poll(what, seconds, probe) {
  for (let i = 0; i < seconds; i++) { const v = probe(); if (v) return v; await sleep(1000); }
  throw new Error(`timed out waiting for ${what}`);
}
const rows = file => fs.existsSync(file) ? fs.readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap(l => { try { return [JSON.parse(l)]; } catch { return []; } }) : [];

async function launch(o) {
  let step = 'preflight';
  const done = (msg) => console.log(`${step}: ${msg}`);
  try {
    const profile = selectVoiceProfile({aspect: o.aspect, layer: o.layer, harness: 'claude', model: o.model, effort: o.effort});
    o = {...o, model: profile.model, effort: profile.effort};
    preflightModel(o.model);

    step = 'workspace';
    if (!fs.statSync(o.workspace).isDirectory()) throw new Error(`workspace is not a directory: ${o.workspace}`);
    fs.accessSync(o.workspace, fs.constants.R_OK | fs.constants.X_OK);
    done(`${o.workspace} is available`);

    step = 'prompt';
    const skillNames = orderSkillsForPrompt(resolveSkillDependencies(BIRTH_SKILLS));
    const composition = composeFirstPrompt({brief: fs.readFileSync(o.brief, 'utf8'), exists: liveSkillExists(o.workspace), skillNames});
    const firstSkillPrompt = composition.skillPrompts[0];
    const promptFile = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'claude-main-flow-launch-')), 'first-skill-prompt.md');
    fs.writeFileSync(promptFile, firstSkillPrompt);
    done(`composed ${skillNames.length} selected skills into ${composition.skillPrompts.length} native prompt batches; main-flow leads`);

    step = 'flow';
    const sessionId = crypto.randomUUID();
    const flowId = claimFlow(path.join(o.workspace, 'flows'), sessionId);
    const title = canonicalTitleFor(o.aspect, o.model, flowId, o.layer);
    done(`Flow ID ${flowId} for session ${sessionId}, directory ${path.join(o.workspace, 'flows', flowId)}`);

    step = 'pane';
    const ws = pickWorkspace(herdr(o.herdrSession, 'workspace', 'list').workspaces, o.herdrWorkspaceLabel);
    const created = herdr(o.herdrSession, 'tab', 'create', '--workspace', ws.workspace_id, '--cwd', o.workspace, '--label', o.layer ? `${o.aspect} ${o.layer}` : `${o.aspect} ${requireModelTitle(o.model)}`, '--no-focus');
    const tabId = created.tab?.tab_id ?? created.tab_id;
    const panes = herdr(o.herdrSession, 'pane', 'list').panes.filter(p => p.tab_id === tabId);
    if (!tabId || panes.length !== 1) throw new Error('new tab has no single pane');
    const paneId = panes[0].pane_id;
    done(`${paneId} in tab ${tabId} of workspace ${ws.workspace_id}, cwd ${o.workspace}`);

    step = 'harness';
    const transcript = transcriptPath(o.workspace, sessionId);
    if (fs.existsSync(transcript)) throw new Error(`transcript already exists: ${transcript}`);
    const mode = mainFlowMode(o.workspace, sessionId, os.homedir(), o.systemPromptFile);
    writeMainFlowMode(mode);
    const unset = UNSET_ENV.map(v => `-u ${v}`).join(' ');
    const command = `cd ${sh(o.workspace)} && exec env ${unset} claude --session-id ${sessionId} --model ${sh(o.model)} --effort ${sh(o.effort)} --name ${sh(title)} --remote-control --dangerously-skip-permissions --system-prompt-file ${sh(mode.promptFile)} --settings ${sh(mode.settingsFile)} "$(cat ${sh(promptFile)})"`;
    execFileSync('herdr', ['--session', o.herdrSession, 'pane', 'run', paneId, command], {encoding: 'utf8', timeout: 15000});
    await poll('the native transcript', 120, () => fs.existsSync(transcript));
    done(`claude session ${sessionId}, transcript ${transcript}; system prompt ${mode.promptFile}, settings ${mode.settingsFile}`);

    step = 'skill loading';
    let transcriptRows = await poll('the first native skill body', 120, () => {
      const current = rows(transcript);
      return readLoadedSkillBlocks(current, o.workspace).length ? current : null;
    });
    let loadedCount = validateLoadedSkillBlocks(readLoadedSkillBlocks(transcriptRows, o.workspace), skillNames, liveSkillReader(o.workspace));
    await poll('the first startup response', 180, () => {
      transcriptRows = rows(transcript);
      return hasCompletedResponseAfter(transcriptRows, 0) ? transcriptRows : null;
    });
    let responseCount = assistantResponses(transcriptRows).length;

    while (loadedCount < skillNames.length) {
      const nextSkills = skillNames.slice(loadedCount, loadedCount + MAX_SKILLS_PER_PROMPT);
      const startupPrompt = composeSkillPrompt({skillNames: nextSkills, exists: liveSkillExists(o.workspace)});
      submitPrompt(o.herdrSession, paneId, startupPrompt);
      const previousResponses = responseCount;
      transcriptRows = await poll(`skills ${nextSkills.join(' ')}`, 180, () => {
        const current = rows(transcript);
        const count = validateLoadedSkillBlocks(readLoadedSkillBlocks(current, o.workspace), skillNames, liveSkillReader(o.workspace));
        return count > loadedCount && hasCompletedResponseAfter(current, previousResponses) ? current : null;
      });
      loadedCount = validateLoadedSkillBlocks(readLoadedSkillBlocks(transcriptRows, o.workspace), skillNames, liveSkillReader(o.workspace));
      responseCount = assistantResponses(transcriptRows).length;
    }
    if (loadedCount !== skillNames.length) throw new Error(`expected ${skillNames.length} selected skill bodies, got ${loadedCount}`);
    done(`native transcript contains all ${loadedCount} selected skill bodies once, in resolver order`);

    step = 'launch brief';
    const previousResponses = responseCount;
    submitPrompt(o.herdrSession, paneId, composition.prompt);
    transcriptRows = await poll('the one launch brief and its response', 180, () => {
      const current = rows(transcript);
      const exactBriefs = readUserPrompts(current).filter(prompt => prompt.text.trim() === composition.prompt.trim());
      return exactBriefs.length === 1 && hasCompletedResponseAfter(current, previousResponses) ? current : null;
    });
    const exactBriefs = readUserPrompts(transcriptRows).filter(prompt => prompt.text.trim() === composition.prompt.trim());
    if (exactBriefs.length !== 1) throw new Error(`expected the launch brief once, found ${exactBriefs.length}`);
    done(`launch brief accepted once after ${loadedCount} verified skill bodies`);

    step = 'harness settings';
    const assistant = assistantResponses(transcriptRows).at(-1);
    if (assistant.message.model !== o.model) throw new Error(`native model differs: ${assistant.message.model}`);
    if (assistant.effort !== o.effort || assistant.perTurnEffort !== o.effort) throw new Error(`native effort differs: ${assistant.effort ?? assistant.perTurnEffort}`);
    done(`model ${assistant.message.model}, effort ${o.effort} and remote control as started`);

    step = 'title';
    const named = await poll('the session name in the transcript', 60, () => titleRecords(rows(transcript), sessionId).find(t => t === title));
    const terminal = herdr(o.herdrSession, 'pane', 'list').panes.find(p => p.pane_id === paneId)?.terminal_title_stripped;
    if (terminal !== title) throw new Error(`Herdr terminal title differs: ${terminal}`);
    done(`read back "${named}"; terminal title "${terminal}"`);

    step = 'herdr agent';
    const name = (o.layer ? `${o.aspect}_${o.layer}_${flowId}` : `${o.aspect}_${requireModelTitle(o.model)}_${flowId}`).toLowerCase().replace(/[^a-z0-9_]/g, '_');
    execFileSync('herdr', ['--session', o.herdrSession, 'pane', 'report-agent-session', paneId, '--source', 'herdr:claude', '--agent', 'claude', '--agent-session-id', sessionId, '--session-start-source', 'claude-main-flow-launch'], {encoding: 'utf8', timeout: 15000});
    herdr(o.herdrSession, 'agent', 'rename', paneId, name);
    await poll('an agent bound to the session', 180, () => {
      const a = herdr(o.herdrSession, 'agent', 'get', name).agent;
      return hasExactRegistrationBinding(a, paneId, sessionId);
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
    const skillNames = orderSkillsForPrompt(resolveSkillDependencies(BIRTH_SKILLS));
    const composition = composeFirstPrompt({brief: fs.readFileSync(o.brief, 'utf8'), exists: liveSkillExists(o.workspace), skillNames});
    process.stdout.write(`${composition.skillPrompts.map((prompt, i) => `# Skill batch ${i + 1}\n${prompt}`).join('\n')}\n# Launch brief\n${composition.prompt}`);
  } else await launch(o);
}
