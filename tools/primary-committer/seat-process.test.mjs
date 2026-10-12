import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {test} from 'node:test';
import {seatProcessPlan, proofHook} from './seat-process.mjs';

test('dedicated server command inherits fixed seat identity; no shared wrapper or lifecycle RPC', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'committer-process-'));
  const system = path.join(root, 'system.md'); fs.writeFileSync(system, 'private fixture only');
  const binary = '/nix/store/lh877phhgv4j3yrnhf168jwcnrj4pbp5-codex-next-candidate-0.161.0-alpha.2/bin/codex';
  const options = {flowId: 'abcdef', binary, codexHome: root, socket: path.join(root, 'seat.sock'), workspace: root, systemPromptFile: system};
  const inherited = {...process.env, FLOW_ID: 'parent', CODEX_THREAD_ID: 'parent-thread'};
  const plan = seatProcessPlan(options, inherited);
  assert.equal(inherited.FLOW_ID, 'parent');
  assert.equal(plan.env.FLOW_ID, 'abcdef');
  assert.equal(plan.env.CODEX_THREAD_ID, undefined);
  assert.deepEqual(plan.args.slice(0, 3), ['app-server', '--listen', `unix://${options.socket}`]);
  assert.ok(!plan.args.some(arg => /daemon|restart|bootstrap|resume|bypass-hook/.test(arg)));
  assert.ok(plan.args.includes('model="gpt-6-luna"'));
  assert.ok(plan.args.includes('model_reasoning_effort="low"'));
  const child = spawnSync(process.execPath, ['-e', 'process.stdout.write(process.env.FLOW_ID)'], {env: plan.env, encoding: 'utf8'});
  assert.equal(child.status, 0); assert.equal(child.stdout, 'abcdef');
  const output = path.join(root, 'hook.json');
  const proof = seatProcessPlan({...options, proofOutput: output}, inherited);
  assert.ok(proof.hookProof.hash.startsWith('sha256:'));
  assert.ok(proof.args.some(arg => arg.includes('trusted_hash')));
  assert.deepEqual(proofHook(proof.hookProof.hook.command), proof.hookProof);
  // Executes just the authored hook fixture, not a native server or model.
  const event = {hook_event_name: 'SessionStart', session_id: 'native-fixture-id'};
  const hook = spawnSync(process.execPath, [path.join(import.meta.dirname, 'environment-proof.mjs'), output], {env: proof.env, input: JSON.stringify(event), encoding: 'utf8'});
  assert.equal(hook.status, 0, hook.stderr);
  assert.deepEqual(JSON.parse(fs.readFileSync(output)), {hook_event_name: 'SessionStart', native_session_id: event.session_id, flow_id: 'abcdef', child_flow_id: 'abcdef', child_exit: 0});
  assert.throws(() => seatProcessPlan({...options, binary: '/home/li/.nix-profile/bin/codex-next'}), /raw Codex binary/);
  fs.writeFileSync(options.socket, 'occupied fixture');
  assert.throws(() => seatProcessPlan(options), /already exists/);
  assert.equal(fs.readFileSync(options.socket, 'utf8'), 'occupied fixture');
});
