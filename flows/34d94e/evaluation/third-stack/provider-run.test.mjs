#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';
const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'third-stack-provider-test-'));
const driver = path.join(path.dirname(new URL(import.meta.url).pathname), 'provider-run.mjs');
const descriptor = path.join(dir, 'descriptor.json'), output = path.join(dir, 'out');
fs.writeFileSync(descriptor, JSON.stringify({access_authorized: true, baseURL: 'https://example.invalid/api', model: 'fixture', expected_opencode_version: '1.17.13'}));
function run(extra) { return new Promise(resolve => { const p = spawn(process.execPath, [driver, '--provider-descriptor', descriptor, '--secret-fd', '99', '--opencode', process.execPath, '--output', output, ...extra], {stdio: ['ignore', 'pipe', 'pipe']}); let out = ''; p.stdout.on('data', c => out += c); p.on('close', code => resolve({code, out})); }); }
try {
  const dry = await run(['--dry-run']); assert.equal(dry.code, 0, dry.out); const report = JSON.parse(fs.readFileSync(path.join(output, 'provider-run-dry.json'))); assert.equal(report.hidden_expectations_injected, false); assert.equal(report.cases.length, 12); assert.ok(report.cases.every(c => c.prompt && !c.prompt.includes('hidden')));
  const gated = await run([]); assert.equal(gated.code, 2); assert.match(gated.out, /secret fd was empty|bad file descriptor/);
  const denied = path.join(dir, 'denied.json'); fs.writeFileSync(denied, JSON.stringify({access_authorized: false, baseURL: 'https://example.invalid', model: 'fixture', expected_opencode_version: '1.17.13'}));
  const refused = await new Promise(resolve => { const p = spawn(process.execPath, [driver, '--provider-descriptor', denied, '--secret-fd', '99', '--opencode', process.execPath, '--output', output], {stdio: ['ignore', 'pipe', 'ignore']}); let out = ''; p.stdout.on('data', c => out += c); p.on('close', code => resolve({code, out})); }); assert.equal(refused.code, 2); assert.match(refused.out, /access_authorized/);
  process.stdout.write('provider-run offline gate tests passed\n');
} finally { fs.rmSync(dir, {recursive: true, force: true}); }
