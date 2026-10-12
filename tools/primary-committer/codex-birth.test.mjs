import assert from 'node:assert/strict';
import {test} from 'node:test';
import {spawnSync} from 'node:child_process';
import {prepareCodexBirth, codexOwnerConfig} from './codex-birth.mjs';

test('real returned identity is claimed before cold resume; no prompt or turn is sent', async () => {
  const id = '00000000-0000-4000-8000-000000000001';
  const events = [];
  const thread = {id, turns: []};
  const call = async (method, params) => {
    events.push({method, params});
    if (method === 'thread/start') return {thread};
    if (method === 'thread/unsubscribe') return {status: 'unsubscribed'};
    if (method === 'thread/resume') return {thread, model: 'gpt-6-luna', cwd: '/fixture/primary'};
    throw new Error(`unexpected RPC ${method}`);
  };
  const request = {call, claim: async native => { assert.equal(native, id); events.push({method: 'claim'}); return 'abcdef'; }, workspace: '/fixture/primary', model: 'gpt-6-luna', effort: 'low', systemPromptFile: '/fixture/system.md'};
  const result = await prepareCodexBirth(request);
  assert.deepEqual(events.map(e => e.method), ['thread/start', 'claim', 'thread/unsubscribe', 'thread/resume']);
  assert.equal(result.flowId, 'abcdef');
  assert.equal(events[3].params.config['shell_environment_policy.set.FLOW_ID'], 'abcdef');
  assert.equal(events[3].params.config['model_reasoning_effort'], 'low');
  assert.equal(events[3].params.config['hooks.Stop'], undefined);
  await assert.rejects(() => prepareCodexBirth({...request, call: async () => ({thread: {id, turns: [{}]}})}), /empty thread/);
  await assert.rejects(() => prepareCodexBirth({...request, call: async (method, p) => method === 'thread/unsubscribe' ? {status: 'notSubscribed'} : call(method, p)}), /did not detach/);
  await assert.rejects(() => prepareCodexBirth({...request, claim: async () => ''}), /claimed FLOW_ID/);
});

test('remote hook command and shell tools receive the same owner; no hook trust bypass', () => {
  const config = codexOwnerConfig('abcdef', {workspace: '/fixture/primary', committer: '123456'});
  const command = config['hooks.Stop'][0].hooks[0].command;
  assert.equal(config['shell_environment_policy.set.FLOW_ID'], 'abcdef');
  assert.ok(command.startsWith("env FLOW_ID='abcdef' "));
  assert.ok(!JSON.stringify(config).includes('bypass'));
  const prefix = command.slice(0, command.indexOf(`'${process.execPath}'`));
  const result = spawnSync('/bin/sh', ['-c', `${prefix}'${process.execPath}' -e 'process.stdout.write(process.env.FLOW_ID)'`], {encoding: 'utf8', env: {...process.env, FLOW_ID: 'parent'}});
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout, 'abcdef');
});
