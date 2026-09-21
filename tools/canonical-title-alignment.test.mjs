import assert from 'node:assert/strict';
import test from 'node:test';
import { alignFlow, desired, plan } from './canonical-title-alignment.mjs';

const flow = '6db4fe';
const role = { flow_id: flow, aspect: 'Field', power: 'High', native_thread: 'native', harness: 'codex' };

function fixture(failure = null) {
  const hm = { agent: 'codex', native_thread: 'native', session: 'session', pane_id: 'pane', terminal_id: 'terminal', name: 'old' };
  const agent = { ...hm, tab_id: 'shared', name: 'old' };
  const pane = { ...hm, tab_id: 'shared', label: null };
  const tab = { tab_id: 'shared', pane_count: 2, label: 'Shared' };
  const native = { id: 'native', name: 'old-title', path: '/fixture-native.jsonl' };
  const state = { hm, agent, pane, tab, native };
  const snapshot = () => structuredClone({ flow, ...state });
  const io = {
    live: async () => snapshot(),
    registration: async () => structuredClone(state.hm),
    herdr: async (_session, kind, action, _id, value) => {
      const item = state[kind];
      if (action === 'get') return structuredClone(item);
      if (action !== 'rename') throw new Error('unexpected Herdr call');
      if (kind === 'agent') item.name = value;
      else item.label = value === '--clear' ? null : value;
      if (failure === `${kind}-after-write`) throw new Error(`${kind} mutation failed after write`);
      return structuredClone(item);
    },
    readCodexThreadMetadata: async () => structuredClone(state.native),
    setCodexThreadName: async (_id, name) => {
      state.native.name = name;
      if (failure === 'native-after-write' && name === 'Field High 6db4fe') throw new Error('native mutation failed after write');
    },
    rebind: async (_flow, oldName, newName) => {
      assert.equal(state.hm.name, oldName);
      state.hm.name = newName;
      if (failure === 'rebind-after-write' && newName === 'flow-6db4fe') throw new Error('rebind failed after write');
    },
  };
  return { state, snapshot, io };
}

test('canonical title uses explicit aspect, power, and own Flow ID while preserving shared tab', () => {
  const { snapshot } = fixture();
  assert.deepEqual(desired(flow, role), { title: 'Field High 6db4fe', agentName: 'flow-6db4fe', paneLabel: '6db4fe' });
  const proposed = plan(snapshot(), role);
  assert.equal(proposed.operations.tabLabel, 'unchanged');
  assert.equal(proposed.route.tabPaneCount, 2);
  for (const bad of [
    { ...role, aspect: 'Other' }, { ...role, power: 'Astra' }, { ...role, flow_id: '7091ea' },
    { ...role, native_thread: 'other' }, { ...role, harness: 'claude' },
  ]) assert.throws(() => plan(snapshot(), bad));
});

test('guarded Codex apply verifies native, pane, agent, HM, and unchanged tab', async () => {
  const { state, io } = fixture();
  const result = await alignFlow(flow, { apply: true, role, io });
  assert.equal(result.outcome, 'verified', JSON.stringify(result));
  assert.equal(state.native.name, 'Field High 6db4fe');
  assert.equal(state.agent.name, 'flow-6db4fe');
  assert.equal(state.hm.name, 'flow-6db4fe');
  assert.equal(state.pane.label, flow);
  assert.equal(state.tab.label, 'Shared');
});

test('title-only correction keeps an existing shared route and tab untouched', async () => {
  const { state, io } = fixture();
  const result = await alignFlow(flow, { apply: true, titleOnly: true, role, io });
  assert.equal(result.outcome, 'verified');
  assert.deepEqual(result.steps, ['codex-title']);
  assert.equal(state.native.name, 'Field High 6db4fe');
  assert.equal(state.hm.name, 'old');
  assert.equal(state.agent.name, 'old');
  assert.equal(state.pane.label, null);
  assert.equal(state.tab.label, 'Shared');
});

test('failure after HM mutation rolls all changed surfaces back in reverse order', async () => {
  const { state, io } = fixture('rebind-after-write');
  const result = await alignFlow(flow, { apply: true, role, io });
  assert.equal(result.outcome, 'failed');
  assert.deepEqual(result.rollback, ['hm-rebind', 'herdr-pane', 'herdr-agent', 'codex-title']);
  assert.equal(state.hm.name, 'old');
  assert.equal(state.agent.name, 'old');
  assert.equal(state.pane.label, null);
  assert.equal(state.native.name, 'old-title');
  assert.equal(state.tab.label, 'Shared');
});

test('failure after native mutation rolls title back', async () => {
  const { state, io } = fixture('native-after-write');
  const result = await alignFlow(flow, { apply: true, role, io });
  assert.equal(result.outcome, 'failed');
  assert.deepEqual(result.rollback, ['codex-title']);
  assert.equal(state.native.name, 'old-title');
});

test('native readback mismatch reports failed rollback rather than verified alignment', async () => {
  const { state, io } = fixture();
  io.readCodexThreadMetadata = async () => ({ ...structuredClone(state.native),
    name: state.native.name === 'Field High 6db4fe' ? 'stale-display' : state.native.name });
  const result = await alignFlow(flow, { apply: true, role, io });
  assert.equal(result.outcome, 'failed');
  assert.match(result.error, /title readback mismatch/);
  assert.match(result.rollbackError, /Title rollback guard failed/);
});

test('changed terminal route prevents alignment and leaves title untouched', async () => {
  const { state, io } = fixture();
  const registered = io.registration;
  io.registration = async () => ({ ...(await registered()), terminal_id: 'other-terminal' });
  const result = await alignFlow(flow, { apply: true, role, io });
  assert.equal(result.outcome, 'failed');
  assert.deepEqual(result.steps, []);
  assert.equal(state.native.name, 'old-title');
});

test('Claude apply is blocked without a supported title adapter', async () => {
  const { io, snapshot } = fixture();
  const claudeRole = { ...role, harness: 'claude' };
  io.live = async () => ({ ...snapshot(), hm: { ...snapshot().hm, agent: 'claude' } });
  await assert.rejects(() => alignFlow(flow, { apply: true, role: claudeRole, io }), /Claude apply requires/);
});
