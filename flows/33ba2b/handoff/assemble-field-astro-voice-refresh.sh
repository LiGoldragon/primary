#!/usr/bin/env bash
# Deterministically assemble the two-seat Field refresh handoff from witnessed
# workspace sources. Run from the Primary checkout root or any directory.
set -euo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
out_dir="$root/flows/33ba2b/handoff"
prompt="$out_dir/field-astro-voice-refresh.md"
manifest="$out_dir/field-astro-voice-source-manifest.md"
primary_commit=7cbaa9d5f575

sources=(
  "flows/8393ca/vision/operational-herdrVoiceAccess.md"
  "flows/8393ca/handoff/primary-field-context.md"
  ".claude/skills/field/SKILL.md"
  ".claude/skills/messaging/SKILL.md"
  ".claude/skills/herdr/SKILL.md"
  ".claude/skills/behavior/SKILL.md"
  ".claude/skills/testing/SKILL.md"
  ".claude/skills/subflow/SKILL.md"
  "flows/b05237/messaging-skill-design.md"
  "reports/herdr-user-guide-0.8.2.md"
  "Vision/nexus.md"
  "flows/b05237/vision/operational-theField.md"
  "flows/b05237/vision/operational-mainFlowUsesSubflows.md"
  "flows/b05237/vision/operational-fieldFlowNotReaper.md"
  "flows/b05237/vision/operational-fieldTestingAndUltraLow.md"
  "flows/b05237/vision/operational-skillTypesTriad.md"
  "flows/33ba2b/vision/operational-fieldRefreshSuccession.md"
)

for source in "${sources[@]}"; do
  test -f "$root/$source" || { echo "missing source: $source" >&2; exit 1; }
done

test "$(jj file show -r "$primary_commit" \
  flows/8393ca/vision/operational-herdrVoiceAccess.md | sha256sum | cut -d' ' -f1)" = \
  "$(sha256sum "$root/flows/8393ca/vision/operational-herdrVoiceAccess.md" | cut -d' ' -f1)" || {
  echo "voice source differs from $primary_commit" >&2; exit 1;
}

{
  cat <<'PROMPT'
# Field two-seat refresh: first-turn brief

This is a mechanically assembled source bundle for a **two-seat** refresh of
Field Sol `33ba2b`. It does not launch either seat.

## Launch identities and boundaries

Launch two distinct descendant main flows, each with a newly claimed,
distinct `FLOW_ID` and its own `FLOW_DIRECTORY`:

| Name | Role and native runtime | Scope |
| --- | --- | --- |
| `field-astra-of-33ba2b` | Field Astra; companion Field seat. The launcher must witness and record its actual native model and effort before naming them. | Diagnose, design, investigate, and help repair the Field. It is neither Psyche nor Mind. |
| `field-sol-of-33ba2b` | Field Sol; `gpt-5.6-sol`, medium effort. | Inherits the ongoing Field ownership and coordinates maintenance. |

`of-33ba2b` means *descendant of* the predecessor, not a current active ID.
The naming and two-seat refresh shape are candidate core refresh-skill vision,
not merely an ad-hoc label; do not silently treat that future skill change as
already deployed.

Neither seat replaces Psyche or Mind. Neither activates the chartered private
layer. The main flow delegates bounded task work; do not use collaboration
subagents as native Flow-Nexus flows. Start investigation with Luna and retain
its findings if escalation to Terra is needed. No automatic reaping: a Field
observer reports evidence and the authorized lifecycle owner decides any
cleanup.

## Field mission and honest state

The living wants the Field kept deployed, repaired, and working well. Treat
that as an operational mission, not a present-tense success claim. Field Astra
diagnoses, designs, and helps repair; descendant Field Sol inherits ongoing
maintenance. Do not say “running well,” “fixed,” or “deployed” absent current
live witnesses for the specific boundary.

Open ownership carried forward:

- Desktop voice route remains **unproven**: the desktop application has a
  separate app-server/discovery boundary from a managed remote daemon.
- Stale desktop writer/archive cleanup; Field Nexus conceptual reports;
  headset-hold gesture verification after a new login; and branch-psyche
  consolidation remain open.
- Approved target-repository migration remains unperformed. The proposed
  Spirit sentence remains unapproved.
- The newest psyche/mind logging architecture is open and unmigrated: raw
  material belongs under `raw/<flow-id>`; distilled Psyche is organized by
  subject spaces and notion/vision/intent/spirit; Mind holds witnesses and
  technical chronology. Current words must be logged into Psyche on Primary
  main now. Primary Next will later migrate data into repos named `Psyche
  data` and `Mind data` and link them from Primary Next. Do not create, move,
  or claim deployment of those trees in this refresh.
- OS staging is reported only: CriomOS-home `e17ec33a`, CriomOS `63edfc9f`,
  deployments 20/21 `Completed/Succeeded` with `ProfileOnly`; login is still
  required and the headset key is unverified. These are handoff claims, not
  fresh verification.
- Protect Field Sol from routine probes/retries. Field low is Terra; Field
  ultra-low is Luna and is the disposable isolated testing tier.

## Required launch acceptance gates

Do not call the refresh complete until the following are independently
witnessed and recorded with exact bindings:

1. The generated skills are current/deployed through the established route.
2. Both named descendants are live with distinct fresh IDs, their native
   model/effort witnessed, and their Herdr/terminal endpoints identified.
3. Each seat is HM addressable through a fresh, exact identity-to-endpoint
   registration, and its recipient-side acknowledgment is directly observed.
4. The intended managed remote daemon, terminal attachment, desktop discovery,
   and interactive voice are tested as one route. A daemon/phone/TUI witness
   alone does not prove desktop voice access.
5. Relevant services and message routing have current live checks; known Field
   defects are explicitly assigned with evidence rather than assumed gone.

Use the receipt grades in the attached messaging source. A route’s submission,
presentation, reader acknowledgement, and requested completion are distinct.
For the launch back-ack to predecessor `33ba2b`, record the exact source seat,
destination binding, transport, time, receipt grade, and recipient-side text.

## Herdr and messaging posture

Herdr is the terminal workspace substrate, not the identity resolver or durable
receipt ledger. Prefer one active zoomed pane and one companion; use a named
tab/workspace for overflow and only a temporary named 2×2 monitoring grid.
Closing a pane is not itself proof that a harness died. A watcher may mark an
endpoint suspect or stale and report it, but cannot silently stop sessions,
reap, change layouts, or rewrite the authoritative messaging index.

Use a current exact identity binding per attempt. Preserve the distinction
between durable attempts and compatibility transport; do not replay a parked
attempt automatically. Keep living words, quoted source, STT corrections, and
Field-authored framing distinct.

## First actions

1. Read the attached exact sources and locate current live state with safe,
   bounded, Luna-first investigation.
2. Make a small evidence-backed Field status report: live witnesses, reported
   claims, unknowns, and assigned defects. Do not mutate OS, deployment,
   terminal, or archive state merely to make the report.
3. Ask Psyche about desired/undecided shape and Mind for current evidenced
   state, without substituting either role.
4. Form a scoped repair plan only after identity, route, and ownership are
   witnessed. Keep all unapproved and unperformed items explicitly open.

## Exact source attachments

The remainder of this document is the deterministic source bundle. Each block
is source material, not a new claim made by the two seats.

PROMPT
  for source in "${sources[@]}"; do
    printf '\n## Source: `%s`\n\n' "$source"
    sed 's/^/    /' "$root/$source"
    printf '\n'
  done
} > "$prompt"

{
  printf '%s\n\n' '# Field two-seat refresh source manifest'
  printf '%s\n' 'Generated by flows/33ba2b/handoff/assemble-field-astro-voice-refresh.sh.'
  printf '%s\n' 'The generation checks that the voice source is byte-identical to Primary commit'
  printf '`%s`; all paths below must exist before assembly. Skill entries are\n' "$primary_commit"
  cat <<'MANIFEST'
the current generated read-only projections used as runtime evidence; authored
skill changes remain subject to their Curriculum-source workflow.

| Source path | SHA-256 |
| --- | --- |
MANIFEST
  for source in "${sources[@]}"; do
    printf '| `%s` | `%s` |\n' "$source" "$(sha256sum "$root/$source" | cut -d' ' -f1)"
  done
  cat <<'MANIFEST'

The generated prompt declares two fresh descendants, not an active replacement
of predecessor `33ba2b`: `field-astra-of-33ba2b` and
`field-sol-of-33ba2b`. It specifies no launch or deployment action.

## Current open architecture direction

The living's newest direction, supplied with this refresh, is intentionally
recorded here as an open architecture item rather than as a deployed source
tree: raw material under `raw/<flow-id>`; distilled Psyche by subject spaces
and notion/vision/intent/spirit; Mind for witnesses and technical chronology.
Current words must be logged into Psyche on Primary main now. Primary Next will
later migrate data into repos named `Psyche data` and `Mind data` and link them
from Primary Next. No tree was created or moved, and migration remains
unperformed.
MANIFEST
} > "$manifest"

echo "assembled: $prompt"
echo "manifest: $manifest"
