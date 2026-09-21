import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {test} from 'node:test';
import {due, runCycle} from './field-census-cycle.mjs';

test('notification cadence holds uncertain attempts and avoids immediate repeats', () => {
  const time = Date.parse('2026-09-20T23:00:00Z');
  assert.equal(due({}, time, 1800), true);
  assert.equal(due({last_completed_at:'2026-09-20T22:45:00Z'}, time, 1800), false);
  assert.equal(due({last_completed_at:'2026-09-20T22:30:00Z'}, time, 1800), true);
  assert.equal(due({last_completed_at:'2026-09-20T21:00:00Z', hold:{status:'uncertain'}}, time, 1800), false);
});

test('observe-only refreshes the census without reading recipients or sending, and leaves notification hold unchanged', async () => {
  const stateDirectory = fs.mkdtempSync(path.join(os.tmpdir(), 'field-census-observe-'));
  const previousPath = process.env.PATH;
  try {
    const notification = path.join(stateDirectory, 'notification-state.json');
    const before = '{"last_completed_at":"2026-09-20T00:00:00Z"}\n';
    fs.writeFileSync(notification, before);
    const configPath = path.join(stateDirectory, 'recipients.json');
    fs.writeFileSync(configPath, JSON.stringify({sender_flow_id:'9ddcbc',field_low_flow_id:'0347d0',
      field_ultra_flow_id:'c88918',notify_seconds:300}));
    const bin = path.join(stateDirectory, 'bin');
    fs.mkdirSync(bin);
    const marker = path.join(stateDirectory, 'unexpected-send');
    const fakeSend = path.join(bin, 'hm-send');
    fs.writeFileSync(fakeSend, `#!/bin/sh\nprintf called > '${marker}'\n`);
    fs.chmodSync(fakeSend, 0o700);
    process.env.PATH = `${bin}:${previousPath}`;
    const snapshot = {observed_at:'2026-09-21T20:00:00Z', complete:true,
      counts:{panes:12,agents:12,exact_flows:12,stale_registrations:0,unbound_panes:0}};
    await runCycle({
      collectSnapshot: async () => snapshot,
      stateDirectory,
      configPath,
      passive: true,
      preview: false,
    });
    assert.deepEqual(JSON.parse(fs.readFileSync(path.join(stateDirectory, 'latest.json'), 'utf8')), snapshot);
    assert.equal(fs.readFileSync(notification, 'utf8'), before);
    assert.equal(fs.existsSync(marker), false);
    assert.equal(fs.existsSync(path.join(stateDirectory, 'cycle.lock')), false);
  } finally {
    process.env.PATH = previousPath;
    fs.rmSync(stateDirectory, {recursive:true, force:true});
  }
});
