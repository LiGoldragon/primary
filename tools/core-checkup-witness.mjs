#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const sleep = milliseconds => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, milliseconds);
const runtimeDirectory = process.env.XDG_RUNTIME_DIR ?? `/run/user/${process.getuid()}`;
const userBus = {
  ...process.env,
  XDG_RUNTIME_DIR: runtimeDirectory,
  DBUS_SESSION_BUS_ADDRESS: process.env.DBUS_SESSION_BUS_ADDRESS ?? `unix:path=${runtimeDirectory}/bus`,
};
const call = (program, args, options = {}) => spawnSync(program, args, { encoding: 'utf8', env: userBus, ...options });

const [sourceRoster, sourcePolicy, artifactDirectory] = process.argv.slice(2);
if (!sourceRoster || !sourcePolicy || !artifactDirectory) throw new Error('usage: core-checkup-witness ROSTER POLICY ARTIFACT_DIRECTORY');
const artifactPath = path.resolve(artifactDirectory);
const roster = JSON.parse(fs.readFileSync(path.resolve(sourceRoster), 'utf8'));
const policy = JSON.parse(fs.readFileSync(path.resolve(sourcePolicy), 'utf8'));
if (policy.allowRepair !== false || policy.luna !== true) throw new Error('witness requires allowRepair:false and luna:true');
if (policy.wake !== undefined) throw new Error('witness does not permit a wake transport');
fs.mkdirSync(artifactPath, { recursive: true });
const runRoster = path.join(artifactPath, 'roster.json');
const runPolicy = path.join(artifactPath, 'policy.json');
const eventPath = path.join(artifactPath, 'events.ndjson');
const statePath = path.join(artifactPath, 'state.json');
fs.writeFileSync(runRoster, JSON.stringify(roster) + '\n');
fs.writeFileSync(runPolicy, JSON.stringify(policy) + '\n');
const configSha256 = crypto.createHash('sha256').update(fs.readFileSync(runRoster)).update(fs.readFileSync(runPolicy)).digest('hex');
const name = `core-checkup-witness-${process.pid}-${Date.now()}`;
const program = path.resolve(path.dirname(new URL(import.meta.url).pathname), 'core-checkup.mjs');
const command = ['/usr/bin/env', 'node', program, runRoster, runPolicy, eventPath, statePath];
const runtimePath = `${path.join(os.homedir(), '.nix-profile/bin')}:/run/current-system/sw/bin:/usr/bin`;
const start = call('systemd-run', ['--user', `--unit=${name}`, '--on-active=1s', `--setenv=PATH=${runtimePath}`, '--property=RuntimeMaxSec=120', '--property=TimeoutStartSec=120', '--property=MemoryMax=256M', '--property=NoNewPrivileges=yes', ...command], { stdio: 'pipe' });
if (start.status !== 0) throw new Error('systemd-run did not create the transient timer');
const deadline = Date.now() + 125_000;
let observedActive = false;
let result = null;
while (Date.now() < deadline) {
  const show = call('systemctl', ['--user', 'show', `${name}.service`, '--property=ActiveState', '--property=Result', '--property=ExecMainStatus']);
  const fields = Object.fromEntries(show.stdout.trim().split('\n').filter(Boolean).map(line => line.split('=', 2)));
  observedActive ||= fields.ActiveState === 'active';
  if (observedActive && ['inactive', 'failed'].includes(fields.ActiveState)) { result = fields; break; }
  sleep(500);
}
const timer = call('systemctl', ['--user', 'show', `${name}.timer`, '--property=ActiveState', '--property=LastTriggerUSec']);
const journal = call('journalctl', ['--user-unit', `${name}.service`, '--no-pager', '--output=short-iso']);
fs.writeFileSync(path.join(artifactPath, 'journal.txt'), journal.stdout);
const receipt = {
  schema: 'core-checkup-witness/v1',
  unit: name,
  command,
  configSha256,
  observedActive,
  result,
  timer: Object.fromEntries(timer.stdout.trim().split('\n').filter(Boolean).map(line => line.split('=', 2))),
  eventsSha256: fs.existsSync(eventPath) ? crypto.createHash('sha256').update(fs.readFileSync(eventPath)).digest('hex') : null,
  cleanup: null,
};
call('systemctl', ['--user', 'stop', `${name}.timer`, `${name}.service`]);
call('systemctl', ['--user', 'reset-failed', `${name}.timer`, `${name}.service`]);
const remains = call('systemctl', ['--user', 'show', `${name}.timer`, `${name}.service`, '--property=LoadState']);
receipt.cleanup = remains.stdout.includes('LoadState=loaded') ? 'cleanup-needs-review' : 'own-units-removed';
fs.writeFileSync(path.join(artifactPath, 'receipt.json'), JSON.stringify(receipt, null, 2) + '\n');
if (!result || result.Result !== 'success' || result.ExecMainStatus !== '0') process.exitCode = 1;
