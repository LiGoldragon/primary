import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';

const script = new URL('./field-flow-preflight.mjs', import.meta.url).pathname;
test('verified native and HM evidence cannot promote UnknownFlow or stale Herdr route', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'field-flow-gate-'));
  try {
    const receipt = path.join(dir, 'receipt.json');
    const registry = path.join(dir, 'registry.json');
    const flow = path.join(dir, 'flow');
    fs.writeFileSync(receipt, JSON.stringify({ status: 'verified', threadId: 'native-123' }));
    fs.writeFileSync(registry, JSON.stringify({ native_thread: 'native-123', name: 'flow-753e69', pane_id: 'wQ:pA', terminal_id: 'term-old' }));
    fs.writeFileSync(flow, '#!/bin/sh\nprintf "RecipientResolutionRejected.UnknownFlow\\n"\n', { mode: 0o700 });
    const run = spawnSync(process.execPath, [script, '--flow', '753e69', '--receipt', receipt, '--registry', registry, '--flow-bin', flow, '--nexus-bin', flow], { encoding: 'utf8' });
    assert.equal(run.status, 0, run.stderr);
    const result = JSON.parse(run.stdout);
    assert.equal(result.native.receiptAndRegistryMatch, true);
    assert.equal(result.installed.resolution, 'unknown-flow');
    assert.equal(result.readyForFlowLifecycle, false);
    assert.deepEqual(result.blockers, ['flow-unknown-flow', 'running-nexus-unverified-or-different', 'current-herdr-binding-not-witnessed', 'source-installed-parity-unproven']);
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});

test('positive path requires exact resolved identity and fresh external route and source receipts', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'field-flow-ready-'));
  try {
    const receipt = path.join(dir, 'receipt.json');
    const registry = path.join(dir, 'registry.json');
    const binding = path.join(dir, 'binding.json');
    const attestation = path.join(dir, 'source.json');
    const flow = path.join(dir, 'flow');
    const now = new Date().toISOString();
    fs.writeFileSync(receipt, JSON.stringify({ status: 'verified', threadId: 'native-123' }));
    fs.writeFileSync(registry, JSON.stringify({ native_thread: 'native-123', name: 'flow-753e69', pane_id: 'wQ:pA', terminal_id: 'term-current', session: 'managed', agent: 'codex' }));
    fs.writeFileSync(binding, JSON.stringify({ source: 'herdr-direct-read', flowId: '753e69', nativeThreadId: 'native-123', paneId: 'wQ:pA', terminalId: 'term-current', session: 'managed', agent: 'codex', readiness: 'ready', observedAt: now }));
    fs.writeFileSync(flow, '#!/bin/sh\nprintf "RecipientResolved.{ 753e69 native-123 Codex Available.{ /tmp/endpoint Ready } Available.{ managed flow-753e69 wQ:pA term-current } { 753e69 native-123 turn } Active }\\n"\n', { mode: 0o700 });
    const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
    fs.writeFileSync(attestation, JSON.stringify({ sourceRevision: 'a'.repeat(40), remoteCheck: 'passed', observedAt: now, flowSha256: sha(flow), nexusSha256: sha(process.execPath), runningNexusSha256: sha(process.execPath) }));
    const options = [script, '--flow', '753e69', '--receipt', receipt, '--registry', registry, '--flow-bin', flow, '--nexus-bin', process.execPath, '--nexus-pid', String(process.pid), '--binding-evidence', binding, '--source-attestation', attestation];
    const invoke = () => {
      const run = spawnSync(process.execPath, options, { encoding: 'utf8' });
      assert.equal(run.status, 0, run.stderr);
      return JSON.parse(run.stdout);
    };
    assert.equal(invoke().readyForFlowLifecycle, true);
    fs.writeFileSync(binding, JSON.stringify({ ...JSON.parse(fs.readFileSync(binding)), terminalId: 'term-stale' }));
    assert.equal(invoke().readyForFlowLifecycle, false);
    fs.writeFileSync(binding, JSON.stringify({ ...JSON.parse(fs.readFileSync(binding)), terminalId: 'term-current' }));
    fs.writeFileSync(flow, '#!/bin/sh\nprintf "RecipientResolved.{ other native-123 Codex Available.{ /tmp/endpoint Ready } Available.{ managed flow-753e69 wQ:pA term-current } { 753e69 native-123 turn } Active }\\n"\n', { mode: 0o700 });
    assert.equal(invoke().readyForFlowLifecycle, false);
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});

test('candidate typed CLI is queried read-only after legacy syntax refusal', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'field-flow-datom-'));
  try {
    const receipt = path.join(dir, 'receipt.json');
    const registry = path.join(dir, 'registry.json');
    const flow = path.join(dir, 'flow');
    fs.writeFileSync(receipt, JSON.stringify({ status: 'verified', threadId: 'native-123' }));
    fs.writeFileSync(registry, JSON.stringify({ native_thread: 'native-123', name: 'flow-753e69' }));
    fs.writeFileSync(flow, '#!/bin/sh\nif [ "$1" = "ResolveRecipient.753e69" ]; then printf "RecipientResolutionRejected.UnknownFlow\\n"; else exit 2; fi\n', { mode: 0o700 });
    const run = spawnSync(process.execPath, [script, '--flow', '753e69', '--receipt', receipt, '--registry', registry, '--flow-bin', flow], { encoding: 'utf8' });
    assert.equal(run.status, 0, run.stderr);
    const result = JSON.parse(run.stdout);
    assert.equal(result.installed.dialect, 'datom');
    assert.equal(result.installed.resolution, 'unknown-flow');
    assert.equal(result.readyForFlowLifecycle, false);
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});
