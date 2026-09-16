#!/usr/bin/env node
/* Explicit, disabled-by-default wake submission adapter. It has no scheduler. */
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import crypto from 'node:crypto';

const own = (value, keys) => value && typeof value === 'object' && !Array.isArray(value) && Object.keys(value).every(key => keys.includes(key)) && keys.every(key => Object.hasOwn(value, key));
const rejected = reason => ({ accepted: false, delivery: 'not-attempted', reason });
const eligible = observation => own(observation, ['status', 'idleMinutes', 'openWork']) && observation.status === 'idle' && Number.isFinite(observation.idleMinutes) && observation.idleMinutes >= 90 && observation.openWork === true;

export function validateConfig(config) {
  if (!own(config, ['enabled', 'targets']) || typeof config.enabled !== 'boolean' || !Array.isArray(config.targets)) throw new Error('unsafe wake configuration');
  if (config.enabled === true && config.targets.length === 0) throw new Error('enabled wake configuration needs a target');
  for (const target of config.targets) {
    if (!target || typeof target !== 'object' || Array.isArray(target) || typeof target.name !== 'string' || target.name.length === 0) throw new Error('unsafe wake target');
    if (target.kind === 'claude' && own(target, ['name', 'kind', 'sessionShort']) && typeof target.sessionShort === 'string' && target.sessionShort.length > 0) continue;
    if (target.kind === 'codex' && own(target, ['name', 'kind', 'threadId']) && typeof target.threadId === 'string' && target.threadId.length > 0) continue;
    throw new Error('unsafe wake target');
  }
  if (new Set(config.targets.map(target => target.name)).size !== config.targets.length) throw new Error('wake target names must be unique');
  return config;
}

const peerFileEnvelope = (messageFile, message) => JSON.stringify({ provenance: { source_path: messageFile, source_format: 'peer-file', source_message_id: crypto.createHash('sha256').update(message, 'utf8').digest('hex'), source_timestamp: null, sha256_utf8: crypto.createHash('sha256').update(message, 'utf8').digest('hex') } });

export async function wake(config, messageFile, observations, { run = argv => spawnSync(argv[0], argv.slice(1), { encoding: 'utf8', shell: false, timeout: 10_000, maxBuffer: 65_536, stdio: ['ignore', 'pipe', 'pipe'] }), promptRelay = path.join(path.dirname(new URL(import.meta.url).pathname), 'prompt-relay') } = {}) {
  validateConfig(config);
  if (config.enabled !== true) return { accepted: false, delivery: 'not-attempted', reason: 'disabled', results: [] };
  if (typeof messageFile !== 'string' || messageFile.length === 0) return { accepted: false, delivery: 'not-attempted', reason: 'message-file-required', results: [] };
  let message;
  try { message = fs.readFileSync(messageFile, 'utf8'); } catch { return { accepted: false, delivery: 'not-attempted', reason: 'message-file-unreadable', results: [] }; }
  if (message.length === 0) return { accepted: false, delivery: 'not-attempted', reason: 'message-file-empty', results: [] };
  const results = [];
  for (const target of config.targets) {
    const observation = observations?.[target.name];
    if (!eligible(observation)) { results.push({ name: target.name, ...rejected('not-eligible') }); continue; }
    const argv = target.kind === 'claude'
      ? [promptRelay, 'claude', '--source', messageFile, '--source-format', 'peer-file', '--session-short', target.sessionShort]
      : ['codex', 'queue', '--thread', target.threadId, '--message', `${peerFileEnvelope(messageFile, message)}\n\n${message}`];
    let result;
    try { result = await run(argv); } catch { result = { status: 1 }; }
    const code = result?.status ?? result?.code;
    const accepted = code === 0;
    results.push({ name: target.name, accepted, delivery: accepted ? 'unobserved' : 'not-accepted', reason: accepted ? undefined : 'submission-refused' });
  }
  return { accepted: results.length > 0 && results.every(result => result.accepted), delivery: results.every(result => result.delivery === 'unobserved') ? 'unobserved' : 'not-accepted', results };
}

const usage = 'usage: wake-adapter --config CONFIG.json --message-file MESSAGE.txt --observations OBSERVATIONS.json';
if (process.argv[1] && new URL(import.meta.url).pathname === process.argv[1]) {
  const args = process.argv.slice(2);
  const option = name => { const index = args.indexOf(name); if (index < 0 || args[index + 1] === undefined) throw new Error(usage); const value = args[index + 1]; args.splice(index, 2); return value; };
  try {
    const configPath = option('--config'), messageFile = option('--message-file'), observationsPath = option('--observations');
    if (args.length > 0) throw new Error(usage);
    const result = await wake(JSON.parse(fs.readFileSync(configPath, 'utf8')), messageFile, JSON.parse(fs.readFileSync(observationsPath, 'utf8')));
    process.stdout.write(JSON.stringify({ kind: 'wake-submission', ...result }) + '\n');
    if (!result.accepted) process.exitCode = 2;
  } catch (error) { process.stdout.write(JSON.stringify({ kind: 'wake-refused', accepted: false, delivery: 'not-attempted', reason: error.message }) + '\n'); process.exitCode = 2; }
}
