import assert from 'node:assert/strict';
import {test} from 'node:test';
import {joinCensus} from './field-census.mjs';

test('only an exact pane, terminal, name, harness, and session binds a Flow', () => {
  const agent = {name:'field-low', agent:'codex', agent_status:'idle', pane_id:'wA:p1', terminal_id:'term_a', interactive_ready:true};
  const pane = {pane_id:'wA:p1', terminal_id:'term_a', agent:'codex'};
  const binding = {flow_id:'abc123', session:'messaging-build', name:'field-low', agent:'codex', pane_id:'wA:p1', terminal_id:'term_a', native_thread:null};
  const common = {agents:[agent], panes:[pane], screens:new Map([['field-low',{ok:true,value:'Context 61% used · weekly 2% left'}]]), locks:new Map(), codexIndex:new Map()};
  const exact = joinCensus({...common, bindings:[binding]});
  assert.equal(exact.length, 1);
  assert.equal(exact[0].flow_id, 'abc123');
  assert.equal(exact[0].binding_state, 'exact');
  assert.equal(exact[0].provenance_gap, true);
  assert.equal(exact[0].native_thread, null);
  assert.equal(exact[0].herdr_session, 'messaging-build');
  assert.equal(exact[0].context_pct, 61);
  assert.equal(exact[0].quota_pct, 2);

  const mismatched = joinCensus({...common, bindings:[{...binding, terminal_id:'term_old'}]});
  assert.deepEqual(mismatched.map(row => row.binding_state), ['unbound', 'stale']);
  assert.equal(mismatched[0].flow_id, null);
  assert.equal(mismatched[1].flow_id, 'abc123');
});

test('duplicate exact bindings remain ambiguous', () => {
  const agent = {name:'field-low', agent:'codex', agent_status:'done', pane_id:'wA:p1', terminal_id:'term_a'};
  const binding = {session:'messaging-build', name:'field-low', agent:'codex', pane_id:'wA:p1', terminal_id:'term_a', native_thread:null};
  const rows = joinCensus({agents:[agent], panes:[{pane_id:'wA:p1', terminal_id:'term_a'}], bindings:[{...binding,flow_id:'abc123'},{...binding,flow_id:'def456'}], screens:new Map(), locks:new Map(), codexIndex:new Map()});
  assert.equal(rows[0].binding_state, 'ambiguous');
  assert.equal(rows[0].flow_id, null);
  assert.deepEqual(rows.slice(1).map(x => x.binding_state), ['stale','stale']);
});
