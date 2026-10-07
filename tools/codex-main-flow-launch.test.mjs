#!/usr/bin/env node
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {ASPECT_SKILLS, BIRTH_SKILLS, EFFORTS, LAYERS, codexHarnessCommand, claimFlow, composeFirstPrompt, hasExactRegistrationBinding, liveSkillReader, parseArgs, pickWorkspace} from './codex-main-flow-launch.mjs';
import {STANDING_SKILLS} from './standing-skill-selection.mjs';
import {canonicalTitleFor} from './native-main-flow-launch-shared.mjs';

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
assert.throws(() => parseArgs([]), /--brief is required/);
assert.throws(() => parseArgs(['--model', 'gpt-6-astra']), /required/);
assert.throws(() => parseArgs(['--model', 'gpt-6-nova', '--brief', 'b']), /unmapped exact native model/);
assert.throws(() => parseArgs(['--model', 'claude-fable-5-1', '--brief', 'b']), /not a Codex model/);
assert.throws(() => parseArgs(['--model', 'gpt-6-astra', '--brief', 'b', '--aspect', 'Psyche']), /no startup skill set/);
assert.equal(parseArgs(['--model', 'gpt-6-astra', '--brief', 'b', '--aspect', 'Field']).aspect, 'Field');
assert.deepEqual(EFFORTS, ['low', 'medium', 'high', 'xhigh', 'max']);
assert.deepEqual(LAYERS, ['Primary', 'Tertiary', 'Quaternary']);
assert.equal(parseArgs(['--model', 'gpt-6-luna', '--brief', 'b', '--aspect', 'Field', '--layer', 'Primary']).layer, 'Primary');
assert.equal(parseArgs(['--model', 'gpt-6-astra', '--brief', 'b', '--layer', 'Quaternary']).layer, 'Quaternary');
assert.throws(() => parseArgs(['--model', 'gpt-6-astra', '--brief', 'b', '--layer', 'Secondary']), /no additive layer: Secondary/);
assert.equal(canonicalTitleFor('Mind', 'gpt-6-luna', '918df4', 'Quaternary'), 'Mind.{ Luna 918df4 }');
assert.equal(canonicalTitleFor('Mind', 'gpt-6-luna', 'abcdef'), 'Mind.{ Luna abcdef }');
assert.equal(canonicalTitleFor('Field', 'gpt-6-luna', 'abcdef', 'Secondary'), 'Field.{ Luna abcdef }');
assert.equal(canonicalTitleFor('Field', 'gpt-6-luna', 'abcdef', 'Primary'), 'Field.{ Luna abcdef }');
assert.equal(canonicalTitleFor('Field', 'gpt-6-luna', 'abcdef', 'Tertiary'), 'Field.{ Luna abcdef }');
assert.equal(canonicalTitleFor('Field', 'gpt-6-luna', 'abcdef', 'Quaternary'), 'Field.{ Luna abcdef }');
assert.throws(() => canonicalTitleFor('Field', 'gpt-6-unknown', 'abcdef'), /unmapped exact native model/);
assert.equal(parseArgs(['--model', 'gpt-6-astra', '--brief', 'b', '--effort', 'low']).effort, 'low');
assert.throws(() => parseArgs(['--model', 'gpt-6-astra', '--brief', 'b', '--effort', 'tiny']), /no supported Codex effort: tiny/);
assert.throws(() => parseArgs(['--model', '--brief', 'b']), /bad argument: --model/);
const o = parseArgs(['--brief', 'b']);
assert.equal(o.workspace, '/home/li/primary'); assert.equal(o.herdrSession, 'default'); assert.equal(o.aspect, 'Mind'); assert.equal(o.model, undefined); assert.equal(o.effort, undefined);
const bad = run('--model', 'gpt-6-astra');
assert.equal(bad.status, 2); assert.match(bad.stderr, /^arguments: FAILED/);

// Registration has an exact pane/thread binding, without requiring an idle or
// readiness marker from the native harness.
assert.ok(hasExactRegistrationBinding({pane_id: 'p', agent_session: {value: 'thread'}, interactive_ready: false, agent_status: 'working'}, 'p', 'thread'));
assert.ok(!hasExactRegistrationBinding({pane_id: 'other', agent_session: {value: 'thread'}}, 'p', 'thread'));
assert.ok(!hasExactRegistrationBinding({pane_id: 'p', agent_session: {value: 'other'}}, 'p', 'thread'));

// Composition: main-flow leads, then every Mind startup skill in order, then the brief.
const read = name => `---\nname: ${name}\n---\n\nbody of ${name}\n`;
const {prompt, leading} = composeFirstPrompt({workspace: '/w', aspect: 'Mind', brief: 'Say ready.\n', read});
assert.ok(prompt.startsWith(leading));
assert.ok(leading.startsWith('Base directory for this skill: /w/.agents/skills/operation-main-flow\n\n---\nname: operation-main-flow'));
const order = [...prompt.matchAll(/^Base directory for this skill: \/w\/\.agents\/skills\/(.+)$/gm)].map(m => m[1]);
assert.deepEqual(order, BIRTH_SKILLS('Mind'));
for (const name of STANDING_SKILLS) assert.equal(order.filter(candidate => candidate === name).length, 1, `${name} loads exactly once`);
assert.ok(prompt.endsWith('# Launch brief\n\nSay ready.\n'));
const transitive = composeFirstPrompt({workspace: '/w', aspect: 'Mind', brief: 'Say ready.\n', read, skillNames: ['operation-main-flow', 'compensation-behavior', 'compensation-correction', 'spirit']});
assert.deepEqual([...transitive.prompt.matchAll(/^Base directory for this skill: \/w\/\.agents\/skills\/(.+)$/gm)].map(m => m[1]), ['operation-main-flow', 'compensation-behavior', 'compensation-correction', 'spirit']);
assert.match(transitive.prompt, /body of compensation-behavior/);
assert.match(transitive.prompt, /body of compensation-correction/);
assert.throws(() => composeFirstPrompt({workspace: '/w', aspect: 'Mind', brief: 'x', read: n => n === 'knowledge-vocabulary' ? '' : read(n)}), /skill input missing or empty: knowledge-vocabulary/);
assert.throws(() => composeFirstPrompt({workspace: '/w', aspect: 'Mind', brief: ' ', read}), /brief is empty/);
assert.throws(() => composeFirstPrompt({workspace: '/w', aspect: 'Mind', brief: 'x', read: n => 'y'.repeat(24000)}), /exceeds one argument/);

// The launcher uses the delivered skill files, not a repository revision.
const skillWorkspace = fs.mkdtempSync(path.join(os.tmpdir(), 'codex-main-flow-launch-skills-'));
const skillFile = path.join(skillWorkspace, '.agents', 'skills', 'operation-main-flow', 'SKILL.md');
fs.mkdirSync(path.dirname(skillFile), {recursive: true}); fs.writeFileSync(skillFile, 'live skill\n');
assert.equal(liveSkillReader(skillWorkspace)('operation-main-flow'), 'live skill\n');
assert.throws(() => liveSkillReader(skillWorkspace)('missing'), /ENOENT/);

// Flow claim in a scratch flows root: one thread, one alias; a repeat claim agrees.
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'codex-main-flow-launch-flows-'));
const thread = '01a0e0a1-7075-7cc2-928d-13fc5610abcd';
const flowId = claimFlow(root, thread);
assert.match(flowId, /^[0-9a-f]{6}$/);
assert.equal(claimFlow(root, thread), flowId);
assert.ok(fs.statSync(path.join(root, flowId)).isDirectory());
assert.match(claimFlow(root, "01a0e0a1-7075-7cc2-928d-13fc5610abce"), /^(?!c5610a$)[0-9a-f]{6,}$/); // a colliding thread gets a longer alias

console.log('codex-main-flow-launch tests passed');

// Execute only a disposable fake client, never Codex or Herdr.
const environmentRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'fresh-codex-environment-'));
try {
  const fakeClient = path.join(environmentRoot, 'fake-client');
  const brief = path.join(environmentRoot, 'brief');
  fs.writeFileSync(brief, 'offline fixture');
  fs.writeFileSync(fakeClient, `#!${process.execPath}
console.log(JSON.stringify({environment:Object.fromEntries(['CODEX_THREAD_ID','CODEX_SESSION_ID','CLAUDE_CODE_SESSION_ID','CLAUDE_SESSION_ID','THREAD_ID','FLOW_ID','FLOW_DIRECTORY','HERDR_ENV','HERDR_PANE_ID','HERDR_SOCKET_PATH'].map(k=>[k,process.env[k]??null])), args:process.argv.slice(2)}));
`, {mode: 0o700});
  const identities = ['CODEX_THREAD_ID','CODEX_SESSION_ID','CLAUDE_CODE_SESSION_ID','CLAUDE_SESSION_ID','THREAD_ID','FLOW_ID','FLOW_DIRECTORY'];
  const environment = {...process.env, ...Object.fromEntries(identities.map(k => [k, 'parent-identity'])), HERDR_ENV: '1', HERDR_PANE_ID: 'fixture-pane', HERDR_SOCKET_PATH: '/fixture-herdr.sock'};
  const command = codexHarnessCommand({command: fakeClient, expectedPath: fakeClient}, {model:'gpt-6.1-sol',effort:'low',workspace:environmentRoot}, brief);
  const child = spawnSync('sh', ['-c', command], {encoding:'utf8',env:environment});
  assert.equal(child.status, 0, child.stderr);
  const actual = JSON.parse(child.stdout);
  for (const key of identities) assert.equal(actual.environment[key], null, key);
  assert.equal(actual.environment.HERDR_ENV, '1');
  assert.equal(actual.environment.HERDR_PANE_ID, 'fixture-pane');
  assert.equal(actual.environment.HERDR_SOCKET_PATH, '/fixture-herdr.sock');
  assert.ok(actual.args.includes('model_reasoning_effort="low"'), 'explicit low effort reaches the Codex launcher config');
  assert.ok(!actual.args.includes('model_reasoning_effort="medium"'), 'explicit low effort does not retain the medium default');
} finally { fs.rmSync(environmentRoot, {recursive:true,force:true}); }
