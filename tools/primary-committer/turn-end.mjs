#!/usr/bin/env node
// A completed turn notifies the one committer. This hook never publishes.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';

function command(program, args, options = {}) {
  const result = spawnSync(program, args, {encoding: 'utf8', ...options});
  if (result.error || result.status !== 0) throw new Error(`${program} failed: ${result.error?.message ?? result.stderr?.trim() ?? result.status}`);
  return result.stdout;
}

export function notifyTurnEnd({primary, committer, committerMetaflow, event, env = process.env, run = command}) {
  const flow = env.FLOW_ID;
  const root = fs.realpathSync(primary);
  // A restored sole publisher can have a new identity while editor settings stay loaded.
  // Read the owned routing value on each invocation, not from a harness snapshot.
  const recipientFile = path.join(root, 'tools', 'primary-committer', 'recipient.json');
  if (fs.existsSync(recipientFile)) {
    const routing = JSON.parse(fs.readFileSync(recipientFile, 'utf8'));
    committer = routing.flow_id; // Runtime guard only; never an hm-send target.
    committerMetaflow = routing.metaflow;
  }
  if (!/^[a-f0-9]{6,64}$/.test(committer ?? '')) throw new Error('the standing committer FLOW_ID is required');
  if (!/^[A-Za-z0-9][A-Za-z0-9_-]* [A-Za-z0-9][A-Za-z0-9_-]* [A-Za-z0-9][A-Za-z0-9_-]*$/.test(committerMetaflow ?? ''))
    throw new Error('the standing committer registered metaflow name is required');
  if (flow === committer) return {status: 'self', notified: false, recipient: committerMetaflow};
  if (event?.hook_event_name !== 'Stop') throw new Error('this adapter requires an actual Stop event');
  const gitEnv = {...env, GIT_OPTIONAL_LOCKS: '0'};
  const actualRoot = run('git', ['-C', root, 'rev-parse', '--show-toplevel'], {env: gitEnv}).trim();
  if (fs.realpathSync(actualRoot) !== root) throw new Error('Primary must name the repository root');
  // Primary owns gitlink revisions, not uncommitted bytes inside nested repositories.
  const dirty = run('git', ['-C', root, 'status', '--porcelain=v1', '-z', '--untracked-files=normal', '--ignore-submodules=dirty'], {env: gitEnv});
  if (!dirty) return {status: 'clean', notified: false, recipient: committerMetaflow};
  if (flow && !/^[a-f0-9]{6,64}$/.test(flow)) throw new Error('FLOW_ID is malformed');
  if (typeof event.session_id !== 'string' || !event.session_id || /[\x00-\x1f]/.test(event.session_id))
    throw new Error('dirty turn has no valid native session_id');
  if (!path.isAbsolute(event.transcript_path ?? '') || !fs.statSync(event.transcript_path).isFile())
    throw new Error('dirty turn has no readable native transcript path');
  const message = [
    'Primary turn ended with dirty work. Read this firing session transcript, identify the owner’s paths, and publish through your sole deterministic selected-path tool; never move the shared working copy or accept a supplied base.',
    JSON.stringify({flow_id: flow || null, identity_kind: flow ? 'claimed_flow' : 'native_session', session_id: event.session_id, transcript_path: event.transcript_path, primary: root}),
    ...(flow ? [] : ['Only the actual native session identity is supplied. Resolve an existing flow claim from its transcript or use its demonstrated edited paths; never derive a Flow ID or invent lane ownership.']),
    'Other writers may still be editing. Report a shared-path collision; do not include their paths. Do not wake a second committer.',
  ].join('\n');
  const receipt = run('hm-send', [committerMetaflow, '--stdin'], {env, input: message, timeout: 15000});
  if (!/^Transported\./.test(receipt.trim())) throw new Error(`committer message was not transported: ${receipt.trim()}`);
  return {status: 'notified', notified: true, recipient: committerMetaflow, receipt: receipt.trim()};
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const args = process.argv.slice(2);
    if (args.length !== 4 || args[0] !== '--primary' || args[2] !== '--committer')
      throw new Error('usage: turn-end.mjs --primary ABSOLUTE_PRIMARY --committer RUNTIME_ID (recipient.json supplies registered metaflow)');
    const event = JSON.parse(fs.readFileSync(0, 'utf8'));
    console.log(JSON.stringify(notifyTurnEnd({primary: args[1], committer: args[3], event})));
  } catch (error) {
    console.error(`primary committer hook: ${error.message}`);
    process.exitCode = 1;
  }
}
