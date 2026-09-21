import assert from 'node:assert/strict';
import {test} from 'node:test';
import {structuralReport} from './field-structure.mjs';

const aspects = ['Field','Mind','Psyche'], tiers = ['high','medium','low','ultra_low'];
const native = '11111111-1111-1111-1111-111111111111';
const time = Date.parse('2026-09-20T23:00:00Z');
function fixture() {
  let index=0;
  const roster={version:1,revision:'r1',aspects:{},protected_extras:{}};
  const rows=[];
  for(const aspect of aspects) {
    roster.aspects[aspect]={};
    for(const tier of tiers) {
      const flow_id=(++index).toString(16).padStart(6,'0');
      roster.aspects[aspect][tier]={flow_id,native_thread:native,role:`${aspect} ${tier}`,
        harness:'codex',model:'gpt-5.6-luna',effort:'medium',native_receipt_ref:`receipt-${flow_id}`};
      rows.push({flow_id,native_thread:native,binding_state:'exact',provenance_gap:false,
        pane_id:`p${index}`,terminal_id:`t${index}`,agent_name:`agent-${index}`,
        harness:'codex',interactive_ready:true,status:'idle',display_model:'gpt-5.6-luna',
        display_effort:'medium',model_evidence:'terminal-status'});
    }
  }
  return {roster,snapshot:{complete:true,observed_at:'2026-09-20T22:59:59Z',session:'messaging-build',rows}};
}

test('a complete unique grid has twelve mapped cells but native assignment stays unverified', () => {
  const {roster,snapshot}=fixture();
  const report=structuralReport(snapshot,roster,time);
  assert.equal(report.structural_state,'Inconclusive');
  assert.equal(report.findings.uniquely_mapped_cells,12);
  assert.equal(report.ghosts.length,0);
  assert.equal(report.gaps.length,0);
  assert.equal(report.unknown_cells.length,12);
});

test('twelve panes still fail when one cell is absent and one extra pane is retained', () => {
  const {roster,snapshot}=fixture();
  const missing=snapshot.rows.shift();
  snapshot.rows.push({...missing,flow_id:'abc123',native_thread:'22222222-2222-2222-2222-222222222222',pane_id:'extra',terminal_id:'term-extra'});
  roster.protected_extras.abc123={disposition:'Protected',reason:'retained crossover'};
  const report=structuralReport(snapshot,roster,time);
  assert.equal(report.findings.observed_panes,12);
  assert.equal(report.structural_state,'Nonconforming');
  assert.equal(report.gaps.length,1);
  assert.equal(report.gaps[0].reason,'MissingPane');
  assert.equal(report.ghosts.length,1);
  assert.equal(report.ghosts[0].disposition,'Protected');
  assert.equal(report.ghosts[0].removal_authorized,false);
});

test('a mapped pane with unavailable harness fails health separately from a gap', () => {
  const {roster,snapshot}=fixture();
  snapshot.rows[0].interactive_ready=false;
  let report=structuralReport(snapshot,roster,time);
  assert.equal(report.gaps.length,0);
  assert.equal(report.harness_findings[0].health,'Unavailable');
  assert.equal(report.structural_state,'Nonconforming');
  assert.equal(report.ghosts.length,0);
  snapshot.rows[0].interactive_ready=true;
  snapshot.rows[0].interactive_ready=null;
  report=structuralReport(snapshot,roster,time);
  assert.equal(report.harness_findings[0].health,'Unknown');
  snapshot.rows[0].interactive_ready=true;
  report=structuralReport(snapshot,roster,time);
  assert.equal(report.structural_state,'Inconclusive');
  assert.equal(report.unknown_cells.length,12);
  assert.equal(report.unknown_cells[0].assignment,'Unverified');
  snapshot.complete=false;
  assert.equal(structuralReport(snapshot,roster,time).structural_state,'Inconclusive');
});

test('eight designated panes plus one extra are four gaps and one ghost', () => {
  const {roster,snapshot}=fixture();
  snapshot.rows=snapshot.rows.slice(0,8);
  snapshot.rows.push({pane_id:'extra',terminal_id:'extra-term',flow_id:null,binding_state:'unbound',status:'idle'});
  const report=structuralReport(snapshot,roster,time);
  assert.equal(report.findings.observed_panes,9);
  assert.equal(report.findings.gap_count,4);
  assert.equal(report.findings.ghost_count,1);
});

test('duplicate mapping conflicts, while repeated joins to one physical pane do not inflate count', () => {
  const {roster,snapshot}=fixture();
  snapshot.rows.push({...snapshot.rows[0]});
  let report=structuralReport(snapshot,roster,time);
  assert.equal(report.findings.observed_panes,12);
  assert.equal(report.gaps.length,0);
  assert.equal(report.ghosts.length,0);
  snapshot.rows.push({...snapshot.rows[0],pane_id:'p-duplicate',terminal_id:'t-duplicate'});
  report=structuralReport(snapshot,roster,time);
  assert.equal(report.findings.observed_panes,13);
  assert.equal(report.gaps[0].reason,'DuplicateMapConflict');
  assert.equal(report.ghosts.length,2);
  assert.equal(report.ghosts.every(x=>x.removal_authorized===false),true);
});

test('declared Haiku profile is retained for a missing Psyche Ultra Low binding', () => {
  const {roster,snapshot}=fixture();
  roster.aspects.Psyche.ultra_low=null;
  roster.expected_profiles={Psyche:{ultra_low:{role:'Psyche ultra low',model:'Haiku',harness:'claude',effort:null,source:'living-correction'}}};
  const report=structuralReport(snapshot,roster,time);
  const gap=report.gaps.find(x=>x.cell==='Psyche/ultra_low');
  assert.equal(gap.reason,'MissingBinding');
  assert.equal(gap.declared_model,'Haiku');
  assert.equal(gap.declared_harness,'claude');
  assert.equal(gap.flow_id,null);
  assert.equal(report.launch_authorized,false);
});
