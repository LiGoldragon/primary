#!/usr/bin/env node
// Runner-plumbing tests use a local fake executable; they do not claim an
// OpenCode gate or provider-adapter witness.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';

const here = path.dirname(new URL(import.meta.url).pathname);
const adapter = path.join(here, 'offline-adapter.mjs');
const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'third-stack-adapter-test-'));
const fake = path.join(temp, 'fake-opencode.mjs');
const descendantPid = path.join(temp, 'timeout-descendant.pid');
const fakeSource = `#!/usr/bin/env node
import fs from 'node:fs';
import {spawn} from 'node:child_process';
const timeoutDescendantPath = null;
if (process.argv[2] === '--version') { process.stdout.write(process.env.FAKE_VERSION || '1.17.13\\n'); process.exit(0); }
if (process.env.PROVIDER_SECRET || process.env.API_KEY) process.exit(91);
if (timeoutDescendantPath) { const descendant = spawn(process.execPath, ['-e', 'setInterval(() => {}, 1000)'], {stdio: 'ignore'}); fs.writeFileSync(timeoutDescendantPath, String(descendant.pid)); await new Promise(() => {}); }
if (process.env.FAKE_MODE === 'timeout') { setInterval(() => {}, 1000); }
const config = JSON.parse(fs.readFileSync(process.env.OPENCODE_CONFIG));
const base = config.provider.fixture.options.baseURL;
const first = {model: 'fixture', messages: [{role: 'user', content: 'Read fixture.txt'}], tools: [{type: 'function', function: {name: 'read', description: 'Read a file', parameters: {type: 'object', properties: {filePath: {type: 'string'}}, required: ['filePath']}}}]};
const one = await fetch(base + '/chat/completions', {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify(first)});
if (!one.ok) process.exit(92);
const second = {model: 'fixture', messages: [{role: 'user', content: 'Read fixture.txt'}, {role: 'assistant', reasoning_content: 'fixture reasoning', tool_calls: [{id: 'call_fixture', type: 'function', function: {name: 'read', arguments: JSON.stringify({filePath: process.cwd() + '/fixture.txt'})}}]}, {role: 'tool', tool_call_id: 'call_fixture', content: 'offline adapter fixture: known content\\n'}]};
const two = await fetch(base + '/chat/completions', {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify(second)});
if (!two.ok) process.exit(93);
process.stdout.write(JSON.stringify({ok: true}) + '\\n');
`;
fs.writeFileSync(fake, fakeSource, {mode: 0o755});
const wrongVersionFake = path.join(temp, 'fake-opencode-wrong-version.mjs');
fs.writeFileSync(wrongVersionFake, fakeSource.replaceAll('1.17.13', '1.17.12'), {mode: 0o755});
const timeoutFake = path.join(temp, 'fake-opencode-timeout.mjs');
fs.writeFileSync(timeoutFake, fakeSource.replace('const timeoutDescendantPath = null;', `const timeoutDescendantPath = ${JSON.stringify(descendantPid)};`), {mode: 0o755});
const badContinuationFake = path.join(temp, 'fake-opencode-bad-continuation.mjs');
fs.writeFileSync(badContinuationFake, fakeSource.replaceAll("reasoning_content: 'fixture reasoning'", "reasoning_content: 'wrong reasoning'").replace("if (!two.ok) process.exit(93);", "if (!two.ok) await two.arrayBuffer();"), {mode: 0o755});
const auxiliaryFake = path.join(temp, 'fake-opencode-auxiliary.mjs');
fs.writeFileSync(auxiliaryFake, fakeSource.replace("const first = {model: 'fixture'", "const title = await fetch(base + '/chat/completions', {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify({model: 'fixture', messages: [{role: 'user', content: 'Name this session'}]})});\nif (!title.ok) process.exit(94);\nconst first = {model: 'fixture'"), {mode: 0o755});

function run(args, env = {}) {
  return new Promise(resolve => {
    const child = spawn(process.execPath, [adapter, ...args], {env: {...process.env, ...env}, stdio: ['ignore', 'pipe', 'pipe']});
    let stdout = '', stderr = '';
    child.stdout.on('data', chunk => { stdout += chunk; }); child.stderr.on('data', chunk => { stderr += chunk; });
    child.on('close', (code, signal) => resolve({code, signal, stdout, stderr}));
  });
}

try {
  const success = await run(['--opencode', fake], {PROVIDER_SECRET: 'must-not-cross-boundary', API_KEY: 'must-not-cross-boundary'});
  assert.equal(success.code, 0, success.stderr || success.stdout);
  assert.equal(JSON.parse(success.stdout).status, 'adapter-replay-passed');
  const auxiliary = await run(['--opencode', auxiliaryFake]);
  assert.equal(auxiliary.code, 0, auxiliary.stderr || auxiliary.stdout);
  const auxiliaryReport = JSON.parse(auxiliary.stdout);
  assert.equal(auxiliaryReport.requests, 3);
  assert.equal(auxiliaryReport.replay_requests, 2);

  const missing = await run(['--opencode', path.join(temp, 'missing')]);
  assert.equal(missing.code, 2); assert.equal(JSON.parse(missing.stdout).status, 'adapter-witness-failed');

  const wrongVersion = await run(['--opencode', wrongVersionFake]);
  assert.equal(wrongVersion.code, 1); assert.match(wrongVersion.stdout, /expected OpenCode 1\.17\.13/);

  const timedOut = await run(['--opencode', timeoutFake], {OFFLINE_ADAPTER_TIMEOUT_MS: '500'});
  assert.equal(timedOut.code, 1); assert.match(timedOut.stdout, /timed out/);
  const timeoutReport = JSON.parse(timedOut.stdout);
  assert.deepEqual(timeoutReport.request_count, 0);
  assert.equal(timeoutReport.stage, 'run');
  assert.equal(timeoutReport.child.timed_out, true);
  const pid = Number(fs.readFileSync(descendantPid, 'utf8'));
  assert.throws(() => process.kill(pid, 0), {code: 'ESRCH'});
  const badContinuation = await run(['--opencode', badContinuationFake]);
  assert.equal(badContinuation.code, 1); assert.match(badContinuation.stdout, /protocol assertion failed/);
  process.stdout.write('offline-adapter runner-plumbing tests passed\n');
} finally {
  fs.rmSync(temp, {recursive: true, force: true});
}
