#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

export const majorKinds = ['main_promoted', 'activation', 'failure', 'living_word_unseen', 'successor_ready', 'none', 'unavailable'];
const sha256 = text => crypto.createHash('sha256').update(text, 'utf8').digest('hex');

export function quotaInterval(quota, now = Date.now(), staleAfterMinutes = 120) {
  if (!quota || !Number.isFinite(quota.remainingPercent) || !quota.observedAt) return { minutes: 60, reason: 'quota_unknown' };
  const age = now - Date.parse(quota.observedAt);
  if (!Number.isFinite(age) || age > staleAfterMinutes * 60_000) return { minutes: 60, reason: 'quota_stale' };
  const remaining = quota.remainingPercent;
  return { minutes: remaining >= 50 ? 15 : remaining >= 20 ? 30 : remaining >= 5 ? 60 : 120, reason: 'quota_observed' };
}

export function latestQuota(eventText) {
  let latest = null;
  for (const line of eventText.split('\n')) {
    try {
      const event = JSON.parse(line);
      if (event?.kind === 'quota' && Number.isFinite(event.remainingPercent) && event.observedAt) latest = event;
    } catch { /* malformed historical event is ignored */ }
  }
  return latest && { remainingPercent: latest.remainingPercent, windowMinutes: latest.windowMinutes ?? null, resetsAt: latest.resetsAt ?? null, observedAt: latest.observedAt };
}

const readSnapshot = (file, limit = 8192) => {
  const text = fs.readFileSync(file, 'utf8');
  return { path: file, sha256: sha256(text), utf8_bytes: Buffer.byteLength(text), text: text.slice(-limit), truncated: Buffer.byteLength(text) > limit };
};
export function collectSnapshot(config) {
  const collect = files => (files ?? []).map(file => readSnapshot(file));
  return {
    schema: 'heartbeat-snapshot/v1',
    lane_tips: collect(config.laneTips),
    peer_reports: collect(config.reportFiles),
    last_user_turns: collect(config.lastUserTurnFiles),
  };
}

const lunaSchema = { type: 'object', additionalProperties: false, required: ['major', 'summary', 'recipients'], properties: {
  major: { enum: majorKinds }, summary: { type: 'string', maxLength: 480 }, recipients: { type: 'array', maxItems: 4, items: { type: 'string', maxLength: 80 } },
} };
export function runLunaWakeCheck(snapshot, { invoke = spawnSync, cwd = process.cwd() } = {}) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'heartbeat-luna-'));
  const schemaPath = path.join(directory, 'schema.json'), outputPath = path.join(directory, 'output.json');
  try {
    fs.writeFileSync(schemaPath, JSON.stringify(lunaSchema));
    const prompt = ['You are a bounded heartbeat classifier.', 'Use only the supplied curated snapshot. Do not run commands, read files, propose commands, repair, restart, edit settings, or send messages.', 'Choose a major enum only for a concrete main promotion, activation, failure, unseen living word, or ready successor. Otherwise choose none.', JSON.stringify(snapshot)].join('\n');
    const result = invoke('codex', ['exec', '--ephemeral', '--model', 'gpt-5.6-luna', '--sandbox', 'read-only', '--cd', cwd, '--output-schema', schemaPath, '--output-last-message', outputPath, prompt], { encoding: 'utf8', timeout: 90_000, maxBuffer: 65_536, stdio: 'ignore' });
    if (result.error || result.status !== 0 || !fs.existsSync(outputPath)) return { major: 'unavailable', summary: 'Luna unavailable', recipients: [] };
    const value = JSON.parse(fs.readFileSync(outputPath, 'utf8'));
    if (!majorKinds.includes(value.major) || typeof value.summary !== 'string' || value.summary.length > 480 || !Array.isArray(value.recipients) || value.recipients.length > 4 || value.recipients.some(x => typeof x !== 'string' || x.length > 80)) throw new Error('invalid Luna result');
    return value;
  } catch { return { major: 'unavailable', summary: 'Luna unavailable', recipients: [] }; } finally { fs.rmSync(directory, { recursive: true, force: true }); }
}

export async function heartbeat({ config, now = () => new Date().toISOString(), luna = runLunaWakeCheck }) {
  const quota = latestQuota(fs.readFileSync(config.quotaEventLog, 'utf8'));
  const interval = quotaInterval(quota, Date.parse(now()), config.staleAfterMinutes ?? 120);
  const snapshot = collectSnapshot(config);
  const decision = luna(snapshot);
  const event = { schema: 'heartbeat/v1', at: now(), kind: 'heartbeat', quota, interval, decision, deliveries: [{ route: 'file', receipt_kind: 'file_only', recipients: decision.recipients }] };
  fs.mkdirSync(path.dirname(config.reportFile), { recursive: true });
  fs.writeFileSync(config.reportFile, JSON.stringify(event) + '\n');
  return event;
}

const main = async () => {
  const [configPath] = process.argv.slice(2);
  if (!configPath) throw new Error('usage: heartbeat CONFIG');
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const event = await heartbeat({ config, luna: config.luna === true ? runLunaWakeCheck : () => ({ major: 'unavailable', summary: 'Luna disabled by configuration', recipients: [] }) });
  process.stdout.write(JSON.stringify(event) + '\n');
};
if (process.argv[1] && new URL(import.meta.url).pathname === process.argv[1]) main().catch(error => { process.stderr.write(`${error.message}\n`); process.exitCode = 2; });
