import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {collectClaudeContext} from './claude-context.mjs';

const id = '11111111-1111-4111-8111-111111111111';
const other = '22222222-2222-4222-8222-222222222222';
const at = '2026-09-21T12:00:00.000Z';
const row = (type, extras = {}) => JSON.stringify({type, sessionId: id, timestamp: at, ...extras});
const usage = {input_tokens: 2, cache_creation_input_tokens: 100, cache_read_input_tokens: 900, output_tokens: 30};

function fixture(lines, statusline) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-context-'));
  const transcriptPath = path.join(dir, `${id}.jsonl`);
  fs.writeFileSync(transcriptPath, `${lines.join('\n')}\n`);
  const statuslinePath = path.join(dir, 'status.json');
  if (statusline) fs.writeFileSync(statuslinePath, JSON.stringify(statusline));
  return {transcriptPath, statuslinePath, cleanup: () => fs.rmSync(dir, {recursive: true, force: true})};
}

test('bounded transcript tail reads metadata without confusing cumulative output with occupancy', async () => {
  const f = fixture([row('assistant', {message: {model: 'claude-sonnet-5', usage}})]);
  try {
    const r = await collectClaudeContext({nativeThreadId: id, transcriptPath: f.transcriptPath, now: new Date(at).getTime() + 1000});
    assert.equal(r.occupancy.usedTokens, 1002);
    assert.equal(r.occupancy.usedPct, null);
    assert.equal(r.usage.outputTokens, 30);
    assert.equal(r.quota, null);
    assert.equal(r.model, 'claude-sonnet-5');
  } finally { f.cleanup(); }
});

test('later prompt or compaction makes prior response occupancy unknown', async () => {
  for (const later of [row('user'), row('system', {subtype: 'compact_boundary'})]) {
    const f = fixture([row('assistant', {message: {usage}}), later]);
    try {
      const r = await collectClaudeContext({nativeThreadId: id, transcriptPath: f.transcriptPath, now: Date.parse(at) + 1000});
      assert.equal(r.occupancy.usedTokens, null);
      assert.equal(r.freshness.state, 'superseded');
    } finally { f.cleanup(); }
  }
});

test('statusline exact identity supplies official live occupancy and quota', async () => {
  const f = fixture([], {session_id: id, context_window: {total_input_tokens: 500, context_window_size: 200000, used_percentage: 0.25, remaining_percentage: 99.75, current_usage: usage}, rate_limits: {seven_day: {used_percentage: 42, resets_at: 1800000000}}});
  try {
    const r = await collectClaudeContext({nativeThreadId: id, transcriptPath: f.transcriptPath, statuslinePath: f.statuslinePath, now: Date.parse(at)});
    assert.equal(r.source, 'claude-statusline');
    assert.equal(r.occupancy.usedPct, 0.25);
    assert.equal(r.quota.sevenDay.usedPct, 42);
  } finally { f.cleanup(); }
});

test('statusline reset has unknown occupancy until the next API response', async () => {
  const f = fixture([], {session_id: id, context_window: {total_input_tokens: 0, current_usage: null, used_percentage: null, remaining_percentage: null}});
  try {
    const r = await collectClaudeContext({nativeThreadId: id, statuslinePath: f.statuslinePath, now: Date.parse(at)});
    assert.equal(r.occupancy.status, 'unknown');
    assert.equal(r.occupancy.usedTokens, null);
  } finally { f.cleanup(); }
});

test('mismatched or incomplete statusline and partial transcript never fabricate zero', async () => {
  const f = fixture([row('assistant', {message: {usage}}), '{partial'], {session_id: other, context_window: {used_percentage: 1}});
  try {
    const r = await collectClaudeContext({nativeThreadId: id, transcriptPath: f.transcriptPath, statuslinePath: f.statuslinePath, now: Date.parse(at)});
    assert.equal(r.occupancy.usedTokens, null);
    assert.equal(r.occupancy.usedPct, null);
    assert.ok(r.errors.some(x => x.includes('statusline identity')));
    assert.equal(r.freshness.state, 'partial');
  } finally { f.cleanup(); }
});

test('optional publisher keeps only metadata and preserves display output', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-statusline-'));
  try {
    const input = JSON.stringify({session_id: id, cwd: '/private', context_window: {used_percentage: 12.5}, rate_limits: {seven_day: {used_percentage: 42}}});
    const command = spawnSync(process.execPath, [new URL('./claude-statusline-publish.mjs', import.meta.url).pathname, dir, 'cat'], {input, encoding: 'utf8'});
    assert.equal(command.status, 0);
    assert.equal(command.stdout, input);
    const file = path.join(dir, `${id}.json`);
    const snapshot = JSON.parse(fs.readFileSync(file, 'utf8'));
    assert.equal(snapshot.cwd, undefined);
    assert.equal(snapshot.context_window.used_percentage, 12.5);
    assert.equal(fs.statSync(file).mode & 0o777, 0o600);
  } finally { fs.rmSync(dir, {recursive: true, force: true}); }
});
