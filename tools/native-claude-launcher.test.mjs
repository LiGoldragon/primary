import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { launchPreparedNativeClaude, prepareNativeClaudeLaunch } from './native-claude-launcher.mjs';

const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'native-claude-launcher-'));
const system = Buffer.from('system context stays in this file\n', 'utf8');
const malicious = 'first; $(echo shell-never-runs) "quotes" `backticks`\nlast';
const user = Buffer.from(malicious, 'utf8');
const digest = value => crypto.createHash('sha256').update(value).digest('hex');
const writePackage = ({ systemBytes = system, userBytes = user, userHash = digest(user) } = {}) => {
  fs.writeFileSync(path.join(directory, 'system-prompt.md'), systemBytes);
  fs.writeFileSync(path.join(directory, 'user-prompt.md'), userBytes);
  fs.writeFileSync(path.join(directory, 'manifest.json'), JSON.stringify({ artifacts: [
    { role: 'system', path: 'system-prompt.md', bytes: systemBytes.length, sha256: digest(systemBytes) },
    { role: 'user', path: 'user-prompt.md', bytes: userBytes.length, sha256: userHash },
  ] }));
};
writePackage();
const plan = prepareNativeClaudeLaunch({ packageDirectory: directory, name: 'primary-claude-proof', model: 'fable', environment: { PATH: process.env.PATH, NO_COLOR: '1' } });
assert.equal(plan.proof.stdin, 'DEVNULL'); assert.equal(plan.proof.noColorAbsent, true); assert.equal(plan.proof.system.passedByFile, true); assert.equal(plan.proof.user.passedExactlyOnce, true);
assert.equal(plan.args.at(-1), malicious); assert.equal(plan.args.filter(value => value === malicious).length, 1); assert.ok(!plan.args.includes(system.toString('utf8'))); assert.equal(plan.options.env.NO_COLOR, undefined);

const report = path.join(directory, 'child.json');
const mock = path.join(directory, 'mock-claude.mjs');
fs.writeFileSync(mock, "import fs from 'node:fs'; fs.writeFileSync(process.argv[2], JSON.stringify({ stdin: fs.readFileSync(0, 'utf8'), args: process.argv.slice(3) }));");
const result = launchPreparedNativeClaude(plan, { spawn: (command, args, options) => spawnSync(process.execPath, [mock, report, ...args], options) });
assert.equal(result.status, 0); const child = JSON.parse(fs.readFileSync(report, 'utf8')); assert.equal(child.stdin, ''); assert.deepEqual(child.args, plan.args); assert.equal(child.args.at(-1), malicious);

fs.unlinkSync(path.join(directory, 'system-prompt.md')); assert.throws(() => prepareNativeClaudeLaunch({ packageDirectory: directory, name: 'proof', model: 'fable' }), /ENOENT/);
writePackage({ userHash: '0'.repeat(64) }); assert.throws(() => prepareNativeClaudeLaunch({ packageDirectory: directory, name: 'proof', model: 'fable' }), /sha256 differs/);
writePackage();
assert.throws(() => prepareNativeClaudeLaunch({ packageDirectory: directory, name: 'proof', model: 'fable', maxUserArgumentBytes: 1 }), /exceeds configured/);
console.log('native Claude launcher stdin-proof fixtures passed');
