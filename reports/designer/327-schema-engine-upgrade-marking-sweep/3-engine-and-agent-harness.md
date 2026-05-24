*Kind: Triage · Topic: schema-engine-upgrade-marking-sweep slice C · Date: 2026-05-24*

# 327/3 · Slice C — engine + agent-harness + persona contracts

Subagent C's edits for §6.3 of the marking sweep frame. Four
component triads plus one agent-harness backend, eight repos.
Seven repos had a current `ARCHITECTURE.md` on disk; one
(`persona-pi`) had no documentation files at all. One repo
(`persona`) also had `INTENT.md`. All edits applied; all
commits landed cleanly via `jj describe`; no pushes.

## §1 · Edit summary table

| Repo | ARCH | INTENT | Triad slot | jj change | commit |
|---|---|---|---|---|---|
| `persona` | edited | edited | engine-management daemon (narrowed per /318 W4) | `twmpnyvl` | `833e2572` |
| `signal-persona` | edited | absent | persona wire contract (retired shim) | `rwwymmoy` | `b7cf89a9` |
| `signal-persona-origin` | edited | absent | persona origin vocabulary | `vloktuzy` | `a75bb4e0` |
| `upgrade` | edited | absent | upgrade triad daemon | `qllnxwvs` | `b1cd21ab` |
| `signal-upgrade` | edited | absent | upgrade ordinary contract | `nkuusrlv` | `854f3405` |
| `owner-signal-upgrade` | edited | absent | upgrade owner contract | `prwuqxrn` | `54033d07` |
| `sema-upgrade` | edited | absent | transitional library (retiring) | `oqolkkox` | `0c5fcdf3` |
| `persona-pi` | created | absent | agent-harness backend (Pi) | `oxkrplsx` | `015b347d` |

Seven repos got an ARCH edit (one of those plus an INTENT edit);
one (`persona-pi`) got a new ARCH file created from scratch.
**Edits: 7. Creations: 1. Blockers: 0.**

## §2 · Per-repo notes

### §2.1 · `persona` (engine-management daemon)

- File: `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md`
- Existing tail: `## See Also` section at line 1775 with three
  links (`active-repositories.md`, `persona-mind/ARCHITECTURE.md`,
  `signal-persona-mind/ARCHITECTURE.md`). Schema-engine upgrade
  section inserted **before** that See Also.
- Per-component concerns: explicitly called out the **narrowed
  role post-/318 Wave-4** (engine supervision + systemd unit-start;
  AttemptHandover + handover dispatch shed to the upgrade triad);
  named the manager state shape (engine catalog + lifecycle event
  log + snapshot projections + active-version reducer, per
  `persona/ARCHITECTURE.md:766-810`) as the storage shape the
  schema declares; flagged that the Design D `SCM_RIGHTS` public-
  socket handoff at §1.6.7 is descriptor-level routing and stays
  out of the schema cutover.
- INTENT.md edit: new `## Pending schema-engine upgrade` section
  inserted before the existing `## See also` section
  (`INTENT.md:226`). Restated narrowed-role framing for the
  intent reader: Persona's contract surface is now small post-/318
  because the upgrade-orchestration verbs moved to the upgrade
  triad; the schema cutover follows Spirit's pilot.
- jj: `twmpnyvl` / commit `833e2572` — `persona: mark pending
  schema-engine upgrade per /326-v13 + /324`.

### §2.2 · `signal-persona` (retired persona wire contract)

- File: `/git/github.com/LiGoldragon/signal-persona/ARCHITECTURE.md`
- Existing tail: `## Invariant` section at lines 17-21 declaring
  that this crate is a retired compatibility shim. No `## See
  also` section. Schema-engine upgrade section appended after the
  Invariant section.
- Per-component concerns: called out that **this crate is a
  retired compatibility shim** (per the §"Replacement Repositories"
  table at lines 6-12) and that the substantive Persona wire
  surface cutover lands in `owner-signal-persona` +
  `signal-engine-management`, not here. Noted that the retirement
  timeline may obsolete this crate before its own schema cutover,
  in which case the bead deletes the crate rather than rewrites
  it. Post-/318 the AttemptHandover verb is explicitly named as
  shed from this surface.
- INTENT.md: absent in this repo.
- jj: `rwwymmoy` / commit `b7cf89a9` — `signal-persona: mark
  pending schema-engine upgrade per /326-v13 + /324`.

### §2.3 · `signal-persona-origin` (persona origin vocabulary)

- File: `/git/github.com/LiGoldragon/signal-persona-origin/ARCHITECTURE.md`
- Existing tail: `## See also` section at line 200. Schema-engine
  upgrade section inserted **before** that See also.
- Pre-existing in-flight change handled cleanly: the working copy
  arrived with an undescribed change adding a `**Pending rename
  (per Spirit record 259)**` note inside `## 1 · Owned surface`
  (the `ComponentName` → `ComponentPrincipal` rename). To avoid
  bundling that unrelated change into my schema-engine commit, I
  temporarily reverted my schema-engine addition, committed the
  pre-existing rename note as its own revision (`zupzsoyt` /
  `9b994335` — `signal-persona-origin: note pending ComponentName
  to ComponentPrincipal rename per Spirit 259`), then re-applied
  the schema-engine section in a fresh working copy and committed
  it on top. The two commits are now distinct and described
  honestly.
- Per-component concerns: noted this crate is a **vocabulary-
  fragment crate, not a wire-channel crate** — no
  `signal_channel!` invocation here, so the schema is consumed via
  import and emits no dispatcher (per `signal-persona-origin/ARCHITECTURE.md:17-20`).
  Named the trust-gradient ARCH section that lands with the
  cutover (how `Caller` + `IngressContext` + `MessageOrigin` +
  `ConnectionClass` compose into the schema's authority surface,
  per /301 + primary-5k6n). Called out that the pending
  `ComponentName` → `ComponentPrincipal` rename (Spirit 259) +
  bundled `EngineIdentifier` / `RouteIdentifier` /
  `ChannelIdentifier` source-level rename (Spirit 277, 278)
  should ideally land before the schema cutover so the macro
  pipeline sees the final names.
- INTENT.md: absent in this repo.
- jj: `vloktuzy` / commit `a75bb4e0` — `signal-persona-origin:
  mark pending schema-engine upgrade per /326-v13 + /324`.

### §2.4 · `upgrade` (upgrade triad daemon)

- File: `/git/github.com/LiGoldragon/upgrade/ARCHITECTURE.md`
- Existing tail: `## Status` section at lines 51-53 noting U1
  scaffold-only state. No `## See also` section exists in this
  file. Schema-engine upgrade section appended after the Status
  section.
- Per-component concerns: this is the **load-bearing entry** in
  Slice C. Called out that **the upgrade triad orchestrates its
  own schema cutover as part of the brilliant macro library
  landing** — schema-daemon's persistent registry (per /326-v13
  §4) is the upgrade triad's natural home; the schema-engine
  pipeline produces schema fingerprints / migration paths /
  VersionProjection, and the upgrade daemon is exactly the
  runtime that registers them, gates handovers on them, and
  quarantines on failure. Noted that U2/U3/U4 work and the
  schema cutover may **interleave** rather than sequence
  strictly — the macro library could be the substrate U4 is
  built against from the start, rather than U4 landing hand-
  written first and converting later. Made the self-reference
  explicit: this component's schema describes what migrations
  look like and how the runtime executes them, so the brilliant
  macro library landing should land both together.
- INTENT.md: absent in this repo.
- jj: `qllnxwvs` / commit `b1cd21ab` — `upgrade: mark pending
  schema-engine upgrade per /326-v13 + /324`.

### §2.5 · `signal-upgrade` (upgrade ordinary contract)

- File: `/git/github.com/LiGoldragon/signal-upgrade/ARCHITECTURE.md`
- Existing tail: `## Invariants` section at lines 42-48. No `##
  See also` section exists in this file. Schema-engine upgrade
  section appended after the Invariants section.
- Per-component concerns: called out the **merge** per /318
  (from `signal-version-handover` + `signal-sema-upgrade`) and
  that the schema cutover absorbs `AttemptUpgrade` + the
  handover-protocol verbs (`AskHandoverMarker`,
  `ReadyToHandover`, `HandoverCompleted`, `Mirror`, `Divergence`,
  `RecoverFromFailure`) into one schema file. Noted that
  `Mirror` and `Divergence` payloads carry raw bytes in typed
  containers — the schema declares the byte-carrying record
  shapes, but projection policy stays in `version-projection`
  and execution policy stays in the `upgrade` runtime. Called
  out the `version-projection` dependency for `ComponentName` /
  `ContractVersion` / `RecordKind`; the schema imports that
  vocabulary from `version-projection`'s own macro-pattern
  integration (named here as a hand-off to Slice D's substrate-
  library marking).
- INTENT.md: absent in this repo.
- jj: `nkuusrlv` / commit `854f3405` — `signal-upgrade: mark
  pending schema-engine upgrade per /326-v13 + /324`.

### §2.6 · `owner-signal-upgrade` (upgrade owner contract)

- File: `/git/github.com/LiGoldragon/owner-signal-upgrade/ARCHITECTURE.md`
- Existing tail: `## Invariants` section at lines 36-44. No `##
  See also` section exists. Schema-engine upgrade section
  appended after the Invariants.
- Per-component concerns: enumerated the seven owner verbs the
  schema covers (`Register`, `Allow`, `Block`, `Query`,
  `ForceFlip`, `Rollback`, `Quarantine`). Called out the
  deliberate **AttemptHandover absence** per /318 design — peers
  call `AttemptUpgrade` on the ordinary `signal-upgrade` contract;
  owner authority configures the gating policy. The schema
  cutover preserves this owner/ordinary split: the macro emits
  two dispatchers, not one merged surface. Called out the
  `signal-upgrade` dependency for `ComponentName` /
  `MigrationIdentifier` / migration `Version` — the schema
  imports that vocabulary from `signal-upgrade`'s schema.
- INTENT.md: absent in this repo.
- jj: `prwuqxrn` / commit `54033d07` — `owner-signal-upgrade:
  mark pending schema-engine upgrade per /326-v13 + /324`.

### §2.7 · `sema-upgrade` (transitional / retiring)

- File: `/git/github.com/LiGoldragon/sema-upgrade/ARCHITECTURE.md`
- Existing tail: `## Nix Surface` section at lines 20-24 noting
  the crate is buildable-only as a compatibility breadcrumb. No
  `## See also` section. Schema-engine upgrade section appended
  after the Nix Surface section.
- Per-component concerns: called out that the **substantive
  migration surface has already moved** to the `upgrade` triad
  (per /318 retirement; `PrototypeHandover` retired per /317-1);
  there is no separate `sema-upgrade/sema-upgrade.schema` target
  on the roadmap. The **preferred outcome** is deletion of this
  repo when the last old pin is gone, not a separate schema
  cutover. Made the **negative invariant** explicit: if a
  schema-cutover bead were ever opened for `sema-upgrade`, treat
  it as a sign that work landed in the wrong place — redirect to
  `upgrade` / `signal-upgrade`. Noted the likely outcome that
  this section becomes moot when the crate is deleted.
- INTENT.md: absent in this repo.
- jj: `oqolkkox` / commit `0c5fcdf3` — `sema-upgrade: mark
  pending schema-engine upgrade per /326-v13 + /324`.

### §2.8 · `persona-pi` (agent-harness backend)

- File: `/git/github.com/LiGoldragon/persona-pi/ARCHITECTURE.md`
  (**created**; did not exist before this sweep).
- Repo arrived in a half-initialised state: no `ARCHITECTURE.md`,
  no `AGENTS.md`, no `README.md`, no `INTENT.md`. Working copy
  carried four uncommitted-but-undescribed files (`flake.nix`,
  `nix/pi-subagents.nix`, `nix/pi-linkup.nix`,
  `nix/persona-pi-criomos.nix`) parented to `zzzzzzzz` (root).
  These files are pre-existing scaffolding from when the repo
  was checked out (1 day ago per `jj op log`); they are not my
  authorship.
- Sequencing decision: to avoid bundling those undescribed pre-
  existing files into my schema-engine commit, I used `jj split`
  to commit them as their own honestly-described revision
  (`tkuprztr` / `98f908a2` — `persona-pi: initial flake + nix
  package wiring`), then committed my new `ARCHITECTURE.md` as a
  separate revision on top. This created the repo's first `main`
  bookmark (none existed before; the repo had no described
  commits at all).
- Created ARCH content: a full minimal architecture file
  covering role (Nix-packaged Pi harness for Persona's agent-
  harness slot), boundaries (this repo owns the Nix package; it
  does NOT own Pi source or harness contracts), Pi-side wiring
  (per-engine `PI_CODING_AGENT_DIR` / `PI_CODING_AGENT_SESSION_DIR`
  isolation; auth-bootstrap-inside-sandbox; local Prometheus-
  backed model path), Code Map, and the Pending schema-engine
  upgrade section.
- Per-component concerns: named the **Spirit record 371 agent-
  harness exception** that lets this crate retain its `persona-`
  prefix (other components shed it; agent-harness backends keep
  it because they bind to Persona's harness lifecycle and inherit
  Persona's authority surface). First repo to land that
  retention-discipline. Schema cutover lands **after the agent
  triad** lands its schema substrate (per Slice B's `signal-
  agent` work); most likely this crate stays Nix-package-only
  and gains no schema file of its own, because the agent triad
  covers harness-spawn lifecycle / identity / control verbs. Pi
  auth bootstrap + per-engine sandbox isolation are package-
  shape state, not contract-shape state.
- INTENT.md: not created. The frame allows minimal ARCH creation
  but does not require INTENT creation, and the upstream psyche
  surface for persona-pi already lives in `persona`'s INTENT.md
  (Pi as preferred first harness for the sandbox witness).
- jj: `oxkrplsx` / commit `015b347d` — `persona-pi: create
  ARCHITECTURE and mark pending schema-engine upgrade per
  /326-v13 + /324`.

## §3 · Cross-cutting observations

### §3.1 · Upgrade triad as schema-host (load-bearing)

The most consequential observation in Slice C is that the
**upgrade triad is the natural runtime home for schema-daemon's
persistent registry** (per /326-v13 §4). The upgrade triad's
schema cutover should not be sequenced like an ordinary
component cutover (Spirit pilots, then per-component cutovers
in some order). Instead, the brilliant macro library landing
**should land the upgrade triad and the macro substrate
together** because the macro pipeline produces exactly what the
upgrade daemon registers/gates-on/quarantines (fingerprints,
migration paths, VersionProjection), and the upgrade daemon's
catalogue + event log + quarantine list ARE the storage shape
the schema-language MVP exists to express.

Operator's `primary-ezqx.1` work should consider folding U4
runtime work and macro-library-substrate work into one landing
rather than two sequential ones. The marking in
`upgrade/ARCHITECTURE.md` makes this explicit; restated here so
the overview (file 5) can carry it forward.

### §3.2 · `signal-persona` retirement may obsolete its own cutover

`signal-persona` is a retired compatibility shim. The
substantive Persona wire surface cutover lands in
`owner-signal-persona` + `signal-engine-management` (both
covered by Slice B). The marking on this crate is honest about
the likely retirement outcome: the schema cutover bead may
delete the crate rather than rewrite it. Overview (file 5)
should note this as one of the **non-cutover targets** — repos
marked but where the actual cutover may simply be deletion.
`sema-upgrade` is in the same category for the same reason
(transitional / retiring).

### §3.3 · `signal-persona-origin` is import-only

`signal-persona-origin` has no `signal_channel!` invocation —
it is a vocabulary-fragment crate that other Persona contracts
import. The macro pipeline emits no dispatcher for it; the
schema is import-only. This is a useful **test case** for the
macro library's cross-schema import mechanism: the cutover
exercises that mechanism without committing to dispatcher
emission. The marking explicitly recommends landing this
cutover alongside (or just before) the first downstream Persona
contract that imports it through the schema pipeline.

### §3.4 · `persona-pi` is the first agent-harness-prefix marker

`persona-pi` is the first repo in the workspace to formally
carry **Spirit record 371's agent-harness exception** to the
prefix-shedding pattern in its ARCH. The newly-created
`persona-pi/ARCHITECTURE.md` documents the exception
explicitly:

> The package keeps the `persona-` prefix per Spirit record
> 371's **agent-harness exception** to the prefix-shedding
> pattern: agent-harness backends remain inside the Persona
> namespace because they bind to Persona's harness lifecycle
> and inherit Persona's authority surface.

Future agent-harness packages (`persona-claude`,
`persona-codex`, etc., if/when they exist) should follow this
template.

### §3.5 · Pre-existing in-flight state on two repos

Two of the eight repos arrived with non-empty working copies
that needed careful handling:

- **`signal-persona-origin`**: undescribed change adding the
  `ComponentName` → `ComponentPrincipal` rename note. Handled
  by splitting into two described commits: first the rename
  note (described honestly), then the schema-engine section.
- **`persona-pi`**: four undescribed flake/nix files in the
  working copy parented to root. Handled by splitting them
  into a "persona-pi: initial flake + nix package wiring"
  commit, then committing the new ARCHITECTURE.md on top.
  This created the repo's first `main` bookmark.

Both cases follow `skills/jj.md` §"Before you commit — the
working-copy check": don't bundle other work into your commit.

### §3.6 · Common gap: no `## See also` in upgrade-triad ARCHs

The upgrade triad's four ARCHs (`upgrade`, `signal-upgrade`,
`owner-signal-upgrade`, `sema-upgrade`) are all short (24-53
lines) and **none** have a `## See also` section. The schema-
engine section was appended as the new final section in each.
This is not a problem for the sweep but is a cross-reference
opportunity the operator's next pass on these ARCHs could fill:
each could link the others, `version-projection`, and the
designer reports.

## §4 · What carries forward

For operator's lane (per the frame's §7 overview-integration
list):

1. **Upgrade triad ↔ brilliant macro library landing co-design.**
   Operator should not treat `primary-ezqx.1` (Spirit pilot) and
   the upgrade triad's schema cutover as fully sequential. The
   upgrade triad is the natural home for the schema-daemon
   registry; landing the macro library against the upgrade
   triad's U4 runtime work simultaneously avoids a second
   "convert U4 from hand-written to macro-emitted" pass later.

2. **Non-cutover repos.** `signal-persona` and `sema-upgrade` are
   marked but their schema cutover may simply be deletion. The
   overview should track these as a distinct category from
   "components awaiting cutover".

3. **Naming renames before schema cutover.** `signal-persona-
   origin`'s `ComponentName` → `ComponentPrincipal` rename
   (Spirit 259) plus the `Identifier` source-level renames
   (Spirit 277, 278) should ideally land before the schema
   cutover so the macro pipeline sees the final names. Otherwise
   the schema carries the legacy names and a follow-up macro-
   rename bead is needed.

4. **`persona-pi` flake commit.** I authored a description for
   the pre-existing flake/nix files (`persona-pi: initial flake +
   nix package wiring`) so they would not bundle into my
   ARCHITECTURE.md commit. If the original psyche/operator
   intent for those files was different, the description can be
   amended via `jj describe <rev> -m '<msg>'`. The substance is
   intact; only the description framing is mine.

## §5 · Cross-references to upstream design reports

No edits required to upstream design reports. The marking sweep
is downstream of `/324` and `/326-v13`; both are sufficiently
specified for this marking pass. The two observations worth
folding back upstream are:

- **`/326-v13` §4 (schema-daemon registry) ↔ upgrade triad as
  natural home** — could be made explicit in /326-v13 if a
  revision lands, or carried in the overview (file 5) as the
  sweep's cross-cutting finding.
- **Spirit record 371's agent-harness exception** is now
  exercised by `persona-pi/ARCHITECTURE.md`; if /318 or a
  successor designer report enumerates the agent-harness
  triads, it can cite this marking as the first concrete
  application of the exception.

## §6 · Slice C summary

**Slice C summary: 7 edits + 1 creation + 0 blockers.**

## See also

- `0-frame-and-method.md` — the orchestrator frame for this
  sweep, including the marking format template (§3.1) and the
  hard constraints (§4) every slice followed.
- `1-core-persona-triads.md` — Slice A's edits across the five
  core persona triads (spirit, mind, router, message, orchestrate).
- `2-adjacent-persona-triads.md` — Slice B's edits across the
  adjacent persona triads (terminal, harness, introspect, system,
  engine-management, agent).
