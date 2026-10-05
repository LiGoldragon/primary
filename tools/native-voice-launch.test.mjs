#!/usr/bin/env node
import assert from 'node:assert/strict';
import path from 'node:path';
import {dispatchCommand, parseArgs} from './native-voice-launch.mjs';
const field = parseArgs(['--voice', 'Field.Primary', '--brief', '/tmp/field.md']);
assert.deepEqual(field, {aspect: 'Field', layer: 'Primary', brief: '/tmp/field.md'});
const command = dispatchCommand(field);
assert.equal(command.command, process.execPath);
assert.deepEqual(command.args.slice(-6), ['--aspect', 'Field', '--layer', 'Primary', '--brief', '/tmp/field.md']);
assert.match(command.args[0], /codex-main-flow-launch\.mjs$/);
assert.throws(() => parseArgs(['--voice', 'Field.Primary']), /usage/);
assert.throws(() => dispatchCommand(parseArgs(['--voice', 'Mind.Secondary', '--brief', '/tmp/mind.md'])), /correspondence is pending/);
console.log('native-voice-launch tests passed');
