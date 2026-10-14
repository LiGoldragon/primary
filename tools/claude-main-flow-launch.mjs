#!/usr/bin/env node
/* Start one Claude Code main-flow seat in Herdr: the Claude twin of
   codex-main-flow-launch.mjs.

   node tools/claude-main-flow-launch.mjs --brief FILE --layer LAYER (--root --metaflow FILE [--topic Topic] | --predecessor FLOW_ID)
        [--aspect Psyche|Field] [--layer Primary|Secondary|Tertiary|Quaternary] [--workspace /home/li/primary] [--herdr-session default]
        [--herdr-workspace-label LABEL] [--compose-only]
        [--system-prompt-file FILE] [--effort low|medium|high|xhigh|max]

   A flow is aspect + topic + layer. --topic is a dense PascalCase name
   (Ethos, Nexus); without it a root flow's topic is Core. The topic is
   stored in the continuation record, so a --predecessor launch inherits it,
   and it stands between aspect and layer in the title unless it is Core.
   The session UUID is chosen here, so the Flow ID is claimed before start and
   the canonical title is given as the session's name. Claude accepts only a
   bounded number of slash commands in one prompt, so resolved skills are
   injected through its native slash-command interface in bounded prompts.
   The launch brief is sent once, after the transcript proves every selected
   skill body was loaded exactly once. Remote control is on.
   CLAUDE_CODE_CHILD_SESSION and
   CLAUDE_JOB_DIR are unset for the seat.  As every main seat, it starts with
   the main-flow core and selected system modules as its system prompt (--system-prompt-file) and with the
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
import {secondaryBeforePrimary} from './secondary-first.mjs';
import {selectVoiceProfile} from './native-voice-profiles.mjs';
import {canonicalTitleFor, nativeAgentName, continuationForLaunch, requireTopic, writeContinuationRecord, orderSkillsForPrompt, pickWorkspace, resolveSkillDependencies} from './native-main-flow-launch-shared.mjs';
import {composeSpiritSystemPrompt, mainSystemModules} from './main-flow-mode/spirit-system-prompt.mjs';
import {STANDING_SKILLS} from './standing-skill-selection.mjs';
import {defaultLaunchConfig, birthSkillsFromConfig, metaflowFor, firstPromptFromConfig} from './main-flow-mode/launch-config.mjs';
import {makeContextRefreshBinding} from './main-flow-mode/context-refresh.mjs';

// Roots are expanded by Curriculum at launch; prompt composition keeps
// compensation-main-flow first.
// Claude expands at most six skill commands from one prompt.
export const MAX_SKILLS_PER_PROMPT = 6;
export const LAUNCH_CONFIG = defaultLaunchConfig();
export const BIRTH_SKILLS = birthSkillsFromConfig(LAUNCH_CONFIG);
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
  const known = new Set(['--model', '--brief', '--aspect', '--layer', '--workspace', '--herdr-session', '--herdr-workspace-label', '--system-prompt-file', '--effort', '--predecessor', '--metaflow', '--topic']);
  const o = {aspect: 'Psyche', effort: undefined, model: undefined, workspace: '/home/li/primary', herdrSession: 'default', herdrWorkspaceLabel: undefined, composeOnly: false, systemPromptFile: undefined, root: false, predecessor: undefined, metaflow: undefined, topic: undefined};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--compose-only') { o.composeOnly = true; continue; }
    if (a === '--root') { o.root = true; continue; }
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
  if (!o.composeOnly && o.layer === undefined) throw new Error('--layer is required for a native voice launch');
  if (!o.composeOnly && o.root === Boolean(o.predecessor)) throw new Error('choose exactly one of --root or --predecessor');
  if (!o.composeOnly && o.root && !o.metaflow) throw new Error('--root requires --metaflow');
  if (!o.composeOnly && !o.root && o.metaflow) throw new Error('--metaflow is only valid with --root');
  if (o.topic !== undefined) requireTopic(o.topic);
  if (!o.composeOnly && !o.root && o.topic !== undefined) throw new Error('--topic is only valid with --root; a continuation inherits its topic');
  if (o.metaflow !== undefined) o.metaflow = path.resolve(o.metaflow);
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
  return `${skillNames.map(n => `/${n}`).join(' ')}\n`;
}

export function composeFirstPrompt({brief, exists, launchConfig = LAUNCH_CONFIG, metaflowConfig = metaflowFor(launchConfig, {aspect: 'Psyche', topic: 'Core', layer: 'Primary'}), skillNames = BIRTH_SKILLS.filter(name => !name.startsWith('intent-'))}) {
  if (!Array.isArray(skillNames) || skillNames.length === 0) throw new Error('resolved skill closure is empty');
  if (new Set(skillNames).size !== skillNames.length) throw new Error('resolved skill closure contains duplicates');
  if (skillNames.some(name => name === 'spirit' || name.startsWith('spirit-') || name.startsWith('intent-'))) throw new Error('startup spirit and intent modules belong only in the main system prompt');
  if (skillNames[0] !== 'compensation-main-flow') throw new Error('compensation-main-flow must lead the resolved skill closure');
  for (const name of skillNames) if (!exists(name)) throw new Error(`skill input missing or empty: ${name}`);
  if (!brief.trim()) throw new Error('launch brief is empty');
  const modules = composeSkillPrompt({skillNames, exists});
  const prompt = firstPromptFromConfig(launchConfig, metaflowConfig, {modules, handover: brief});
  if (Buffer.byteLength(prompt) >= 120 * 1024) throw new Error('launch brief exceeds one argument (120 KiB)');
  return {prompt};
}

// The main-flow mode a main seat starts in: the replacing system prompt, and the
// settings whose UserPromptSubmit hook re-adds the main-flow core.  The hook's
// count lives in the job directory; CLAUDE_JOB_DIR is unset, so it is named.
export function mainFlowMode(workspace, sessionId, home = os.homedir(), systemPromptFile = undefined, seat = {}, committer = undefined) {
  const modeDir = path.join(workspace, 'tools', 'main-flow-mode');
  const promptFile = systemPromptFile ?? path.join(modeDir, 'system-prompt.md');
  const jobDir = path.join(home, '.claude', 'jobs', `native-${sessionId}`);
  const hook = ['python3', sh(path.join(modeDir, 'reminder-hook.py')), '--prompt-file', sh(promptFile),
    '--state-dir', sh(path.join(jobDir, 'main-flow-reminder')), '--every', '20'].join(' ');
  const settings = {hooks: {UserPromptSubmit: [{hooks: [{type: 'command', command: hook, timeout: 10}]}]}};
  // Field supplies the actual standing seat only after the approved cutover.
  if (committer !== undefined) {
    if (!/^[a-f0-9]{6,64}$/.test(committer)) throw new Error('invalid standing committer FLOW_ID');
    const notify = [sh(process.execPath), sh(path.join(workspace, 'tools', 'primary-committer', 'turn-end.mjs')), '--primary', sh(workspace), '--committer', sh(committer)].join(' ');
    settings.hooks.Stop = [{hooks: [{type: 'command', command: notify, timeout: 20}]}];
  }
  const refresh = [sh(process.execPath), sh(path.join(workspace, 'tools', 'context-refresh-hook.mjs')), '--config', sh(seat.refreshConfigPath ?? path.join(workspace, 'config', 'context-refresh.json'))].join(' ');
  settings.hooks.Stop = [...(settings.hooks.Stop ?? []), {hooks: [{type: 'command', command: refresh, timeout: 30}]}];
  return {seat, sourcePromptFile: promptFile, workspace, promptFile: path.join(jobDir, 'main-flow-system-prompt.md'), settingsFile: path.join(jobDir, 'main-flow-settings.json'), settings};
}

export function claudeFlowEnvironment(flowId) {
  if (!/^[a-f0-9]{6,64}$/.test(flowId ?? '')) throw new Error('actual claimed FLOW_ID required before harness exec');
  return `${UNSET_ENV.map(v => `-u ${v}`).join(' ')} FLOW_ID=${sh(flowId)}`;
}

export function writeMainFlowMode(mode) {
  if (!fs.statSync(mode.sourcePromptFile).isFile() || !fs.readFileSync(mode.sourcePromptFile, 'utf8').trim()) throw new Error(`main-flow system prompt missing or empty: ${mode.promptFile}`);
  fs.mkdirSync(path.dirname(mode.settingsFile), {recursive: true, mode: 0o700});
  const base = fs.readFileSync(mode.sourcePromptFile, 'utf8');
  const prompt = mode.seat?.aspect && mode.seat?.layer
    ? composeSpiritSystemPrompt(base, mainSystemModules(mode.workspace, '.claude', mode.seat))
    : base;
  fs.writeFileSync(mode.promptFile, prompt, {flag: 'wx', mode: 0o600});
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
  const prompts = [];
  const commands = new Map();
  for (const row of rows.filter(r => r.type === 'user' && !r.isMeta && !(Array.isArray(r.message?.content) && r.message.content.some(x => x.type === 'tool_result')))) {
      const text = textOf(row);
      // Herdr's native paste can wrap one complete prompt. Require a whole
      // wrapper with the same hexadecimal identifier; never match a substring.
      const pasted = /^\s*<pasted_content id="([a-fA-F0-9]+)">\r?\n([\s\S]*)\r?\n<\/pasted_content id="\1">\s*$/.exec(text);
      const command = /^<command-message>([A-Za-z0-9_-]+)<\/command-message>\n<command-name>\/\1<\/command-name>\n<command-args>([\s\S]*)<\/command-args>$/.exec(text);
      if (command && row.promptId) {
        let group = commands.get(row.promptId);
        if (!group) {
          group = {id: row.promptId, text: command[2], commands: []};
          commands.set(row.promptId, group);
          prompts.push(group);
        }
        if (group.text !== command[2]) throw new Error('native command arguments differ within one prompt');
        group.commands.push(command[1]);
      } else prompts.push({id: row.promptId ?? row.uuid, text: pasted ? pasted[2] : text});
  }
  return prompts;
}

export function matchesFirstPrompt(receipt, prompt, skillNames) {
  if (!receipt.commands) return receipt.text.trim() === prompt.trim();
  const prefix = skillNames.map(name => `/${name}`).join(' ');
  return receipt.commands.length === skillNames.length && receipt.commands.every((name, index) => name === skillNames[index]) &&
    prompt.startsWith(prefix) && receipt.text.trim() === prompt.slice(prefix.length).trim();
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
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function poll(what, seconds, probe) {
  for (let i = 0; i < seconds; i++) { const v = probe(); if (v) return v; await sleep(1000); }
  throw new Error(`timed out waiting for ${what}`);
}
const rows = file => fs.existsSync(file) ? fs.readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap(l => { try { return [JSON.parse(l)]; } catch { return []; } }) : [];

async function launch(o) {
  let releaseDependency = () => {};
  let step = 'preflight';
  const done = (msg) => console.log(`${step}: ${msg}`);
  try {
    const profile = selectVoiceProfile({aspect: o.aspect, layer: o.layer, harness: 'claude', model: o.model, effort: o.effort});
    o = {...o, model: profile.model, effort: profile.effort};
    preflightModel(o.model);
    const flowsRoot = path.join(o.workspace, 'flows');
    const continuation = continuationForLaunch({flowsRoot, root: o.root, predecessor: o.predecessor, metaflowFile: o.metaflow, topic: o.topic});
    releaseDependency = secondaryBeforePrimary(o, continuation);

    step = 'workspace';
    if (!fs.statSync(o.workspace).isDirectory()) throw new Error(`workspace is not a directory: ${o.workspace}`);
    fs.accessSync(o.workspace, fs.constants.R_OK | fs.constants.X_OK);
    done(`${o.workspace} is available`);

    step = 'prompt';
    const metaflow = metaflowFor(LAUNCH_CONFIG, {aspect: o.aspect, topic: continuation.topic, layer: o.layer});
    const startupSkills = resolveSkillDependencies(metaflow['user-modules'] ?? BIRTH_SKILLS);
    const systemSeat = {...o, topic: continuation.topic, metaflow: continuation.metaflow, startupSkills, launchConfig: LAUNCH_CONFIG, metaflowConfig: metaflow};
    const systemBase = o.systemPromptFile ?? path.join(o.workspace, 'tools/main-flow-mode/system-prompt.md');
    composeSpiritSystemPrompt(fs.readFileSync(systemBase, 'utf8'), mainSystemModules(o.workspace, '.claude', systemSeat));
    const skillNames = orderSkillsForPrompt(startupSkills.filter(name => !name.startsWith('spirit-') && name !== 'spirit' && !name.startsWith('intent-') && !(name === 'vision-design' && (o.aspect === 'Psyche' || o.layer === 'Primary'))));
    const composition = composeFirstPrompt({brief: fs.readFileSync(o.brief, 'utf8'), exists: liveSkillExists(o.workspace), skillNames, launchConfig: LAUNCH_CONFIG, metaflowConfig: metaflow});
    const promptFile = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'claude-main-flow-launch-')), 'first-topic-prompt.md');
    fs.writeFileSync(promptFile, composition.prompt);
    done(`composed one topic prompt from EDN with ${skillNames.length} selected skills, handover and raw psyche paths`);

    step = 'flow';
    const sessionId = crypto.randomUUID();
    const flowId = claimFlow(flowsRoot, sessionId);
    const lineage = writeContinuationRecord(flowsRoot, flowId, continuation);
    const title = canonicalTitleFor(o.aspect, o.model, flowId, o.layer, continuation.topic);
    done(`Flow ID ${flowId} for session ${sessionId}, directory ${path.join(o.workspace, 'flows', flowId)}; continuation record ${lineage.recordPath}`);

    step = 'pane';
    const ws = pickWorkspace(herdr(o.herdrSession, 'workspace', 'list').workspaces, o.herdrWorkspaceLabel);
    const created = herdr(o.herdrSession, 'tab', 'create', '--workspace', ws.workspace_id, '--cwd', o.workspace, '--label', title.slice(2, -2).replace(` ${flowId}`, ''), '--no-focus');
    const tabId = created.tab?.tab_id ?? created.tab_id;
    const panes = herdr(o.herdrSession, 'pane', 'list').panes.filter(p => p.tab_id === tabId);
    if (!tabId || panes.length !== 1) throw new Error('new tab has no single pane');
    const paneId = panes[0].pane_id;
    done(`${paneId} in tab ${tabId} of workspace ${ws.workspace_id}, cwd ${o.workspace}`);

    step = 'harness';
    const transcript = transcriptPath(o.workspace, sessionId);
    if (fs.existsSync(transcript)) throw new Error(`transcript already exists: ${transcript}`);
    const refreshConfigPath = path.join(os.homedir(), '.claude', 'jobs', `native-${sessionId}`, 'context-refresh.json');
    fs.mkdirSync(path.dirname(refreshConfigPath), {recursive: true, mode: 0o700});
    const refreshBase = JSON.parse(fs.readFileSync(path.join(o.workspace, 'config', 'context-refresh.json'), 'utf8'));
    fs.writeFileSync(refreshConfigPath, `${JSON.stringify(makeContextRefreshBinding({baseConfig: refreshBase, nativeSessionId: sessionId, flowId, aspect: o.aspect, topic: continuation.topic, layer: o.layer, harness: 'claude', model: o.model, seatTarget: `${o.aspect} ${continuation.topic} ${o.layer}`, warningWindowFraction: refreshBase.warningWindowFraction, claudeWarningTokens: refreshBase.claude.warningTokens, codexModelWindows: refreshBase.codex.models}))}\n`, {flag: 'wx', mode: 0o600});
    const mode = mainFlowMode(o.workspace, sessionId, os.homedir(), o.systemPromptFile, {...systemSeat, refreshConfigPath}, process.env.PRIMARY_COMMITTER_FLOW_ID);
    writeMainFlowMode(mode);
    const command = `cd ${sh(o.workspace)} && exec env ${claudeFlowEnvironment(flowId)} claude --session-id ${sessionId} --model ${sh(o.model)} --effort ${sh(o.effort)} --name ${sh(title)} --remote-control --dangerously-skip-permissions --system-prompt-file ${sh(mode.promptFile)} --settings ${sh(mode.settingsFile)} "$(cat ${sh(promptFile)})"`;
    execFileSync('herdr', ['--session', o.herdrSession, 'pane', 'run', paneId, command], {encoding: 'utf8', timeout: 15000});
    await poll('the native transcript', 120, () => fs.existsSync(transcript));
    done(`claude session ${sessionId}, transcript ${transcript}; system prompt ${mode.promptFile}, settings ${mode.settingsFile}`);

    step = 'first topic response';
    const responseTimeout = metaflow['first-response-timeout-seconds'] ?? LAUNCH_CONFIG.shared['first-response-timeout-seconds'];
    if (!Number.isInteger(responseTimeout) || responseTimeout < 1) throw new Error('EDN first-response-timeout-seconds is required');
    const transcriptRows = await poll('the first topic prompt and its proposal response', responseTimeout, () => {
      const current = rows(transcript);
      const exact = readUserPrompts(current).filter(receipt => matchesFirstPrompt(receipt, composition.prompt, skillNames));
      return exact.length === 1 && hasCompletedResponseAfter(current, 0) ? current : null;
    });
    const loadedCount = validateLoadedSkillBlocks(readLoadedSkillBlocks(transcriptRows, o.workspace), skillNames, liveSkillReader(o.workspace));
    if (loadedCount !== skillNames.length) throw new Error(`expected ${skillNames.length} selected skill bodies, got ${loadedCount}`);
    done(`one EDN topic prompt accepted; ${loadedCount} selected skill bodies and a completed first response witnessed`);

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
    const name = nativeAgentName(o.aspect, o.layer, continuation.topic, flowId);
    execFileSync('herdr', ['--session', o.herdrSession, 'pane', 'report-agent-session', paneId, '--source', 'herdr:claude', '--agent', 'claude', '--agent-session-id', sessionId, '--session-start-source', 'claude-main-flow-launch'], {encoding: 'utf8', timeout: 15000});
    herdr(o.herdrSession, 'agent', 'rename', paneId, name);
    await poll('an agent bound to the session', 180, () => {
      const a = herdr(o.herdrSession, 'agent', 'get', name).agent;
      return hasExactRegistrationBinding(a, paneId, sessionId);
    });
    done(`${name} on ${paneId}, agent session ${sessionId}`);

    step = 'register';
    done(execFileSync('hm-register', [flowId, name, '--session', o.herdrSession, '--native-thread', sessionId, '--aspect', o.aspect, '--topic', continuation.topic, '--layer', o.layer], {encoding: 'utf8', timeout: 60000}).trim());
    releaseDependency();
  } catch (error) {
    releaseDependency();
    console.error(`${step}: FAILED: ${error.message}`);
    process.exit(1);
  }
}

const invokedDirectly = process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname);
if (invokedDirectly) {
  let o;
  try { o = parseArgs(process.argv.slice(2)); } catch (e) { console.error(`arguments: FAILED: ${e.message}`); process.exit(2); }
  if (o.composeOnly) {
    const metaflow = metaflowFor(LAUNCH_CONFIG, {aspect: o.aspect, topic: o.topic ?? 'Core', layer: o.layer ?? 'Primary'});
    const startupSkills = resolveSkillDependencies(metaflow['user-modules'] ?? BIRTH_SKILLS);
    const skillNames = orderSkillsForPrompt(startupSkills.filter(name => !name.startsWith('spirit-') && name !== 'spirit' && !name.startsWith('intent-') && !(name === 'vision-design' && (o.aspect === 'Psyche' || o.layer === 'Primary'))));
    const composition = composeFirstPrompt({brief: fs.readFileSync(o.brief, 'utf8'), exists: liveSkillExists(o.workspace), skillNames, launchConfig: LAUNCH_CONFIG, metaflowConfig: metaflow});
    process.stdout.write(composition.prompt);
  } else await launch(o);
}
