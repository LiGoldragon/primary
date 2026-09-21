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
  try {
    const notification = path.join(stateDirectory, 'notification-state.json');
    const held = '{"hold":{"status":"uncertain","failed_flow":"0347d0"}}\n';
    fs.writeFileSync(notification, held);
    const snapshot = {observed_at:'2026-09-21T20:00:00Z', complete:true,
      counts:{panes:12,agents:12,exact_flows:12,stale_registrations:0,unbound_panes:0}};
    let sends = 0;
    await runCycle({
      collectSnapshot: async () => snapshot,
      submit: () => { sends++; throw new Error('unexpected send'); },
      stateDirectory,
      configPath: path.join(stateDirectory, 'no-recipients-config.json'),
      passive: true,
      preview: false,
    });
    assert.deepEqual(JSON.parse(fs.readFileSync(path.join(stateDirectory, 'latest.json'), 'utf8')), snapshot);
    assert.equal(fs.readFileSync(notification, 'utf8'), held);
    assert.equal(sends, 0);
    assert.equal(fs.existsSync(path.join(stateDirectory, 'cycle.lock')), false);
  } finally {
    fs.rmSync(stateDirectory, {recursive:true, force:true});
  }
});
