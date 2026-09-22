import test from 'node:test';
import assert from 'node:assert/strict';
import {analyzeHarnessVisualState} from './harness-visual-indicators.mjs';

const claudeProcess = {foreground_processes: [{argv: ['/bin/claude', '--session-id', 'fixture']}]};

test('Claude footer /rc is text-pane evidence for feature enabled only', () => {
  const r = analyzeHarnessVisualState({processInfo: claudeProcess, pane: {pane_id: 'w1:p1', terminal_id: 'term_1', agent: 'claude'},
    paneText: 'prior output\nFable 5.1·medium  ctx 58%  /rc\n'});
  assert.equal(r.harness.kind, 'claude');
  assert.equal(r.indicators.remoteControl.featureEnabled, true);
  assert.equal(r.indicators.remoteControl.evidence.grade, 'text-pane');
  assert.equal(r.indicators.remoteControl.accountAuthenticated, null);
  assert.equal(r.indicators.remoteControl.remoteUrlPresent, null);
  assert.equal(r.indicators.remoteControl.externalClientAttached, null);
  assert.equal(r.indicators.model.value, 'Fable 5.1');
  assert.equal(r.indicators.effort.value, 'medium');
  assert.equal(r.indicators.contextPercent.value, 58);
});

test('command history and remote-control prose do not become an /rc footer indicator', () => {
  const r = analyzeHarnessVisualState({processInfo: claudeProcess,
    paneText: '❯ /rc\n/remote-control is available with Claude for Enterprise\nFable 5.1·medium ctx 0%\n'});
  assert.equal(r.indicators.remoteControl.featureEnabled, null);
  assert.equal(r.indicators.remoteControl.evidence, null);
});

test('Claude footer accepts a bounded context annotation between model and effort', () => {
  const r = analyzeHarnessVisualState({processInfo: claudeProcess,
    paneText: 'Opus 4.6 (1M context)·medium  ctx 25%  wk 70% left  /rc\n'});
  assert.equal(r.indicators.model.value, 'Opus 4.6');
  assert.equal(r.indicators.effort.value, 'medium');
  assert.equal(r.indicators.remoteControl.featureEnabled, true);
});

test('expired login is negative auth evidence and never feature or reachability evidence', () => {
  const r = analyzeHarnessVisualState({processInfo: claudeProcess,
    paneText: 'Login expired · Please run /login\nNot logged in · Run /login\nFable 5.1·medium ctx 0%\n'});
  assert.equal(r.indicators.accountAuthenticated.value, false);
  assert.equal(r.indicators.accountAuthenticated.evidenceGrade, 'text-pane');
  assert.equal(r.indicators.remoteControl.featureEnabled, null);
  assert.equal(r.indicators.remoteControl.externalClientAttached, null);
});

test('accepted full-screen model observation can establish enabled while preserving other claims unknown', () => {
  const r = analyzeHarnessVisualState({paneText: '', visualObservation: {status: 'observed', fullScreen: true,
    fact: 'remote-control-indicator', enabled: true, confidence: 'high', model: 'visual-fixture'}});
  assert.equal(r.indicators.remoteControl.featureEnabled, true);
  assert.equal(r.indicators.remoteControl.evidence.grade, 'model-visual');
  assert.equal(r.indicators.remoteControl.accountAuthenticated, null);
});

test('partial, low-confidence, malformed, and negative visual observations fail closed to unknown', () => {
  for (const visualObservation of [
    {status: 'observed', fullScreen: false, fact: 'remote-control-indicator', enabled: true, confidence: 'high', model: 'x'},
    {status: 'observed', fullScreen: true, fact: 'remote-control-indicator', enabled: true, confidence: 'low', model: 'x'},
    {status: 'error'},
    {status: 'observed', fullScreen: true, fact: 'remote-control-indicator', enabled: false, confidence: 'high', model: 'x'},
  ]) {
    const r = analyzeHarnessVisualState({visualObservation});
    assert.equal(r.indicators.remoteControl.featureEnabled, null);
  }
});

test('Codex harness comes from process evidence while absent visual facts remain unknown', () => {
  const r = analyzeHarnessVisualState({processInfo: {foreground_processes: [{argv: ['/bin/codex', 'resume', 'id']}]},
    paneText: 'The report preserves /rc as feature-enabled only.\ngpt-6-astra medium · Ready · Context 20% used\n'});
  assert.equal(r.harness.kind, 'codex');
  assert.equal(r.harness.grade, 'machine');
  assert.equal(r.indicators.remoteControl.featureEnabled, null);
});

test('structured result never emits raw pane content', () => {
  const sentinel = 'OAUTH_PAIRING_SECRET_SENTINEL';
  const r = analyzeHarnessVisualState({processInfo: claudeProcess,
    paneText: `${sentinel}\nFable 5.1·medium ctx 1%\n`});
  assert.equal(JSON.stringify(r).includes(sentinel), false);
});
