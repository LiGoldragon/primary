#!/usr/bin/env node
import fs from 'node:fs';

export const failureEpisode = (previous, observed) => observed === 'active' ? false : !previous;

export async function checkup({ run, now = () => new Date().toISOString(), endpoints = [], units = [], liveness = [], quota = null, state = {}, allowRepair = false, wake }) {
  const events = [];
  const observe = async (kind, name, argv) => {
    let result;
    try { result = await run(argv); } catch (error) { result = { code: 1, error: String(error.message ?? error) }; }
    const status = result.code === 0 ? 'active' : 'failed';
    events.push({ at: now(), kind, name, status });
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
  for (const item of liveness) events.push({ at: now(), kind: 'liveness', name: item.name, status: item.status, idleMinutes: item.idleMinutes ?? null, openWork: Boolean(item.openWork) });
  events.push({ at: now(), kind: 'message-semantic-health', name: 'message', status: 'unverified' });
  events.push({ at: now(), kind: 'quota', name: 'providers', status: quota ? 'observed' : 'unverified' });
  const primary = liveness.find(item => item.name === 'primary');
  const wakeEligible = primary?.status === 'idle' && primary.idleMinutes >= 90 && primary.openWork;
  if (wakeEligible) {
    const receipt = await wake?.({ summary: events, questions: ['why idle', 'is quota low', 'which crucial items'] });
    events.push({ at: now(), kind: 'wake', name: 'primary', status: receipt?.accepted ? 'accepted' : 'undelivered' });
  }
  return { events, state: { failed: nextFailures } };
}

const main = async () => {
  const [configPath, eventPath, statePath] = process.argv.slice(2);
  if (!configPath || !eventPath || !statePath) throw new Error('usage: core-checkup CONFIG EVENT_LOG STATE');
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  // Addresses are deployment-projected input, never guessed by this job.
  const prior = fs.existsSync(statePath) ? JSON.parse(fs.readFileSync(statePath, 'utf8')) : {};
  const result = await checkup({ ...config, state: prior, run: async argv => ({ code: (await import('node:child_process')).spawnSync(argv[0], argv.slice(1), { stdio: 'ignore' }).status ?? 1 }) });
  fs.appendFileSync(eventPath, result.events.map(event => JSON.stringify(event)).join('\n') + '\n');
  fs.writeFileSync(statePath, JSON.stringify(result.state) + '\n');
};
if (process.argv[1] && new URL(import.meta.url).pathname === process.argv[1]) main().catch(error => { process.stderr.write(`${error.message}\n`); process.exitCode = 2; });
