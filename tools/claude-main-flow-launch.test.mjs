#!/usr/bin/env node
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {BIRTH_SKILLS, claimFlow, composeFirstPrompt, parseArgs, readFirstPrompt, titleRecords, transcriptPath} from './claude-main-flow-launch.mjs';

// Arguments: refused before anything is touched.
assert.throws(() => parseArgs([]), /--model and --brief are required/);
assert.throws(() => parseArgs(['--model', 'gpt-6-astra', '--brief', 'b']), /not a Claude model/);
assert.throws(() => parseArgs(['--model', 'claude-nova-9', '--brief', 'b']), /unmapped exact native model/);
assert.throws(() => parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--aspect', 'Soul']), /no such aspect/);
assert.throws(() => parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--effort', 'high']), /bad argument: --effort/);
const o = parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b']);
assert.equal(o.aspect, 'Psyche'); assert.equal(o.workspace, '/home/li/primary'); assert.equal(o.herdrSession, 'default');
assert.equal(parseArgs(['--model', 'claude-opus-5-5', '--brief', 'b', '--aspect', 'Field']).aspect, 'Field');
const bad = spawnSync(process.execPath, [path.join(import.meta.dirname, 'claude-main-flow-launch.mjs'), '--model', 'claude-opus-5-5'], {encoding: 'utf8'});
assert.equal(bad.status, 2); assert.match(bad.stderr, /^arguments: FAILED/);

// Composition: the six birth commands at the head, then the brief as their argument.
assert.equal(BIRTH_SKILLS.length, 6); assert.equal(BIRTH_SKILLS[0], 'main-flow');
const prompt = composeFirstPrompt({brief: 'Say ready.\n', exists: () => true});
assert.equal(prompt, '/main-flow /spirit /psyche /psyche-interraction /vocabulary /edit-coordination # Launch brief\n\nSay ready.\n');
assert.throws(() => composeFirstPrompt({brief: 'x', exists: n => n !== 'vocabulary'}), /skill missing on main: vocabulary/);
assert.throws(() => composeFirstPrompt({brief: ' ', exists: () => true}), /brief is empty/);

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

// Flow claim in a scratch flows root: the session UUID decides the alias.
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-main-flow-launch-flows-'));
const session = '3f2a9c10-7075-4cc2-928d-13fc5610abcd';
const id = claimFlow(root, session);
assert.equal(id, '3f2a9c');
assert.ok(fs.statSync(path.join(root, id)).isDirectory());

console.log('claude-main-flow-launch tests passed');
