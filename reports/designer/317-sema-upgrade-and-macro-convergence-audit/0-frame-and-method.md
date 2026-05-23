*Kind: Frame · Topic: sema-upgrade-and-macro-convergence-audit · Date: 2026-05-24*

# 317 · Frame — sema-upgrade path audit + macro convergence + next-as-dependency

## §1 Psyche ask

> research and audit the sema-upgrade path in signal, and the rework
> we want to do in signal/sema macros — to be bundled with a macro
> review which incorporates documentation, small-header (64 bit of
> enums) generation and encoding/decoding capability in nota, as
> well as the upgrade path through the 'next' being a dependency of
> the current signal/sema schema

Two intent records captured before this dispatch:

- **Spirit 366** (Decision · signal-version-migration · Maximum) —
  the upgrade path is encoded as the next-version crate being a
  Cargo dependency of the current schema crate; macro has
  compile-time visibility into both schemas and emits the
  `VersionProjection` at the current version's compile time.
- **Spirit 367** (Decision · signal-macro · Maximum) — the
  macro convergence bundles four concerns (Help docs, 64-bit Tier 1
  header, NOTA codec, next-as-dep upgrade path) into one epic; they
  are not separable because they converge on the
  `signal-frame-macros` extension surface.

## §2 Why a meta-report directory

Three large slices, each with its own current-state-read load, and
the slices interlock. A flat report would either (a) elide the audit
details to fit synthesis prose, or (b) explode past readability. The
meta-report directory keeps each slice's substance addressable while
the overview (file 4) tells the integrated story.

Per spirit record 231 sub-agent dispatch shape:

- `0-frame-and-method.md` (this file) — orchestrator frame.
- `1-sema-upgrade-path-audit.md` — Subagent A · audit of the
  deployed upgrade path (version-projection, signal-version-handover,
  sema-engine.CommitSequence, sema-upgrade daemon, persona-spirit
  private socket, persona-as-orchestrator). Gap analysis: what's
  shipped vs what's designed.
- `2-macro-current-state-audit.md` — Subagent B · audit of the
  current macro surface (signal-frame-macros, nota-derive,
  signal-derive). What does `signal_channel!` emit today; what's
  outstanding from the 8 macro beads
  (l02o/8r1j/915w/3cl1/v5n2/avog/li0p/2cjv); concrete diff to
  reach the convergence epic.
- `3-next-as-dependency-design.md` — Subagent C · fresh design
  for the next-as-dep upgrade path. Cargo mechanics, macro
  consumption of next-schema, cycle-avoidance, bootstrap (no next
  exists at v0.1.0 land time), interaction with the existing
  `VersionProjection` trait, interaction with the macro convergence.
- `4-overview.md` — orchestrator synthesis: the integrated picture,
  one consolidated bead epic that subsumes the 8 macro beads + the
  sema-upgrade absorption, recommended landing order, open psyche
  questions.

## §3 Slice contracts — what each subagent must answer

### §3.1 Subagent A — sema-upgrade path audit

Must produce a structured report covering:

- **Per-crate current state.** For each of `version-projection`,
  `signal-version-handover`, `owner-signal-version-handover` (may
  not exist yet), `sema-engine` (CommitSequence), `sema-upgrade`,
  `persona-spirit` (private upgrade socket), `persona` (upgrade
  orchestrator role): read the deployed `src/`, list (a) what's
  landed and ratified, (b) what's stubbed but unfinished, (c) what's
  in ARCH but not in code.
- **End-to-end live path.** Trace one Spirit v0.1.0 → v0.1.1
  handover step (the proven sandbox migration) through the deployed
  code paths. Name the actual file:line for each step.
- **Gap matrix.** Table of (designed-in /285/287/315 vs in-code) per
  concern: VersionProjection impl, AskHandoverMarker exchange,
  ReadyToHandover exchange, HandoverCompleted exchange, Mirror
  payload (per spirit 274 settled as raw bytes), Divergence,
  RecoverFromFailure, ForceFlip/Rollback/Quarantine
  (owner-signal-version-handover), Persona-as-orchestrator.
- **Spirit pilot first-live-test focus.** Make explicit which gaps
  are on the Spirit pilot's critical path (`primary-x3ci` Spirit
  cutover) and which are deferred to the second component cutover.
- **Surface the Mirror-payload retirement (per /314 §7).** The
  Possible-features entries in 3 ARCH files can collapse to one
  sentence; flag whether the slice is a P3 cleanup or already part
  of the main convergence.

Hard constraints for the subagent:
- **Read, don't write code.** Audit only. Reports + Read tools only.
- **No `/nix/store` filesystem search.** Use `nix eval` / `nix
  flake show` / `nix path-info` if needed.
- **Write to `reports/designer/317-.../1-sema-upgrade-path-audit.md`.**
- **No horizontal-rule lines (`---`) in the report.**
- **No emojis.**
- **Cite each claim with file:line.**

### §3.2 Subagent B — macro current state audit

Must produce a structured report covering:

- **Per-crate current macro emission.** Read `signal-frame-macros`,
  `signal-derive`, `nota-derive`, `nota-codec`. For each: what
  proc-macros / derives exist, what they emit today.
- **Per-bead status.** For each of `primary-l02o`, `primary-8r1j`,
  `primary-915w`, `primary-3cl1`, `primary-v5n2`, `primary-avog`,
  `primary-li0p`, `primary-2cjv`: (a) the design report (one of
  /307, /308, /312), (b) the bead description, (c) whether any code
  has been started, (d) the diff to land it.
- **Convergence map.** Show on one mermaid diagram how the 8 beads
  collapse onto one `signal_channel!` extension surface emitting:
  (i) the per-enum Help variant + HelpReply auto-derive, (ii) the
  Tier 1 `frame_micro` u64 projection, (iii) the
  golden-ratio-allocated discriminator range, (iv) the cross-triad
  `assert_triad_sections!` check, (v) the per-channel NOTA
  encode/decode (already done by nota-derive — confirm gap).
- **What's missing for next-as-dep.** Surface what the macro
  doesn't have today that the next-as-dep design will need (read
  Subagent C's report once written if cross-reference helpful).
- **Concrete diff sketch.** For each missing emission, ~10-line
  sketch of what the macro should generate. Not implementation —
  enough that an operator picking this up sees the target.

Hard constraints (same as Subagent A): read-only, NOTA single-arg
discipline, no horizontal rules, no emojis, file:line citations,
write to `2-macro-current-state-audit.md`.

### §3.3 Subagent C — next-as-dependency design

Must produce a fresh design (not just audit). Covers:

- **The Cargo mechanic.** How does `signal-persona-spirit` v0.1.0
  declare `signal-persona-spirit` v0.1.1 as a dependency without
  name collision? Three candidates to evaluate:
  1. Cargo rename (`signal-persona-spirit-next =
     { version = "0.1.1", package = "signal-persona-spirit" }`).
  2. Separate crate-per-version naming
     (`signal-persona-spirit-v0_1_0`, `-v0_1_1` each in their own
     crate; the current pattern then becomes "current is v0_1_0
     aliased to plain `signal-persona-spirit`").
  3. Path-only or git-pinned alias inside the workspace.
- **The macro consumption.** How does `signal_channel!` see the
  next-version's types? Two candidates:
  1. The macro reads a `next_schema:` attribute pointing at the
     next-crate's `Operation`/`Reply`/etc enums and emits the
     `VersionProjection` impl from the current-crate's types to the
     next-crate's types.
  2. Side macro `version_projection!` invoked in the current crate
     that takes both schemas and emits the projection — keeping
     `signal_channel!` itself unchanged.
- **Cycle-avoidance proof.** Argue why current→next dependency
  direction is cycle-free, including the boundary case where v0.1.1
  is being prototyped: does `signal_channel!` in v0.1.0 require
  v0.1.1 to compile? (Probably yes — so the bootstrap is a
  conditional emission.)
- **Bootstrap — first version, no next yet.** At v0.1.0 land time,
  there is no v0.1.1 to depend on. How does the macro handle this?
  Candidates: omit projection emission, generate a placeholder
  `NoNextVersion` projection, require explicit opt-in via
  `next_schema:` attribute.
- **Interaction with the existing `VersionProjection` trait** (per
  /285/287). The trait is `VersionProjection<Source, Target>` with
  a `project()` method. Confirm whether the macro emits an `impl
  VersionProjection<v0_1_0::Foo> for v0_1_1::Foo` or vice versa —
  this matches whose code owns the migration logic.
- **The N+2 case.** If v0.1.1 lands, then v0.1.2, how does v0.1.0
  migrate to v0.1.2? Two-hop projection (v0.1.0 → v0.1.1 → v0.1.2)
  composed at runtime, or every version pair gets its own direct
  projection? Recommend the two-hop chain (simpler) unless field
  loss makes it lossy.
- **Mirror payload coupling.** Per /315 §2.3 and spirit 274, Mirror
  payload is raw bytes in its own container. Does next-as-dep
  change this — i.e. could the macro emit typed Mirror payload now
  that it has visibility into both schemas? Recommend keeping
  current decision (typed enum import cost still high) but record
  whether the typed alternative is now more attractive than before.
- **Concrete worked example.** Walk through Spirit v0.1.0 → v0.1.1
  (the Magnitude widening: 3-variant Certainty → 7-variant
  Magnitude) under the next-as-dep design. How does the macro emit
  the projection? Where does the Certainty→Magnitude mapping live?
  (Probably in a `From<historical::Certainty> for Magnitude` impl
  declared in v0.1.0's macro invocation as part of the projection.)
- **Operator-bead decomposition.** Sized for parallel pickup.

Hard constraints: same as A/B. Write to
`3-next-as-dependency-design.md`. This subagent has more design
latitude than A/B; A/B are audits, C is a design.

## §4 What the overview (file 4) will do

After A/B/C return:

1. **Integrated picture.** One mermaid showing macro convergence +
   sema-upgrade absorption + next-as-dep as one operator landing.
2. **One consolidated epic.** Subsume the 8 macro beads + relevant
   sema-upgrade beads into one tracked epic (likely re-using
   `primary-ezqx` per /313's macro convergence framing).
3. **Spirit pilot tie-back.** Name explicitly which work blocks
   `primary-x3ci` (Spirit cutover) and which is parallel.
4. **Landing order.** Concrete sequence: what lands first to unblock
   what.
5. **Open psyche questions.** Distilled from A/B/C's questions; ≤8.

## §5 Constraints to keep in mind across the slice

- **Persona absorbs orchestration** (spirit 208-210); no
  `sema-upgrade-daemon` triad on disk.
- **Mirror payload is raw bytes in a separate container** (spirit
  274 Maximum); typed-enum alternative rejected.
- **Per-component byte-0 namespace, golden-ratio split**
  (spirit 326-327, reports /305-v2 + /307).
- **`Frame { micro: u64, body }` pre-typed envelope** (spirit 328,
  report /308).
- **Help-on-every-enum, Help is a noun at end of path** (spirit
  359/363/364, report /312).
- **CLI single-NOTA-argument rule** (spirit 365); examples in any
  report must use `spirit '(Help)'`-shape, never shell-multi-arg.
- **PascalCase identifiers spelled in full** (`Identifier` not
  `Id`; `Entry` not `IntentEntry`).
- **`jj` headless only** when committing — `-m '<msg>'` or
  `--use-destination-message`.
