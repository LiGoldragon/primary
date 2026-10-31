#!/usr/bin/env node
// Sole publisher: Git objects plus compare-and-swap metadata, never a checkout or JJ operation.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const requireFact = (ok, message) => { if (!ok) throw new Error(message); };

export function validateRequest(request) {
  requireFact(request && typeof request === 'object' && !Array.isArray(request), 'request must be an object');
  requireFact(Object.keys(request).every(key => ['paths', 'message'].includes(key)), 'only paths and message are accepted; caller base/revision is forbidden');
  requireFact(typeof request.message === 'string' && request.message.trim() && !request.message.includes('\0'), 'nonempty commit message required');
  requireFact(Array.isArray(request.paths) && request.paths.length > 0, 'explicit selected paths required');
  requireFact(new Set(request.paths).size === request.paths.length, 'duplicate selected path');
  for (const name of request.paths) {
    requireFact(typeof name === 'string' && name && !path.isAbsolute(name) && !/[\x00-\x1f*?\[\]\\]/.test(name), 'literal relative file paths only');
    requireFact(name.split('/').every(part => part && !['.', '..', '.git', '.jj'].includes(part)), 'repository metadata or path traversal forbidden');
  }
  return request;
}

function run(program, args, options = {}) {
  const result = spawnSync(program, args, {encoding: 'utf8', maxBuffer: 32 * 1024 * 1024, ...options});
  if (result.error || result.status !== 0) {
    // These call sites run only Git plumbing and Observe.Locks. Never print
    // stdin (file contents/commit message) or the process environment.
    const command = [program, ...args].map(value => JSON.stringify(value)).join(' ');
    const excerpt = value => String(value ?? '').trim().slice(0, 8192) || '(empty)';
    throw new Error(`${command} failed: status=${result.status ?? 'none'} signal=${result.signal ?? 'none'}; error=${result.error?.message ?? 'none'}; stdout=${excerpt(result.stdout)}; stderr=${excerpt(result.stderr)}`);
  }
  return result.stdout;
}

export function verifyLifetime(snapshot, flow, sentinel) {
  const match = /^\s*Observed\.Locks\.\s*\[([\s\S]*)\]\s*$/.exec(snapshot);
  requireFact(match, 'invalid lifetime lock snapshot');
  let rest = match[1];
  const rows = [];
  while (rest.trim()) {
    const row = /^\s*\{\s*(\d+)\s+(\S+)\s+(\S+)\s+\[([^\[\]]*)\]\s*(?:«[^«»]*»|[^\s{}]+)\s*\}/.exec(rest);
    requireFact(row, 'invalid lifetime lock row');
    rows.push({id: row[1], name: row[2], owner: row[3], paths: row[4].trim().split(/\s+/).filter(Boolean)});
    rest = rest.slice(row[0].length);
  }
  const relevant = rows.filter(row => row.name === 'PrimaryPublish' || row.paths.some(p => p === sentinel || sentinel.startsWith(`${p}/`)));
  requireFact(relevant.length === 1 && relevant[0].name === 'PrimaryPublish' && relevant[0].owner === flow && relevant[0].paths.length === 1 && relevant[0].paths[0] === sentinel, 'sole lifetime lock does not match current recipient');
  return relevant[0].id;
}

export function publishSelected(primary, request, {env = process.env, lockSnapshot} = {}) {
  validateRequest(request); // Reject a supplied base before even reading repository state.
  const root = fs.realpathSync(primary);
  const recipient = JSON.parse(fs.readFileSync(path.join(root, 'tools/primary-committer/recipient.json'), 'utf8')).flow_id;
  requireFact(/^[a-f0-9]{6,64}$/.test(recipient ?? '') && env.FLOW_ID === recipient, 'only the current sole recipient may publish');
  const lock = verifyLifetime(lockSnapshot ?? run('orchestrate', ['Observe.Locks'], {env, timeout: 10000}), recipient, path.join(root, '.PrimaryPublish.lock'));
  // No inherited Git index, directory, worktree, or injected command configuration.
  const gitEnv = Object.fromEntries(Object.entries(env).filter(([key]) => !key.startsWith('GIT_')));
  gitEnv.GIT_OPTIONAL_LOCKS = '0';
  const git = (args, options = {}) => run('git', ['--literal-pathspecs', '-C', root, ...args], {env: gitEnv, ...options});
  requireFact(fs.realpathSync(git(['rev-parse', '--show-toplevel']).trim()) === root, 'repository root required');
  const gitDirectory = git(['rev-parse', '--absolute-git-dir']).trim();
  const index = path.join(gitDirectory, 'index');
  const indexLock = `${index}.lock`;
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'primary-selected-publish-'));
  const lockFd = fs.openSync(indexLock, 'wx', 0o600);
  let remoteCommit = null;
  let metadataUpdated = false;
  try {
    const originalIndex = fs.readFileSync(index);
    const base = git(['rev-parse', 'HEAD']).trim();
    const headBinding = fs.readFileSync(path.join(gitDirectory, 'HEAD'), 'utf8');
    requireFact(headBinding.trim() === base || headBinding.trim() === 'ref: refs/heads/main', 'HEAD must be main or detached at current main');
    const remote = () => {
      const rows = git(['ls-remote', '--exit-code', 'origin', 'refs/heads/main'], {timeout: 30000}).trim().split('\n');
      requireFact(rows.length === 1 && rows[0].split(/\s+/)[1] === 'refs/heads/main', 'one remote main required');
      return rows[0].split(/\s+/)[0];
    };
    requireFact(remote() === base && git(['rev-parse', 'refs/heads/main']).trim() === base && git(['rev-parse', 'refs/remotes/origin/main']).trim() === base, 'shared HEAD/main/origin and fresh remote differ; no automatic repair');
    const captureIndex = path.join(temporary, 'capture.index');
    const nextIndex = path.join(temporary, 'next.index');
    fs.writeFileSync(nextIndex, originalIndex);
    const inIndex = (file, args, options = {}) => git(args, {...options, env: {...gitEnv, GIT_INDEX_FILE: file}});
    inIndex(captureIndex, ['read-tree', base]); // Private index only; no -u, no worktree operation.
    const selected = new Set(request.paths);
    const stages = git(['ls-files', '--stage', '-z']);
    requireFact(!stages.split('\0').filter(Boolean).some(row => !/^[0-7]+ [a-f0-9]+ 0\t/.test(row)), 'unmerged index; no automatic repair');
    const originalForeign = stages.split('\0').filter(row => row && !selected.has(row.slice(row.indexOf('\t') + 1))).join('\0');
    for (const name of request.paths) {
      const pieces = name.split('/');
      for (let n = 1; n < pieces.length; n++) {
        const parent = path.join(root, ...pieces.slice(0, n));
        if (!fs.existsSync(parent)) break;
        requireFact(!fs.lstatSync(parent).isSymbolicLink(), 'symlink parent forbidden');
      }
      const headEntry = git(['ls-tree', '-z', base, '--', name]).split('\0').filter(Boolean);
      requireFact(headEntry.length <= 1 && !headEntry.some(row => row.startsWith('160000 ') || row.startsWith('040000 ')), 'gitlink or directory selection requires separate source ownership');
      const filename = path.join(root, name);
      let stat;
      try { stat = fs.lstatSync(filename); } catch (error) { if (error.code !== 'ENOENT') throw error; }
      let mode = '0', blob = '0'.repeat(base.length);
      if (stat) {
        requireFact(stat.isFile() || stat.isSymbolicLink(), 'only files or symlinks may be selected');
        if (!headEntry.length) {
          // check-ignore accepts exact filenames, not Git pathspec magic. Request validation already refuses globs.
          const ignored = spawnSync('git', ['-C', root, 'check-ignore', '--quiet', '--', name], {env: gitEnv, encoding: 'utf8'});
          requireFact(ignored.status === 1, ignored.status === 0 ? 'ignored untracked path refused' : `untracked ignore check failed: ${ignored.stderr?.trim() || ignored.error?.message || ignored.status}`);
        }
        mode = stat.isSymbolicLink() ? '120000' : (stat.mode & 0o111) ? '100755' : '100644';
        const bytes = stat.isSymbolicLink() ? Buffer.from(fs.readlinkSync(filename)) : fs.readFileSync(filename);
        blob = git(['hash-object', '-w', '--stdin'], {input: bytes}).trim();
      } else requireFact(headEntry.length === 1, 'selected path is absent from both main and working copy');
      const staged = stages.split('\0').find(row => row.endsWith(`\t${name}`));
      const prior = headEntry[0]?.split('\t')[0].replace(' blob ', ' ') ?? null;
      const stagedValue = staged?.split('\t')[0].replace(/ 0$/, '') ?? null;
      const captured = mode === '0' ? null : `${mode} ${blob}`;
      let intentOnly = false;
      if (staged && prior === null && stagedValue !== captured) {
        // An empty blob alone is not intent-to-add: a user may have staged an
        // actual empty file. Require Git's CE_INTENT_TO_ADD flag as well.
        const debug = git(['ls-files', '--debug', '-z', '--', name]);
        const nul = debug.indexOf('\0');
        const flags = /\tflags: ([0-9a-f]+)\n$/.exec(debug.slice(nul + 1));
        requireFact(nul >= 0 && debug.slice(0, nul) === name && flags, 'cannot qualify selected index flags; preserve them');
        const emptyBlob = git(['hash-object', '--stdin'], {input: ''}).trim();
        intentOnly = (BigInt(`0x${flags[1]}`) & 0x20000000n) !== 0n
          && stagedValue?.split(' ')[1] === emptyBlob;
      }
      requireFact(intentOnly || stagedValue === prior || stagedValue === captured, 'selected staged bytes differ from both main and current file; preserve them');
      const entry = `${mode} ${blob}\t${name}\0`;
      inIndex(captureIndex, ['update-index', '-z', '--index-info'], {input: entry});
      inIndex(nextIndex, ['update-index', '-z', '--index-info'], {input: entry});
    }
    const nextForeign = inIndex(nextIndex, ['ls-files', '--stage', '-z']).split('\0').filter(row => row && !selected.has(row.slice(row.indexOf('\t') + 1))).join('\0');
    requireFact(nextForeign === originalForeign, 'foreign staged entries changed');
    const tree = inIndex(captureIndex, ['write-tree']).trim();
    if (tree === git(['rev-parse', `${base}^{tree}`]).trim()) return {status: 'unchanged', commit: base, lock};
    git(['diff', '--check', base, tree]);
    const changed = git(['diff', '--name-only', '-z', base, tree]).split('\0').filter(Boolean);
    requireFact(changed.every(name => selected.has(name)), 'candidate includes an unselected path');
    const commit = git(['commit-tree', tree, '-p', base], {input: `${request.message.trim()}\n`}).trim();
    requireFact(fs.readFileSync(index).equals(originalIndex) && fs.readFileSync(path.join(gitDirectory, 'HEAD'), 'utf8') === headBinding && git(['rev-parse', 'HEAD']).trim() === base && remote() === base, 'concurrent state changed before push; candidate retained, no repair');
    // Normal fast-forward only. No force, rewrite, JJ command or source-file write exists here.
    remoteCommit = commit; // A failed transport may already have published: never retry by inference.
    git(['push', 'origin', `${commit}:refs/heads/main`], {timeout: 60000});
    requireFact(remote() === commit, `push outcome differs; stop with candidate ${commit}`);
    const updates = [`update refs/heads/main ${commit} ${base}`];
    if (headBinding.trim() === base) updates.push(`update HEAD ${commit} ${base}`);
    // git push normally updates origin/main itself; compare its actual value.
    const tracking = git(['rev-parse', 'refs/remotes/origin/main']).trim();
    requireFact(tracking === base || tracking === commit, 'tracking ref changed unexpectedly');
    updates.push(`update refs/remotes/origin/main ${commit} ${tracking}`);
    fs.writeFileSync(lockFd, fs.readFileSync(nextIndex));
    fs.fsyncSync(lockFd);
    git(['update-ref', '--stdin'], {input: `start\noption no-deref\n${updates.join('\n')}\nprepare\ncommit\n`});
    fs.closeSync(lockFd);
    fs.renameSync(indexLock, index); // Only selected entries differ; payload files are never written.
    metadataUpdated = true;
    return {status: 'published', commit, parent: base, paths: changed, lock, remoteMatch: true, workingFilesWritten: 0};
  } catch (error) {
    throw new Error(`${error.message}${remoteCommit ? `; remote may contain ${remoteCommit}; no retry or rollback` : ''}; private candidate evidence: ${temporary}`);
  } finally {
    if (!metadataUpdated) { try { fs.closeSync(lockFd); } catch {} try { fs.unlinkSync(indexLock); } catch {} }
    // Keep private candidate indexes after success/failure; never clean a working tree.
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    requireFact(process.argv.length === 2, 'no CLI options or revision arguments accepted; provide JSON paths/message on stdin');
    const primary = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
    console.log(JSON.stringify(publishSelected(primary, JSON.parse(fs.readFileSync(0, 'utf8')))));
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
