import assert from 'node:assert/strict';
import {test} from 'node:test';
import {assess} from './field-checkup-shadow.mjs';

const now = Date.parse('2026-09-20T23:00:00Z');
const native = '11111111-1111-1111-1111-111111111111';
const tiers = ['high','medium','low','ultra_low'];
const aspects = ['Field','Mind','Psyche'];
function fixture() {
  let number = 1;
  const roster = {version:1, revision:'fixture', aspects:{}};
  const rows = [];
  for (const aspect of aspects) {
    roster.aspects[aspect] = {};
    for (const tier of tiers) {
      const flow_id = (number++).toString(16).padStart(6,'0');
      roster.aspects[aspect][tier] = {flow_id, native_thread:native};
      rows.push({flow_id, binding_state:'exact', native_thread:native, provenance_gap:false, status:'idle', pane_id:`p${flow_id}`});
    }
  }
  return {roster, snapshot:{complete:true, observed_at:'2026-09-20T22:59:59Z', rows}};
}

test('no duty never becomes a wake decision even with twelve idle exact seats', () => {
  const {roster,snapshot} = fixture();
  const result = assess(snapshot, roster, undefined, now);
  assert.equal(result.aspects.Field.decision, 'DutyUnknown');
  assert.equal(result.aspects.Mind.decision, 'DutyUnknown');
  assert.equal(result.census_fresh, true);
  assert.equal(result.wake_attempts, 0);
});

test('missing seat and source gap block a due review', () => {
  const {roster,snapshot} = fixture();
  roster.aspects.Psyche.ultra_low = null;
  const due = {aspects:{Psyche:{mode:'ReviewDue',duty_id:'review-1'}}};
  let result = assess(snapshot, roster, due, now);
  assert.equal(result.aspects.Psyche.decision, 'Inconclusive');
  assert.deepEqual(result.aspects.Psyche.recovery_required, ['ultra_low']);
  snapshot.complete = false;
  result = assess(snapshot, roster, due, now);
  assert.equal(result.aspects.Psyche.decision, 'Inconclusive');
  assert.equal(result.wake_attempts, 0);
});

test('working hints suppress review; otherwise pending evidence remains required', () => {
  const {roster,snapshot} = fixture();
  const due = {aspects:{Field:{mode:'WorkDue',duty_id:'work-1'}}};
  snapshot.rows.find(row => row.flow_id === roster.aspects.Field.low.flow_id).status = 'working';
  assert.equal(assess(snapshot, roster, due, now).aspects.Field.decision, 'SuppressedByObservedActivity');
  snapshot.rows.find(row => row.flow_id === roster.aspects.Field.low.flow_id).status = 'idle';
  assert.equal(assess(snapshot, roster, due, now).aspects.Field.decision, 'PendingAndDeliveryEvidenceRequired');
});
