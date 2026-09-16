import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { collectSnapshot, heartbeat, latestQuota, quotaInterval, runLunaWakeCheck } from './heartbeat.mjs';

test('reads the latest monitor quota shape and slows when quota is low', () => {
  const quota = latestQuota('{"kind":"quota","name":"account.primary","remainingPercent":16,"windowMinutes":10080,"resetsAt":"2026-09-19T15:05:28Z","observedAt":"2026-09-16T15:52:39.020Z"}\n');
  assert.deepEqual(quota, { remainingPercent: 16, windowMinutes: 10080, resetsAt: '2026-09-19T15:05:28Z', observedAt: '2026-09-16T15:52:39.020Z' });
  assert.deepEqual(quotaInterval(quota, Date.parse('2026-09-16T16:00:00Z')), { minutes: 60, reason: 'quota_observed' });
  assert.deepEqual(quotaInterval(null), { minutes: 60, reason: 'quota_unknown' });
  assert.deepEqual(quotaInterval(quota, Date.parse('2026-09-16T20:00:00Z')), { minutes: 60, reason: 'quota_stale' });
});

test('records a file-only outcome and exposes only configured snapshot files', async () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'heartbeat-'));
  const quota = path.join(directory, 'events.ndjson'), tip = path.join(directory, 'tip'), report = path.join(directory, 'report'), turn = path.join(directory, 'turn'), output = path.join(directory, 'out.json');
  fs.writeFileSync(quota, '{"kind":"quota","remainingPercent":60,"observedAt":"2026-09-16T16:00:00Z"}\n'); fs.writeFileSync(tip, 'tip'); fs.writeFileSync(report, 'report'); fs.writeFileSync(turn, 'user turn');
  const config = { quotaEventLog: quota, reportFile: output, laneTips: [tip], reportFiles: [report], lastUserTurnFiles: [turn] };
  const snapshot = collectSnapshot(config); assert.deepEqual(Object.keys(snapshot), ['schema', 'lane_tips', 'peer_reports', 'last_user_turns']); assert.equal(snapshot.lane_tips[0].text, 'tip');
  const event = await heartbeat({ config, now: () => '2026-09-16T16:01:00Z', luna: () => ({ major: 'successor_ready', summary: 'v6 passed', recipients: ['efa157'] }) });
  assert.equal(event.interval.minutes, 15); assert.deepEqual(event.deliveries, [{ route: 'file', receipt_kind: 'file_only', recipients: ['efa157'] }]); assert.deepEqual(JSON.parse(fs.readFileSync(output, 'utf8')).decision.recipients, ['efa157']);
});

test('CLI writes a typed file-only event from fixture configuration', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'heartbeat-cli-'));
  const quota = path.join(directory, 'events.ndjson'), output = path.join(directory, 'report.json'), config = path.join(directory, 'config.json');
  fs.writeFileSync(quota, '{"kind":"quota","remainingPercent":3,"observedAt":"2999-01-01T00:00:00Z"}\n');
  fs.writeFileSync(config, JSON.stringify({ quotaEventLog: quota, reportFile: output, laneTips: [], reportFiles: [], lastUserTurnFiles: [] }));
  const stdout = execFileSync(process.execPath, [new URL('./heartbeat.mjs', import.meta.url).pathname, config], { encoding: 'utf8' });
  assert.equal(JSON.parse(stdout).interval.minutes, 120);
  assert.equal(JSON.parse(fs.readFileSync(output, 'utf8')).deliveries[0].receipt_kind, 'file_only');
});

test('rejects a malformed Luna response', () => {
  const result = runLunaWakeCheck({}, { invoke: (_bin, args) => { fs.writeFileSync(args[args.indexOf('--output-last-message') + 1], '{"major":"shell","summary":"bad","recipients":[]}'); return { status: 0 }; } });
  assert.equal(result.major, 'unavailable');
});
