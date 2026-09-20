/* Twelve-cell Field/Mind/Psyche grid projection. Diagnosis only. */
const aspects = ['Field', 'Mind', 'Psyche'];
const tiers = ['high', 'medium', 'low', 'ultra_low'];

function expectedCell(roster, aspect, tier) {
  const declaration = roster.aspects[aspect][tier];
  return {cell:`${aspect}/${tier}`, aspect, tier, declaration};
}

export function structuralReport(snapshot, roster, nowMs = Date.now()) {
  const expected = aspects.flatMap(aspect => tiers.map(tier => expectedCell(roster, aspect, tier)));
  const distinct = new Map();
  for (const row of snapshot.rows.filter(row => row.binding_state !== 'stale' && row.pane_id)) {
    const key = `${row.herdr_session ?? snapshot.session}\0${row.pane_id}\0${row.terminal_id}`;
    if (!distinct.has(key)) distinct.set(key, row);
  }
  const panes = [...distinct.values()];
  const matchedPanes = new Set(), cells = [], gaps = [], unknown_cells = [];
  const harness_findings = [], assignment_findings = [];
  const ageSeconds = (nowMs - Date.parse(snapshot.observed_at)) / 1000;
  const fresh = snapshot.complete === true && Number.isFinite(ageSeconds) && ageSeconds >= 0 && ageSeconds <= 600;

  for (const item of expected) {
    const declared = item.declaration;
    const base = {cell:item.cell, aspect:item.aspect, tier:item.tier,
      declared_role:declared?.role ?? null, declared_model:declared?.model ?? null,
      declared_effort:declared?.effort ?? null, declared_harness:declared?.harness ?? null,
      flow_id:declared?.flow_id ?? null, native_thread:declared?.native_thread ?? null};
    if (!declared) {
      const result = {...base, state:'Gap', reason:'MissingDeclaration', pane_id:null,
        harness_health:'Unknown', assignment:'Unverified', pending_response:'Unknown'};
      cells.push(result); gaps.push(result); continue;
    }
    const candidates = panes.filter(row => row.flow_id === declared.flow_id);
    const exact = candidates.filter(row => row.binding_state === 'exact' && row.native_thread === declared.native_thread && !row.provenance_gap);
    const row = exact.length === 1 ? exact[0] : null;
    let state, reason;
    if (!candidates.length) { state='Gap'; reason=snapshot.rows.some(r => r.flow_id === declared.flow_id) ? 'StaleBindingOrMissingPane' : 'MissingPane'; }
    else if (exact.length !== 1) { state='Gap'; reason=exact.length > 1 ? 'DuplicateMapConflict' : 'BindingMismatch'; }
    else { state='Mapped'; reason='UniquePhysicalPane'; }
    const harness_health = !row ? 'Unknown'
      : row.interactive_ready === false || !['codex','claude'].includes(row.harness) || row.status === 'unreachable' ? 'Unavailable'
      : row.native_health?.state === 'Operational' && row.native_health?.thread_id === declared.native_thread ? 'Operational' : 'Unknown';
    const assignment = !row ? 'Unverified'
      : declared.harness && row.harness !== declared.harness ? 'HarnessMismatch'
      : declared.model && row.display_model && declared.model !== row.display_model ? 'ModelMismatch'
      : declared.effort && row.display_effort && declared.effort !== row.display_effort ? 'EffortMismatch'
      : 'Unverified';
    const result = {...base, state, reason, pane_id:row?.pane_id ?? candidates[0]?.pane_id ?? null,
      terminal_id:row?.terminal_id ?? candidates[0]?.terminal_id ?? null,
      observed_harness:row?.harness ?? candidates[0]?.harness ?? null,
      observed_model:row?.display_model ?? null, observed_effort:row?.display_effort ?? null,
      observed_status:row?.status ?? candidates[0]?.status ?? null,
      harness_health, assignment, harness_interactive_hint:row?.interactive_ready ?? null,
      native_receipt_ref:declared.native_receipt_ref ?? null,
      model_evidence:row?.model_evidence ?? null,
      pending_response:'Unknown'};
    cells.push(result);
    if (state === 'Gap') gaps.push(result);
    else if (harness_health === 'Unknown' || assignment === 'Unverified') unknown_cells.push(result);
    if (row) matchedPanes.add(`${row.pane_id}\0${row.terminal_id}`);
    if (state === 'Mapped' && harness_health !== 'Operational') harness_findings.push({cell:item.cell, health:harness_health, pane_id:row.pane_id});
    if (state === 'Mapped' && assignment !== 'Matched') assignment_findings.push({cell:item.cell, assignment, pane_id:row.pane_id});
  }

  const protectedExtras = roster.protected_extras ?? {};
  const ghosts = panes.filter(row => !matchedPanes.has(`${row.pane_id}\0${row.terminal_id}`)).map(row => {
    const protection = protectedExtras[row.terminal_id] ?? (row.flow_id ? protectedExtras[row.flow_id] : null);
    return {pane_id:row.pane_id, terminal_id:row.terminal_id, flow_id:row.flow_id,
      agent_name:row.agent_name, harness:row.harness, status:row.status,
      native_thread:row.native_thread, binding_state:row.binding_state,
      disposition:protection?.disposition ?? 'Unreviewed',
      disposition_reason:protection?.reason ?? null,
      lock_count:row.lock_count ?? 0,
      removal_authorized:false};
  });
  const definiteMismatch = harness_findings.some(x => x.health === 'Unavailable') || assignment_findings.some(x => x.assignment.endsWith('Mismatch'));
  const structural_state = !fresh ? 'Inconclusive'
    : gaps.length || ghosts.length || definiteMismatch ? 'Nonconforming'
    : unknown_cells.length ? 'Inconclusive' : 'Conforming';
  return {version:1, kind:'StructuralReport', snapshot_at:snapshot.observed_at,
    snapshot_complete:snapshot.complete, snapshot_age_seconds:ageSeconds,
    policy_revision:roster.revision ?? null, scope:{session:snapshot.session ?? null, aspects, tiers},
    expected_cells:expected.map(x => x.cell), cells, gaps, unknown_cells, ghosts,
    harness_findings, assignment_findings,
    findings:{observed_panes:panes.length, expected_panes:12, uniquely_mapped_cells:matchedPanes.size,
      gap_count:gaps.length, ghost_count:ghosts.length, unknown_cell_count:unknown_cells.length},
    structural_state, removal_authorized:false, launch_authorized:false};
}
