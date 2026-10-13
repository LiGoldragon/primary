/*
 * Turn-boundary context warning policy.
 *
 * This module consumes an observation already produced by a native context
 * collector. It never reads transcripts, credentials, account quota, or a
 * native session itself. A caller supplies the exact registered seat target
 * and a delivery function that returns a typed receipt.
 */
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {collectClaudeContext} from './field-census/claude-context.mjs';
import {collectCodexContext} from './field-census/codex-context.mjs';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const FLOW = /^[a-z0-9]{6,}$/;
const DEFAULT_CONFIG = path.resolve(new URL('../config/context-refresh.json', import.meta.url).pathname);

function positiveInteger(value) {
  return Number.isSafeInteger(value) && value > 0;
}

function exactIdentity(identity) {
  if (!identity || typeof identity !== 'object') return 'missing native identity';
  if (!UUID.test(identity.nativeSessionId || '')) return 'invalid native session identity';
  if (typeof identity.seatTarget !== 'string' || !identity.seatTarget.trim()) return 'missing registered seat target';
  if (!['Psyche', 'Mind', 'Field'].includes(identity.aspect) || typeof identity.topic !== 'string' || !identity.topic ||
      !['Primary', 'Secondary', 'Tertiary', 'Quaternary'].includes(identity.layer)) return 'incomplete typed seat identity';
  if (!['claude', 'codex'].includes(identity.harness)) return 'missing explicit harness';
  if (identity.flowId !== undefined && !FLOW.test(identity.flowId)) return 'invalid flow identity';
  return null;
}

function bindingFor(identity, config) {
  const binding = config.bindings?.find(item => item.nativeSessionId === identity.nativeSessionId);
  if (!binding) return {error: 'native identity is not in the qualified binding registry'};
  if (binding.aspect !== identity.aspect || binding.topic !== identity.topic || binding.layer !== identity.layer ||
      binding.seatTarget !== identity.seatTarget ||
      binding.harness !== identity.harness ||
      binding.seatTarget !== `${binding.aspect} ${binding.topic} ${binding.layer}`) return {error: 'native binding metadata mismatch'};
  return {binding};
}

export function readContextRefreshConfig(file = DEFAULT_CONFIG) {
  const config = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (config.version !== 1 || !(config.warningWindowFraction > 0 && config.warningWindowFraction <= 1) ||
      !positiveInteger(config.claude?.warningTokens)) {
    throw new Error('unsupported context refresh configuration');
  }
  if (!config.codex?.models || Object.values(config.codex.models).some(x => !positiveInteger(x))) {
    throw new Error('invalid Codex model windows');
  }
  if (config.recipients?.field !== 'Field Core Secondary' || !Array.isArray(config.bindings) ||
      config.bindings.some(item => !UUID.test(item.nativeSessionId || '') || !['Psyche', 'Mind', 'Field'].includes(item.aspect) ||
        !['Primary', 'Secondary', 'Tertiary', 'Quaternary'].includes(item.layer) ||
        !['claude', 'codex'].includes(item.harness) || typeof item.model !== 'string' || !item.model ||
        item.seatTarget !== `${item.aspect} ${item.topic} ${item.layer}`)) throw new Error('invalid qualified binding');
  return config;
}

function thresholdFor(observation, config) {
  const source = observation?.source;
  if (source === 'claude' || source === 'claude-statusline' || source === 'claude-transcript') {
    return {tokens: config.claude.warningTokens, quality: observation?.occupancy?.status === 'exact' ? 'exact' : 'proxy', window: observation?.occupancy?.windowTokens ?? null};
  }
  if (source !== 'codex') return {error: 'unsupported context source'};
  const model = observation.model;
  const nominal = config.codex.models[model];
  if (!positiveInteger(nominal)) return {error: 'unknown Codex model window'};
  return {tokens: Math.floor(nominal * config.warningWindowFraction), quality: 'proxy', nominal};
}

function occupancyFor(observation) {
  const occupancy = observation?.occupancy;
  if (!occupancy || observation.freshness?.state === 'superseded' || observation.freshness?.state === 'partial') {
    return {error: 'occupancy is superseded or incomplete'};
  }
  if (Number.isSafeInteger(occupancy.usedTokens) && occupancy.usedTokens >= 0) {
    return {tokens: occupancy.usedTokens, quality: occupancy.status === 'exact' ? 'exact' : 'proxy'};
  }
  if (Number.isSafeInteger(occupancy.lastInputTokens) && occupancy.lastInputTokens >= 0) {
    return {tokens: occupancy.lastInputTokens, quality: 'proxy'};
  }
  return {error: 'occupancy unavailable'};
}

function keyFor(identity) {
  return identity.nativeSessionId;
}

function above(observation, config) {
  if (observation?.nativeThreadId !== undefined && observation.nativeThreadId !== observation.identityNativeSessionId) {
    return {state: 'unknown', reason: 'observation native identity mismatch'};
  }
  const threshold = thresholdFor(observation, config);
  if (threshold.error) return {state: 'unknown', reason: threshold.error};
  const occupancy = occupancyFor(observation);
  if (occupancy.error) return {state: 'unknown', reason: occupancy.error, threshold: threshold.tokens};
  return {state: occupancy.tokens >= threshold.tokens ? 'threshold' : 'below',
    tokens: occupancy.tokens, threshold: threshold.tokens,
    quality: occupancy.quality, nominal: threshold.nominal ?? null};
}

function handover(identity, measurement) {
  return {
    kind: 'ContextRefreshHandover',
    nativeSessionId: identity.nativeSessionId,
    instruction: 'The refresh procedure has started. Before compaction or restart, Field must freshly re-read exact occupancy and last-compaction state; below threshold closes this warning. Write a judgment-only handover of decisions and unresolved reasons, name the context topics to split to existing or new topic flows, and include no facts that tools can look up. Field will compact or restart only after readiness.',
    observedTokens: measurement.tokens,
    thresholdTokens: measurement.threshold,
    measurementQuality: measurement.quality,
    action: 'refresh-started',
    decisions: [],
    unresolvedReasons: ['refresh requires recompact or a successor flow decision'],
    contextSplit: {existingTopicFlows: [], newTopicFlows: [], reason: 'seat must name topics from its own unresolved work'},
    windowTokens: measurement.window ?? measurement.nominal ?? null
  };
}

function delivered(receipt) {
  return receipt?.type === 'Presented' || receipt?.type === 'Transported';
}

export function createContextRefreshHook({config = readContextRefreshConfig(), delivery} = {}) {
  if (typeof delivery !== 'function') throw new TypeError('delivery function is required');
  const states = new Map();
  return async function observe({identity, observation}) {
    const identityError = exactIdentity(identity);
    if (identityError) return {state: 'refused', reason: identityError};
    const binding = bindingFor(identity, config);
    if (binding.error) return {state: 'refused', reason: binding.error};
    const measurement = above({...observation, identityNativeSessionId: identity.nativeSessionId}, config);
    const key = keyFor(identity);
    if (measurement.state === 'below') {
      states.delete(key);
      return {state: 'below', measurement};
    }
    if (measurement.state !== 'threshold') return {state: 'unknown', measurement};
    let state = states.get(key);
    if (!state) state = {field: false, seat: false, handover: handover(identity, measurement)};
    if (state.field && state.seat) return {state: 'warned', measurement, results: {}};
    const body = state.handover;
    const results = {};
    if (!state.field) {
      try { results.field = await delivery(config.recipients.field, body); if (delivered(results.field)) state.field = true; }
      catch (error) { results.field = {type: 'Held', reason: String(error.message || error)}; }
    }
    if (!state.seat) {
      try { results.seat = await delivery(binding.binding.seatTarget, body); if (delivered(results.seat)) state.seat = true; }
      catch (error) { results.seat = {type: 'Held', reason: String(error.message || error)}; }
    }
    if (state.field && state.seat) states.set(key, {...state, warned: true});
    else states.set(key, state);
    return {state: state.field && state.seat ? 'warned' : 'pending', measurement, results};
  };
}

function statePaths(stateDirectory) {
  return {directory: stateDirectory, file: path.join(stateDirectory, 'state.json'), lock: path.join(stateDirectory, 'state.lock')};
}

function readState(paths) {
  try { return JSON.parse(fs.readFileSync(paths.file, 'utf8')); }
  catch (error) { if (error.code === 'ENOENT') return {}; throw error; }
}

function writeState(paths, state) {
  fs.mkdirSync(paths.directory, {recursive: true, mode: 0o700});
  fs.chmodSync(paths.directory, 0o700);
  const temporary = `${paths.file}.${process.pid}.tmp`;
  fs.writeFileSync(temporary, JSON.stringify(state), {mode: 0o600});
  fs.chmodSync(temporary, 0o600);
  fs.renameSync(temporary, paths.file);
}

function withStateLock(stateDirectory, action) {
  const paths = statePaths(stateDirectory);
  fs.mkdirSync(paths.directory, {recursive: true, mode: 0o700});
  try { fs.mkdirSync(paths.lock, {mode: 0o700}); }
  catch (error) { if (error.code === 'EEXIST') throw new Error('state lock held'); throw error; }
  try { return action(paths); }
  finally { fs.rmSync(paths.lock, {recursive: true, force: true}); }
}

export function runDurableObservation({stateDirectory, config = readContextRefreshConfig(), identity, observation, delivery}) {
  const identityError = exactIdentity(identity);
  if (identityError) return {state: 'refused', reason: identityError};
  const binding = bindingFor(identity, config);
  if (binding.error) return {state: 'refused', reason: binding.error};
  if (!stateDirectory) return {state: 'refused', reason: 'XDG state directory unavailable'};
  return withStateLock(stateDirectory, paths => {
    const stored = readState(paths);
    const key = keyFor(identity);
    const previous = stored[key];
    const measurement = above({...observation, identityNativeSessionId: identity.nativeSessionId}, config);
    if (measurement.state === 'below') { delete stored[key]; writeState(paths, stored); return {state: 'below', measurement}; }
    if (measurement.state !== 'threshold') return {state: measurement.state, measurement};
    const state = previous || {field: false, seat: false, handover: handover(identity, measurement)};
    if (state.field && state.seat) return {state: 'warned', measurement, results: {}};
    const results = {};
    if (!state.field) {
      try { results.field = delivery(config.recipients.field, state.handover); }
      catch (error) { results.field = {type: 'Held', reason: String(error.message || error)}; }
      if (delivered(results.field)) state.field = true;
    }
    if (!state.seat) {
      try { results.seat = delivery(binding.binding.seatTarget, state.handover); }
      catch (error) { results.seat = {type: 'Held', reason: String(error.message || error)}; }
      if (delivered(results.seat)) state.seat = true;
    }
    stored[key] = state;
    writeState(paths, stored);
    return {state: state.field && state.seat ? 'warned' : 'pending', measurement, results};
  });
}

function option(name) {
  const index = process.argv.indexOf(name);
  return index < 0 ? null : process.argv[index + 1] || null;
}

function hmDelivery(target, body) {
  const sender = process.env.FLOW_ID;
  if (!sender) return {type: 'Held', reason: 'FLOW_ID sender identity unavailable'};
  const result = spawnSync('hm-send', [target, '--stdin'], {input: JSON.stringify(body), encoding: 'utf8', env: process.env});
  if (result.error) return {type: 'Held', reason: String(result.error.message || result.error)};
  const output = `${result.stdout || ''}${result.stderr || ''}`;
  const match = output.match(/\b(Presented|Transported|Held|Uncertain|RepairRequired)\b/);
  return match ? {type: match[1], raw: output.trim()} : {type: 'Held', reason: 'untyped messenger receipt', raw: output.trim()};
}

export async function runNativeStop({input, harness = null, configPath = DEFAULT_CONFIG, stateDirectory = process.env.XDG_STATE_HOME ? path.join(process.env.XDG_STATE_HOME, 'context-refresh-hook') : null, delivery = hmDelivery} = {}) {
  const config = readContextRefreshConfig(configPath);
  const source = harness || input.harness;
  if (!['claude', 'codex'].includes(source)) return {state: 'refused', reason: 'explicit harness is required'};
  if (input.session_id && input.thread_id && input.session_id !== input.thread_id) return {state: 'refused', reason: 'native session identity fields conflict'};
  const nativeSessionId = input.session_id || input.thread_id;
  const transcriptPath = input.transcript_path;
  if (!nativeSessionId || !transcriptPath) return {state: 'refused', reason: 'native session and transcript_path are required'};
  const observation = source === 'claude'
    ? await collectClaudeContext({nativeThreadId: nativeSessionId, transcriptPath})
    : await collectCodexContext({nativeThreadId: nativeSessionId, rolloutPath: transcriptPath});
  const binding = config.bindings.find(item => item.nativeSessionId === nativeSessionId && item.harness === source);
  if (!binding) return {state: 'refused', reason: 'native identity is not in the qualified binding registry'};
  if (source === 'codex' && !observation.model) observation.model = binding.model;
  const identity = {nativeSessionId, aspect: binding.aspect, topic: binding.topic, layer: binding.layer,
    seatTarget: binding.seatTarget, harness: source, flowId: binding.flowId};
  const verifiedDelivery = (target, body) => {
    if (binding.flowId && process.env.FLOW_ID !== binding.flowId) return {type: 'Held', reason: 'verified sender FLOW_ID unavailable or mismatched'};
    return delivery(target, body);
  };
  return runDurableObservation({stateDirectory, config, identity, observation, delivery: verifiedDelivery});
}

export { exactIdentity, thresholdFor, occupancyFor };

if (import.meta.url === `file://${process.argv[1]}`) {
  if (process.argv.includes('--help')) {
    process.stdout.write('Usage: context-refresh-hook.mjs [--config PATH] [--state-dir PATH]\n' +
      'Reads one native Stop JSON object from stdin; observes only session_id/thread_id and transcript_path;\n' +
      'uses the bounded context collector, persists owner-only dedup state, and sends typed hm-send receipts.\n');
    process.exit(0);
  }
  let input = '';
  for await (const chunk of process.stdin) input += chunk;
  try {
    const request = JSON.parse(input);
    const result = await runNativeStop({input: request, configPath: option('--config') || request.configPath || DEFAULT_CONFIG,
      stateDirectory: option('--state-dir') || request.stateDirectory || process.env.CONTEXT_REFRESH_STATE_DIR,
      delivery: hmDelivery});
    process.stdout.write(JSON.stringify(result) + '\n');
  } catch (error) {
    process.stdout.write(JSON.stringify({state: 'refused', reason: String(error.message || error)}) + '\n');
    process.exitCode = 2;
  }
}
