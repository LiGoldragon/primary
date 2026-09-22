import assert from 'node:assert/strict';
import test from 'node:test';
import {createState, transition, plan} from './network-mode-nexus.mjs';

const iface = (kind, name) => ({kind, name});
const edge = mode => ({id: 'ouranos', mode, uplink: iface('integrated', 'enp1s0'), downlink: iface('usb', 'enx-usb0')});
const transit = mode => ({id: 'prometheus', mode, parent: 'ouranos', uplink: iface('integrated', 'enp2s0'), downlink: iface('usb', 'enx-usb1')});
const leaf = {id: 'zeus', mode: 'leaf', parent: 'prometheus', uplink: iface('integrated', 'enp3s0')};
const apply = (state, node, actor = 'network-admin') => transition(state, {expectedRevision: state.revision, actor, reason: 'test transition', at: '2026-09-22T00:00:00Z', node});

function chain() {
  let state = createState({rootPool: '10.44.0.0/16', linkPrefix: 24});
  state = apply(state, edge('edge-gateway'));
  state = apply(state, transit('transit-gateway'));
  return apply(state, leaf);
}

test('allocates a routed chain with one edge NAT owner', () => {
  const output = plan(chain());
  assert.deepEqual(output.natOwners, ['ouranos']);
  assert.equal(output.allocations['link:ouranos:prometheus'].cidr, '10.44.0.0/24');
  assert.equal(output.allocations['link:prometheus:zeus'].cidr, '10.44.1.0/24');
  assert.equal(output.actions.filter(x => x.kind === 'OwnEgressNat').length, 1);
  assert.ok(output.actions.some(x => x.kind === 'PublishRoute' && x.prefix === '10.44.1.0/24'));
  assert.equal(output.liveNetworkChanged, false);
});

test('optional AP gets an explicit separate subnet', () => {
  let state = chain();
  state = apply(state, edge('edge-gateway-ap'));
  const output = plan(state);
  assert.equal(output.allocations['ap:ouranos'].cidr, '10.44.2.0/24');
  assert.ok(output.actions.some(x => x.kind === 'EnableOptionalAp' && x.node === 'ouranos' && x.automatic === false));
});

test('disabled and re-enabled AP keeps its reservation', () => {
  let state = chain();
  state = apply(state, edge('edge-gateway-ap'));
  const held = state.allocations['ap:ouranos'].cidr;
  state = apply(state, edge('edge-gateway'));
  assert.equal(plan(state).allocations['ap:ouranos'].active, false);
  state = apply(state, edge('edge-gateway-ap'));
  assert.equal(plan(state).allocations['ap:ouranos'].cidr, held);
});

test('stale compare-and-swap revision refuses', () => {
  const state = chain();
  assert.throws(() => transition(state, {expectedRevision: 0, actor: 'admin', reason: 'stale', node: leaf}), /stale revision/);
});

test('cycles, duplicate edges, and ambiguous interface roles refuse', () => {
  let state = chain();
  assert.throws(() => apply(state, {...edge('edge-gateway'), id: 'other'}), /exactly one edge/);
  assert.throws(() => apply(state, {...transit('transit-gateway'), downlink: iface('usb', 'enp2s0')}), /must differ/);
  state = apply(state, {...leaf, mode: 'transit-gateway', downlink: iface('usb', 'enx-usb2')});
  assert.throws(() => apply(state, {...state.nodes.prometheus, parent: 'zeus'}), /cycle/);
});

test('audit records actor, reason, revision, and mode transition without secrets', () => {
  const state = chain();
  assert.equal(state.revision, 3);
  assert.deepEqual(Object.keys(state.audit[2]).sort(), ['actor','at','fromMode','nodeId','reason','revision','toMode'].sort());
  assert.equal(state.audit[2].actor, 'network-admin');
});

test('persisted duplicate or malformed allocation records refuse', () => {
  const duplicate = chain();
  duplicate.allocations['link:prometheus:zeus'] = {...duplicate.allocations['link:ouranos:prometheus']};
  assert.throws(() => plan(duplicate), /duplicated/);
  const wrongCidr = chain();
  wrongCidr.allocations['link:prometheus:zeus'].cidr = '10.44.99.0/24';
  assert.throws(() => plan(wrongCidr), /does not match/);
  const missing = chain();
  delete missing.allocations['link:prometheus:zeus'];
  assert.throws(() => plan(missing), /allocation missing/);
});
