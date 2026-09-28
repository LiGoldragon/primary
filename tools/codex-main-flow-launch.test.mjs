#!/usr/bin/env node
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {ASPECT_SKILLS, claimFlow, composeFirstPrompt, parseArgs, pickWorkspace} from './codex-main-flow-launch.mjs';

// Herdr workspace: the only one whatever its label; a label chooses among several.
const w1 = {workspace_id: 'w1', label: '56ae53'}, w2 = {workspace_id: 'w2', label: 'other'};
assert.equal(pickWorkspace([w1], undefined), w1);
assert.equal(pickWorkspace([w1], 'primary'), w1);
assert.equal(pickWorkspace([w1, w2], 'other'), w2);
assert.throws(() => pickWorkspace([w1, w2], undefined), /holds 2 workspaces/);
assert.throws(() => pickWorkspace([w1, w2], 'primary'), /labelled primary, found 0/);
assert.throws(() => pickWorkspace([], undefined), /holds 0 workspaces/);

const tool = path.join(import.meta.dirname, 'codex-main-flow-launch.mjs');
const run = (...args) => spawnSync(process.execPath, [tool, ...args], {encoding: 'utf8'});

// Arguments: refused before anything is touched.
assert.throws(() => parseArgs([]), /--model and --brief are required/);
assert.throws(() => parseArgs(['--model', 'gpt-6-astra']), /required/);
assert.throws(() => parseArgs(['--model', 'gpt-6-nova', '--brief', 'b']), /unmapped exact native model/);
assert.throws(() => parseArgs(['--model', 'claude-fable-5-1', '--brief', 'b']), /not a Codex model/);
assert.throws(() => parseArgs(['--model', 'gpt-6-astra', '--brief', 'b', '--aspect', 'Field']), /no startup skill set/);
assert.throws(() => parseArgs(['--model', 'gpt-6-astra', '--brief', 'b', '--effort', 'high']), /bad argument: --effort/);
assert.throws(() => parseArgs(['--model', '--brief', 'b']), /bad argument: --model/);
const o = parseArgs(['--model', 'gpt-6-astra', '--brief', 'b']);
assert.equal(o.workspace, '/home/li/primary'); assert.equal(o.herdrSession, 'default'); assert.equal(o.aspect, 'Mind');
const bad = run('--model', 'gpt-6-astra');
assert.equal(bad.status, 2); assert.match(bad.stderr, /^arguments: FAILED/);

// Composition: main-flow leads, then every Mind startup skill in order, then the brief.
const read = name => `---\nname: ${name}\n---\n\nbody of ${name}\n`;
const {prompt, leading} = composeFirstPrompt({workspace: '/w', aspect: 'Mind', brief: 'Say ready.\n', read});
assert.ok(prompt.startsWith(leading));
assert.ok(leading.startsWith('Base directory for this skill: /w/.agents/skills/main-flow\n\n---\nname: main-flow'));
const order = [...prompt.matchAll(/^Base directory for this skill: \/w\/\.agents\/skills\/(.+)$/gm)].map(m => m[1]);
assert.deepEqual(order, ['main-flow', ...ASPECT_SKILLS.Mind]);
assert.ok(prompt.endsWith('# Launch brief\n\nSay ready.\n'));
assert.throws(() => composeFirstPrompt({workspace: '/w', aspect: 'Mind', brief: 'x', read: n => n === 'herdr' ? '' : read(n)}), /skill missing on main: herdr/);
assert.throws(() => composeFirstPrompt({workspace: '/w', aspect: 'Mind', brief: ' ', read}), /brief is empty/);
assert.throws(() => composeFirstPrompt({workspace: '/w', aspect: 'Mind', brief: 'x', read: n => 'y'.repeat(8000)}), /exceeds one argument/);

// Flow claim in a scratch flows root: one thread, one alias; a repeat claim agrees.
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'codex-main-flow-launch-flows-'));
const thread = '01a0e0a1-7075-7cc2-928d-13fc5610abcd';
const flowId = claimFlow(root, thread);
assert.match(flowId, /^[0-9a-f]{6}$/);
assert.equal(claimFlow(root, thread), flowId);
assert.ok(fs.statSync(path.join(root, flowId)).isDirectory());
assert.match(claimFlow(root, "01a0e0a1-7075-7cc2-928d-13fc5610abce"), /^(?!c5610a$)[0-9a-f]{6,}$/); // a colliding thread gets a longer alias

console.log('codex-main-flow-launch tests passed');
