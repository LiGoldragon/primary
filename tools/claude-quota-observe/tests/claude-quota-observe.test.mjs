import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { runHarness, Timeout, HarnessFailed } from '../harness.mjs';

const here = import.meta.dirname;
const tool = path.join(here, '..', 'claude-quota-observe');
const fakeClaude = path.join(here, 'fake-claude.mjs');
const fixture = name => path.join(here, '..', 'fixtures', name);

let count = 0;
const scratchStateHome = () => fs.mkdtempSync(path.join(os.tmpdir(), `claude-quota-observe-state-${count++}-`));

const run = (argument, env = {}) =>
  new Promise(resolve => {
    const child = spawn(process.execPath, [tool, argument], { env: { ...process.env, ...env } });
    let stdout = '';
    child.stdout.on('data', d => {
      stdout += d;
    });
    child.stderr.on('data', () => {});
    child.on('exit', code => resolve({ code, lines: stdout.split('\n').filter(Boolean) }));
  });

const logOf = stateHome => {
  const file = path.join(stateHome, 'claude-quota-observe', 'log.ndjson');
  if (!fs.existsSync(file)) return [];
  return fs
    .readFileSync(file, 'utf8')
    .split('\n')
    .filter(Boolean)
    .map(line => JSON.parse(line));
};

/* The real captured run: a stream-json turn with one rate_limit_event line, captured by hand
   on 2026-09-16 by running the exact harness command once against a live account. The expected
   line below is authored from that capture's own numbers (0.1, 0.66, 0.78 utilization; resetsAt
   1789822800 for seven_day; status allowed_warning), not derived by running the parser. */
{
  const stateHome = scratchStateHome();
  const out = await run(`Observe.{ Fixture.«${fixture('real-run-2026-09-16.jsonl')}» }`, { XDG_STATE_HOME: stateHome });
  assert.equal(out.code, 0);
  assert.equal(out.lines.length, 1);
  assert.equal(out.lines[0], 'QuotaObserved.{ 10 66 78 2026-09-19T13:00:00Z allowed_warning }');
  const log = logOf(stateHome);
  assert.equal(log.length, 1);
  assert.equal(log[0].kind, 'QuotaObserved');
  assert.equal(log[0].fiveHourPercentUsed, 10);
  assert.equal(log[0].sevenDayPercentUsed, 66);
  assert.equal(log[0].overagePercentUsed, 78);
  assert.equal(log[0].sevenDayResetsAtIso, '2026-09-19T13:00:00Z');
  assert.equal(log[0].status, 'allowed_warning');
}

/* A stream that never carries a rate_limit_event line at all: refused, nothing logged. */
{
  const stateHome = scratchStateHome();
  const out = await run(`Observe.{ Fixture.«${fixture('no-rate-limit-event.jsonl')}» }`, { XDG_STATE_HOME: stateHome });
  assert.equal(out.code, 2);
  assert.equal(out.lines.length, 1);
  assert.equal(out.lines[0], 'ObserveRefused.NoRateLimitEvent');
  assert.deepEqual(logOf(stateHome), []);
}

/* A stream cut off mid-write, before any rate_limit_event line completed: the half-written
   line is skipped, not parsed as data, so this refuses the same way an absent event does. */
{
  const stateHome = scratchStateHome();
  const out = await run(`Observe.{ Fixture.«${fixture('truncated.jsonl')}» }`, { XDG_STATE_HOME: stateHome });
  assert.equal(out.code, 2);
  assert.equal(out.lines.length, 1);
  assert.equal(out.lines[0], 'ObserveRefused.NoRateLimitEvent');
  assert.deepEqual(logOf(stateHome), []);
}

/* A malformed request is refused before any fixture is read or harness run. */
{
  const stateHome = scratchStateHome();
  const out = await run('Nonsense.{ 1 }', { XDG_STATE_HOME: stateHome });
  assert.equal(out.code, 2);
  assert.match(out.lines[0], /^ObserveRefused\.«malformedRequest:/);
  assert.deepEqual(logOf(stateHome), []);
}

/* runHarness against a fake claude, invoked as `node fake-claude.mjs` rather than through its
   own shebang (a build sandbox need not have /usr/bin/env, the same reason the CLI itself is
   always spawned as `node claude-quota-observe` above): a clean success returns exactly the
   stdout it wrote. */
{
  const text = await runHarness({
    command: process.execPath,
    args: [fakeClaude],
    timeoutMs: 5000,
    env: { ...process.env, FAKE_CLAUDE_MODE: 'success', FAKE_CLAUDE_FIXTURE: fixture('real-run-2026-09-16.jsonl') },
  });
  assert.equal(text, fs.readFileSync(fixture('real-run-2026-09-16.jsonl'), 'utf8'));
}

/* runHarness against a fake claude that exits nonzero: HarnessFailed carries the exit code. */
{
  let caught = null;
  try {
    await runHarness({
      command: process.execPath,
      args: [fakeClaude],
      timeoutMs: 5000,
      env: { ...process.env, FAKE_CLAUDE_MODE: 'exit-nonzero', FAKE_CLAUDE_EXIT_CODE: '17' },
    });
  } catch (error) {
    caught = error;
  }
  assert.ok(caught instanceof HarnessFailed);
  assert.equal(caught.exitCode, 17);
}

/* runHarness against a fake claude that hangs: the bound fires Timeout, and the process is
   actually killed, not merely abandoned — the marker it would write after the bound never
   lands. */
{
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-quota-observe-marker-'));
  const marker = path.join(directory, 'ran');
  let caught = null;
  try {
    await runHarness({
      command: process.execPath,
      args: [fakeClaude],
      timeoutMs: 200,
      env: { ...process.env, FAKE_CLAUDE_MODE: 'hang', FAKE_CLAUDE_MARKER: marker },
    });
  } catch (error) {
    caught = error;
  }
  assert.ok(caught instanceof Timeout);
  assert.ok(Number.isInteger(caught.pid));
  const deadline = Date.now() + 2000;
  let alive = true;
  while (Date.now() < deadline) {
    try {
      process.kill(caught.pid, 0);
    } catch {
      alive = false;
      break;
    }
    await new Promise(resolve => setTimeout(resolve, 20));
  }
  assert.equal(alive, false, 'the timed-out process should have been killed');
  await new Promise(resolve => setTimeout(resolve, 1100));
  assert.equal(fs.existsSync(marker), false, 'the killed process should never have reached its own delayed write');
}

console.log('claude-quota-observe fixtures passed');
