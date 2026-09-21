import assert from 'node:assert/strict';
import test from 'node:test';
import { alignFlow, desired, plan } from './canonical-title-alignment.mjs';

const flow = '6db4fe';
const role = { flow_id: flow, aspect: 'Field', power: 'High', native_thread: 'native', harness: 'codex' };

function fixture(failure = null, harness = 'codex', paneCount = 2) {
  const hm = { agent: harness, native_thread: 'native', session: 'session', pane_id: 'pane', terminal_id: 'terminal', name: 'old' };
  const agent = { ...hm, tab_id: 'shared', name: 'old', cwd: '/fixture', interactive_ready: true, agent_status: 'idle' };
  const pane = { ...hm, tab_id: 'shared', label: null };
  const tab = { tab_id: 'shared', pane_count: paneCount, label: 'Shared' };
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
      if (failure === `${kind}-after-write` && value !== 'old' && value !== 'Shared' && value !== '--clear') {
        throw new Error(`${kind} mutation failed after write`);
      }
      return structuredClone(item);
    },
    readCodexThreadMetadata: async () => structuredClone(state.native),
    readClaudeSessionMetadata: async () => structuredClone(state.native),
    setCodexThreadName: async (_id, name) => {
      state.native.name = name;
      if (failure === 'native-after-write' && name === 'Field High 6db4fe') throw new Error('native mutation failed after write');
    },
    setClaudeSessionTitle: async (_snapshot, name) => {
      state.native.name = name;
      if (failure === 'native-after-write' && name === 'Field High 6db4fe') throw new Error('native mutation failed after write');
    },
    rebind: async (_flow, oldName, newName) => {
      assert.equal(state.hm.name, oldName);
      assert.equal(state.agent.name, newName, 'HM rebind requires the new Herdr name at the exact pane');
      state.hm.name = newName;
      if (failure === 'rebind-after-write' && newName === 'flow-6db4fe') throw new Error('rebind failed after write');
    },
  };
  return { state, snapshot, io };
}

test('canonical title uses explicit aspect, power, and own Flow ID while preserving shared tab', () => {
  const { snapshot } = fixture();
  assert.deepEqual(desired(flow, role), { title: 'Field High 6db4fe', agentName: 'flow-6db4fe',
    paneLabel: 'Field High 6db4fe', tabLabel: 'Field High 6db4fe' });
  const proposed = plan(snapshot(), role);
  assert.equal(proposed.operations.tabLabel, false);
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
  assert.equal(state.pane.label, 'Field High 6db4fe');
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

test('single-pane tab receives canonical title without changing its ID', async () => {
  const { state, io } = fixture(null, 'codex', 1);
  const result = await alignFlow(flow, { apply: true, role, io });
  assert.equal(result.outcome, 'verified', JSON.stringify(result));
  assert.deepEqual(result.steps, ['codex-title', 'herdr-agent', 'herdr-pane', 'herdr-tab', 'hm-rebind']);
  assert.equal(state.tab.tab_id, 'shared');
  assert.equal(state.tab.label, 'Field High 6db4fe');
});

test('single-pane tab partial failure restores tab before pane and route', async () => {
  const { state, io } = fixture('tab-after-write', 'codex', 1);
  const result = await alignFlow(flow, { apply: true, role, io });
  assert.equal(result.outcome, 'failed', JSON.stringify(result));
  assert.deepEqual(result.rollback, ['herdr-tab', 'herdr-pane', 'herdr-agent', 'codex-title']);
  assert.equal(state.tab.label, 'Shared');
  assert.equal(state.pane.label, null);
  assert.equal(state.agent.name, 'old');
  assert.equal(state.native.name, 'old-title');
});

test('failure after HM mutation rolls all changed surfaces back in reverse order', async () => {
  const { state, io } = fixture('rebind-after-write');
  const result = await alignFlow(flow, { apply: true, role, io });
  assert.equal(result.outcome, 'failed');
  assert.deepEqual(result.rollback, ['herdr-pane', 'herdr-agent', 'hm-rebind', 'codex-title']);
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

test('Claude apply uses supported native title adapter and preserves shared tab', async () => {
  const { io, state } = fixture(null, 'claude');
  const claudeRole = { ...role, harness: 'claude' };
  const result = await alignFlow(flow, { apply: true, allowClaudeTitleFixture: true, role: claudeRole, io });
  assert.equal(result.outcome, 'verified', JSON.stringify(result));
  assert.deepEqual(result.steps, ['claude-title', 'herdr-agent', 'herdr-pane', 'hm-rebind']);
  assert.equal(state.native.name, 'Field High 6db4fe');
  assert.equal(state.pane.label, 'Field High 6db4fe');
  assert.equal(state.hm.name, 'flow-6db4fe');
  assert.equal(state.tab.label, 'Shared');
});

test('Claude partial native mutation rolls back through the same adapter', async () => {
  const { io, state } = fixture('native-after-write', 'claude');
  const result = await alignFlow(flow, { apply: true, allowClaudeTitleFixture: true,
    role: { ...role, harness: 'claude' }, io });
  assert.equal(result.outcome, 'failed');
  assert.deepEqual(result.rollback, ['claude-title']);
  assert.equal(state.native.name, 'old-title');
});

test('Claude apply is blocked without a supported title adapter', async () => {
  const { io } = fixture(null, 'claude');
  delete io.setClaudeSessionTitle;
  await assert.rejects(() => alignFlow(flow, { apply: true, allowClaudeTitleFixture: true,
    role: { ...role, harness: 'claude' }, io }), /Claude apply requires/);
});

test('live Claude native-title mutation is disabled after observed sibling propagation', async () => {
  const { io } = fixture(null, 'claude');
  await assert.rejects(() => alignFlow(flow, { apply: true,
    role: { ...role, harness: 'claude' }, io }), /affects sibling sessions/);
});

test('Claude route-only alignment does not send native rename', async () => {
  const { io, state } = fixture(null, 'claude');
  io.setClaudeSessionTitle = async () => { throw new Error('native rename must not occur'); };
  const result = await alignFlow(flow, { apply: true, routeOnly: true,
    role: { ...role, harness: 'claude' }, io });
  assert.equal(result.outcome, 'verified', JSON.stringify(result));
  assert.deepEqual(result.steps, ['herdr-agent', 'herdr-pane', 'hm-rebind']);
  assert.equal(result.nativeTitleStatus, 'deferred-isolation-unproven');
  assert.equal(state.native.name, 'old-title');
  assert.equal(state.agent.name, 'flow-6db4fe');
});
