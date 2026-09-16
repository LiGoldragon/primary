#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createAccountClient, createUnixWebSocketTransport } from './codex-app-server-client.mjs';
import { collectHarnessFacts } from './harness-facts.mjs';

export const failureEpisode = (previous, observed) => observed === 'active' ? false : !previous;

const lunaSchema = {
  type: 'object',
  additionalProperties: false,
  required: ['status', 'findings'],
  properties: {
    status: { enum: ['clear', 'attention', 'unavailable'] },
    findings: { type: 'array', maxItems: 3, items: { enum: ['failed_probe', 'permission_wait', 'semantic_health_unverified', 'wake_undelivered', 'quota_unavailable', 'no_finding'] } },
  },
};

export const thinSummary = events => events.map(({ kind, name, status, idleMinutes, openWork, action }) => ({ kind, name, status, idleMinutes: idleMinutes ?? null, openWork: Boolean(openWork), action: action ?? null }));

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

export function runLunaAnalysis(events, { invoke = spawnSync, cwd = process.cwd() } = {}) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'core-checkup-luna-'));
  const schemaPath = path.join(directory, 'schema.json');
  const outputPath = path.join(directory, 'output.json');
  try {
    fs.writeFileSync(schemaPath, JSON.stringify(lunaSchema));
    const prompt = [
      'You are a bounded read-only core checkup analyst.',
      'Assess only this deterministic probe summary. Do not run commands, read files, change anything, or propose shell commands.',
      'Return the JSON-schema response only. Mark attention only for failed checks, an explicit blocked permission wait, unavailable semantic health, or an eligible wake that was undelivered.',
      JSON.stringify(thinSummary(events)),
    ].join('\n');
    const result = invoke('codex', ['exec', '--ephemeral', '--model', 'gpt-5.6-luna', '--sandbox', 'read-only', '--skip-git-repo-check', '--cd', cwd, '--output-schema', schemaPath, '--output-last-message', outputPath, prompt], { encoding: 'utf8', timeout: 90_000, maxBuffer: 65_536, stdio: 'ignore' });
    if (result.error || result.status !== 0 || !fs.existsSync(outputPath)) return { status: 'unavailable', findings: ['no_finding'] };
    const parsed = JSON.parse(fs.readFileSync(outputPath, 'utf8'));
    if (!lunaSchema.properties.status.enum.includes(parsed.status) || !Array.isArray(parsed.findings) || parsed.findings.length > 3 || parsed.findings.some(finding => !lunaSchema.properties.findings.items.enum.includes(finding))) throw new Error('invalid Luna output');
    return { status: parsed.status, findings: parsed.findings };
  } catch {
    return { status: 'unavailable', findings: ['no_finding'] };
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
}

export async function checkup({ run, now = () => new Date().toISOString(), endpoints = [], units = [], liveness = [], quota = null, state = {}, allowRepair = false, claimRepair = async () => {}, wake, luna = null }) {
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
    const routedThroughYgg = route.code === 0 && /(?:^|\s)dev\s+yggTun(?:\s|$)/.test(String(route.stdout ?? ''));
    const ping = routedThroughYgg ? await run(['ping', '-6', '-c', '1', '-W', '3', endpoint.address]) : { code: 1 };
    record({ at: now(), kind: 'ygg', name: endpoint.name, status: routedThroughYgg && ping.code === 0 ? 'active' : 'failed' });
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
    if (allowRepair && !repairAttempted && status === 'failed' && unit.owned && unit.allowRestart && failureEpisode(prior, status)) {
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
  const primary = liveness.find(item => item.name === 'primary');
  const wakeEligible = wake?.enabled === true && primary?.status === 'idle' && primary.idleMinutes >= 90 && primary.openWork;
  if (wakeEligible) {
    const receipt = await wake.send?.({ summary: events, questions: ['why idle', 'is quota low', 'which crucial items'] });
    record({ at: now(), kind: 'wake', name: 'primary', status: receipt?.accepted ? 'accepted' : 'undelivered' });
  }
  if (luna) {
    const result = await luna(thinSummary(events));
    record({ at: now(), kind: 'luna', name: 'core-checkup', status: result.status, findings: Array.isArray(result.findings) ? result.findings.slice(0, 3) : [] });
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
    if (!Array.isArray(roster.endpoints) || !Array.isArray(roster.units) || typeof roster.allowRestart !== 'boolean' || typeof policy.eventLog?.retention !== 'string') throw new Error('invalid configuration');
  } catch {
    const status = fs.existsSync(rosterPath) && fs.existsSync(policyPath) ? 'invalid' : 'missing';
    thinFailure(eventPath, 'config', status);
    throw new Error('configuration unavailable');
  }
  const rosterUnits = roster.units.filter(unit => unit && typeof unit.name === 'string' && ['user', 'system'].includes(unit.scope));
  const policyByName = new Map((Array.isArray(policy.units) ? policy.units : []).filter(unit => unit && typeof unit.name === 'string').map(unit => [unit.name, unit]));
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
  if (units.some(unit => !rosterUnits.some(allowed => allowed.name === unit.name && allowed.scope === unit.scope))) { thinFailure(eventPath, 'config', 'invalid'); throw new Error('policy added unit'); }
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
  const lockPath = `${statePath}.lock`;
  let lock;
  try { fs.mkdirSync(path.dirname(statePath), { recursive: true }); lock = fs.openSync(lockPath, 'wx'); }
  catch { thinFailure(eventPath, 'state', 'locked'); throw new Error('repair state locked'); }
  try {
    const result = await checkup({ ...policy, wake: policy.wake?.enabled === true ? policy.wake : { enabled: false }, endpoints: roster.endpoints, units, liveness, quota, state: prior, claimRepair: async claimed => writeState(claimed), luna: policy.luna === true ? summary => runLunaAnalysis(summary) : null, run: async argv => { const result = spawnSync(argv[0], argv.slice(1), { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }); return { code: result.status ?? 1, stdout: result.stdout ?? '' }; } });
    fs.appendFileSync(eventPath, result.events.map(event => JSON.stringify(event)).join('\n') + '\n');
    writeState(result.state);
  } finally { fs.closeSync(lock); fs.unlinkSync(lockPath); }
};
if (process.argv[1] && new URL(import.meta.url).pathname === process.argv[1]) main().catch(error => { process.stderr.write(`${error.message}\n`); process.exitCode = 2; });
