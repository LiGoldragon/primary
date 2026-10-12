#!/usr/bin/env node
// Field owns the lifetime of this one native execution process and its socket.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const quote = value => `'${value.replaceAll("'", `'\\''`)}'`;
const canonical = value => Array.isArray(value) ? value.map(canonical) : value && typeof value === 'object'
  ? Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])])) : value;

// Native 0.161.0-alpha.2 normalized command-hook trust, scoped to CLI config.
// Field must compare this hash with the actual hooks/list response before birth.
export function proofHook(command) {
  const hook = {type: 'command', command, timeout: 20, async: false};
  const identity = {event_name: 'session_start', hooks: [hook]};
  const hash = `sha256:${crypto.createHash('sha256').update(JSON.stringify(canonical(identity))).digest('hex')}`;
  return {hook, hash, key: '/<session-flags>/config.toml:session_start:0:0'};
}

export function seatProcessPlan({flowId, binary, codexHome, socket, workspace, systemPromptFile, proofOutput}, inherited = process.env) {
  if (!/^[a-f0-9]{6,64}$/.test(flowId ?? '')) throw new Error('explicit preassigned seat FLOW_ID required');
  for (const [name, value] of Object.entries({binary, codexHome, socket, workspace, systemPromptFile}))
    if (typeof value !== 'string' || !path.isAbsolute(value)) throw new Error(`${name} must be absolute`);
  if (!/^\/nix\/store\/[^/]+\/bin\/codex$/.test(binary)) throw new Error('qualified immutable raw Codex binary required; not a remote wrapper');
  if (socket.length > 100) throw new Error('seat socket path exceeds the bounded Unix socket length');
  const parent = fs.lstatSync(path.dirname(socket));
  if (!parent.isDirectory() || parent.isSymbolicLink() || parent.uid !== process.getuid() || (parent.mode & 0o077))
    throw new Error('seat socket needs its own existing owner-only directory');
  if (fs.existsSync(socket)) throw new Error('seat socket already exists; no replacement or unlink');
  for (const file of [binary, systemPromptFile]) if (!fs.statSync(file).isFile()) throw new Error(`${file} is not a file`);
  const env = {...inherited};
  for (const key of ['CODEX_THREAD_ID', 'CODEX_SESSION_ID', 'CLAUDE_CODE_SESSION_ID', 'CLAUDE_SESSION_ID', 'THREAD_ID', 'FLOW_DIRECTORY']) delete env[key];
  env.FLOW_ID = flowId;
  // Reuse the qualified existing native home/account route. Never copy credentials.
  env.CODEX_HOME = codexHome;
  const config = {model: 'gpt-6-luna', model_reasoning_effort: 'low', model_instructions_file: systemPromptFile};
  let hookProof;
  if (proofOutput !== undefined) {
    if (!path.isAbsolute(proofOutput) || fs.existsSync(proofOutput)) throw new Error('new absolute private proof output required');
    const command = [quote(process.execPath), quote(path.join(import.meta.dirname, 'environment-proof.mjs')), quote(proofOutput)].join(' ');
    hookProof = proofHook(command);
    config['features.hooks'] = true;
    config['hooks.SessionStart'] = [{hooks: [hookProof.hook]}];
    config[`hooks.state.${JSON.stringify(hookProof.key)}.enabled`] = true;
    config[`hooks.state.${JSON.stringify(hookProof.key)}.trusted_hash`] = hookProof.hash;
  }
  // JSON primitives and arrays-of-inline-tables are rendered explicitly as TOML.
  const toml = value => Array.isArray(value) ? `[${value.map(toml).join(', ')}]` : value && typeof value === 'object'
    ? `{${Object.entries(value).map(([key, item]) => `${JSON.stringify(key)} = ${toml(item)}`).join(', ')}}` : JSON.stringify(value);
  const args = ['app-server', '--listen', `unix://${socket}`];
  for (const [key, value] of Object.entries(config)) args.push('-c', `${key}=${toml(value)}`);
  return {binary, args, cwd: workspace, env, hookProof};
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const keys = {'--flow-id': 'flowId', '--binary': 'binary', '--codex-home': 'codexHome', '--socket': 'socket', '--workspace': 'workspace', '--system-prompt': 'systemPromptFile', '--proof-output': 'proofOutput'};
    const options = {};
    const args = process.argv.slice(2);
    for (let i = 0; i < args.length; i += 2) {
      const key = keys[args[i]];
      if (!key || !args[i + 1] || options[key] !== undefined) throw new Error('invalid or duplicate seat-process argument');
      options[key] = args[i + 1];
    }
    const plan = seatProcessPlan(options);
    // Deliberately no environment dump, daemon bootstrap, restart or cleanup.
    const child = spawn(plan.binary, plan.args, {cwd: plan.cwd, env: plan.env, stdio: 'inherit'});
    for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => child.kill(signal));
    child.on('error', error => { console.error(error.message); process.exitCode = 1; });
    child.on('exit', (code, signal) => { process.exitCode = code ?? (signal === 'SIGINT' ? 130 : 143); });
  } catch (error) { console.error(`committer process: ${error.message}`); process.exitCode = 1; }
}
