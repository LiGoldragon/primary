#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const nowIso = () => new Date().toISOString();
const hash = value => crypto.createHash('sha256').update(JSON.stringify(value)).digest('hex');
const models = new Set(['gpt-5.6-terra', 'gpt-5.6-luna']);
export const jobKey = job => hash({ task: job.task, sourceRevision: job.sourceRevision, outputContract: job.outputContract });

export function readState(statePath) {
  if (!fs.existsSync(statePath)) return { version: 1, jobs: {}, deadline: null };
  const value = JSON.parse(fs.readFileSync(statePath, 'utf8'));
  if (value?.version !== 1 || typeof value.jobs !== 'object') throw new Error('corrupt queue state');
  return value;
}
export function writeState(statePath, state) {
  fs.mkdirSync(path.dirname(statePath), { recursive: true });
  const temporary = `${statePath}.${process.pid}.tmp`;
  fs.writeFileSync(temporary, JSON.stringify(state, null, 2) + '\n', { mode: 0o600 });
  fs.renameSync(temporary, statePath);
}
export function acquire(lockPath) {
  fs.mkdirSync(path.dirname(lockPath), { recursive: true });
  return fs.openSync(lockPath, 'wx', 0o600);
}
export function release(lockPath, fd) { fs.closeSync(fd); fs.unlinkSync(lockPath); }
export function select(state, jobs, { now = Date.now(), deadlineMs = 8 * 60 * 60 * 1000, codexQuota } = {}) {
  if (state.deadline && now > Date.parse(state.deadline)) return null;
  if (!state.deadline) state.deadline = new Date(now + deadlineMs).toISOString();
  for (const job of jobs) {
    const key = jobKey(job), current = state.jobs[key] ?? { status: 'Pending', attempts: 0 };
    if (current.status === 'Succeeded' || current.attempts >= 2) continue;
    if (!models.has(job.model) || !job.promptHash || hash(job.prompt) !== job.promptHash || !job.workspace?.includes('overnight-') || !job.sourceRevision || !job.outputContract) continue;
    if (job.provider === 'codex' && (!codexQuota || codexQuota.status !== 'available' || now - Date.parse(codexQuota.observedAt) > 15 * 60 * 1000)) continue;
    if (!['Pending', 'Interrupted', 'Failed'].includes(current.status)) continue;
    const runId = crypto.randomUUID();
    state.jobs[key] = { ...current, status: 'Running', attempts: current.attempts + 1, runId, startedAt: new Date(now).toISOString(), ownerPid: process.pid, checkpoint: { sourceRevision: job.sourceRevision, outputContract: job.outputContract, promptHash: job.promptHash, model: job.model } };
    return { job, key, runId };
  }
  return null;
}
export function complete(state, key, runId, result) {
  const current = state.jobs[key];
  if (!current || current.status !== 'Running' || current.runId !== runId) throw new Error('stale queue completion');
  state.jobs[key] = result.ok
    ? { ...current, status: 'Succeeded', completedAt: nowIso(), outputRef: result.outputRef, outputHash: result.outputHash }
    : { ...current, status: 'Interrupted', interruptedAt: nowIso(), reason: result.reason ?? 'process-failed' };
}
export function runOnce({ statePath, lockPath, jobs, codexQuota, spawn = spawnSync }) {
  let fd;
  try { fd = acquire(lockPath); } catch { return { status: 'locked' }; }
  try {
    const state = readState(statePath);
    for (const entry of Object.values(state.jobs)) {
      if (entry.status === 'Running' && (!Number.isInteger(entry.ownerPid) || (() => { try { process.kill(entry.ownerPid, 0); return false; } catch { return true; } })())) entry.status = 'Interrupted', entry.reason = 'orphaned-owner';
    }
    const claim = select(state, jobs, { codexQuota });
    writeState(statePath, state); // Durable claim before child execution.
    if (!claim) return { status: 'idle' };
    const outputPath = path.join(path.dirname(statePath), `${claim.key}.${claim.runId}.last-message.txt`);
    const remaining = Date.parse(state.deadline) - Date.now();
    const timeout = Math.min(claim.job.timeoutMs ?? 7 * 60 * 60 * 1000, remaining);
    const child = spawn('codex', ['exec', '--json', '--sandbox', 'workspace-write', '-m', claim.job.model, '-C', claim.job.workspace, '--output-last-message', outputPath, claim.job.prompt], { stdio: 'inherit', timeout, detached: true });
    if (child.signal === 'SIGTERM' || child.error?.code === 'ETIMEDOUT') { try { process.kill(-child.pid, 'SIGKILL'); } catch {} }
    const outputHash = fs.existsSync(outputPath) ? crypto.createHash('sha256').update(fs.readFileSync(outputPath)).digest('hex') : null;
    complete(state, claim.key, claim.runId, child.status === 0 && outputHash && !child.signal
      ? { ok: true, outputRef: outputPath, outputHash }
      : { ok: false, reason: child.error?.code ?? `exit-${child.status ?? 'signal'}` });
    writeState(statePath, state);
    return { status: state.jobs[claim.key].status, key: claim.key };
  } finally { release(lockPath, fd); }
}
if (process.argv[1] === new URL(import.meta.url).pathname) {
  const [configPath, statePath, lockPath] = process.argv.slice(2);
  if (!configPath || !statePath || !lockPath) throw new Error('usage: overnight-queue CONFIG STATE LOCK');
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const result = runOnce({ statePath, lockPath, jobs: config.jobs, codexQuota: config.codexQuota ?? 'available' });
  process.stdout.write(JSON.stringify(result) + '\n');
}
