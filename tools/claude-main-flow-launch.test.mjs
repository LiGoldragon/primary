#!/usr/bin/env node
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {BIRTH_SKILLS, claimFlow, claudeCodeVersion, composeFirstPrompt, hasExactRegistrationBinding, liveSkillExists, mainFlowMode, parseArgs, preflightModel, readFirstPrompt, titleRecords, transcriptPath, writeMainFlowMode} from './claude-main-flow-launch.mjs';

// Arguments: refused before anything is touched.
assert.throws(() => parseArgs([]), /--model and --brief are required/);
assert.throws(() => parseArgs(['--model', 'gpt-6-astra', '--brief', 'b']), /not a Claude model/);
assert.throws(() => parseArgs(['--model', 'claude-nova-9', '--brief', 'b']), /unmapped exact native model/);
assert.throws(() => parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--aspect', 'Soul']), /no such aspect/);
assert.throws(() => parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--effort', 'high']), /bad argument: --effort/);
const o = parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b']);
assert.equal(o.aspect, 'Psyche'); assert.equal(o.workspace, '/home/li/primary'); assert.equal(o.herdrSession, 'default');
assert.equal(parseArgs(['--model', 'claude-sonnet-5-5', '--brief', 'b']).model, 'claude-sonnet-5-5');
assert.equal(parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--aspect', 'Field']).aspect, 'Field');
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
const preflightFailure = spawnSync(process.execPath, [path.join(import.meta.dirname, 'claude-main-flow-launch.mjs'), '--model', 'claude-sonnet-5-5', '--brief', brief, '--workspace', path.join(cliDir, 'not-a-workspace')], {encoding: 'utf8', env: {...process.env, PATH: `${cliDir}:${process.env.PATH}`}});
assert.equal(preflightFailure.status, 1);
assert.match(preflightFailure.stderr, /^preflight: FAILED: claude-sonnet-5-5 requires Claude Code 2\.1\.284 or later; installed 2\.1\.280/);
assert.doesNotMatch(preflightFailure.stderr, /workspace is not a directory/);

// Registration accepts an exact pane/session binding even while the native
// agent is working and exposes no readiness proof.
assert.ok(hasExactRegistrationBinding({pane_id: 'p', agent_session: {value: 'session'}, interactive_ready: false, agent_status: 'working'}, 'p', 'session'));
assert.ok(!hasExactRegistrationBinding({pane_id: 'other', agent_session: {value: 'session'}}, 'p', 'session'));
assert.ok(!hasExactRegistrationBinding({pane_id: 'p', agent_session: {value: 'other'}}, 'p', 'session'));

// Composition: the six birth commands at the head, then the brief as their argument.
assert.equal(BIRTH_SKILLS.length, 6); assert.equal(BIRTH_SKILLS[0], 'main-flow');
const prompt = composeFirstPrompt({brief: 'Say ready.\n', exists: () => true});
assert.equal(prompt, '/main-flow /spirit /psyche /psyche-interraction /vocabulary /edit-coordination # Launch brief\n\nSay ready.\n');
assert.throws(() => composeFirstPrompt({brief: 'x', exists: n => n !== 'vocabulary'}), /skill input missing or empty: vocabulary/);
assert.throws(() => composeFirstPrompt({brief: ' ', exists: () => true}), /brief is empty/);

// The launcher reads the delivered skill input from disk, with no repository lookup.
const skillWorkspace = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-main-flow-launch-skills-'));
for (const name of BIRTH_SKILLS) {
  const file = path.join(skillWorkspace, '.claude', 'skills', name, 'SKILL.md');
  fs.mkdirSync(path.dirname(file), {recursive: true}); fs.writeFileSync(file, `${name}\n`);
}
assert.equal(liveSkillExists(skillWorkspace)('main-flow'), true);
fs.writeFileSync(path.join(skillWorkspace, '.claude', 'skills', 'psyche', 'SKILL.md'), '  \n');
assert.equal(liveSkillExists(skillWorkspace)('psyche'), false);

// Transcript path as Claude derives it from the working directory.
assert.equal(transcriptPath('/home/li/primary', 'u'), path.join(os.homedir(), '.claude/projects/-home-li-primary/u.jsonl'));

// Transcript reading, on the shape a chained start argument leaves.
const cmd = (n, p) => ({type: 'user', promptId: p, message: {role: 'user', content: `<command-message>${n}</command-message>\n<command-name>/${n}</command-name>\n<command-args># Launch brief\n\nSay ready.</command-args>`}});
const body = (n, p) => ({type: 'user', isMeta: true, promptId: p, message: {role: 'user', content: [{type: 'text', text: `Base directory for this skill: /home/li/primary/.claude/skills/${n}\n\nbody`}]}});
const turn = BIRTH_SKILLS.flatMap(n => [cmd(n, 'p1'), body(n, 'p1')]);
const named = {type: 'user', isMeta: true, promptId: 'p0', message: {role: 'user', content: 'The user named this session'}};
const tool = {type: 'user', promptId: 'p1', message: {role: 'user', content: [{type: 'tool_result', content: 'x'}]}};
const fp = readFirstPrompt([named, ...turn, tool]);
assert.deepEqual(fp.promptIds, ['p1']);
assert.deepEqual(fp.commands, BIRTH_SKILLS); assert.deepEqual(fp.expanded, BIRTH_SKILLS);
assert.ok(fp.args.includes('# Launch brief'));
assert.equal(readFirstPrompt([...turn, {type: 'user', promptId: 'p2', message: {role: 'user', content: 'again'}}]).promptIds.length, 2);
assert.deepEqual(readFirstPrompt(turn.slice(0, 4)).expanded, ['main-flow', 'spirit']);
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

// Flow claim in a scratch flows root: the session UUID decides the alias.
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-main-flow-launch-flows-'));
const session = '3f2a9c10-7075-4cc2-928d-13fc5610abcd';
const id = claimFlow(root, session);
assert.equal(id, '3f2a9c');
assert.ok(fs.statSync(path.join(root, id)).isDirectory());

console.log('claude-main-flow-launch tests passed');
