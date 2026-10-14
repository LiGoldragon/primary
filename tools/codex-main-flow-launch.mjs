#!/usr/bin/env node
/* Start one Codex main-flow seat in Herdr, without the Flow Nexus.

   node tools/codex-main-flow-launch.mjs --brief FILE --layer LAYER (--root --metaflow FILE [--topic Topic] | --predecessor FLOW_ID)
        [--aspect Mind|Field] [--layer Primary|Tertiary|Quaternary] [--effort low|medium|high|xhigh|max] [--workspace /home/li/primary] [--herdr-session default]
        [--herdr-workspace-label LABEL] [--compose-only]

   The seat opens in Herdr's only workspace; the label chooses one only when
   Herdr holds several.

   One line per step; the first failure stops the launch and names its step.
   The first prompt is given once, with the Curriculum-resolved skill bodies,
   and is never retried. The Flow ID is the native thread's alias, so it is
   claimed as soon as the thread exists, before the title and the registration. */
import {execFileSync} from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {requireModelTitle} from './model-display-name.mjs';
import {secondaryBeforePrimary} from './secondary-first.mjs';
import {selectVoiceProfile} from './native-voice-profiles.mjs';
import {canonicalTitleFor, nativeAgentName, continuationForLaunch, requireTopic, writeContinuationRecord, clientForModel, herdrSessionReportArgs, orderSkillsForPrompt, pickWorkspace, resolveSkillDependencies, setAndReadNativeTitle, withRpc} from './native-main-flow-launch-shared.mjs';
import {codexModelSystemPrompt} from './main-flow-mode/spirit-system-prompt.mjs';
import {makeContextRefreshBinding} from './main-flow-mode/context-refresh.mjs';
import {STANDING_SKILLS} from './standing-skill-selection.mjs';
import {defaultLaunchConfig, birthSkillsFromConfig, metaflowFor, firstPromptFromConfig} from './main-flow-mode/launch-config.mjs';
export {pickWorkspace} from './native-main-flow-launch-shared.mjs';

// Startup roots per aspect. Curriculum expands their declared dependencies before composition.
export const EFFORTS = ['low', 'medium', 'high', 'xhigh', 'max'];
export const LAYERS = ['Primary', 'Secondary', 'Tertiary', 'Quaternary'];

export const LAUNCH_CONFIG = defaultLaunchConfig();
export const ASPECT_SKILLS = Object.fromEntries(['Mind', 'Field'].map(aspect => [aspect, birthSkillsFromConfig(LAUNCH_CONFIG, aspect)]));
export const BIRTH_SKILLS = aspect => birthSkillsFromConfig(LAUNCH_CONFIG, aspect);

const canonical = value => Array.isArray(value) ? value.map(canonical) : value && typeof value === 'object' ? Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])])) : value;
export function codexStopHookConfig({command, ...identity}) {
  const binding = makeContextRefreshBinding({...identity, harness: 'codex', seatTarget: `${identity.aspect} ${identity.topic} ${identity.layer}`});
  const spec = codexBirthHookSpec({command});
  return {...binding, hook: spec.hook, hooksState: {[spec.hookKey]: {enabled: true, trusted_hash: spec.hash}}, hookKey: spec.hookKey};
}
export const codexResumeCommand = (executable, threadId, prompt) => {
  if (!/^[a-f0-9-]{36}$/i.test(threadId)) throw new Error('exact native UUID required for resume');
  return `${sh(executable)} resume ${sh(threadId)} ${sh(prompt)}`;
};
export function codexBirthHookSpec({command}) {
  if (!command) throw new Error('Codex hook command is required before thread/start');
  const hook = {type: 'command', command, timeout: 30, async: false};
  const hash = `sha256:${crypto.createHash('sha256').update(JSON.stringify(canonical({event_name: 'stop', hooks: [hook]}))).digest('hex')}`;
  return {hook, hookKey: '/<session-flags>/config.toml:stop:0:0', hash};
}
export async function codexBirthResume({threadStart, claim, writeBinding, resume, hookCommand, prompt}) {
  const spec = codexBirthHookSpec({command: hookCommand});
  const started = await threadStart({hooks: spec});
  const threadId = started?.thread?.id;
  if (!threadId) throw new Error('thread/start returned no native thread UUID; resume refused');
  const flowId = await claim(threadId);
  if (!flowId) throw new Error('Flow claim failed; resume refused');
  await writeBinding({threadId, flowId, hook: spec});
  return resume(threadId, prompt);
}

// Registration binds the exact native thread to the exact Herdr pane.  It does
// not need a separate readiness or idleness assertion.
export function hasExactRegistrationBinding(agent, paneId, threadId) {
  return agent?.pane_id === paneId && agent.agent_session?.value === threadId;
}

export function parseArgs(argv) {
  const known = new Set(['--model', '--brief', '--aspect', '--layer', '--effort', '--workspace', '--herdr-session', '--herdr-workspace-label', '--predecessor', '--metaflow', '--topic']);
  const o = {aspect: 'Mind', effort: undefined, model: undefined, workspace: '/home/li/primary', herdrSession: 'default', herdrWorkspaceLabel: undefined, composeOnly: false, root: false, predecessor: undefined, metaflow: undefined, topic: undefined};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--compose-only') { o.composeOnly = true; continue; }
    if (a === '--root') { o.root = true; continue; }
    if (!known.has(a) || argv[i + 1] === undefined || argv[i + 1].startsWith('--')) throw new Error(`bad argument: ${a}`);
    o[a.slice(2).replace(/-(\w)/g, (_, c) => c.toUpperCase())] = argv[++i];
  }
  if (!o.brief) throw new Error('--brief is required');
  if (!ASPECT_SKILLS[o.aspect]) throw new Error(`no startup skill set for aspect ${o.aspect}`);
  if (o.layer !== undefined && !LAYERS.includes(o.layer)) throw new Error(`no additive layer: ${o.layer}`);
  if (o.effort !== undefined && !EFFORTS.includes(o.effort)) throw new Error(`no supported Codex effort: ${o.effort}`);
  if (o.model !== undefined && !/^gpt-/.test(o.model)) throw new Error(`not a Codex model: ${o.model}`);
  if (o.model !== undefined) requireModelTitle(o.model);
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

// Skill text is read from the generated Codex tree that the new seat will use.
export const liveSkillReader = workspace => name =>
  fs.readFileSync(path.join(workspace, '.agents', 'skills', name, 'SKILL.md'), 'utf8');

export const skillBlock = (workspace, name, text) =>
  `Base directory for this skill: ${path.join(workspace, '.agents', 'skills', name)}\n\n${text.trim()}\n`;

export function composeFirstPrompt({workspace, aspect, brief, read, launchConfig = LAUNCH_CONFIG, metaflowConfig = metaflowFor(launchConfig, {aspect, topic: 'Core', layer: 'Primary'}), skillNames = BIRTH_SKILLS(aspect).filter(name => !name.startsWith('intent-'))}) {
  if (skillNames[0] !== 'compensation-main-flow') throw new Error('compensation-main-flow must lead the resolved skill closure');
  if (skillNames.some(name => name === 'spirit' || name.startsWith('spirit-') || name.startsWith('intent-'))) throw new Error('startup spirit and intent modules belong only in the main system prompt');
  const blocks = skillNames.map(name => {
    const text = read(name);
    if (!text || !text.trim()) throw new Error(`skill input missing or empty: ${name}`);
    return skillBlock(workspace, name, text);
  });
  if (!brief.trim()) throw new Error('launch brief is empty');
  const prompt = firstPromptFromConfig(launchConfig, metaflowConfig, {modules: blocks.join('\n'), handover: brief});
  if (Buffer.byteLength(prompt) >= 120 * 1024) throw new Error('first prompt exceeds one argument (120 KiB)');
  return {prompt, leading: blocks[0], blocks};
}

export function claimFlow(flowsRoot, threadId) {
  const id = execFileSync('flow-id', ['codex', '--flows-root', flowsRoot], {encoding: 'utf8', env: {...process.env, CODEX_SESSION_ID: threadId}}).trim();
  if (!/^[0-9a-f]{6,}$/.test(id) || !fs.statSync(path.join(flowsRoot, id)).isDirectory()) throw new Error(`flow-id returned no flow directory: ${id}`);
  return id;
}

const sh = s => `'${s.replaceAll("'", `'\\''`)}'`;
export function codexHarnessCommand(client, o, promptFile, systemPromptFile, threadId = undefined) {
  if (!systemPromptFile || !path.isAbsolute(systemPromptFile)) throw new Error('composed main-flow system prompt file required');
  const identities = ['CODEX_THREAD_ID', 'CODEX_SESSION_ID', 'CLAUDE_CODE_SESSION_ID', 'CLAUDE_SESSION_ID', 'THREAD_ID', 'FLOW_ID', 'FLOW_DIRECTORY'];
  // Preserve Herdr's destination pane/socket while dropping parent seat identity.
  return `exec env ${identities.map(name => `-u ${name}`).join(' ')} ${sh(client.expectedPath)} -m ${sh(o.model)} -c ${sh(`model_instructions_file=${JSON.stringify(systemPromptFile)}`)} -c ${sh(`model_reasoning_effort="${o.effort}"`)} --dangerously-bypass-approvals-and-sandbox -C ${sh(o.workspace)} ${threadId ? `resume ${sh(threadId)} ` : ''}"$(cat ${sh(promptFile)})"`;
}
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
  let releaseDependency = () => {};
  let step = 'workspace';
  const done = (msg) => console.log(`${step}: ${msg}`);
  try {
    const profile = selectVoiceProfile({aspect: o.aspect, layer: o.layer, harness: 'codex', model: o.model, effort: o.effort});
    o = {...o, model: profile.model, effort: profile.effort};
    const flowsRoot = path.join(o.workspace, 'flows');
    const continuation = continuationForLaunch({flowsRoot, root: o.root, predecessor: o.predecessor, metaflowFile: o.metaflow, topic: o.topic});
    releaseDependency = secondaryBeforePrimary(o, continuation);
    if (!fs.statSync(o.workspace).isDirectory()) throw new Error(`workspace is not a directory: ${o.workspace}`);
    fs.accessSync(o.workspace, fs.constants.R_OK | fs.constants.X_OK);
    done(`${o.workspace} is available`);

    step = 'prompt';
    const startupSkills = resolveSkillDependencies(BIRTH_SKILLS(o.aspect));
    const skillNames = orderSkillsForPrompt(startupSkills.filter(name => !name.startsWith('spirit-') && name !== 'spirit' && !name.startsWith('intent-') && !(name === 'vision-design' && (o.aspect === 'Psyche' || o.layer === 'Primary'))));
    const metaflow = metaflowFor(LAUNCH_CONFIG, {aspect: o.aspect, topic: continuation.topic, layer: o.layer});
    const {prompt, leading, blocks} = composeFirstPrompt({workspace: o.workspace, aspect: o.aspect, brief: fs.readFileSync(o.brief, 'utf8'), read: liveSkillReader(o.workspace), skillNames, launchConfig: LAUNCH_CONFIG, metaflowConfig: metaflow});
    const promptFile = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'codex-main-flow-launch-')), 'first-prompt.md');
    fs.writeFileSync(promptFile, prompt);
    done(`composed ${Buffer.byteLength(prompt)} bytes from the workspace into ${promptFile}`);

    const client = clientForModel(o.model);
    const systemPromptFile = path.join(path.dirname(promptFile), 'main-flow-system-prompt.md');
    fs.writeFileSync(systemPromptFile, codexModelSystemPrompt(client, o.model, o.workspace, {...o, topic: continuation.topic, metaflow: continuation.metaflow, startupSkills, launchConfig: LAUNCH_CONFIG, metaflowConfig: metaflow}), {flag: 'wx', mode: 0o600});

    step = 'pane';
    const sessions = path.join(path.dirname(path.dirname(client.endpoint)), 'sessions');
    const ws = [pickWorkspace(herdr(o.herdrSession, 'workspace', 'list').workspaces, o.herdrWorkspaceLabel)];
    const label = o.layer ? `${o.aspect} ${o.layer}` : `${o.aspect} ${requireModelTitle(o.model)}`;
    const created = herdr(o.herdrSession, 'tab', 'create', '--workspace', ws[0].workspace_id, '--cwd', o.workspace, '--label', label, '--no-focus');
    const tabId = created.tab?.tab_id ?? created.tab_id;
    const panes = herdr(o.herdrSession, 'pane', 'list').panes.filter(p => p.tab_id === tabId);
    if (!tabId || panes.length !== 1) throw new Error('new tab has no single pane');
    const paneId = panes[0].pane_id;
    done(`${paneId} in tab ${tabId} of workspace ${ws[0].workspace_id}, cwd ${o.workspace}`);

    step = 'native birth and refresh binding';
    const refreshConfigPath = path.join(path.dirname(promptFile), 'context-refresh.json');
    const baseConfig = JSON.parse(fs.readFileSync(path.join(o.workspace, 'config/context-refresh.json'), 'utf8'));
    const hookCommand = [sh(process.execPath), sh(path.join(o.workspace, 'tools/context-refresh-hook.mjs')), '--config', sh(refreshConfigPath)].join(' ');
    let threadId, flowId, lineage;
    await codexBirthResume({
      hookCommand, prompt,
      threadStart: ({hooks}) => withRpc(client.endpoint, call => call('thread/start', {
        model: o.model, cwd: o.workspace, approvalPolicy: 'never', sandbox: 'danger-full-access',
        baseInstructions: fs.readFileSync(systemPromptFile, 'utf8'), ephemeral: false,
        config: {model_reasoning_effort: o.effort, 'features.hooks': true,
          'hooks.Stop': [{hooks: [hooks.hook]}],
          'hooks.state': {[hooks.hookKey]: {enabled: true, trusted_hash: hooks.hash}}}
      })),
      claim: id => { threadId = id; flowId = claimFlow(flowsRoot, id); return flowId; },
      writeBinding: () => {
        const binding = makeContextRefreshBinding({baseConfig, nativeSessionId: threadId, flowId,
          aspect: o.aspect, topic: continuation.topic, layer: o.layer, harness: 'codex', model: o.model,
          seatTarget: `${o.aspect} ${continuation.topic} ${o.layer}`});
        fs.writeFileSync(refreshConfigPath, JSON.stringify(binding) + '\n', {flag: 'wx', mode: 0o600});
        lineage = writeContinuationRecord(flowsRoot, flowId, continuation);
      },
      resume: id => execFileSync('herdr', ['--session', o.herdrSession, 'pane', 'run', paneId,
        codexHarnessCommand(client, o, promptFile, systemPromptFile, id)], {encoding: 'utf8', timeout: 15000})
    });
    done(`thread ${threadId}, claimed ${flowId}; exact refresh binding written before resume`);
    const rollout = await poll('the exact native rollout', 120, () =>
      rolloutFiles(sessions).find(file => rows(file)[0]?.payload?.id === threadId));
    const ctx = await poll('the first turn context', 120, () => rows(rollout).find(r => r.type === 'turn_context')?.payload);
    if (ctx.model !== o.model || ctx.effort !== o.effort || ctx.approval_policy !== 'never' || ctx.sandbox_policy?.type !== 'danger-full-access')
      throw new Error(`native settings differ: ${ctx.model} ${ctx.effort} ${ctx.approval_policy} ${ctx.sandbox_policy?.type}`);
    done(`${client.command} thread ${threadId}: ${ctx.model}, effort ${ctx.effort}, approval never, no sandbox`);

    step = 'first prompt';
    const texts = r => (r.type === 'response_item' && r.payload?.role === 'user' ? r.payload.content ?? [] : []).map(c => c.text ?? '');
    const accepted = await poll('the first prompt in the rollout', 60, () => rows(rollout).flatMap(texts).find(t => t.startsWith(leading)));
    const missing = blocks.filter(block => !accepted.includes(block));
    if (missing.length) throw new Error(`accepted prompt omitted resolved skill bodies: ${missing.length}`);
    done(`accepted once; main-flow leads and ${blocks.length} resolved skill bodies are present`);

    step = 'flow';
    done(`Flow ID ${flowId}, directory ${path.join(o.workspace, 'flows', flowId)}; continuation record ${lineage.recordPath}`);

    step = 'title';
    const title = canonicalTitleFor(o.aspect, o.model, flowId, o.layer, continuation.topic);
    const thread = await withRpc(client.endpoint, call => setAndReadNativeTitle(call, threadId, title));
    done(`read back "${thread.name}"`);

    step = 'herdr agent';
    const name = nativeAgentName(o.aspect, o.layer, continuation.topic, flowId);
    execFileSync('herdr', herdrSessionReportArgs({session: o.herdrSession, paneId}, threadId), {encoding: 'utf8', timeout: 15000});
    herdr(o.herdrSession, 'agent', 'rename', paneId, name);
    await poll('an agent bound to the thread', 120, () => {
      const a = herdr(o.herdrSession, 'agent', 'get', name).agent;
      return hasExactRegistrationBinding(a, paneId, threadId);
    });
    done(`${name} on ${paneId}, agent session ${threadId}`);

    step = 'register';
    done(execFileSync('hm-register', [flowId, name, '--session', o.herdrSession, '--native-thread', threadId, '--aspect', o.aspect, '--topic', continuation.topic, '--layer', o.layer], {encoding: 'utf8', timeout: 60000}).trim());
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
    const startupSkills = resolveSkillDependencies(BIRTH_SKILLS(o.aspect));
    const skillNames = orderSkillsForPrompt(startupSkills.filter(name => !name.startsWith('spirit-') && name !== 'spirit' && !name.startsWith('intent-') && !(name === 'vision-design' && (o.aspect === 'Psyche' || o.layer === 'Primary'))));
    const metaflow = metaflowFor(LAUNCH_CONFIG, {aspect: o.aspect, topic: o.topic ?? 'Core', layer: o.layer ?? 'Primary'});
    process.stdout.write(composeFirstPrompt({workspace: o.workspace, aspect: o.aspect, brief: fs.readFileSync(o.brief, 'utf8'), read: liveSkillReader(o.workspace), skillNames, launchConfig: LAUNCH_CONFIG, metaflowConfig: metaflow}).prompt);
  } else await launch(o);
}
