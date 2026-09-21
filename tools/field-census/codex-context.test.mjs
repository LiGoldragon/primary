import assert from 'node:assert/strict';
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { collectCodexContext, latestCodexTokenEvent } from './codex-context.mjs';

const ID = '01a0c44c-784a-7fc1-bd0a-65c6db4fe4f8';
const usage = (input) => ({ input_tokens: input, cached_input_tokens: input - 2,
  cache_write_input_tokens: 0, output_tokens: 3, reasoning_output_tokens: 1,
  total_tokens: input + 3 });

test('bounded tail prefers newer per-response usage and keeps quota separate', async () => {
  const dir = await mkdtemp(path.join(os.tmpdir(), 'codex-context-test-'));
  const file = path.join(dir, `rollout-fixture-${ID}.jsonl`);
  try {
    const rows = [
      { type: 'response_item', payload: { type: 'message', content: 'do not disclose' } },
      { timestamp: '2026-09-21T15:00:00Z', type: 'event_msg', payload: { type: 'token_count',
        info: { total_token_usage: usage(10), last_token_usage: usage(8), model_context_window: 100 },
        rate_limits: { limit_id: 'codex', primary: { used_percent: 40 } } } },
      { timestamp: '2026-09-21T15:00:01Z', type: 'token_usage_record', payload: {
        usage: usage(15), turn_token_usage: usage(30), thread_token_usage: usage(80) } },
    ];
    await writeFile(file, rows.map((row) => JSON.stringify(row)).join('\n') + '\n');
    const event = await latestCodexTokenEvent(file);
    assert.equal(event.usageRecord.usage.input_tokens, 15);
    assert.equal(event.info.model_context_window, 100);
    const result = await collectCodexContext({ nativeThreadId: ID, socketPath: '/nonexistent/socket',
      rolloutPath: file, timeoutMs: 100 });
    assert.equal(result.method, 'rollout-tail-fallback');
    assert.equal(result.usage.total.inputTokens, 80);
    assert.equal(result.usage.turn.inputTokens, 30);
    assert.equal(result.occupancy.lastInputTokens, 15);
    assert.equal(result.occupancy.exactTokens, null);
    assert.equal(result.occupancy.remainingEstimateTokens, 85);
    assert.equal(result.quota.primary.used_percent, 40);
    assert.equal(result.freshness.exactBinding, false);
  } finally { await rm(dir, { recursive: true, force: true }); }
});

test('missing usage remains unknown and partial first record is ignored', async () => {
  const dir = await mkdtemp(path.join(os.tmpdir(), 'codex-context-test-'));
  const file = path.join(dir, `rollout-fixture-${ID}.jsonl`);
  try {
    await writeFile(file, `${JSON.stringify({ timestamp: 'old', type: 'token_usage_record',
      payload: { usage: usage(8), thread_token_usage: usage(10) } })}\n${'x'.repeat(200)}\n`);
    const event = await latestCodexTokenEvent(file, { maxTailBytes: 80 });
    assert.equal(event.usageRecord, null);
    assert.equal(event.tailTruncated, true);
  } finally { await rm(dir, { recursive: true, force: true }); }
});
