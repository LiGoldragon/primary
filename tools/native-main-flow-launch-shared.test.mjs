import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import {clientForModel} from './native-main-flow-launch-shared.mjs';

test('Next follows installed wrapper endpoint and refuses mismatched or ambiguous tuples', () => {
  const home = fs.mkdtempSync(path.join(os.tmpdir(), 'native-launch-endpoint-'));
  try {
    const bin = path.join(home, '.nix-profile', 'bin'); fs.mkdirSync(bin, {recursive: true});
    const wrapper = path.join(bin, 'codex-next');
    const candidate = path.join(home, '.codex-next-candidate');
    const endpoint = path.join(candidate, 'app-server-control', 'app-server-control.sock');
    fs.writeFileSync(wrapper, `export CODEX_HOME=${candidate}; exec codex --remote unix://${endpoint} "$@"`);
    assert.equal(clientForModel('gpt-6-sol', home).endpoint, endpoint);
    assert.equal(clientForModel('gpt-6.1-sol', home).endpoint, endpoint);
    assert.equal(clientForModel('gpt-5.6-sol', home).endpoint, path.join(home, '.codex', 'app-server-control', 'app-server-control.sock'));
    fs.writeFileSync(wrapper, `export CODEX_HOME=${candidate}; exec codex --remote unix:///other/socket "$@"`);
    assert.throws(() => clientForModel('gpt-6-sol', home), /matching literal/);
    fs.writeFileSync(wrapper, `export CODEX_HOME=${candidate}; exec codex --remote unix://${endpoint} --remote unix://${endpoint} "$@"`);
    assert.throws(() => clientForModel('gpt-6-sol', home), /matching literal/);
  } finally { fs.rmSync(home, {recursive: true, force: true}); }
});
