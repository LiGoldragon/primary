import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {createContextRefreshHook, readContextRefreshConfig, runDurableObservation, runNativeStop} from './context-refresh-hook.mjs';

const config = readContextRefreshConfig();
const identity = {nativeSessionId: '33752bfb-ebba-4e2d-ba66-be84b318e939',
  aspect: 'Psyche', topic: 'Core', layer: 'Primary', seatTarget: 'Psyche Core Primary', harness: 'claude', flowId: '42265e'};
const testConfig = {...config, bindings: [{nativeSessionId: identity.nativeSessionId, aspect: identity.aspect,
  topic: identity.topic, layer: identity.layer, seatTarget: identity.seatTarget, harness: identity.harness, model: 'claude-opus'}]};
const observation = (tokens, status = 'exact', source = 'claude-statusline', model = null) => ({source, model,
  occupancy: {status, usedTokens: tokens, lastInputTokens: null, windowTokens: 400000}, freshness: {state: 'current-snapshot'}});
const receipts = () => [];

test('below, equal, and above threshold are distinct', async () => {
  for (const [tokens, expected] of [[199999, 'below'], [200000, 'warned'], [200001, 'warned']]) {
    const calls = [];
    const hook = createContextRefreshHook({config: testConfig, delivery: async (target) => { calls.push(target); return {type: 'Presented'}; }});
    const result = await hook({identity, observation: observation(tokens)});
    assert.equal(result.state, expected);
    assert.equal(calls.length, expected === 'below' ? 0 : 2);
  }
});

test('Codex thresholds use configured model window and proxy quality', async () => {
  const hook = createContextRefreshHook({config: testConfig, delivery: async () => ({type: 'Presented'})});
  const result = await hook({identity: {...identity, contextEpoch: 2}, observation: observation(186500, 'last-input-proxy', 'codex', 'gpt-6.1-sol')});
  assert.equal(result.state, 'warned');
  assert.equal(result.measurement.threshold, 186500);
  assert.equal(result.measurement.quality, 'proxy');
});

test('configured fractions apply without runtime threshold constants', async () => {
  const tuned = {...testConfig, warningWindowFraction: 0.25, claude: {warningTokens: 100000}};
  const hook = createContextRefreshHook({config: tuned, delivery: async () => ({type: 'Presented'})});
  const result = await hook({identity: {...identity, nativeSessionId: identity.nativeSessionId}, observation: observation(100000)});
  assert.equal(result.state, 'warned');
  assert.equal(result.measurement.threshold, 100000);
});

test('Claude absolute threshold works without a context window and ignores a larger window', async () => {
  const hook = createContextRefreshHook({config: testConfig, delivery: async () => ({type: 'Presented'})});
  for (const [tokens, expected] of [[199999, 'below'], [200000, 'warned'], [200001, 'warned']]) {
    const result = await hook({identity, observation: {
      source: 'claude-transcript', model: null, occupancy: {status: 'proxy', usedTokens: tokens, windowTokens: null},
      freshness: {state: 'response-observed'}}});
    assert.equal(result.state, expected);
  }
  const larger = await hook({identity, observation: {
    source: 'claude-statusline', occupancy: {status: 'exact', usedTokens: 200000, windowTokens: 1000000}, freshness: {state: 'current-snapshot'}}});
  assert.equal(larger.state, 'warned');
  assert.equal(larger.measurement.threshold, 200000);
});

test('qualified Codex binding accepts a different aspect and layer', async () => {
  const nativeSessionId = '44444444-4444-4444-8444-444444444444';
  const mind = {nativeSessionId, aspect: 'Mind', topic: 'Core', layer: 'Secondary', seatTarget: 'Mind Core Secondary', harness: 'codex'};
  const tuned = {...testConfig, bindings: [{...mind, model: 'gpt-6-astra'}]};
  const hook = createContextRefreshHook({config: tuned, delivery: async () => ({type: 'Presented'})});
  const result = await hook({identity: mind, observation: observation(136000, 'last-input-proxy', 'codex', 'gpt-6-astra')});
  assert.equal(result.state, 'warned');
});

test('stale, mismatched, and unknown observations fail closed', async () => {
  const hook = createContextRefreshHook({config: testConfig, delivery: async () => { throw new Error('must not send'); }});
  for (const obs of [{...observation(250000), freshness: {state: 'superseded'}}, {...observation(250000), freshness: {state: 'partial'}}, {...observation(null), occupancy: {status: 'unknown'}}]) {
    const result = await hook({identity: {...identity, contextEpoch: Math.floor(Math.random() * 100) + 3}, observation: obs});
    assert.equal(result.state, 'unknown');
  }
  const refused = await hook({identity: {...identity, nativeSessionId: 'bad'}, observation: observation(300000)});
  assert.equal(refused.state, 'refused');
  const mismatch = await hook({identity: {...identity, contextEpoch: 99}, observation: {...observation(300000), nativeThreadId: '22222222-2222-4222-8222-222222222222'}});
  assert.equal(mismatch.state, 'unknown');
  const badMetadata = await hook({identity: {...identity, aspect: 'Field', seatTarget: 'Field Core Primary'}, observation: observation(300000)});
  assert.equal(badMetadata.state, 'refused');
});

test('repeated turns deduplicate and a below-threshold reset permits one new warning', async () => {
  const calls = [];
  const hook = createContextRefreshHook({config: testConfig, delivery: async (target) => { calls.push(target); return {type: 'Presented'}; }});
  assert.equal((await hook({identity, observation: observation(200000)})).state, 'warned');
  assert.equal((await hook({identity, observation: observation(210000)})).state, 'warned');
  assert.equal(calls.length, 2);
  assert.equal((await hook({identity, observation: observation(100000)})).state, 'below');
  assert.equal((await hook({identity, observation: observation(200000)})).state, 'warned');
  assert.equal(calls.length, 4);
});

test('one held recipient remains pending and only the missing recipient is retried', async () => {
  const calls = [];
  let failSeat = true;
  const hook = createContextRefreshHook({config: testConfig, delivery: async (target) => {
    calls.push(target);
    if (target === identity.seatTarget && failSeat) { failSeat = false; return {type: 'Held', reason: 'route unavailable'}; }
    return {type: 'Presented'};
  }});
  assert.equal((await hook({identity: {...identity, contextEpoch: 4}, observation: observation(200000)})).state, 'pending');
  assert.equal((await hook({identity: {...identity, contextEpoch: 4}, observation: observation(200001)})).state, 'warned');
  assert.deepEqual(calls, ['Field Core Secondary', 'Psyche Core Primary', 'Psyche Core Primary']);
});

test('handover contains judgment fields and no source content', async () => {
  const hook = createContextRefreshHook({config: testConfig, delivery: async (target, body) => { assert.deepEqual(body.decisions, []); assert.deepEqual(body.unresolvedReasons.length, 1); assert.equal(body.contextSplit.existingTopicFlows.length, 0); assert.match(body.instruction, /freshly re-read exact occupancy and last-compaction state/); return {type: 'Presented'}; }});
  await hook({identity: {...identity, contextEpoch: 5}, observation: observation(200000)});
});

test('no account, quota, transcript, or source mutation is part of the hook', () => {
  assert.equal(JSON.stringify(createContextRefreshHook.toString()).includes('readCodexAccountQuota'), false);
  assert.equal(JSON.stringify(createContextRefreshHook.toString()).includes('transcript'), false);
  assert.deepEqual(receipts(), []);
});

test('durable state deduplicates across a fresh process and is owner-only', async () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'context-refresh-state-'));
  try {
    const obs = observation(200000);
    const first = runDurableObservation({stateDirectory: directory, config: testConfig, identity, observation: obs,
      delivery: () => ({type: 'Presented'})});
    assert.equal(first.state, 'warned');
    assert.equal(fs.statSync(path.join(directory, 'state.json')).mode & 0o777, 0o600);
    const script = `import {runDurableObservation} from ${JSON.stringify(new URL('./context-refresh-hook.mjs', import.meta.url).href)};
      const identity=${JSON.stringify(identity)}; const observation=${JSON.stringify(obs)};
      const result=runDurableObservation({stateDirectory:${JSON.stringify(directory)},identity,observation,delivery:()=>({type:'Presented'})});
      process.stdout.write(JSON.stringify(result));`;
    const child = spawnSync(process.execPath, ['--input-type=module', '-e', script], {encoding: 'utf8'});
    assert.equal(child.status, 0, child.stderr);
    assert.equal(JSON.parse(child.stdout).state, 'warned');
  } finally { fs.rmSync(directory, {recursive: true, force: true}); }
});

test('native Stop input uses only session and transcript metadata', async () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'context-refresh-stop-'));
  const id = identity.nativeSessionId;
  const transcript = path.join(directory, `${id}.jsonl`);
  fs.writeFileSync(transcript, JSON.stringify({type: 'assistant', sessionId: id, timestamp: '2026-10-13T12:00:00Z',
    message: {usage: {input_tokens: 200000, cache_creation_input_tokens: 0, cache_read_input_tokens: 0, output_tokens: 1}}}) + '\n');
  try {
    const targets = [];
    const result = await runNativeStop({input: {harness: 'claude', session_id: id, transcript_path: transcript,
      last_assistant_message: 'secret content must not be read'}, stateDirectory: directory,
      delivery: (target) => { targets.push(target); return {type: 'Presented'}; }});
    assert.equal(result.state, 'warned');
    assert.deepEqual(targets, ['Field Core Secondary', 'Psyche Core Primary']);
    assert.equal(JSON.stringify(result).includes('secret content'), false);
  } finally { fs.rmSync(directory, {recursive: true, force: true}); }
});

test('Codex Stop dispatch uses session_id with explicit codex binding', async () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'context-refresh-codex-'));
  const id = '99999999-9999-4999-8999-999999999999';
  const rollout = path.join(directory, `rollout-${id}.jsonl`);
  const configPath = path.join(directory, 'config.json');
  const binding = {nativeSessionId: id, aspect: 'Mind', topic: 'Core', layer: 'Secondary', seatTarget: 'Mind Core Secondary', harness: 'codex', model: 'gpt-6-astra'};
  fs.writeFileSync(rollout, JSON.stringify({timestamp: '2026-10-13T12:00:00Z', type: 'token_usage_record', payload: {
    usage: {input_tokens: 136000}, thread_token_usage: {input_tokens: 136000}}}) + '\n');
  fs.writeFileSync(configPath, JSON.stringify({...config, bindings: [binding]}));
  try {
    const targets = [];
    const result = await runNativeStop({input: {harness: 'codex', session_id: id, transcript_path: rollout}, configPath,
      stateDirectory: path.join(directory, 'state'), delivery: target => { targets.push(target); return {type: 'Presented'}; }});
    assert.equal(result.state, 'warned');
    assert.deepEqual(targets, ['Field Core Secondary', 'Mind Core Secondary']);
  } finally { fs.rmSync(directory, {recursive: true, force: true}); }
});
