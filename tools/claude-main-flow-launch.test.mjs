#!/usr/bin/env node
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {BIRTH_SKILLS, LAYERS, MAX_SKILLS_PER_PROMPT, assistantResponses, claimFlow, claudeCodeVersion, composeFirstPrompt, composeSkillPrompt, hasCompletedResponseAfter, hasExactRegistrationBinding, liveSkillExists, mainFlowMode, parseArgs, preflightModel, readLoadedSkillBlocks, readUserPrompts, titleRecords, transcriptPath, validateLoadedSkillBlocks, writeMainFlowMode} from './claude-main-flow-launch.mjs';
import {STANDING_SKILLS} from './standing-skill-selection.mjs';
import {canonicalTitleFor} from './native-main-flow-launch-shared.mjs';

// Arguments: refused before anything is touched.
assert.throws(() => parseArgs([]), /--brief is required/);
assert.throws(() => parseArgs(['--model', 'gpt-6-astra', '--brief', 'b']), /not a Claude model/);
assert.throws(() => parseArgs(['--model', 'claude-nova-9', '--brief', 'b']), /unmapped exact native model/);
assert.throws(() => parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--aspect', 'Soul']), /no such aspect/);
assert.deepEqual(LAYERS, ['Primary', 'Secondary', 'Tertiary', 'Quaternary']);
assert.throws(() => parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--aspect', 'Mind', '--layer', 'Secondary']), /Mind runs on Codex only/);
assert.throws(() => parseArgs(['--model', 'claude-opus-4-6', '--brief', 'b', '--aspect', 'Mind']), /Mind runs on Codex only/);
assert.equal(parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--layer', 'Secondary', '--predecessor', 'abcdef']).layer, 'Secondary');
assert.equal(parseArgs(['--model', 'claude-sonnet-5-5', '--brief', 'b', '--layer', 'Tertiary', '--predecessor', 'abcdef']).layer, 'Tertiary');
assert.equal(parseArgs(['--brief', 'b', '--layer', 'Primary', '--root', '--metaflow', '/tmp/meta']).layer, 'Primary');
assert.throws(() => parseArgs(['--brief', 'b', '--layer', 'Quinary', '--predecessor', 'abcdef']), /no additive layer: Quinary/);
assert.throws(() => parseArgs(['--brief', 'b', '--layer', 'Primary']), /exactly one/);
assert.throws(() => parseArgs(['--brief', 'b', '--layer', 'Primary', '--root']), /requires --metaflow/);
assert.equal(canonicalTitleFor('Mind', 'claude-opus-5-5', 'bfdae1', 'Secondary'), '{ Mind Secondary bfdae1 }');
assert.equal(canonicalTitleFor('Field', 'claude-opus-5-5', 'abcdef', 'Quaternary'), '{ Field Quaternary abcdef }');
assert.throws(() => canonicalTitleFor('Psyche', 'claude-unmapped-1', 'abcdef'), /exact layer/);
assert.throws(() => parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--layer', 'Primary', '--predecessor', 'abcdef', '--effort', 'huge']), /no such effort: huge/);
assert.throws(() => parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--layer', 'Primary', '--predecessor', 'abcdef', '--effort']), /bad argument: --effort/);
assert.equal(parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--layer', 'Primary', '--predecessor', 'abcdef', '--effort', 'high']).effort, 'high');
assert.equal(parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--compose-only']).effort, undefined);
assert.equal(parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--compose-only']).systemPromptFile, undefined);
assert.equal(parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--compose-only', '--system-prompt-file', '/x/p.md']).systemPromptFile, '/x/p.md');
const o = parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--compose-only']);
assert.equal(o.aspect, 'Psyche'); assert.equal(o.workspace, '/home/li/primary'); assert.equal(o.herdrSession, 'default');
assert.equal(parseArgs(['--model', 'claude-sonnet-5-5', '--brief', 'b', '--compose-only']).model, 'claude-sonnet-5-5');
assert.equal(parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--aspect', 'Field', '--compose-only']).aspect, 'Field');
const bad = spawnSync(process.execPath, [path.join(import.meta.dirname, 'claude-main-flow-launch.mjs'), '--model', 'claude-opus-5-5'], {encoding: 'utf8'});
assert.equal(bad.status, 2); assert.match(bad.stderr, /^arguments: FAILED/);

// Sonnet 5.5 is rejected in launcher preflight before launch can claim a flow
// or create a Herdr pane. Other model IDs do not query the local CLI.
assert.deepEqual(claudeCodeVersion('2.1.284 (Claude Code)'), [2, 1, 284]);
assert.throws(() => claudeCodeVersion('Claude Code development'), /could not read Claude Code version/);
assert.throws(() => preflightModel('claude-sonnet-5-5', () => '2.1.280 (Claude Code)'), /requires Claude Code 2\.1\.284 or later; installed 2\.1\.280/);
assert.doesNotThrow(() => preflightModel('claude-sonnet-5-5', () => '2.1.284 (Claude Code)'));
assert.doesNotThrow(() => preflightModel('claude-sonnet-5-5', () => '3.0.0 (Claude Code)'));
assert.doesNotThrow(() => preflightModel('claude-opus-5-5', () => { throw new Error('version reader should not run'); }));
const cliDir = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-main-flow-launch-cli-'));
const fakeClaude = path.join(cliDir, 'claude');
fs.writeFileSync(fakeClaude, '#!/bin/sh\nprintf "2.1.280 (Claude Code)\\n"\n', {mode: 0o755});
const brief = path.join(cliDir, 'brief.md');
fs.writeFileSync(brief, 'unused because preflight must fail first\n');
const preflightFailure = spawnSync(process.execPath, [path.join(import.meta.dirname, 'claude-main-flow-launch.mjs'), '--model', 'claude-sonnet-5-5', '--brief', brief, '--layer', 'Tertiary', '--root', '--metaflow', '/tmp/metaflow', '--workspace', path.join(cliDir, 'not-a-workspace')], {encoding: 'utf8', env: {...process.env, PATH: `${cliDir}:${process.env.PATH}`}});
assert.equal(preflightFailure.status, 1);
assert.match(preflightFailure.stderr, /^preflight: FAILED: claude-sonnet-5-5 requires Claude Code 2\.1\.284 or later; installed 2\.1\.280/);
assert.doesNotMatch(preflightFailure.stderr, /workspace is not a directory/);

// Registration accepts an exact pane/session binding even while the native
// agent is working and exposes no readiness proof.
assert.ok(hasExactRegistrationBinding({pane_id: 'p', agent_session: {value: 'session'}, interactive_ready: false, agent_status: 'working'}, 'p', 'session'));
assert.ok(!hasExactRegistrationBinding({pane_id: 'other', agent_session: {value: 'session'}}, 'p', 'session'));
assert.ok(!hasExactRegistrationBinding({pane_id: 'p', agent_session: {value: 'other'}}, 'p', 'session'));

// Composition: native Claude loads no more than six selected skills per prompt;
// main-flow leads, and the one launch brief is sent only after those prompts.
assert.equal(BIRTH_SKILLS[0], 'operation-main-flow');
for (const name of STANDING_SKILLS) assert.equal(BIRTH_SKILLS.filter(candidate => candidate === name).length, 1, `${name} loads exactly once`);
assert.equal(MAX_SKILLS_PER_PROMPT, 6);
const names = ['operation-main-flow', ...Array.from({length: 12}, (_, i) => `skill-${i + 1}`)];
const composition = composeFirstPrompt({brief: 'Say ready.\n', exists: () => true, skillNames: names});
assert.deepEqual(composition.skillPrompts.map(prompt => [...prompt.matchAll(/\/([A-Za-z0-9_-]+)/g)].map(m => m[1])), [names.slice(0, 6), names.slice(6, 12), names.slice(12)]);
assert.ok(composition.skillPrompts[0].startsWith('/operation-main-flow /skill-1 /skill-2 /skill-3 /skill-4 /skill-5 '));
assert.ok(composition.skillPrompts.every(prompt => prompt.includes('Reply exactly READY')));
assert.equal(composition.prompt, 'Say ready.\n');
assert.equal(composeSkillPrompt({skillNames: ['compensation-behavior'], exists: () => true}), '/compensation-behavior # Startup skills\n\nStartup context only: load these skills for the upcoming launch brief. Do not begin that work or write files yet. Reply exactly READY.\n');
assert.throws(() => composeSkillPrompt({skillNames: ['same', 'same'], exists: () => true}), /duplicate names/);
assert.throws(() => composeSkillPrompt({skillNames: Array(7).fill('x'), exists: () => true}), /between one and 6/);
assert.throws(() => composeFirstPrompt({brief: 'x', exists: () => true, skillNames: ['spirit']}), /operation-main-flow must lead/);
assert.throws(() => composeFirstPrompt({brief: 'x', exists: n => n !== 'knowledge-vocabulary'}), /skill input missing or empty: knowledge-vocabulary/);
assert.throws(() => composeFirstPrompt({brief: ' ', exists: () => true}), /brief is empty/);

// The launcher reads the delivered skill input from disk, with no repository lookup.
const skillWorkspace = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-main-flow-launch-skills-'));
for (const name of BIRTH_SKILLS) {
  const file = path.join(skillWorkspace, '.claude', 'skills', name, 'SKILL.md');
  fs.mkdirSync(path.dirname(file), {recursive: true}); fs.writeFileSync(file, `${name}\n`);
}
assert.equal(liveSkillExists(skillWorkspace)('operation-main-flow'), true);
fs.writeFileSync(path.join(skillWorkspace, '.claude', 'skills', 'knowledge-psyche', 'SKILL.md'), '  \n');
assert.equal(liveSkillExists(skillWorkspace)('knowledge-psyche'), false);

// Transcript path as Claude derives it from the working directory.
assert.equal(transcriptPath('/home/li/primary', 'u'), path.join(os.homedir(), '.claude/projects/-home-li-primary/u.jsonl'));

// Transcript evidence must contain every selected generated body, once and in
// resolver order, before the separate launch brief arrives.
const injectedWorkspace = skillWorkspace;
const skillFiles = new Map([
  ['operation-main-flow', '---\ndescription: main\n---\n\nMain body.\n'],
  ['compensation-behavior', '---\ndescription: behavior\n---\n\nBehavior body.\n'],
]);
const skillReader = name => skillFiles.get(name);
const skillRows = [...skillFiles].map(([name, content], index) => ({
  type: 'user', isMeta: true, promptId: `skill-prompt-${index}`,
  message: {role: 'user', content: [{type: 'text', text: `Base directory for this skill: ${path.join(injectedWorkspace, '.claude', 'skills', name)}\n\n${content.trim()}\n\nARGUMENTS: Startup context only.`}]},
}));
const loaded = readLoadedSkillBlocks(skillRows, injectedWorkspace);
assert.deepEqual(loaded.map(block => block.name), [...skillFiles.keys()]);
assert.equal(validateLoadedSkillBlocks(loaded, [...skillFiles.keys()], skillReader), 2);
assert.throws(() => validateLoadedSkillBlocks(loaded, ['operation-main-flow', 'spirit'], skillReader), /expected spirit, got compensation-behavior/);
assert.throws(() => validateLoadedSkillBlocks([loaded[0], loaded[0]], ['operation-main-flow', 'compensation-behavior'], skillReader), /loaded a skill more than once/);
assert.throws(() => validateLoadedSkillBlocks([{...loaded[0], body: 'altered'}], ['operation-main-flow'], skillReader), /body differs/);
const finalPrompt = {type: 'user', promptId: 'launch', message: {role: 'user', content: 'Say ready.'}};
assert.deepEqual(readUserPrompts([...skillRows, finalPrompt]).at(-1), {id: 'launch', text: 'Say ready.'});
const response = {type: 'assistant', effort: 'medium', perTurnEffort: 'medium', message: {model: 'claude-sonnet-5-5', stop_reason: 'end_turn'}};
assert.deepEqual(assistantResponses([response]), [response]);
assert.equal(hasCompletedResponseAfter([response], 0), true);
assert.equal(hasCompletedResponseAfter([response], 1), false);
assert.deepEqual(titleRecords([{type: 'custom-title', customTitle: 'Psyche.{ Opus abc123 }', sessionId: 's'}, {type: 'agent-name', agentName: 'x', sessionId: 'other'}], 's'), ['Psyche.{ Opus abc123 }']);

// Main-flow mode: the workspace's system prompt, and settings in the job directory
// whose hook reads that prompt and counts in the job directory.
const home = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-main-flow-launch-home-'));
const workspace = path.join(home, 'ws');
fs.mkdirSync(path.join(workspace, 'tools', 'main-flow-mode'), {recursive: true});
fs.writeFileSync(path.join(workspace, 'tools', 'main-flow-mode', 'system-prompt.md'), 'You are the main flow.\n');
const mode = mainFlowMode(workspace, 'sess-1', home);
assert.equal(mode.promptFile, path.join(workspace, 'tools/main-flow-mode/system-prompt.md'));
assert.equal(mode.settingsFile, path.join(home, '.claude/jobs/native-sess-1/main-flow-settings.json'));
const hook = mode.settings.hooks.UserPromptSubmit[0].hooks[0];
assert.equal(hook.command, `python3 '${workspace}/tools/main-flow-mode/reminder-hook.py' --prompt-file '${workspace}/tools/main-flow-mode/system-prompt.md' --state-dir '${home}/.claude/jobs/native-sess-1/main-flow-reminder' --every 20`);
writeMainFlowMode(mode);
assert.deepEqual(JSON.parse(fs.readFileSync(mode.settingsFile, 'utf8')), mode.settings);
assert.throws(() => writeMainFlowMode(mode), /EEXIST/);
fs.writeFileSync(mode.promptFile, ' \n');
assert.throws(() => writeMainFlowMode(mainFlowMode(workspace, 'sess-2', home)), /system prompt missing or empty/);

// A given system prompt replaces the fixed file for the seat and its reminder hook.
const custom = path.join(home, 'assembled.md');
fs.writeFileSync(custom, 'Assembled from modules.\n');
const cmode = mainFlowMode(workspace, 'sess-3', home, custom);
assert.equal(cmode.promptFile, custom);
assert.equal(cmode.settingsFile, path.join(home, '.claude/jobs/native-sess-3/main-flow-settings.json'));
assert.equal(cmode.settings.hooks.UserPromptSubmit[0].hooks[0].command, `python3 '${workspace}/tools/main-flow-mode/reminder-hook.py' --prompt-file '${custom}' --state-dir '${home}/.claude/jobs/native-sess-3/main-flow-reminder' --every 20`);
writeMainFlowMode(cmode);
fs.writeFileSync(custom, '\n');
assert.throws(() => writeMainFlowMode(mainFlowMode(workspace, 'sess-4', home, custom)), /system prompt missing or empty/);

// Flow claim in a scratch flows root: the session UUID decides the alias.
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-main-flow-launch-flows-'));
const session = '3f2a9c10-7075-4cc2-928d-13fc5610abcd';
const id = claimFlow(root, session);
assert.equal(id, '3f2a9c');
assert.ok(fs.statSync(path.join(root, id)).isDirectory());

console.log('claude-main-flow-launch tests passed');
