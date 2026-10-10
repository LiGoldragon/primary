#!/usr/bin/env node
/* Read-only aspect assessment. It never creates duty, sends wake, or changes seats. */
import fs from 'node:fs';
import path from 'node:path';
import {structuralReport} from './field-structure.mjs';

const aspects = ['Field', 'Mind', 'Psyche'];
const tiers = ['high', 'medium', 'low', 'ultra_low'];

function validatedRoster(value) {
  if (!value || value.version !== 1 || !value.aspects) throw new Error('invalid roster version');
  for (const aspect of aspects) {
    const seats = value.aspects[aspect];
    if (!seats || tiers.some(tier => !Object.hasOwn(seats, tier))) throw new Error(`roster lacks ${aspect} tier`);
    for (const tier of tiers) {
      const seat = seats[tier];
      if (seat !== null && (!/^[a-f0-9]{6}$/.test(seat.flow_id) || !/^[0-9a-f-]{36}$/.test(seat.native_thread))) {
        throw new Error(`invalid ${aspect}/${tier} binding declaration`);
      }
      const profile = value.expected_profiles?.[aspect]?.[tier];
      if (profile && (typeof profile.role !== 'string' || typeof profile.model !== 'string' ||
          !['claude','codex'].includes(profile.harness) || typeof profile.source !== 'string' ||
          (profile.effort !== null && typeof profile.effort !== 'string'))) {
        throw new Error(`invalid ${aspect}/${tier} expected profile`);
      }
    }
  }
  return value;
}

export function assess(snapshot, roster, duties = {aspects:{}} , nowMs = Date.now()) {
  validatedRoster(roster);
  const ageSeconds = Math.max(0, (nowMs - Date.parse(snapshot.observed_at)) / 1000);
  const sourcesFresh = snapshot.complete === true && Number.isFinite(ageSeconds) && ageSeconds <= 600;
  const outcomes = {};
  for (const aspect of aspects) {
    const seats = {};
    for (const tier of tiers) {
      const expected = roster.aspects[aspect][tier];
      if (expected === null) { seats[tier] = {state:'missing-declaration', flow_id:null}; continue; }
      const candidates = snapshot.rows.filter(row => row.flow_id === expected.flow_id);
      const row = candidates.length === 1 ? candidates[0] : null;
      let state = 'unobserved';
      if (candidates.length > 1) state = 'ambiguous';
      else if (row?.binding_state === 'exact' && row.native_thread === expected.native_thread && !row.provenance_gap) state = 'exact-observed';
      else if (row) state = 'binding-mismatch';
      seats[tier] = {state, flow_id:expected.flow_id, native_thread:expected.native_thread,
        observed_status:row?.status ?? null, pane_id:row?.pane_id ?? null,
        transcript_available:Boolean(row?.transcript_path), context_pct:row?.context_pct ?? null,
        source_snapshot:snapshot.observed_at};
    }
    const missing = tiers.filter(tier => seats[tier].state !== 'exact-observed');
    const activeHints = tiers.filter(tier => ['working', 'blocked'].includes(seats[tier].observed_status));
    const duty = duties.aspects?.[aspect] ?? null;
    let decision = 'DutyUnknown';
    if (duty?.mode === 'Paused' || duty?.mode === 'Held' || duty?.mode === 'PermittedIdle') decision = 'HealthyIdle';
    else if (duty?.mode === 'ReviewDue' || duty?.mode === 'WorkDue') {
      if (!sourcesFresh || missing.length) decision = 'Inconclusive';
      else if (activeHints.length) decision = 'SuppressedByObservedActivity';
      else decision = 'PendingAndDeliveryEvidenceRequired';
    }
    outcomes[aspect] = {decision, duty_ref:duty?.duty_id ?? null, seats,
      coverage:{exact:tiers.length - missing.length, expected:tiers.length, missing_or_mismatched:missing},
      active_hints:activeHints,
      recovery_required:missing.length ? missing : [],
      wake: 'disabled-shadow',
    };
  }
  return {version:1, kind:'field-checkup-shadow', observed_at:new Date(nowMs).toISOString(),
    census_at:snapshot.observed_at, census_age_seconds:ageSeconds, census_complete:snapshot.complete,
    census_fresh:sourcesFresh, census_sources:snapshot.sources ?? null,
    host_health:snapshot.health ?? null, roster_revision:roster.revision ?? null,
    structure:structuralReport(snapshot, roster, nowMs), aspects:outcomes,
    wake_attempts:0, lifecycle_actions:0};
}

if (process.argv[1] && path.resolve(process.argv[1]) === new URL(import.meta.url).pathname) {
  const [censusFile, rosterFile, dutyFile] = process.argv.slice(2);
  if (!censusFile || !rosterFile) {
    console.error('usage: field-checkup-shadow CENSUS.json ROSTER.json [DUTIES.json]');
    process.exit(2);
  }
  try {
    const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
    const result = assess(read(censusFile), read(rosterFile), dutyFile ? read(dutyFile) : undefined);
    console.log(JSON.stringify(result));
  } catch (error) { console.error(error.stack || error); process.exitCode = 1; }
}
