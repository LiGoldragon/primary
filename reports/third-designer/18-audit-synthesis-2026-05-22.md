# 18 — Audit synthesis, 2026-05-22

*Third-designer pickup-ready handoff. Supersedes the blocker section
of /17 with the post-audit corrections. Synthesises three audits run
by subagents on psyche authorization 2026-05-22: recent reports across
13 lanes since 2026-05-21, open/closed beads (77 open + 6 closed in
last 2 days), component code state across 43 repos. Intent records
152–156 captured this session — Criome-stack naming, Deploy→lojix,
forge boundary affirmed, pure-Rust trajectory, cluster-operator
specialty.*

## 1. Frame

Three things changed materially since /17:

- **Spirit pilot bumped to v0.1.1 in code today.** `persona-spirit`
  and `signal-persona-spirit` both tagged `v0.1.1` 2026-05-22 with
  the sema-magnitude swap and other 2026-05-21 work merged.
  `owner-signal-persona-spirit` stays at `v0.1.0` — asymmetric
  release worth confirming.
- **Live cutover blocker is write drift, not branch merge.** Per
  `cluster-operator/3`: tags exist on both v0.1.1 repos; the
  `operator/spirit-response-protocol` branch from /280 §5 step 1
  does not exist in any audited repo. Real blocker is records 147
  + 150 written to v0.1.0 after v0.1.1 was staged. Beads
  `primary-x3ci` (cutover) + `primary-chpq` (dual-write wrapper,
  new today) carry the work. Note: /280's six-step sequence is
  partially stale — steps 1–2 are already done.
- **`tools/orchestrate status` fixed locally** by cluster-operator.
  Lane field validated as dynamic token, not closed enum. Durable
  destination remains the typed persona-orchestrate lane registry.

The third-designer/17 blockers thus update to:

- ~~B1: branch merge before cutover~~ → **B1 (active)**: dual-write
  vs default-flip vs high-water-mark replay decision for default
  spirit. Live agents are writing to v0.1.0 right now; every minute
  drifts v0.1.0 ahead of staged v0.1.1.
- ~~B2: `tools/orchestrate` broken~~ → **B2 (closed locally)**.
- **B3 (still active)**: Engine-manager Axis 2 — `supervision_socket_*`
  identifiers (17), `.supervision.sock` constants (8), ~30 ARCH
  lines remain on bead `primary-k2mh`. Note: c620's 2026-05-21
  20:11 comment shows persona-orchestrate work already touched the
  signal-persona engine_management surface, so k2mh's audit may
  be partly stale — re-audit current source before pickup.

## 2. Live frontier (decisions waiting on psyche)

### 2.1 — Spirit cutover chain (highest priority)

Beads: `primary-x3ci` (P1, 4 comments today), `primary-chpq` (P1,
filed 2026-05-22, sibling for the dual-write wrapper),
`primary-qk04` (P2, 2 comments today, multi-version coexistence
general machinery).

Versioned deployment works (`primary-1h0h` closed today). Migrated
v0.1.1 DB staged through record 146. Default `spirit` still writes
to v0.1.0. Three competing approaches:

- **Dual-write wrapper** (`primary-chpq`): unsuffixed `spirit`
  routes accepted writes to both v0.1.0 and v0.1.1 during the
  migration window; old daemon confirms and tells the agent to
  switch.
- **Default flip with read-only fallback**: flip
  `spirit -> spirit-v0.1.1` now; v0.1.0 becomes read-only.
- **High-water-mark replay**: don't flip until sema-engine commit
  sequence lands and migration 2 (or a replay path) can catch the
  delta.

Psyche record 113 was Medium-certainty pending; /278 §3.5 cutover
protocol was the deeper design. **First concrete cutover is the
decision point.**

### 2.2 — EffectEmitted payload typing (blocks 8+ observable blocks)

Per `second-designer/140` (persona-spirit triad parity check) +
`intent/component-shape.nota` 2026-05-20T15:00:00Z. The
`observable` macro injects an `EffectEmitted` event variant; its
payload is open:

- **Typed `Effect`** (component-local) — each persona triad's
  effect type is the event payload.
- **Universal `SemaObservation`** — payloadless cross-component
  classification is the payload.

The 7 unmigrated persona triads (mind, router, message, introspect,
system, terminal, harness) all need to add `observable` blocks per
psyche 2026-05-20T02:00:00Z (Tap/Untap mandatory). They wait on
this decision.

### 2.3 — Lane-identifier reservation policy

`second-designer/149` audit of /147 implementation says intent 118
requires reserved-forever lane identifiers (persistent
`(role,authority)→next_ordinal` counter).

`second-operator/165` says newer psyche clarification removed the
rule — retired identifiers can disappear.

`second-operator/166` ships with the "active table" behavior
(retired IDs disappear).

Open question: is intent 118 superseded? If so, /149's audit
follow-up retires; if not, the registry needs a persistent counter.

## 3. Migration cascade state

The picture from the component code state audit:

### 3.1 — Migrated bloc (current, on signal-frame foundation)

| Component | Working signal | Owner signal | Daemon | Tag |
|---|---|---|---|---|
| spirit (pilot) | ✓ | ✓ | ✓ | v0.1.1 ord / v0.1.0 owner |
| persona-orchestrate | ✓ (lane reg) | ✓ (lane reg) | ✓ | none |
| persona (engine-manager) | ✓ (rename landed) | (no owner repo) | ✓ | none |
| repository-ledger | ✓ | (stale) | ✓ | none |
| sema-upgrade triad | ✓ (prototype) | ✓ (prototype) | ✓ (prototype) | none |

### 3.2 — Next-wave queue (ARCH-aligned, code rewrite pending)

14 contracts received the `align ARCH with three-layer model per
/246-v4` commit on 2026-05-20 with MUST IMPLEMENT markers added.
Code rewrites are not done. Operator beads filed 2026-05-21 sit
untouched (zero comments) except c620:

| Contract | Bead | Status |
|---|---|---|
| signal-persona-mind | `primary-e1pm` | Untouched. WORST shape per /257 (15-variant op root, channel choreography needs split). |
| signal-persona-router | `primary-aunn` | Untouched. |
| signal-persona-message | `primary-krbi` | Untouched. |
| signal-persona-introspect | `primary-li7a` | Untouched. `second-designer/144` is pickup-ready Package 1 design refresh. |
| signal-persona-system | `primary-21gn` | Untouched. |
| signal-persona-terminal | `primary-qjdp` | Untouched. |
| signal-persona-harness | `primary-gu7t` | Untouched. |
| signal-criome | `primary-0bls` | Untouched. |
| signal-forge | (no bead) | Stale; `Deploy` should move to signal-lojix per intent 153 (this session). |
| signal-lojix | `primary-9up1` | Migrated on `horizon-leaner-shape` branch (not main); ARCH-aligned on main. |
| owner-signal-persona-terminal | (in qjdp) | Untouched. |
| owner-signal-repository-ledger | `primary-mdhj` | Untouched. |
| persona engine-manager Axis 2 | `primary-k2mh` | Stale audit; may overlap c620's landed work. |

`primary-u8vo` is the EPIC for the 10-contract migration; needs
decomposition into per-contract beads before pickup per
2026-05-22 11:34 operator audit comment.

### 3.3 — Foundation hygiene pile (gates clean downstream)

| Bead | Title | Status |
|---|---|---|
| `primary-k3bu` | Rename UnknownKindForVerb in consumer codec impls | Untouched. ~15 consumer repos. |
| `primary-77hh` | Drop channel-name prefix from `signal_channel!` emitted types | Landed at `signal-frame@653773b`; consumers still carry the alias-dance. |
| `primary-u0lh` | Extend nota-codec derive coverage | Untouched. |
| `primary-uy7o` | Reject labeled-field NOTA record shape | Untouched. |
| `primary-dzrn` | Native Timestamp type, bare ISO-8601 | Untouched. |

Pickup gate. Without these, contract migrations carry forward
alias-dance + missing derive coverage.

## 4. New design surfaces (since /17)

### 4.1 — Recording system + agent identity (second-designer)

Three large new design reports landed in second-designer (today's
audit revealed them as net-new beyond /17):

- **`second-designer/145`** — `persona-listen` real-time intent
  recording system. Mic → VAD → speaker-ID → ASR → spirit
  `(Record …)` sink. Multi-week build, gated on /148 model pick +
  system-specialist verification on the large-ai-node. **11 open
  psyche questions** including component name, buffer window,
  voice enrolment shape, pass-the-mic gesture, marker vocabulary,
  triad shape, wife's parallel persona location.
- **`second-designer/148`** — Open-weights real-time STT/voice-ID
  research. Recommends Path A pipeline (Silero VAD → pyannote
  speaker ID → faster-whisper or Parakeet-TDT → small LLM) over
  Path B (audio-multimodal) for v1. **Open**: psyche reference to
  "Gemma 4 multi-modal" may be STT/vocabulary mismatch — verify
  whether Gemma 4 actually carries audio input or substitute Phi-4-mm
  / Qwen2-Audio / Ultravox / Voxtral.
- **`second-designer/150`** — Agent identity as BLS12-381 keypair.
  Per-role identity (not per-lane). Intent-capture as per-call
  runtime function (intent 126). Pre-Criome ephemeral key migrates
  cleanly when Criome lands. Refines /264 §4–5.

### 4.2 — Pi/DeepSeek library shape

`designer/281` (today 13:37): Pi has two documented headless
modes (RPC over JSONL stdin/stdout; Node SDK `createAgentSession`).
DeepSeek already supported through shared `pi-ai`.

**Open psyche pick**: three library-wrapper shapes for using Pi
as a substrate beyond persona-pi —

- Rust RPC crate (lowest dependency cost).
- Node lib (richest API access).
- Full `signal-deepseek` triad (most workspace-shaped, biggest
  scope).

Custom-tool registration over RPC is unconfirmed (try-it-and-see
required). Relationship to persona-pi (/266) unsettled: shared
substrate, sibling component, or layered?

### 4.3 — nota-designer (new lane, deliverables landed)

`reports/nota-designer/` exists. Lane registered 2026-05-21.
**Bracket-string design landed** on `nota-bracket-strings` branch:
`nota-codec@538555e8` + `nota@40d62711`. Both pushed to origin.
`[ ... ]` at String/Path/map-key positions is inline string;
`[| ... |]` is block string; encoder canonicalizes non-bare to
bracket strings; legacy `"` still decodes.

Lane is not yet in `orchestrate/roles.list` (role-vector pattern
`[Note Designer]` doesn't fit the bash `parallel-of:`/`assistant-of:`
format).

### 4.4 — cluster-operator (new lane, unregistered)

`reports/cluster-operator/` exists. Per intent 156 (this session)
cluster-operator is the **live system operator**: deploying,
updating, changing things on the live system; careful + knowledgeable
about production lojix.

Deliverables:

- `cluster-operator/1`: Bird→Zeus narrow authority via `lojix-cli`
  (Bird's persona operator Aether updates Bird's Zeus through her
  forked workspace without root SSH).
- `cluster-operator/3`: blocker audit + local fix to `tools/orchestrate`.

Lane not in `orchestrate/roles.list`. Same registry-format issue
as nota-designer.

### 4.5 — System lanes activity

- `system-assistant/25` — signal-lojix contract-local-verbs migration
  landed at `ef98dc0a`. Intent normalisations across
  `intent/deploy.nota` and `intent/arca.nota`. `--max-jobs 0`
  directive made workspace-wide.
- `system-assistant/28` — lojix vision gap audit. **Eight gaps**:
  missing `owner-signal-lojix`, missing policy/working state
  taxonomy, Criome-mediated authorization missing from migration
  order, daemon-to-daemon mesh shape, bootstrap-policy path, etc.
- `system-assistant/29` — lean-horizon cluster data shape on
  `horizon-leaner-shape` branches. Synthesis of 2026-05-20→05-21
  settlings: variants over booleans, no port-numbers/constants in
  horizon, Yggdrasil substrate, beautiful-horizon-over-Nix,
  roles-merge.
- `second-system-assistant/7` — persona-spirit deployed via
  production CriomOS-home (2026-05-21 11:27). Foundation for the
  v0.1.0→v0.1.1 cutover work in operator /154–/156.

## 5. Authority chain consolidations

Settled and confirmed (per second-operator/168):

```
Mind  →  owner-signal-persona-orchestrate
            ↓
         owner-signal-persona-router
```

Mind does NOT call Router owner directly. Channel choreography
decisions live in Mind; Orchestrate enacts. This matches the
mind/body analogy from `reports/second-designer-assistant/16`
(now `reports/third-designer/16`) and resolves my Q10 about
Mind/Router authority — Orchestrate is the seam.

Open: the high-level Mind verbs that carry choreography decisions
before Orchestrate calls Router's Grant/Extend/Revoke/Deny.
`second-operator/165` Q3.

## 6. Workspace housekeeping

### 6.1 — Lane registry format gap

`orchestrate/roles.list` uses `parallel-of:<role>` / `assistant-of:<role>`
markers. Specialized lanes with role-vector tokens (e.g.,
`[Note Designer]`, `[Cluster Operator]`) don't fit the format —
they're operator/designer role with a specialty token, not a
parallel-main or assistant lane.

Two new lanes (`nota-designer`, `cluster-operator`) are currently
operating without registry entries. Choices:

- Extend the bash format with a `specialty-of:<role>` or
  `tokens:<token1>,<token2>` marker.
- Just add bare lane lines without the relation marker (the helper
  validates dynamic tokens per cluster-operator's `tools/orchestrate`
  fix; the relation marker may be optional).
- Wait for the typed persona-orchestrate registry to canonicalize
  the role-vector shape (per `second-designer/3` derivation logic).

Designer lean: the bash format is transitional; the typed registry
already handles role vectors via the `(role, authority, prior_count)`
derivation. Adding bare lane lines with a comment explaining the
role-vector shape is the lowest-cost interim move.

### 6.2 — Specialized-role discipline

Per intent 156 (this session): specialized roles like cluster-operator
need explicit scope declarations. Two surfaces:

- **`skills/role-lanes.md`** — extend with a section on specialized
  lanes; describe how role-vector tokens (e.g., `Cluster`, `Note`)
  declare scope subsets within an authority class.
- **Orchestrate role records** — each lane's role record carries a
  scope declaration when token-vectored. The typed shape is in
  `second-designer/3`; the daemon doesn't yet enforce scope.

Designer follow-up; not blocking pickup of any current bead.

### 6.3 — Stale branches to consider deleting

- `signal-frame/wip-observable-grammar` — superseded by /246
  bundled fix per its own tip subject.
- `persona-orchestrate-mvp` (across all three orchestrate legs) —
  stale at 2026-05-19, main moved to 2026-05-22.

Designer lean: defer to operator/system-specialist for the actual
deletion; flag here so it doesn't get rediscovered.

## 7. Consolidated question list (mine + cluster-operator + second-operator + new audits)

These supersede /17's Q1–Q10. Grouped by topic; numbered by current
priority gate.

### Active blockers (decide first)

**Q1 — Spirit cutover default routing.** Dual-write wrapper
(`primary-chpq`) / default flip with v0.1.0 read-only fallback /
high-water-mark replay. Live agents writing to v0.1.0 right now;
every delay widens the drift. Designer lean: dual-write for the
migration window per the operator-side intent in /156 (records
139+140 specifically asked for dual-write); flip after a confidence
period.

**Q2 — Stop-old-start-new for first migration?** Acceptable for
Spirit 0.1.0→0.1.1 with commit-sequence required from migration 2
onward per intent 56? Designer lean: yes.

**Q3 — EffectEmitted payload type.** Typed `Effect` (component-local)
or universal `SemaObservation` (cross-component)? 8+ pending
observable blocks depend.

**Q4 — Lane-identifier reservation policy.** Intent 118 (reserved
forever) vs second-operator/165's "newer clarification removed it".
If superseded, `second-designer/149`'s follow-up retires; if not,
the typed registry needs a persistent counter.

### Architecture decisions (medium urgency)

**Q5 — Sema-upgrade self-upgrade bootstrap.** Recursive self-
application or hand-written bottom-of-stack? Designer lean:
hand-written until contracts stabilise.

**Q6 — Commit-sequence scope.** Per-database or per-component?
Designer lean: per-database.

**Q7 — Engine-manager Axis 2 timing.** Land now with socket-rename +
Nix update (ABI break) or hold with explicit deferral? Note: k2mh's
audit may be partly stale; check c620's 2026-05-21 work first.

**Q8 — Magnitude collapse.** Health/Readiness + `ItemPriority`
onto `signal-sema::Magnitude` (field name carries dimension)? Or
sibling universal `Health` / `Readiness` types? Designer lean:
collapse.

**Q9 — RejectionReason fanout** for sema-upgrade daemon promotion
— 5 concrete variants (source missing / target exists / component
mismatch / version mismatch / engine-internal). Land in same slice
as `primary-l3h5`?

**Q10 — Forge `forge-nix-builder` extraction timing.** Intent 154
this session settles direction (extract as library). When does it
land? Designer lean: after the next concrete forge consumer needs
it (e.g., the Rust pure-component forge that's the second consumer
of signal-forge per intent 155).

### Strategic/sequencing (lower urgency)

**Q11 — Orchestrate executor migration timing.** Bead `primary-c620`
is in flight; per `second-operator/166` 9-step plan, the next slice
is executor migration. Pause for Spirit cutover, or proceed?
Designer lean: proceed — the surfaces are independent.

**Q12 — Pi/DeepSeek library shape.** Rust RPC / Node lib /
`signal-deepseek` triad? `designer/281` §4.4. Awaits psyche pick.

**Q13 — Persona-pi vs sema-upgrade vs Spirit cutover sequencing.**
Where does the next operator implementation proposal focus?
(Cluster-operator/2 Q7.)

**Q14 — Recording-system 11 open questions.** `second-designer/145`
component name / buffer window / voice enrolment / pass-the-mic
gesture / borderline-intent review / marker vocabulary stability /
real-time model choice / recording-vs-transcription substrate /
triad shape / wife's parallel persona location / laptop-side
process shape.

**Q15 — STT model verification.** `second-designer/148`: does
Gemma 4 actually have audio input? If not, substitute Phi-4-mm /
Qwen2-Audio / Ultravox / Voxtral.

**Q16 — Agent identity** ahead of Criome. `second-designer/150`:
proceed with BLS12-381 ephemeral key now, migrate to Criome later?

**Q17 — Mind channel-choreography verbs.** What high-level verbs
does Mind issue to Orchestrate before Orchestrate calls Router's
Grant/Extend/Revoke/Deny? Blocks `primary-e1pm`.

**Q18 — Lojix vision gaps.** `system-assistant/28` lists 8 gaps
including missing `owner-signal-lojix`. Which take priority?
Cluster-operator's likely pickup queue.

**Q19 — Bird→Zeus authority scope.** `cluster-operator/1`: first
allowed action set — `BootOnce` + `Test` only, or include `Switch`?

**Q20 — owner-signal-persona repo presence.** Engine-manager has
no owner-only contract checkout. Intentional (no privileged
lifecycle on the engine-manager) or gap?

**Q21 — Lane registry format extension.** Bash format
(`parallel-of:`/`assistant-of:`) doesn't carry role-vector lanes.
Extend with a marker, allow bare lane lines, or wait for typed
registry? Designer lean: bare lines for now with a comment.

**Q22 — Asymmetric Spirit release.** `persona-spirit` and
`signal-persona-spirit` at v0.1.1; `owner-signal-persona-spirit`
stays at v0.1.0. Intentional or oversight?

**Q23 — Parallel-main designer protocol coverage** (from /17 Q10).
AGENTS.md singles out "the prime designer" for the subagent-dispatch
exception. Per second-operator/165 "lanes are windows into one role
agent" — does that mean second-designer + third-designer + designer
all share identity and inherit the designer protocol's subagent
authorization? My current third-designer session DID dispatch
subagents this turn (explicit psyche authorization), but the
standing rule is ambiguous.

**Q24 — Lane registration timing.** Should `nota-designer` and
`cluster-operator` get registry entries now (per Q21 format) or
wait?

**Q25 — Concept-designer lane.** Per `designer/234` keeper +
second-operator/165 delta Q2. Real lane registration through
Orchestrate or stay as design report only?

**Q26 — Criome owner-session encryption priority.** Per
`criome/ARCHITECTURE.md` + second-operator/165 delta Q3. Near-term
implementation target or stay behind Spirit/sema-upgrade/orchestrate?

**Q27 — Old operator /108–/135 cleanup.** Cleanup pass to retire
into newer successors, or leave as historical keepers? (Second-
operator/165 delta Q4.)

## 8. Pickup-ready next slices (ranked)

For the picking-up agent with limited context, in priority order:

1. **Spirit cutover dual-write wrapper** — `primary-chpq` is the
   live blocker on v0.1.1 default flip. Operator slice. Depends on
   Q1 psyche decision.
2. **persona-orchestrate executor migration** — `primary-c620`,
   `second-operator/166` 9-step plan. Operator slice. Doesn't
   depend on cutover.
3. **u8vo epic decomposition** — split into per-contract beads
   before any operator picks up. Designer slice (mine or any
   designer parallel-main).
4. **persona-introspect Package 1** — `primary-li7a`,
   `second-designer/144` is pickup-ready. Operator slice. Depends
   on Q3 (EffectEmitted) for the observable block.
5. **k2mh re-audit** — check current code against the stale
   audit before pickup. Designer slice.
6. **Pi/DeepSeek wrapper shape** — `designer/281` §4.4 awaits
   Q12 psyche pick.
7. **persona-listen design landing** — `second-designer/145`
   awaits Q14 11 psyche questions + Q15 model verification.
8. **sema-upgrade daemon promotion** — `primary-l3h5` follow-up
   to closed `primary-eanf` / `primary-g0u6` / `primary-1h0h`.
   Depends on Q5 + Q6 + Q9.
9. **Foundation hygiene pile pickup** — `primary-k3bu`, `primary-77hh`,
   `primary-u0lh`, `primary-uy7o`, `primary-dzrn`. Foundation
   cleanup gates downstream contract migrations.
10. **Bird→Zeus authority** — `cluster-operator/1` design is
    pickup-ready. Awaits Q19 scope decision.

## 9. References

**This session's intent records (spirit sema database):**
152 (Criome-stack vocabulary), 153 (Deploy→lojix), 154 (forge
boundary affirmed), 155 (pure-Rust trajectory), 156 (cluster-operator
specialty).

**Audit outputs (read by third-designer; not in workspace):**
`/tmp/audit-reports.md`, `/tmp/audit-beads.md`,
`/tmp/audit-components.md`.

**Net-new reports beyond /17's absorption** (handoff priority):
- `designer/281` (Pi headless research, today)
- `second-designer/140` (spirit triad parity check — EffectEmitted Q)
- `second-designer/143` (designer state digest)
- `second-designer/144` (persona-introspect refresh)
- `second-designer/145` (persona-listen recording system)
- `second-designer/146`/`/147`/`/149` (lane registry trio)
- `second-designer/148` (STT research)
- `second-designer/150` (agent identity)
- `second-operator/167`/`/168`/`/169` (engine backlog, mind/router, criome/lojix)
- `cluster-operator/1` (Bird→Zeus)
- `cluster-operator/3` (blocker audit + tools/orchestrate fix)
- `nota-designer/1`/`/2`/`/3` (bracket-string landed)
- `system-assistant/25` (signal-lojix migration)
- `system-assistant/28` (lojix vision gaps)
- `system-assistant/29` (lean horizon)
- `second-system-assistant/7` (persona-spirit prod deploy)

**Bead beads cited:** primary-x3ci, primary-chpq, primary-qk04,
primary-c620, primary-l3h5, primary-k2mh, primary-li7a,
primary-e1pm, primary-u8vo, primary-77hh, primary-k3bu,
primary-u0lh, primary-uy7o, primary-dzrn. All open. Closures
last 2 days: primary-ao1q (lane registry slice), primary-1h0h
(versioned daemon deployment), primary-g0u6 (sema-upgrade migration
CLI), primary-eanf (sema-upgrade prototype), primary-a4q0 (spirit
parity drift), primary-yrfr (signal-core public requests migration).

This report retires when the picking-up agent has triaged Q1–Q4
(the active blockers) and the next concrete operator slice is
underway.
