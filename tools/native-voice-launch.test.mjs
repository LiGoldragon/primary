#!/usr/bin/env node
import assert from 'node:assert/strict';
import path from 'node:path';
import fs from 'node:fs';
import os from 'node:os';
import {dispatchCommand, parseArgs} from './native-voice-launch.mjs';
const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'voice-dispatch-'));
const flowsRoot = path.join(fixture, 'flows');
fs.mkdirSync(path.join(flowsRoot, 'abcdef'), {recursive: true});
fs.writeFileSync(path.join(flowsRoot, 'abcdef', 'continuation.json'), JSON.stringify({flowId: 'abcdef', topic: 'Core', metaflow: 'mission'}));
const metaflow = path.join(fixture, 'metaflow.edn');
fs.writeFileSync(metaflow, 'mission');
const dispatch = options => dispatchCommand(options, {flowsRoot});
try {
const field = parseArgs(['--voice', 'Field.Primary', '--brief', '/tmp/field.md', '--predecessor', 'abcdef']);
assert.deepEqual(field, {aspect: 'Field', layer: 'Primary', brief: '/tmp/field.md', root: false, predecessor: 'abcdef', metaflow: undefined, topic: undefined});
const command = dispatch(field);
assert.equal(command.command, process.execPath);
assert.deepEqual(command.args.slice(-8), ['--aspect', 'Field', '--layer', 'Primary', '--brief', '/tmp/field.md', '--predecessor', 'abcdef']);
assert.match(command.args[0], /codex-main-flow-launch\.mjs$/);
const root = parseArgs(['--voice', 'Field.Primary', '--brief', '/tmp/field.md', '--root', '--metaflow', metaflow]);
assert.deepEqual(dispatch(root).args.slice(-9), ['--aspect', 'Field', '--layer', 'Primary', '--brief', '/tmp/field.md', '--root', '--metaflow', metaflow]);
const topicRoot = parseArgs(['--voice', 'Field.Primary', '--brief', '/tmp/field.md', '--root', '--metaflow', metaflow, '--topic', 'Ethos']);
assert.deepEqual(dispatch(topicRoot).args.slice(-11), ['--aspect', 'Field', '--layer', 'Primary', '--brief', '/tmp/field.md', '--root', '--metaflow', metaflow, '--topic', 'Ethos']);
assert.throws(() => parseArgs(['--voice', 'Field.Primary', '--brief', '/tmp/field.md', '--root', '--metaflow', metaflow, '--topic', 'ethos-zero']), /dense PascalCase/);
assert.throws(() => parseArgs(['--voice', 'Field.Primary', '--brief', '/tmp/field.md', '--predecessor', 'abcdef', '--topic', 'Ethos']), /--topic is only valid with --root/);
assert.throws(() => parseArgs(['--voice', 'Field.Primary', '--brief', '/tmp/field.md']), /usage/);
assert.throws(() => parseArgs(['--voice', 'Field.Primary']), /usage/);
assert.match(dispatch(parseArgs(['--voice', 'Mind.Secondary', '--brief', '/tmp/mind.md', '--predecessor', 'abcdef'])).args[0], /codex-main-flow-launch/);
for (const [topic, layer] of [['Publisher', 'Quaternary'], ['Illustrator', 'Tertiary']]) {
  assert.match(dispatch({aspect: 'Field', layer, brief: '/tmp/brief.md', root: true, metaflow, topic}).args[0], /claude-main-flow-launch/);
  fs.writeFileSync(path.join(flowsRoot, 'abcdef', 'continuation.json'), JSON.stringify({flowId: 'abcdef', topic, metaflow: 'mission'}));
  assert.match(dispatch({aspect: 'Field', layer, brief: '/tmp/brief.md', root: false, predecessor: 'abcdef'}).args[0], /claude-main-flow-launch/);
}
assert.throws(() => dispatch({aspect: 'Field', layer: 'Quaternary', predecessor: '123456', root: false}), /record is unavailable/);
} finally { fs.rmSync(fixture, {recursive: true, force: true}); }
console.log('native-voice-launch tests passed');
