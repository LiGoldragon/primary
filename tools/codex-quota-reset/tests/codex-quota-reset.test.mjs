import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { start } from './fake-app-server.mjs';

const here = import.meta.dirname;
const tool = path.join(here, '..', 'codex-quota-reset');
const fixture = name => path.join(here, 'fixtures', name);
const NOW = 1789581600; /* 2026-09-16T18:00:00Z; every fixture instant is relative to it. */

let count = 0;
const scratch = () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), `codex-quota-reset-${count++}-`));
  return { directory, socket: path.join(directory, 'app-server.sock'), stateHome: path.join(directory, 'state') };
};

const run = (socket, stateHome, policy, now = NOW) =>
  new Promise(resolve => {
    const child = spawn(process.execPath, [tool, `Check.{ ${fixture(policy)} Socket.«${socket}» At.${now} }`], {
      env: { ...process.env, XDG_STATE_HOME: stateHome },
    });
    let stdout = '';
    child.stdout.on('data', d => {
      stdout += d;
    });
    child.stderr.on('data', () => {});
    child.on('exit', code => resolve({ code, lines: stdout.split('\n').filter(Boolean) }));
  });

const logOf = stateHome =>
  fs
    .readFileSync(path.join(stateHome, 'codex-quota-reset', 'log.ndjson'), 'utf8')
    .split('\n')
    .filter(Boolean)
    .map(line => JSON.parse(line));

const consumes = requests => requests.filter(r => r.method === 'account/rateLimitResetCredit/consume');

/* Above the threshold: observed, held, nothing spent. */
{
  const { socket, stateHome } = scratch();
  const fake = await start(socket, fixture('aboveThreshold.json'));
  const out = await run(socket, stateHome, 'useReset.datom');
  await fake.close();
  assert.equal(out.code, 0);
  assert.equal(out.lines[0], 'QuotaObserved.{ 60 2026-09-20T18:00:00Z 3 }');
  assert.equal(out.lines[1], 'ResetHeld.{ aboveThreshold }');
  assert.equal(consumes(fake.requests).length, 0);
  const initialize = fake.requests.find(r => r.method === 'initialize');
  assert.equal(initialize.params.capabilities.experimentalApi, true);
  const log = logOf(stateHome);
  assert.deepEqual(log.map(r => r.kind), ['QuotaObserved', 'ResetHeld']);
  assert.ok(!JSON.stringify(log).includes('fixture-account-not-printed'));
  assert.ok(!out.lines.join('\n').includes('fixture-account-not-printed'));
}

/* Below the threshold, two live credits: the soonest non-null expiry is the one named. */
let spentKey;
{
  const { socket, stateHome } = scratch();
  const fake = await start(socket, fixture('belowThresholdTwoCredits.json'));
  const out = await run(socket, stateHome, 'useReset.datom');
  assert.equal(out.code, 0);
  assert.equal(out.lines[0], 'QuotaObserved.{ 5 2026-09-19T18:00:00Z 2 }');
  assert.equal(out.lines[1], 'ResetConsumed.{ credit-soon reset }');
  const spent = consumes(fake.requests);
  assert.equal(spent.length, 1);
  assert.equal(spent[0].params.creditId, 'credit-soon');
  assert.match(spent[0].params.idempotencyKey, /^[0-9a-f]{8}-[0-9a-f]{4}-5[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
  spentKey = spent[0].params.idempotencyKey;

  /* A rerun against the same window spends nothing more and reuses the same key. */
  const again = await run(socket, stateHome, 'useReset.datom');
  await fake.close();
  assert.equal(again.code, 0);
  assert.equal(again.lines[1], 'ResetHeld.{ alreadySpentThisWindow }');
  assert.equal(consumes(fake.requests).length, 1);
  const log = logOf(stateHome);
  assert.deepEqual(
    log.map(r => r.kind),
    ['QuotaObserved', 'ResetAttempted', 'ResetConsumed', 'QuotaObserved', 'ResetHeld']
  );
  assert.equal(log[2].idempotencyKey, spentKey);
}

/* The same window instant gives the same key in a fresh state directory: it is derived, not random. */
{
  const { socket, stateHome } = scratch();
  const fake = await start(socket, fixture('belowThresholdTwoCredits.json'));
  const out = await run(socket, stateHome, 'useReset.datom');
  await fake.close();
  assert.equal(out.lines[1], 'ResetConsumed.{ credit-soon reset }');
  assert.equal(consumes(fake.requests)[0].params.idempotencyKey, spentKey);
}

/* Fewer than the policy's minimum days left in the window: held. */
{
  const { socket, stateHome } = scratch();
  const fake = await start(socket, fixture('belowThresholdShortWindow.json'));
  const out = await run(socket, stateHome, 'useReset.datom');
  await fake.close();
  assert.equal(out.code, 0);
  assert.equal(out.lines[0], 'QuotaObserved.{ 3 2026-09-17T18:00:00Z 2 }');
  assert.equal(out.lines[1], 'ResetHeld.{ windowEndsSooner }');
  assert.equal(consumes(fake.requests).length, 0);
}

/* No credits at all: held, and said as noCredit. */
{
  const { socket, stateHome } = scratch();
  const fake = await start(socket, fixture('noCredits.json'));
  const out = await run(socket, stateHome, 'useReset.datom');
  await fake.close();
  assert.equal(out.code, 0);
  assert.equal(out.lines[0], 'QuotaObserved.{ 1 2026-09-19T18:00:00Z 0 }');
  assert.equal(out.lines[1], 'ResetHeld.{ noCredit }');
  assert.equal(consumes(fake.requests).length, 0);
}

/* Hold mode never spends, however little is left. */
{
  const { socket, stateHome } = scratch();
  const fake = await start(socket, fixture('belowThresholdTwoCredits.json'));
  const out = await run(socket, stateHome, 'hold.datom');
  await fake.close();
  assert.equal(out.lines[1], 'ResetHeld.{ modeHold }');
  assert.equal(consumes(fake.requests).length, 0);
}

/* A malformed read is a typed refusal, not a guess. */
{
  const { socket, stateHome } = scratch();
  const fake = await start(socket, fixture('malformedRateLimits.json'));
  const out = await run(socket, stateHome, 'useReset.datom');
  await fake.close();
  assert.equal(out.code, 2);
  assert.equal(out.lines[0], 'ResetRefused.{ malformedRateLimitWindow }');
  assert.equal(consumes(fake.requests).length, 0);
  assert.deepEqual(logOf(stateHome).map(r => r.kind), ['ResetRefused']);
}

/* A policy that is not readable datom is refused before any socket is opened. */
{
  const { directory, socket, stateHome } = scratch();
  const broken = path.join(directory, 'broken.datom');
  fs.writeFileSync(broken, '{ Maybe 15 }');
  const child = await new Promise(resolve => {
    const spawned = spawn(process.execPath, [tool, `Check.{ ${broken} Socket.«${socket}» At.${NOW} }`], {
      env: { ...process.env, XDG_STATE_HOME: stateHome },
    });
    let stdout = '';
    spawned.stdout.on('data', d => {
      stdout += d;
    });
    spawned.stderr.on('data', () => {});
    spawned.on('exit', code => resolve({ code, stdout }));
  });
  assert.equal(child.code, 2);
  assert.match(child.stdout, /^ResetRefused\.\{ «malformedPolicy/);
}

console.log('codex-quota-reset fixtures passed');
