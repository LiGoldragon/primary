import assert from 'node:assert/strict';
import test from 'node:test';
import { alignFlow, desired, plan } from './canonical-title-alignment.mjs';

test('canonical names use the seat Flow ID and leave shared tab unchanged', () => {
  const snapshot = {
    flow: '6db4fe', hm: { agent: 'codex', native_thread: 'native', session: 'session', pane_id: 'pane', terminal_id: 'terminal', name: 'old' },
    agent: { name: 'old' }, pane: { label: null }, tab: { tab_id: 'shared', pane_count: 2, label: 'Shared' },
    native: { name: 'old-title' },
  };
  assert.deepEqual(desired('6db4fe'), { title: '6db4fe', agentName: 'flow-6db4fe', paneLabel: '6db4fe' });
  const proposed = plan(snapshot);
  assert.equal(proposed.operations.tabLabel, 'unchanged');
  assert.equal(proposed.route.tabPaneCount, 2);
});

test('mutation gate prevents incomplete apply implementation', async () => {
  await assert.rejects(() => alignFlow('6db4fe', { apply: true }), /Apply is disabled/);
});
