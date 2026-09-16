#!/usr/bin/env node
/*
 * Native Claude --bg launch preparation. This module intentionally has no
 * command-line entry point: callers must inspect the returned proof before
 * choosing to execute it.
 */
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const cleanEnvironment = environment => Object.fromEntries(Object.entries(environment).filter(([key]) => key !== 'NO_COLOR'));

function fail(message) { throw new Error(`native Claude launch refused: ${message}`); }
function artifactPath(packageDirectory, relative) {
  if (typeof relative !== 'string' || !relative || path.isAbsolute(relative)) fail('artifact path must be a non-empty relative path');
  const root = path.resolve(packageDirectory);
  const resolved = path.resolve(root, relative);
  if (resolved !== root && !resolved.startsWith(`${root}${path.sep}`)) fail(`artifact path escapes package: ${relative}`);
  return resolved;
}
function verifiedArtifacts(packageDirectory, manifest) {
  if (!Array.isArray(manifest.artifacts)) fail('manifest artifacts are missing');
  const expected = new Map(manifest.artifacts.map(artifact => [artifact.role, artifact]));
  const checked = {};
  for (const role of ['system', 'user']) {
    const artifact = expected.get(role);
    if (!artifact || typeof artifact.bytes !== 'number' || !/^[a-f0-9]{64}$/.test(artifact.sha256 ?? '')) fail(`manifest ${role} artifact is invalid`);
    const absolutePath = artifactPath(packageDirectory, artifact.path);
    const bytes = fs.readFileSync(absolutePath);
    if (bytes.length !== artifact.bytes) fail(`${role} byte count differs from manifest`);
    if (sha256(bytes) !== artifact.sha256) fail(`${role} sha256 differs from manifest`);
    checked[role] = { path: absolutePath, bytes, sha256: artifact.sha256 };
  }
  return checked;
}

export function prepareNativeClaudeLaunch({ packageDirectory, manifestPath = path.join(packageDirectory, 'manifest.json'), name, model, maxUserArgumentBytes = 262144, environment = process.env }) {
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(name ?? '')) fail('name is invalid');
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(model ?? '')) fail('model is invalid');
  if (!Number.isSafeInteger(maxUserArgumentBytes) || maxUserArgumentBytes < 1) fail('maximum user argument bytes is invalid');
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const artifacts = verifiedArtifacts(packageDirectory, manifest);
  if (artifacts.user.bytes.length > maxUserArgumentBytes) fail('user prompt exceeds configured argument limit');
  const userPrompt = artifacts.user.bytes.toString('utf8');
  if (!Buffer.from(userPrompt, 'utf8').equals(artifacts.user.bytes)) fail('user prompt is not valid UTF-8');
  const args = ['--bg', '--name', name, '--remote-control', name, '--model', model, '--append-system-prompt-file', artifacts.system.path, '--', userPrompt];
  return {
    command: 'claude', args,
    options: { cwd: path.resolve(packageDirectory), env: cleanEnvironment(environment), stdio: ['ignore', 'pipe', 'pipe'] },
    proof: {
      system: { path: artifacts.system.path, bytes: artifacts.system.bytes.length, sha256: artifacts.system.sha256, passedByFile: true },
      user: { bytes: artifacts.user.bytes.length, sha256: artifacts.user.sha256, argvIndex: args.length - 1, passedExactlyOnce: true },
      noColorAbsent: !Object.hasOwn(cleanEnvironment(environment), 'NO_COLOR'), stdin: 'DEVNULL', shell: false,
    },
  };
}

export function launchPreparedNativeClaude(plan, { spawn = spawnSync } = {}) {
  if (!plan || plan.command !== 'claude' || !Array.isArray(plan.args) || plan.options?.stdio?.[0] !== 'ignore') fail('prepared plan is invalid');
  return spawn(plan.command, plan.args, plan.options);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  console.error('native-claude-launcher is a library: prepare a plan, inspect its proof, then explicitly execute it.');
  process.exit(2);
}
