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

export function latestQuota(eventText, now = Date.now()) {
  let latest = null;
  for (const line of eventText.split('\n')) {
    try {
      const event = JSON.parse(line);
      const observed = Date.parse(event?.observedAt);
      if (event?.kind === 'quota' && event.name === 'account.primary' && Number.isFinite(event.remainingPercent) && event.remainingPercent >= 0 && event.remainingPercent <= 100 && Number.isFinite(observed) && observed <= now) latest = event;
    } catch { /* malformed historical event is ignored */ }
  }
  return latest && { remainingPercent: latest.remainingPercent, windowMinutes: latest.windowMinutes ?? null, resetsAt: latest.resetsAt ?? null, observedAt: latest.observedAt };
}

const readSnapshot = (file, limit = 8192) => {
  const text = fs.readFileSync(file, 'utf8');
  return { path: file, sha256: sha256(text), utf8_bytes: Buffer.byteLength(text), text: text.slice(-limit), truncated: Buffer.byteLength(text) > limit };
};
export function lastUserTurn(file) {
  const text = fs.readFileSync(file, 'utf8'); let found = null;
  for (const line of text.split('\n')) try {
    const record = JSON.parse(line), payload = record.payload ?? record;
    const value = record.type === 'user' ? record.message?.content : payload?.type === 'response_item' && payload.payload?.role === 'user' ? payload.payload.content?.map(x => x.text ?? '').join('') : null;
    if (typeof value === 'string') found = value;
  } catch { /* non-record lines are not user turns */ }
  return found === null ? { status: 'unavailable' } : { status: 'observed', sha256: sha256(found), utf8_bytes: Buffer.byteLength(found), text: found.slice(-8192) };
}
export function laneTip({ repo, bookmark }, { invoke = spawnSync } = {}) {
  if (!repo || !bookmark) return { status: 'unavailable' };
  const result = invoke('jj', ['log', '-r', bookmark, '-T', 'commit_id ++ " " ++ description.first_line()'], { cwd: repo, encoding: 'utf8', timeout: 10_000, maxBuffer: 4096, stdio: ['ignore', 'pipe', 'ignore'] });
  return result.status === 0 ? { status: 'observed', value: result.stdout.trim() } : { status: 'unavailable' };
}
export function collectSnapshot(config) {
  const collect = files => (files ?? []).map(file => readSnapshot(file));
  return {
    schema: 'heartbeat-snapshot/v1',
    lane_tips: collect(config.laneTips),
    peer_reports: collect(config.reportFiles),
    lane_bookmarks: (config.lanes ?? []).map(laneTip),
    last_user_turns: (config.lastUserTurnFiles ?? []).map(lastUserTurn),
  };
}

export const eventIdentity = (snapshot, decision) => sha256(JSON.stringify({ major: decision.major, lane_tips: snapshot.lane_tips.map(x => x.sha256), lane_bookmarks: snapshot.lane_bookmarks, last_user_turns: snapshot.last_user_turns.map(x => x.sha256 ?? null) }));
export const knownRecipients = config => new Map((config.recipients ?? []).filter(r => typeof r?.id === 'string' && ['codex_queue', 'prompt_relay'].includes(r.route)).map(r => [r.id, r]));
export function deliver(event, config, { invoke = spawnSync } = {}) {
  const recipients = knownRecipients(config); const results = [];
  for (const id of event.decision.recipients) {
    const recipient = recipients.get(id);
    if (!recipient) { results.push({ recipient: id, route: 'none', receipt_kind: 'pending' }); continue; }
    if (recipient.route === 'prompt_relay' && recipient.status !== 'idle') { results.push({ recipient: id, route: recipient.route, receipt_kind: 'pending' }); continue; }
    // Explicit binary and argv only: no shell and no model-produced command text.
    if (!recipient.command || !Array.isArray(recipient.argv) || !event.message_file) { results.push({ recipient: id, route: recipient.route, receipt_kind: 'pending' }); continue; }
    const argv = recipient.argv.map(value => value === '{message_file}' ? event.message_file : value);
    const result = invoke(recipient.command, argv, { encoding: 'utf8', timeout: 15_000, maxBuffer: 16_384, stdio: 'ignore' });
    results.push({ recipient: id, route: recipient.route, receipt_kind: result.status === 0 ? 'accepted' : 'pending' });
  }
  return results;
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
  const at = now(), nowMs = Date.parse(at), quota = latestQuota(fs.readFileSync(config.quotaEventLog, 'utf8'), nowMs);
  const interval = quotaInterval(quota, Date.parse(now()), config.staleAfterMinutes ?? 120);
  const snapshot = collectSnapshot(config);
  const state = config.stateFile && fs.existsSync(config.stateFile) ? JSON.parse(fs.readFileSync(config.stateFile, 'utf8')) : { sent: {} };
  if (state.nextAt && nowMs < Date.parse(state.nextAt)) return { schema: 'heartbeat/v1', at, kind: 'suppressed', quota, interval, reason: 'cadence', deliveries: [] };
  const decision = luna(snapshot), identity = eventIdentity(snapshot, decision);
  const remaining = decision.recipients.filter(id => !state.sent?.[identity]?.[id]);
  const messageFile = `${config.reportFile}.message.json`;
  const event = { schema: 'heartbeat/v1', at, kind: 'heartbeat', identity, quota, interval, decision: { ...decision, recipients: remaining }, deliveries: [], file_report: { receipt_kind: 'file_only' }, message_file: messageFile };
  fs.mkdirSync(path.dirname(config.reportFile), { recursive: true });
  fs.writeFileSync(messageFile, JSON.stringify({ type: 'Heartbeat', identity, major: decision.major, summary: decision.summary, recipients: remaining }) + '\n');
  event.deliveries = decision.major === 'none' || decision.major === 'unavailable' ? [] : deliver(event, config);
  fs.appendFileSync(config.reportFile, JSON.stringify(event) + '\n');
  if (config.stateFile) { const accepted = Object.fromEntries(event.deliveries.filter(d => d.receipt_kind === 'accepted').map(d => [d.recipient, true])); fs.mkdirSync(path.dirname(config.stateFile), { recursive: true }); fs.writeFileSync(config.stateFile, JSON.stringify({ nextAt: new Date(nowMs + interval.minutes * 60_000).toISOString(), sent: { ...(state.sent ?? {}), ...(Object.keys(accepted).length ? { [identity]: { ...(state.sent?.[identity] ?? {}), ...accepted } } : {}) } }) + '\n'); }
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
