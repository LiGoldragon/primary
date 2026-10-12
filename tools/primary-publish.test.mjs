import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import {publish} from './primary-publish.mjs';

test('legacy caller refuses without reading request or authority and without creating state', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'retired-primary-publish-'));
  try {
    const request = new Proxy({}, {get() {throw new Error('request must not be read');}});
    const stateFile = path.join(directory, 'state.json');
    const result = publish(request, {authorityFile: '/missing/authority', stateFile});
    assert.equal(result.outcome, 'refused');
    assert.deepEqual(result.paths, []);
    assert.match(result.error, /sole standing committer/);
    assert.match(result.error, /Other repositories/);
    assert.deepEqual(fs.readdirSync(directory), []);
  } finally {fs.rmdirSync(directory);}
});

test('legacy CLI refuses before opening a request or running Git', () => {
  const result = spawnSync(process.execPath, ['tools/primary-publish.mjs', '--request', '/missing/request'], {encoding: 'utf8'});
  assert.equal(result.status, 1);
  assert.equal(JSON.parse(result.stdout).outcome, 'refused');
  assert.equal(result.stderr, '');
});
