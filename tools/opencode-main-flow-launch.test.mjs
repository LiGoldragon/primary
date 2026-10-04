#!/usr/bin/env node
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {AGENT, BIRTH_SKILLS, IDENTITIES, claimFlow, composeFirstPrompt, hasExactRegistrationBinding, liveSkillReader, opencodeHarnessCommand, parseArgs, readFirstTurn, reportedSession, seatConfig} from './opencode-main-flow-launch.mjs';

const model = 'criomos-local/qwen3.6-35b-a3b';
const tool = path.join(import.meta.dirname, 'opencode-main-flow-launch.mjs');
const run = (...args) => spawnSync(process.execPath, [tool, ...args], {encoding: 'utf8'});

// Arguments: refused before anything is touched.
assert.throws(() => parseArgs([]), /--model and --brief are required/);
assert.throws(() => parseArgs(['--model', 'gpt-6-astra', '--brief', 'b']), /not an OpenCode provider\/model reference/);
assert.throws(() => parseArgs(['--model', 'criomos-local/unknown', '--brief', 'b']), /unmapped exact native model/);
assert.throws(() => parseArgs(['--model', model, '--brief', 'b', '--aspect', 'Seer']), /no such aspect/);
assert.throws(() => parseArgs(['--model', model, '--brief', 'b', '--flow-id', '28d84']), /not a short Flow ID/);
assert.throws(() => parseArgs(['--model', model, '--brief', 'b', '--effort', 'high']), /bad argument: --effort/);
const o = parseArgs(['--model', model, '--brief', 'b']);
assert.equal(o.workspace, '/home/li/primary'); assert.equal(o.herdrSession, 'default'); assert.equal(o.aspect, 'Mind'); assert.equal(o.flowId, undefined);
assert.equal(parseArgs(['--model', model, '--brief', 'b', '--flow-id', '28d847']).flowId, '28d847');
assert.equal(o.opencode, 'opencode');
assert.equal(parseArgs(['--model', model, '--brief', 'b', '--opencode', '/nix/store/x/bin/opencode']).opencode, '/nix/store/x/bin/opencode');
assert.throws(() => parseArgs(['--model', model, '--brief', 'b', '--opencode', 'bin/opencode']), /must be an absolute path/);
const bad = run('--model', model);
assert.equal(bad.status, 2); assert.match(bad.stderr, /^arguments: FAILED/);

// The first prompt: every birth skill from the generated OpenCode tree, main-flow leading, then the brief.
const workspace = fs.mkdtempSync(path.join(os.tmpdir(), 'opencode-launch-test-'));
for (const name of BIRTH_SKILLS) {
  fs.mkdirSync(path.join(workspace, '.opencode', 'skills', name), {recursive: true});
  fs.writeFileSync(path.join(workspace, '.opencode', 'skills', name, 'SKILL.md'), `---\nname: ${name}\n---\n${name} body\n`);
}
const {prompt, leading} = composeFirstPrompt({workspace, brief: 'Do the thing.', read: liveSkillReader(workspace)});
assert.ok(prompt.startsWith(leading));
assert.ok(leading.startsWith(`Base directory for this skill: ${path.join(workspace, '.opencode', 'skills', 'main-flow')}`));
assert.deepEqual([...prompt.matchAll(/^Base directory for this skill: .*\/([^/\n]+)$/gm)].map(m => m[1]), BIRTH_SKILLS);
assert.ok(prompt.endsWith('# Launch brief\n\nDo the thing.\n'));
fs.writeFileSync(path.join(workspace, '.opencode', 'skills', 'vocabulary', 'SKILL.md'), '  \n');
assert.throws(() => composeFirstPrompt({workspace, brief: 'x', read: liveSkillReader(workspace)}), /skill input missing or empty: vocabulary/);
assert.throws(() => composeFirstPrompt({workspace, brief: ' ', read: () => 'text'}), /launch brief is empty/);
const composed = run('--model', model, '--brief', path.join(workspace, 'missing'), '--workspace', workspace, '--compose-only');
assert.notEqual(composed.status, 0);

// The main-flow agent replaces OpenCode's own prompt with the main-flow text.
const config = seatConfig('You are a main flow.\n', model);
assert.deepEqual(config.agent[AGENT], {description: 'A main flow seat.', mode: 'primary', model, prompt: 'You are a main flow.\n'});
assert.throws(() => seatConfig('  ', model), /system prompt is empty/);

// The harness command: parent identity dropped, Herdr's variables kept, the
// carried flow exported only when named, and the prompt read once from its file.
const command = opencodeHarnessCommand({workspace: '/w', model}, config, "/tmp/it's/first-prompt.md");
for (const name of IDENTITIES) assert.match(command, new RegExp(`-u ${name}\\b`));
assert.doesNotMatch(command, /HERDR/);
assert.doesNotMatch(command, /FLOW_ID=/);
assert.match(command, /^cd '\/w' && exec env /);
assert.match(command, /'opencode' --model 'criomos-local\/qwen3.6-35b-a3b' --agent main-flow --prompt "\$\(cat '\/tmp\/it'\\''s\/first-prompt.md'\)"$/);
const echoed = spawnSync('sh', ['-c', `printf %s ${command.match(/OPENCODE_CONFIG_CONTENT=('(?:[^']|'\\'')*')/)[1]}`], {encoding: 'utf8'});
assert.deepEqual(JSON.parse(echoed.stdout), config);
const carriedCommand = opencodeHarnessCommand({workspace: '/w', model, opencode: '/built/bin/opencode'}, config, '/p', {flowId: '28d847', directory: '/w/flows/28d847'});
assert.match(carriedCommand, / '\/built\/bin\/opencode' --model /);
assert.match(carriedCommand, /FLOW_ID='28d847' FLOW_DIRECTORY='\/w\/flows\/28d847' OPENCODE_CONFIG_CONTENT=/);

// The session is the one Herdr's OpenCode plugin reported for the pane.
const session = 'ses_efb87fbf8ffeNiz8sYspte4ulU';
assert.equal(reportedSession({agent_session: {source: 'herdr:opencode', value: session}}), session);
assert.equal(reportedSession({agent_session: {source: 'herdr:codex', value: session}}), undefined);
assert.equal(reportedSession({agent_session: {source: 'herdr:opencode', value: '01a0fdcb'}}), undefined);
assert.equal(reportedSession({agent_session: {source: 'herdr:opencode', value: 'ses_abc123'}}), undefined);
assert.equal(reportedSession({agent_session: {source: 'herdr:opencode', value: 'ses_EFB87FBF8FFENiz8sYspte4ulU'}}), undefined);
assert.equal(reportedSession(undefined), undefined);
assert.ok(hasExactRegistrationBinding({pane_id: 'p', agent_session: {value: 'ses_1'}}, 'p', 'ses_1'));
assert.ok(!hasExactRegistrationBinding({pane_id: 'p', agent_session: {value: 'ses_2'}}, 'p', 'ses_1'));

// The Flow ID is claimed through `flow-id opencode --parent-session`: a stub
// pins the argument interface; FLOW_ID_EXECUTABLE runs a real harness build.
const flowsRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'opencode-flows-'));
fs.chmodSync(flowsRoot, 0o755);
const stub = path.join(flowsRoot, '..', `${path.basename(flowsRoot)}-flow-id`);
fs.writeFileSync(stub, `#!/bin/sh\n[ "$*" = "opencode --flows-root ${flowsRoot} --parent-session ${session}" ] || { echo "unexpected: $*" >&2; exit 2; }\nmkdir -m 700 "${flowsRoot}/97a5ca" && echo 97a5ca\n`, {mode: 0o755});
assert.equal(claimFlow(flowsRoot, session, stub), '97a5ca');
fs.rmSync(path.join(flowsRoot, '97a5ca'), {recursive: true});
if (process.env.FLOW_ID_EXECUTABLE) {
  assert.equal(claimFlow(flowsRoot, session, process.env.FLOW_ID_EXECUTABLE), '97a5ca');
  assert.equal(claimFlow(flowsRoot, session, process.env.FLOW_ID_EXECUTABLE), '97a5ca');
}
fs.rmSync(flowsRoot, {recursive: true, force: true});
fs.rmSync(stub, {force: true});

// The first turn, as `opencode export` holds it.
const exported = {messages: [
  {info: {role: 'user', agent: 'main-flow'}, parts: [{type: 'text', text: 'Base directory'}, {type: 'file'}, {type: 'text', text: ' rest'}]},
  {info: {role: 'assistant', providerID: 'criomos-local', modelID: 'qwen3.6-35b-a3b'}, parts: []},
]};
assert.deepEqual(readFirstTurn(exported), {prompts: 1, text: 'Base directory rest', agent: 'main-flow', model});
assert.equal(readFirstTurn({messages: [exported.messages[0]]}).model, undefined);
assert.equal(readFirstTurn(undefined).prompts, 0);

fs.rmSync(workspace, {recursive: true, force: true});
console.log('opencode-main-flow-launch tests passed');
