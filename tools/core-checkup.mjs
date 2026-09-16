#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

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
    const result = invoke('codex', ['exec', '--ephemeral', '--model', 'gpt-5.6-luna', '--sandbox', 'read-only', '--cd', cwd, '--output-schema', schemaPath, '--output-last-message', outputPath, prompt], { encoding: 'utf8', timeout: 90_000, maxBuffer: 65_536, stdio: 'ignore' });
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

export async function checkup({ run, now = () => new Date().toISOString(), endpoints = [], units = [], liveness = [], quota = null, state = {}, allowRepair = false, wake, luna = null }) {
  const events = [];
  const record = event => events.push({ schema: 'core-checkup/v1', ...event });
  const observe = async (kind, name, argv) => {
    let result;
    try { result = await run(argv); } catch (error) { result = { code: 1, error: String(error.message ?? error) }; }
    const status = result.code === 0 ? 'active' : 'failed';
    record({ at: now(), kind, name, status });
    return status;
  };
  for (const endpoint of endpoints) await observe('ygg', endpoint.name, ['ping', '-6', '-c', '1', '-W', '3', endpoint.address]);
  const nextFailures = {};
  for (const unit of units) {
    const status = await observe('unit', unit.name, unit.scope === 'system' ? ['systemctl', 'is-active', '--quiet', unit.name] : ['systemctl', '--user', 'is-active', '--quiet', unit.name]);
    const prior = Boolean(state.failed?.[unit.name]);
    nextFailures[unit.name] = status !== 'active';
    if (allowRepair && unit.owned && unit.allowRestart && failureEpisode(prior, status)) {
      const repair = await observe('repair', unit.name, unit.scope === 'system' ? ['systemctl', 'restart', unit.name] : ['systemctl', '--user', 'restart', unit.name]);
      events.at(-1).action = repair === 'active' ? 'restart-attempted' : 'restart-failed';
    }
  }
  for (const item of liveness) record({ at: now(), kind: 'liveness', name: item.name, status: item.status, idleMinutes: item.idleMinutes ?? null, openWork: Boolean(item.openWork) });
  record({ at: now(), kind: 'message-semantic-health', name: 'message', status: 'unverified' });
  record({ at: now(), kind: 'quota', name: 'providers', status: quota ? 'observed' : 'unverified' });
  const primary = liveness.find(item => item.name === 'primary');
  const wakeEligible = primary?.status === 'idle' && primary.idleMinutes >= 90 && primary.openWork;
  if (wakeEligible) {
    const receipt = await wake?.({ summary: events, questions: ['why idle', 'is quota low', 'which crucial items'] });
    record({ at: now(), kind: 'wake', name: 'primary', status: receipt?.accepted ? 'accepted' : 'undelivered' });
  }
  if (luna) {
    const result = await luna(thinSummary(events));
    record({ at: now(), kind: 'luna', name: 'core-checkup', status: result.status, findings: Array.isArray(result.findings) ? result.findings.slice(0, 3) : [] });
  }
  return { events, state: { failed: nextFailures } };
}

const main = async () => {
  const [configPath, eventPath, statePath] = process.argv.slice(2);
  if (!configPath || !eventPath || !statePath) throw new Error('usage: core-checkup CONFIG EVENT_LOG STATE');
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  // Addresses are deployment-projected input, never guessed by this job.
  const prior = fs.existsSync(statePath) ? JSON.parse(fs.readFileSync(statePath, 'utf8')) : {};
  const result = await checkup({ ...config, state: prior, luna: config.luna === true ? summary => runLunaAnalysis(summary) : null, run: async argv => ({ code: spawnSync(argv[0], argv.slice(1), { stdio: 'ignore' }).status ?? 1 }) });
  fs.appendFileSync(eventPath, result.events.map(event => JSON.stringify(event)).join('\n') + '\n');
  fs.writeFileSync(statePath, JSON.stringify(result.state) + '\n');
};
if (process.argv[1] && new URL(import.meta.url).pathname === process.argv[1]) main().catch(error => { process.stderr.write(`${error.message}\n`); process.exitCode = 2; });
