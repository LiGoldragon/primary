#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createAccountClient, createUnixWebSocketTransport } from './codex-app-server-client.mjs';
import { collectHarnessFacts } from './harness-facts.mjs';

export const failureEpisode = (previous, observed) => observed === 'active' ? false : !previous;
export const COMMAND_TIMEOUT_MS = 10_000;
export const UNIT_TIMEOUT_MS = 180_000;
export const MAX_ROSTER_ENDPOINTS = 8;
export const MAX_ROSTER_UNITS = 8;

// `claude agents --json` has no idle-since field. This mapper deliberately
// preserves that absence: an idle status alone can never satisfy the wake gate.
export const livenessFromAgents = (targets, agents) => targets.map(target => {
  const agent = agents.find(candidate => candidate.id === target.id || candidate.sessionId?.startsWith(target.id));
  if (!agent) return { name: target.name, status: 'unknown', idleMinutes: null, openWork: false };
  const status = agent.status === 'waiting' ? 'waiting' : agent.status === 'idle' ? 'idle' : 'active';
  return { name: target.name, status, idleMinutes: null, openWork: target.openWork === true && agent.state !== 'done' };
});

const quotaEvents = reading => {
  const limits = reading['account/rateLimits/read'];
  const windows = [
    ['account.primary', limits.rateLimits.primary],
    ['codex_bengalfox.primary', limits.rateLimitsByLimitId.codex_bengalfox.primary],
    ['codex_bengalfox.secondary', limits.rateLimitsByLimitId.codex_bengalfox.secondary],
  ];
  return windows.map(([name, window]) => ({
    kind: 'quota', name, status: 'observed', usedPercent: window.usedPercent,
    remainingPercent: 100 - window.usedPercent, windowMinutes: window.windowDurationMins,
    resetsAt: window.resetsAt, observedAt: reading.observedAt,
  }));
};

const collectQuota = async config => {
  const socketPath = config.quotaProbe?.socketPath;
  if (typeof socketPath !== 'string' || socketPath.length === 0) return null;
  const resolvedSocket = socketPath.replace(/^\$HOME(?=\/)/, os.homedir());
  const transport = createUnixWebSocketTransport(resolvedSocket);
  let timeout;
  try {
    const reading = await Promise.race([
      createAccountClient({ transport }).read(),
      new Promise((_, reject) => { timeout = setTimeout(() => reject(new Error('quota timeout')), 15_000); }),
    ]);
    return quotaEvents(reading);
  } catch {
    return null;
  } finally {
    clearTimeout(timeout);
    transport.close();
  }
};

const collectLiveness = config => {
  if (!Array.isArray(config.livenessProbe?.targets)) return config.liveness ?? [];
  try {
    const result = spawnSync('claude', ['agents', '--json'], { encoding: 'utf8', timeout: 15_000, maxBuffer: 1_048_576, stdio: ['ignore', 'pipe', 'ignore'] });
    if (result.status !== 0) throw new Error('agents unavailable');
    return livenessFromAgents(config.livenessProbe.targets, JSON.parse(result.stdout));
  } catch {
    return config.livenessProbe.targets.map(target => ({ name: target.name, status: 'unknown', idleMinutes: null, openWork: false }));
  }
};

export const runDeterministicCommand = (argv, { invoke = spawnSync } = {}) => {
  const result = invoke(argv[0], argv.slice(1), {
    encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], maxBuffer: 1_048_576,
    timeout: COMMAND_TIMEOUT_MS, killSignal: 'SIGKILL',
  });
  return { code: result.status ?? 1, stdout: result.stdout ?? '' };
};

export async function checkup({ run, now = () => new Date().toISOString(), endpoints = [], units = [], liveness = [], quota = null, state = {}, allowRepair = false, claimRepair = async () => {}, wake }) {
  const events = [];
  const record = event => events.push({ schema: 'core-checkup/v1', ...event });
  const observe = async (kind, name, argv) => {
    let result;
    try { result = await run(argv); } catch (error) { result = { code: 1, error: String(error.message ?? error) }; }
    const status = result.code === 0 ? 'active' : 'failed';
    record({ at: now(), kind, name, status });
    return status;
  };
  for (const endpoint of endpoints) {
    const route = await run(['ip', '-6', 'route', 'get', endpoint.address]);
    const routeText = String(route.stdout ?? '');
    const remoteRoute = route.code === 0 && /(?:^|\s)dev\s+yggTun(?:\s|$)/.test(routeText);
    const localRoute = route.code === 0 && /(?:^|\s)dev\s+lo(?:\s|$)/.test(routeText);
    const addresses = localRoute ? await run(['ip', '-6', 'addr', 'show', 'dev', 'yggTun']) : { code: 1 };
    const localYgg = localRoute && addresses.code === 0 && new RegExp(`(?:^|\\s)${endpoint.address.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?:/|\\s|$)`).test(String(addresses.stdout ?? ''));
    const transport = remoteRoute ? 'remote-ygg-route' : localYgg ? 'local-ygg-interface' : 'unverified';
    const ping = transport !== 'unverified' ? await run(['ping', '-6', '-c', '1', '-W', '3', endpoint.address]) : { code: 1 };
    record({ at: now(), kind: 'ygg', name: endpoint.name, status: transport !== 'unverified' && ping.code === 0 ? 'active' : 'failed', transport });
  }
  const nextFailures = { ...(state.failed ?? {}) };
  let repairAttempted = false;
  for (const unit of units) {
    if (unit.applicable === false) {
      record({ at: now(), kind: 'unit', name: unit.name, status: 'not-applicable', scope: unit.scope ?? 'user' });
      nextFailures[unit.name] = false;
      continue;
    }
    const unitCommand = suffix => unit.scope === 'system' ? ['systemctl', suffix, '--quiet', unit.name] : ['systemctl', '--user', suffix, '--quiet', unit.name];
    const active = await run(unitCommand('is-active'));
    let status;
    if (active.code === 0) status = 'active';
    else {
      const failed = await run(unitCommand('is-failed'));
      status = failed.code === 0 ? 'failed' : 'inactive';
    }
    record({ at: now(), kind: 'unit', name: unit.name, status });
    const prior = Boolean(state.failed?.[unit.name]);
    nextFailures[unit.name] = status === 'failed';
    if (allowRepair === true && !repairAttempted && status === 'failed' && unit.owned === true && unit.allowRestart === true && failureEpisode(prior, status)) {
      repairAttempted = true;
      await claimRepair({ failed: nextFailures });
      const repair = await observe('repair', unit.name, unit.scope === 'system' ? ['systemctl', 'restart', unit.name] : ['systemctl', '--user', 'restart', unit.name]);
      events.at(-1).action = repair === 'active' ? 'restart-attempted' : 'restart-failed';
    }
  }
  for (const item of liveness) record({ at: now(), kind: 'liveness', name: item.name, status: item.status, idleMinutes: item.idleMinutes ?? null, openWork: Boolean(item.openWork) });
  record({ at: now(), kind: 'message-semantic-health', name: 'message', status: 'unverified' });
  if (Array.isArray(quota) && quota.length > 0) for (const item of quota) record({ at: now(), ...item });
  else record({ at: now(), kind: 'quota', name: 'codex', status: 'unverified' });
  record({ at: now(), kind: 'quota', name: 'claude', status: 'unknown' });
  const primary = liveness.find(item => item.name === (wake?.primaryTarget ?? 'primary'));
  const wakeEligible = wake?.enabled === true && primary?.status === 'idle' && primary.idleMinutes >= 90 && primary.openWork;
  if (wakeEligible) {
    const receipt = await wake.send?.({ summary: events, questions: ['why idle', 'is quota low', 'which crucial items'] });
    record({ at: now(), kind: 'wake', name: 'primary', status: receipt?.accepted ? 'accepted' : 'undelivered' });
  }
  return { events, state: { failed: nextFailures } };
}

const thinFailure = (eventPath, kind, status) => {
  fs.mkdirSync(path.dirname(eventPath), { recursive: true });
  fs.appendFileSync(eventPath, JSON.stringify({ schema: 'core-checkup/v1', at: new Date().toISOString(), kind, name: 'core-checkup', status }) + '\n');
};

const main = async () => {
  const [rosterPath, policyPath, eventPath, statePath] = process.argv.slice(2);
  if (!rosterPath || !policyPath || !eventPath || !statePath) throw new Error('usage: core-checkup ROSTER POLICY EVENT_LOG STATE');
  let roster;
  let policy;
  try {
    roster = JSON.parse(fs.readFileSync(rosterPath, 'utf8'));
    policy = JSON.parse(fs.readFileSync(policyPath, 'utf8'));
    if (!Array.isArray(roster.endpoints) || roster.endpoints.length > MAX_ROSTER_ENDPOINTS || !Array.isArray(roster.units) || roster.units.length > MAX_ROSTER_UNITS || typeof roster.allowRestart !== 'boolean' || typeof policy.eventLog?.retention !== 'string' || typeof policy.allowRepair !== 'boolean' || policy.luna !== false || (policy.wake !== undefined && (typeof policy.wake !== 'object' || typeof policy.wake.enabled !== 'boolean'))) throw new Error('invalid configuration');
  } catch {
    const status = fs.existsSync(rosterPath) && fs.existsSync(policyPath) ? 'invalid' : 'missing';
    thinFailure(eventPath, 'config', status);
    throw new Error('configuration unavailable');
  }
  const rosterUnits = roster.units.filter(unit => unit && typeof unit.name === 'string' && ['user', 'system'].includes(unit.scope) && typeof unit.owned === 'boolean' && typeof unit.allowRestart === 'boolean' && (unit.applicable === undefined || typeof unit.applicable === 'boolean'));
  const policyUnits = Array.isArray(policy.units) ? policy.units : [];
  if (rosterUnits.length !== roster.units.length || policyUnits.some(unit => !unit || typeof unit.name !== 'string' || (unit.allowRestart !== undefined && typeof unit.allowRestart !== 'boolean') || (unit.applicable !== undefined && typeof unit.applicable !== 'boolean') || !rosterUnits.some(allowed => allowed.name === unit.name && allowed.scope === unit.scope))) { thinFailure(eventPath, 'config', 'invalid'); throw new Error('invalid unit policy'); }
  const policyByName = new Map(policyUnits.map(unit => [unit.name, unit]));
  const units = rosterUnits.map(unit => {
    const policyUnit = policyByName.get(unit.name) ?? {};
    return {
      ...unit,
      applicable: policyUnit.applicable === false ? false : unit.applicable,
      // The OS roster remains authoritative for identity, scope, ownership and
      // restart permission. Generic policy can only request a restart already
      // permitted by that roster.
      allowRestart: roster.allowRestart === true && unit.allowRestart === true && policyUnit.allowRestart === true,
    };
  });
  const codexTargets = (policy.harness?.codexTargets ?? []).map(target => ({ ...target, socketPath: typeof target.socketPath === 'string' ? target.socketPath.replace(/^\$HOME(?=\/)/, os.homedir()) : target.socketPath }));
  const liveness = Array.isArray(policy.harness?.codexTargets) || Array.isArray(policy.harness?.claudeTargets)
    ? (await collectHarnessFacts({ codexTargets, claudeTargets: policy.harness?.claudeTargets })).map(item => ({ name: item.targetIdentifier, status: item.state, idleMinutes: item.idleMinutes, openWork: item.openWork }))
    : collectLiveness(policy);
  const quota = await collectQuota(policy);
  // Addresses are deployment-projected input, never guessed by this job.
  let prior;
  try { prior = fs.existsSync(statePath) ? JSON.parse(fs.readFileSync(statePath, 'utf8')) : {}; }
  catch { thinFailure(eventPath, 'state', 'corrupt'); throw new Error('repair state corrupt'); }
  const writeState = state => {
    fs.mkdirSync(path.dirname(statePath), { recursive: true });
    const temporary = `${statePath}.${process.pid}.tmp`;
    fs.writeFileSync(temporary, JSON.stringify(state) + '\n');
    fs.renameSync(temporary, statePath);
  };
  try {
    const result = await checkup({ ...policy, wake: policy.wake?.enabled === true ? policy.wake : { enabled: false }, endpoints: roster.endpoints, units, liveness, quota, state: prior, claimRepair: async claimed => writeState(claimed), run: async argv => runDeterministicCommand(argv) });
    fs.appendFileSync(eventPath, result.events.map(event => JSON.stringify(event)).join('\n') + '\n');
    writeState(result.state);
  } finally { /* The parent flock holds the lifetime lock. */ }
};

const directInvocation = process.argv[1] && new URL(import.meta.url).pathname === process.argv[1];
const reportMainError = error => { process.stderr.write(`${error.message}\n`); process.exitCode = 2; };

// An advisory lock is held by `flock` for the complete child lifetime. Unlike
// an `O_EXCL` marker, SIGKILL releases it automatically; the file may remain
// as an inert lock inode and is never treated as a stale claim.
const runWithAdvisoryLock = () => {
  const args = process.argv.slice(2);
  const [, , eventPath, statePath] = args;
  if (!statePath || process.env.CORE_CHECKUP_FLOCK_HELD === '1') return main().catch(reportMainError);
  try { fs.mkdirSync(path.dirname(statePath), { recursive: true }); }
  catch { if (eventPath) thinFailure(eventPath, 'state', 'lock-unavailable'); reportMainError(new Error('repair state lock unavailable')); return; }
  const result = spawnSync('flock', ['--no-fork', '--nonblock', '--conflict-exit-code', '75', `${statePath}.lock`, process.execPath, process.argv[1], ...args], {
    env: { ...process.env, CORE_CHECKUP_FLOCK_HELD: '1' }, stdio: 'inherit', timeout: UNIT_TIMEOUT_MS, killSignal: 'SIGKILL',
  });
  if (result.error) {
    thinFailure(eventPath, 'state', 'lock-unavailable');
    reportMainError(new Error('repair state lock unavailable'));
  } else if (result.status === 75) {
    thinFailure(eventPath, 'state', 'locked');
    process.exitCode = 2;
  } else process.exitCode = result.status ?? 2;
};

if (directInvocation) runWithAdvisoryLock();
