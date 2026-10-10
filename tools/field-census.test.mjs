import assert from 'node:assert/strict';
import {test} from 'node:test';
import {enrichOverviewContexts, joinCensus, joinOverview, renderOverview} from './field-census.mjs';

test('only an exact pane, terminal, name, harness, and session binds a Flow', () => {
  const agent = {name:'field-low', agent:'codex', agent_status:'idle', pane_id:'wA:p1', terminal_id:'term_a', interactive_ready:true};
  const pane = {pane_id:'wA:p1', terminal_id:'term_a', agent:'codex'};
  const binding = {flow_id:'abc123', session:'messaging-build', name:'field-low', agent:'codex', pane_id:'wA:p1', terminal_id:'term_a', native_thread:null};
  const common = {agents:[agent], panes:[pane], screens:new Map([['field-low',{ok:true,value:'gpt-5.6-terra medium · Context 61% used · weekly 2% left'}]]), locks:new Map(), codexIndex:new Map()};
  const exact = joinCensus({...common, bindings:[binding]});
  assert.equal(exact.length, 1);
  assert.equal(exact[0].flow_id, 'abc123');
  assert.equal(exact[0].binding_state, 'exact');
  assert.equal(exact[0].provenance_gap, true);
  assert.equal(exact[0].native_thread, null);
  assert.equal(exact[0].herdr_session, 'messaging-build');
  assert.equal(exact[0].context_pct, 61);
  assert.equal(exact[0].quota_pct, 2);
  assert.equal(exact[0].display_model, 'gpt-5.6-terra');
  assert.equal(exact[0].display_effort, 'medium');

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

test('overview counts Herdr agents, exact HM routes, and mismatches separately', () => {
  const agent = {name:'field-low', agent:'codex', agent_status:'idle', pane_id:'wA:p1', terminal_id:'term_a'};
  const binding = {flow_id:'abc123', session:'messaging-build', name:'field-low', agent:'codex', pane_id:'wA:p1', terminal_id:'term_a'};
  const joined = joinOverview([agent, {...agent, name:'unregistered', pane_id:'wA:p2', terminal_id:'term_b'}],
    [binding, {...binding, flow_id:'def456', terminal_id:'term_old'}]);
  assert.deepEqual(joined.rows.map(row => row.route), ['exact', 'unmatched']);
  assert.equal(joined.rows[0].flow_id, 'abc123');
  assert.equal(joined.rows[0].availability, 'unknown');
  assert.equal(joined.rows[0].context_tokens, null);
  assert.deepEqual(joined.unmatched_registrations.map(row => row.flow_id), ['def456']);
  const rendered = renderOverview({observed_at:'2026-09-21T00:00:00Z', counts:{herdr_records:2, exact_registered_routes:1, unmatched_herdr_records:1, unmatched_registrations:1}, sources:{herdr_agents:{status:'ok', error:null},hm_registry:{status:'ok',errors:[]}}, ...joined});
  assert.match(rendered, /Herdr records: 2 · exact registered routes: 1/);
  assert.doesNotMatch(rendered, /abc123|def456|term_a|wA:p1/);
});

test('overview rejects ambiguous routes and does not label missing roster as stale', () => {
  const agent = {name:'field-low', agent:'codex', agent_status:'done', pane_id:'wA:p1', terminal_id:'term_a'};
  const binding = {session:'messaging-build', name:'field-low', agent:'codex', pane_id:'wA:p1', terminal_id:'term_a'};
  const duplicate = joinOverview([agent], [{...binding, flow_id:'abc123'}, {...binding, flow_id:'def456'}]);
  assert.equal(duplicate.rows[0].route, 'ambiguous');
  assert.equal(duplicate.rows[0].availability, 'unknown');
  assert.equal(duplicate.unmatched_registrations.length, 2);
  assert.deepEqual(joinOverview([], [binding], false).unmatched_registrations, []);
});

test('overview reads only exact native bindings and keeps unknown observations null', async () => {
  const id = '01a0c44c-784a-7fc1-bd0a-65c6db4fe4f8';
  const rows = [
    {route:'exact',harness:'codex',native_thread:id,context_tokens:null,context_pct:null},
    {route:'ambiguous',harness:'codex',native_thread:id,context_tokens:null,context_pct:null},
    {route:'exact',harness:'claude',native_thread:null,context_tokens:null,context_pct:null},
  ];
  let calls = 0;
  await enrichOverviewContexts(rows, {codexCollector: async ({nativeThreadId}) => {
    calls++;
    return {nativeThreadId, eventAt:'2026-09-21T15:00:00Z', occupancy:{status:'last-input-proxy',lastInputTokens:25,modelContextWindow:100},
      usage:{scope:'thread-cumulative',total:{inputTokens:120,outputTokens:9}},quota:null};
  }});
  assert.equal(calls, 1);
  assert.equal(rows[0].context_tokens, 25);
  assert.equal(rows[0].context_pct, 25);
  assert.equal(rows[0].context_quality, 'proxy');
  assert.equal(rows[1].context, undefined);
  assert.equal(rows[2].context_tokens, null);
  await enrichOverviewContexts(rows, {codexCollector: async ({nativeThreadId}) => ({
    nativeThreadId, occupancy:{status:'superseded',lastInputTokens:25,modelContextWindow:100},
  })});
  assert.equal(rows[0].context_tokens, null);
  assert.equal(rows[0].context_pct, null);
});

test('overview rejects a collector identity mismatch and preserves unavailable evidence', async () => {
  const id = '01a0c44c-784a-7fc1-bd0a-65c6db4fe4f8';
  const rows = [{route:'exact',harness:'codex',native_thread:id,context_tokens:null,context_pct:null}];
  await enrichOverviewContexts(rows, {codexCollector: async () => ({nativeThreadId:'other',occupancy:{lastInputTokens:9}})});
  assert.equal(rows[0].context_tokens, null);
  assert.equal(rows[0].context, undefined);
  await enrichOverviewContexts(rows, {codexCollector: async () => { throw new Error('offline'); }});
  assert.equal(rows[0].context.method, 'unavailable');
  assert.equal(rows[0].context_tokens, null);
});
