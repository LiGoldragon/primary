#!/usr/bin/env node
/*
 * The controller starts this program for one enrolled caller.  It constructs
 * Git objects through a private index; it never changes the shared checkout.
 */
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const DEFAULT_AUTHORITY = '/run/user/1001/primary-publish/authority.json';
const DEFAULT_STATE = '/home/li/.local/state/primary-publish/state.json';
const DEFAULT_RETRIES = 2;
const fail = message => { throw new Error(message); };
const json = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const fsyncDirectory = directory => { const fd = fs.openSync(directory, 'r'); try { fs.fsyncSync(fd); } finally { fs.closeSync(fd); } };

export function atomicJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  const temporary = `${file}.tmp-${process.pid}-${crypto.randomUUID()}`;
  const fd = fs.openSync(temporary, 'wx', 0o600);
  try { fs.writeFileSync(fd, `${JSON.stringify(value, null, 2)}\n`); fs.fsyncSync(fd); }
  finally { fs.closeSync(fd); }
  fs.renameSync(temporary, file); fsyncDirectory(path.dirname(file));
}

function procIdentity(pid) {
  const fields = fs.readFileSync(`/proc/${pid}/stat`, 'utf8').trim().split(' ');
  return { pid: Number(pid), startTicks: fields[21], bootId: fs.readFileSync('/proc/sys/kernel/random/boot_id', 'utf8').trim() };
}
function privateRegular(file) {
  const fd = fs.openSync(file, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
  try {
    const stat = fs.fstatSync(fd);
    if (!stat.isFile() || stat.uid !== process.getuid() || (stat.mode & 0o777) !== 0o600) fail('authority file is not a private controller file');
    return JSON.parse(fs.readFileSync(fd, 'utf8'));
  } finally { fs.closeSync(fd); }
}
function ancestors(pid = process.pid) {
  const result = [];
  for (let current = pid; current > 1;) {
    let identity;
    try { identity = procIdentity(current); } catch { break; }
    result.push(identity);
    const fields = fs.readFileSync(`/proc/${current}/stat`, 'utf8').trim().split(' ');
    current = Number(fields[3]);
  }
  return result;
}
export function enrolledBinding(authority, processChain = ancestors()) {
  if (authority?.version !== 1 || !Array.isArray(authority.bindings)) fail('authority is malformed');
  const binding = authority.bindings.find(candidate => candidate.enabled && processChain.some(actual =>
    actual.pid === candidate.pid && actual.startTicks === String(candidate.startTicks) && actual.bootId === candidate.bootId));
  if (!binding) fail('caller is not enrolled by the controller');
  if (!path.isAbsolute(binding.laneRoot) || !Array.isArray(binding.allowedRelativePrefixes) || !Array.isArray(binding.excludedRelativePrefixes)) fail('authority binding is malformed');
  return binding;
}
function normal(relative) {
  if (typeof relative !== 'string' || !relative || /[\x00-\x1f\x7f]/.test(relative) || path.isAbsolute(relative) || relative.split('/').includes('..')) fail('path is not a safe relative path');
  const result = path.posix.normalize(relative);
  if (result === '.' || result.startsWith('../')) fail('path is not a safe relative path');
  return result;
}
function allowed(binding, relative) {
  const value = normal(relative);
  if (value === '.git' || value.startsWith('.git/') || value === '.jj' || value.startsWith('.jj/')) fail(`internal path refused: ${value}`);
  if (binding.excludedRelativePrefixes.some(prefix => value === normal(prefix) || value.startsWith(`${normal(prefix)}/`))) fail(`private path refused: ${value}`);
  if (!binding.allowedRelativePrefixes.some(prefix => value === normal(prefix) || value.startsWith(`${normal(prefix)}/`))) fail(`path is outside enrolled lane: ${value}`);
  return value;
}
function noSymlinkAncestor(root, relative) {
  let current = root;
  for (const part of relative.split('/').slice(0, -1)) {
    current = path.join(current, part);
    if (fs.lstatSync(current).isSymbolicLink()) fail(`symlink ancestor refused: ${relative}`);
  }
}
function mode(stat) { return stat.mode & 0o111 ? '100755' : '100644'; }
function fingerprint(stat) { return `${stat.dev}:${stat.ino}:${stat.size}:${stat.mtimeMs}:${stat.ctimeMs}:${stat.mode}`; }
export function captureOne(root, item) {
  const relativePath = normal(item.path); noSymlinkAncestor(root, relativePath);
  const file = path.join(root, relativePath);
  if (item.delete === true) {
    try { fs.lstatSync(file); fail(`deletion target still exists: ${relativePath}`); } catch (error) { if (error.code !== 'ENOENT') throw error; }
    noSymlinkAncestor(root, relativePath);
    try { fs.lstatSync(file); fail(`deletion target changed while captured: ${relativePath}`); } catch (error) { if (error.code !== 'ENOENT') throw error; }
    return { relativePath, present: false, explicitDelete: true, mode: null, bytes: null };
  }
  if (item.delete) fail(`invalid deletion intent: ${relativePath}`);
  const first = fs.lstatSync(file);
  let bytes, fileMode;
  if (first.isSymbolicLink()) { bytes = Buffer.from(fs.readlinkSync(file)); fileMode = '120000'; }
  else if (first.isFile()) {
    const fd = fs.openSync(file, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
    try {
      const opened = fs.fstatSync(fd), resolved = fs.realpathSync(`/proc/self/fd/${fd}`);
      if (!resolved.startsWith(`${root}/`) || fingerprint(first) !== fingerprint(opened)) fail(`path changed while captured: ${relativePath}`);
      bytes = fs.readFileSync(fd); fileMode = mode(opened);
    } finally { fs.closeSync(fd); }
  }
  else fail(`unsupported path type: ${relativePath}`);
  const second = fs.lstatSync(file);
  if (fingerprint(first) !== fingerprint(second) || (second.isSymbolicLink() && !Buffer.from(fs.readlinkSync(file)).equals(bytes))) fail(`busy editing: ${relativePath}`);
  return { relativePath, present: true, mode: fileMode, bytes };
}
function treeEntry(root, relativePath) {
  const output = git(root, ['ls-tree', '-z', 'origin/main', '--', relativePath]).stdout;
  if (!output) return { present: false, mode: null, blobOid: null };
  const row = output.split('\0')[0]; const match = /^(\d+) \w+ ([0-9a-f]+)\t(.+)$/.exec(row);
  if (!match || match[3] !== relativePath) fail(`unexpected remote tree entry: ${relativePath}`);
  return { present: true, mode: match[1], blobOid: match[2] };
}
function sameEntry(a, b) { return a.present === b.present && a.mode === b.mode && a.blobOid === b.blobOid; }
function git(root, args, options = {}) {
  const result = spawnSync('git', args, { cwd: root, encoding: 'utf8', input: options.input, env: { ...process.env, ...options.env } });
  if (result.error || result.status !== 0) fail(`git ${args[0]} failed`);
  return { stdout: result.stdout.trim(), stderr: result.stderr.trim() };
}
function stateTemplate(root, remote = 'origin', branch = 'main') { return { version: 1, repository: { root, remote, branch }, lanes: {}, requests: {}, receipts: {} }; }
function loadState(file, root) {
  if (!fs.existsSync(file)) return stateTemplate(root);
  const state = json(file);
  if (state.version !== 1 || state.repository?.root !== root || state.repository.remote !== 'origin' || state.repository.branch !== 'main') fail('publisher state is incompatible');
  return state;
}
function lock(stateFile) {
  const directory = `${stateFile}.lock`;
  try { fs.mkdirSync(directory, { mode: 0o700 }); }
  catch (error) {
    if (error.code !== 'EEXIST') throw error;
    let previous;
    try { previous = json(path.join(directory, 'owner.json')); } catch { fail('publisher lock needs controller recovery'); }
    if (!Number.isInteger(previous.pid) || typeof previous.startTicks !== 'string' || typeof previous.bootId !== 'string' || typeof previous.token !== 'string') fail('publisher lock needs controller recovery');
    let live = false;
    try { const identity = procIdentity(previous.pid); live = identity.startTicks === previous.startTicks && identity.bootId === previous.bootId; } catch {}
    if (live) fail('publisher lock is held');
    // The recorded process identity is conclusively absent or replaced.  This
    // removes only a complete, validated dead-owner record; malformed locks
    // require controller recovery rather than a stale-unlink guess.
    try { fs.unlinkSync(path.join(directory, 'owner.json')); fs.rmdirSync(directory); fs.mkdirSync(directory, { mode: 0o700 }); }
    catch { fail('publisher lock needs controller recovery'); }
  }
  const owner = { ...procIdentity(process.pid), token: crypto.randomUUID(), path: directory };
  atomicJson(path.join(directory, 'owner.json'), owner);
  return () => {
    try {
      const recorded = json(path.join(directory, 'owner.json'));
      if (recorded.token !== owner.token) return;
      fs.unlinkSync(path.join(directory, 'owner.json')); fs.rmdirSync(directory);
    } catch {}
  };
}
function snapshotDirectory(stateFile, requestId) { return path.join(path.dirname(stateFile), 'requests', crypto.createHash('sha256').update(requestId).digest('hex')); }
function storeSnapshot(directory, captured) {
  if (fs.existsSync(directory)) fail('private snapshot directory already exists');
  const requests = path.dirname(directory);
  if (fs.existsSync(requests)) {
    const parent = fs.lstatSync(requests);
    if (!parent.isDirectory() || parent.isSymbolicLink() || parent.uid !== process.getuid() || (parent.mode & 0o777) !== 0o700) fail('private snapshot parent is unsafe');
  }
  fs.mkdirSync(directory, { recursive: true, mode: 0o700 }); fs.chmodSync(requests, 0o700); fs.chmodSync(directory, 0o700);
  const entries = captured.map((entry, index) => ({ relativePath: entry.relativePath, present: entry.present, explicitDelete: entry.explicitDelete === true, mode: entry.mode, file: entry.present ? `${index}.blob` : null }));
  for (let index = 0; index < captured.length; index++) if (captured[index].present) fs.writeFileSync(path.join(directory, `${index}.blob`), captured[index].bytes, { mode: 0o600, flag: 'wx' });
  atomicJson(path.join(directory, 'manifest.json'), entries); return entries;
}
function readSnapshot(directory) {
  return json(path.join(directory, 'manifest.json')).map(entry => ({ ...entry, bytes: entry.present ? fs.readFileSync(path.join(directory, entry.file)) : null }));
}
function capturedEntry(root, entry) {
  if (!entry.present) return { present: false, mode: null, blobOid: null };
  const blobOid = git(root, ['hash-object', '-w', '--stdin'], { input: entry.bytes }).stdout;
  return { present: true, mode: entry.mode, blobOid };
}
function publishAttempt({ root, state, request, captured, stateFile, hooks = {} }) {
  for (const entry of captured) if (!entry.present) captureOne(root, { path: entry.relativePath, delete: true });
  git(root, ['fetch', 'origin', 'main']);
  const baseRemoteOid = git(root, ['rev-parse', 'origin/main']).stdout;
  const lane = state.lanes[request.bindingId] ?? { baseline: {} };
  const updates = [], already = [];
  for (const entry of captured) {
    const baseline = lane.baseline[entry.relativePath];
    if (!entry.present && !entry.explicitDelete) fail(`deletion lacks explicit intent: ${entry.relativePath}`);
    const remote = treeEntry(root, entry.relativePath), candidate = capturedEntry(root, entry);
    // A new file is the one unambiguous missing-baseline case.  A controller
    // must enroll every pre-existing or deletion target before it can land.
    if (!baseline && !remote.present && candidate.present) updates.push({ entry, candidate });
    else if (!baseline) fail(`missing enrolled baseline: ${entry.relativePath}`);
    else if (sameEntry(remote, baseline)) updates.push({ entry, candidate });
    else if (sameEntry(remote, candidate)) already.push({ entry, candidate });
    else fail(`remote owned-path conflict: ${entry.relativePath}`);
  }
  if (!updates.length) return { outcome: 'already-current', publishedPaths: already.map(update => update.entry.relativePath), updates: already };
  const index = path.join(request.snapshotDir, 'index'); const env = { GIT_INDEX_FILE: index };
  try { fs.unlinkSync(index); } catch (error) { if (error.code !== 'ENOENT') throw error; }
  git(root, ['read-tree', 'origin/main'], { env });
  for (const update of updates) {
    if (update.candidate.present) git(root, ['update-index', '--add', '--cacheinfo', `${update.candidate.mode},${update.candidate.blobOid},${update.entry.relativePath}`], { env });
    else git(root, ['update-index', '--remove', '--', update.entry.relativePath], { env });
  }
  const tree = git(root, ['write-tree'], { env }).stdout;
  const candidateOid = git(root, ['commit-tree', tree, '-p', baseRemoteOid], { input: request.description || 'Primary publish' }).stdout;
  Object.assign(request, { phase: 'prepared', baseRemoteOid, candidateOid }); atomicJson(stateFile, state);
  const current = git(root, ['ls-remote', '--refs', 'origin', 'refs/heads/main']).stdout.split(/\s+/)[0];
  if (current !== baseRemoteOid) return { outcome: 'race' };
  request.phase = 'push-uncertain'; atomicJson(stateFile, state);
  hooks.beforePush?.();
  try { git(root, ['push', 'origin', `${candidateOid}:refs/heads/main`]); }
  catch (error) {
    // A non-fast-forward after the admission read is an ordinary bounded race,
    // not an uncertain push: refresh and re-evaluate every owned path.
    try { git(root, ['fetch', 'origin', 'main']); if (git(root, ['rev-parse', 'origin/main']).stdout !== baseRemoteOid) return { outcome: 'race' }; } catch {}
    return { outcome: 'push-uncertain', error: error.message };
  }
  try { hooks.afterPush?.(); } catch (error) { return { outcome: 'push-uncertain', error: error.message }; }
  git(root, ['fetch', 'origin', 'main']);
  if (git(root, ['rev-parse', 'origin/main']).stdout !== candidateOid) return { outcome: 'push-uncertain', error: 'push result did not verify' };
  return { outcome: 'published', publishedPaths: [...updates, ...already].map(update => update.entry.relativePath), updates: [...updates, ...already] };
}
function finish(state, request, result, stateFile) {
  if (result.outcome === 'published') {
    const lane = state.lanes[request.bindingId] ??= { baseline: {} };
    for (const update of result.updates) lane.baseline[update.entry.relativePath] = update.candidate;
    request.phase = 'published'; state.receipts[request.requestId] = { outcome: 'published', publishedPaths: result.publishedPaths };
  } else if (result.outcome === 'already-current') {
    const lane = state.lanes[request.bindingId] ??= { baseline: {} };
    for (const update of result.updates) lane.baseline[update.entry.relativePath] = update.candidate;
    request.phase = 'published'; state.receipts[request.requestId] = { outcome: result.outcome, publishedPaths: result.publishedPaths };
  } else if (result.outcome === 'push-uncertain') request.lastError = result.error;
  else { request.phase = 'refused'; request.lastError = result.error || result.outcome; state.receipts[request.requestId] = { outcome: 'refused', publishedPaths: [] }; }
  atomicJson(stateFile, state);
}
export function publish(request, options = {}) {
  const authorityFile = options.authorityFile ?? DEFAULT_AUTHORITY, stateFile = options.stateFile ?? DEFAULT_STATE;
  const authority = privateRegular(authorityFile), binding = enrolledBinding(authority, options.processChain);
  if (!request || typeof request.requestId !== 'string' || !Array.isArray(request.paths) || !request.paths.length) fail('request is malformed');
  const root = binding.laneRoot, release = lock(stateFile);
  try {
    const state = loadState(stateFile, root); let stored = state.requests[request.requestId];
    if (stored?.phase === 'published') return { outcome: state.receipts[request.requestId]?.outcome ?? 'published', paths: state.receipts[request.requestId]?.publishedPaths ?? [], capturedSnapshot: true, observedPostCaptureChange: 'unknown' };
    if (!stored) {
      const wanted = request.paths.map(item => ({ path: allowed(binding, item.path), delete: item.delete === true }));
      if (new Set(wanted.map(item => item.path)).size !== wanted.length) fail('duplicate request path');
      const captured = wanted.map(item => captureOne(root, item)); const directory = snapshotDirectory(stateFile, request.requestId);
      storeSnapshot(directory, captured);
      const description = typeof request.description === 'string' ? request.description : 'Primary publish';
      if (description.length > 240 || /[\x00-\x1f\x7f]/.test(description)) fail('description is not safe');
      stored = state.requests[request.requestId] = { requestId: request.requestId, bindingId: binding.bindingId, paths: wanted, snapshotDir: directory, phase: 'captured', baseRemoteOid: null, candidateOid: null, lastError: null, description };
      atomicJson(stateFile, state);
      options.hooks?.afterCapture?.();
    }
    if (stored.bindingId !== binding.bindingId) fail('request binding differs from caller');
    if (stored.phase === 'push-uncertain') {
      git(root, ['fetch', 'origin', 'main']);
      const captured = readSnapshot(stored.snapshotDir);
      const remoteMatchesCapture = captured.every(entry => sameEntry(treeEntry(root, entry.relativePath), capturedEntry(root, entry)));
      if (stored.candidateOid && remoteMatchesCapture && git(root, ['merge-base', '--is-ancestor', stored.candidateOid, 'origin/main']).stdout === '') {
        const result = { outcome: 'published', publishedPaths: stored.paths.map(item => item.path), updates: [] };
        for (const entry of captured) result.updates.push({ entry, candidate: capturedEntry(root, entry) });
        finish(state, stored, result, stateFile); return { outcome: 'published', paths: result.publishedPaths, capturedSnapshot: true, observedPostCaptureChange: 'unknown' };
      }
      return { outcome: 'push-uncertain', paths: [], capturedSnapshot: true, observedPostCaptureChange: 'unknown' };
    }
    const captured = readSnapshot(stored.snapshotDir); let result;
    try {
      for (let attempt = 0; attempt < (options.retries ?? DEFAULT_RETRIES); attempt++) { result = publishAttempt({ root, state, request: stored, captured, stateFile, hooks: options.hooks }); if (result.outcome !== 'race') break; }
    } catch (error) { result = { outcome: 'refused', error: error.message }; }
    if (result.outcome === 'race') result = { outcome: 'refused', error: 'remote raced during bounded publication' };
    finish(state, stored, result, stateFile);
    return { outcome: result.outcome, paths: result.publishedPaths ?? [], capturedSnapshot: true, observedPostCaptureChange: 'unknown' };
  } finally { release(); }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const index = process.argv.indexOf('--request');
  if (index < 0 || !process.argv[index + 1]) { console.error('usage: primary-publish.mjs --request REQUEST.json'); process.exit(2); }
  try { console.log(JSON.stringify(publish(json(process.argv[index + 1])))); }
  catch (error) { console.log(JSON.stringify({ outcome: 'refused', paths: [], error: error.message })); process.exitCode = 1; }
}
