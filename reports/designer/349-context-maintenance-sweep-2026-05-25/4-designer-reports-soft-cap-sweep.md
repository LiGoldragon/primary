*Kind: Synthesis · Topic: designer-reports-soft-cap-sweep · Date: 2026-05-25 · Lane: designer (Subagent D)*

# 4 · Designer reports soft-cap sweep

## §1 Frame

This subagent's remit: triage every report in `reports/designer/` against
the 12-report soft cap (per `skills/reporting.md` §"Soft cap"); apply
the drop/forward/migrate/keep decision per `skills/context-maintenance.md`
§2; retire what's done; leave only what's load-bearing.

**Scope boundary.** Subagents A/B/C of this same /349 session own
specific recent reports: A owns the schema-driven full-stack POC stack
(`/341, /343, /345, /346`); B owns `/348` (NOTA string discipline); C
owns `/347` (Spirit v0.2.0 integration). Subagent D owns every OTHER
designer report — the older surface that accumulated through the
MVP-pivot, MVP-build, and schema-engine-vision arcs.

**Aggressiveness target.** Per the orchestrator frame: *"if you find
yourself keeping >5 from the older set, you're being too lenient."*
This sweep retires the whole older set; 0 KEEPs in the D-scope. The
schema-driven full-stack POC has crystallized and is now landing in
code (per /341 + Subagent A's work); the path-to-here reports are
journey docs that the commit tree preserves.

## §2 Pre-sweep inventory (D's scope)

Pre-sweep designer/ count: 50 entries (47 markdown + 3 meta-directories).
D's scope was every entry except `/341, /343, /345, /346, /347, /348` —
36 entries.

| Path | Topic (one-line) | Decision |
|---|---|---|
| `/249-component-intent-gap-analysis.md` | Pre-schema persona-component intent-gap audit | DROP |
| `/257-signal-contracts-names-and-shape-audit.md` | Pre-schema signal-contracts name/shape audit | DROP |
| `/263-schema-specification-language-design.md` | Original schema-language design sketch | DROP |
| `/266-persona-pi-triad-design.md` | Persona-pi triad sketch (status-bannered) | DROP |
| `/279-nota-schema-language-and-version-hash.md` | NOTA schema grammar + content-address hash | DROP |
| `/281-headless-pi-research.md` | Pi headless modes research (status-bannered) | DROP |
| `/285-versionprojection-trait-and-handover-protocol-specification.md` | VersionProjection trait spec (status-bannered, landed) | DROP |
| `/287-version-handover-component-explained.md` | Version-handover visual reference (landed in upgrade triad) | DROP |
| `/293-designer-and-research-batch-2026-05-23/` (5 files) | Vocabulary sweep + 3 research probes + gap closure | DROP (entire meta-dir) |
| `/299-design-origin-process-and-agent-identity.md` | signal-persona-origin design (landed) | DROP |
| `/301-design-elegant-cli-macro-with-caller-injection.md` | signal_cli! macro design (landed in signal-frame) | DROP |
| `/305-v2-design-64bit-signal-per-component-namespacing.md` | Per-component 64-bit namespacing (status-bannered, in ARCH) | DROP |
| `/307-design-golden-ratio-namespace-split.md` | Golden-ratio split design (substance in signal-frame ARCH) | DROP |
| `/308-design-pretyped-envelope-and-tap-anywhere.md` | Pre-typed envelope design (substance landed in ShortHeader) | DROP |
| `/309-design-agent-component-abstraction.md` | persona-agent triad design (status-bannered) | DROP |
| `/312-design-recursive-help-on-every-enum.md` | Recursive Help-on-every-enum design | DROP |
| `/315-design-sema-upgrade-and-handover-current-state.md` | Sema-upgrade current state consolidation | DROP |
| `/316-design-forge-family-current-direction.md` | Forge family direction consolidation | DROP |
| `/317-sema-upgrade-and-macro-convergence-audit/` (4 files) | Macro convergence + sema-upgrade audit meta-dir | DROP (entire meta-dir) |
| `/318-upgrade-merger-and-persona-prefix-rename/` (4 files) | Upgrade triad merger + persona-prefix rename meta-dir | DROP (entire meta-dir) |
| `/319-schema-stack-context-maintenance-sweep/` (4 files) | Prior context-maintenance sweep meta-dir | DROP (entire meta-dir) |
| `/320-mvp-schema-language-pilot-unblock.md` | MVP design closing 13 holes (status-bannered) | DROP |
| `/321-mvp-visual-state-of-play.md` | MVP visual state of play (status-bannered) | DROP |
| `/322-spirit-mvp-positional-schema-worked-example.md` | Spirit MVP worked example | DROP |
| `/323-mvp-scope-expansion-per-operator-directive.md` | MVP scope expansion + cutover discipline | DROP |
| `/324-migration-mvp-spirit-handover-re-specification.md` | MVP+handover re-specification (canonical at the time) | DROP |
| `/325-nota-box-library-design-and-implementation.md` | nota-box library design (operator-ready, landed) | DROP |
| `/326-v13-spirit-complete-schema-vision.md` | v13 uniform schema vision (superseded by /341+/345) | DROP |
| `/327-schema-engine-upgrade-marking-sweep/` (7 files) | Workspace ARCH "pending upgrade" markings meta-dir | DROP (entire meta-dir) |
| `/329-schema-macro-component-extensibility.md` | InputStruct-per-variant pattern | DROP |
| `/330-parallel-implementation-pivot-and-spirit-nspawn-plan.md` | Parallel-impl pivot + nspawn plan | DROP |
| `/332-schema-macro-coverage-audit.md` | Schema-macro coverage audit (point-in-time) | DROP |
| `/333-upgrade-mechanism-full-design-explained.md` | Upgrade mechanism narrative | DROP |
| `/333-v2-upgrade-mechanism-corrections-from-real-world-test.md` | /333 errata from real-world test | DROP |
| `/334-multi-pass-nota-first-schema-reader.md` | Multi-pass NOTA-first reader concept | DROP |
| `/334-v2-multi-pass-nota-first-schema-reader.md` | Multi-pass corrections from subagent witness | DROP |
| `/335-state-audit-and-test-verification/` (5 files) | Test-claims + impl-state + problems meta-dir | DROP (entire meta-dir) |
| `/336-designer-leans-on-27-psyche-questions-and-mvp-plan.md` | Designer leans on /335's 27 questions | DROP |
| `/337-current-state-research-for-real-mvp-pass.md` | Pre-real-MVP state research | DROP |
| `/337-real-pipeline-mvp/` (1 file: last-run nota) | Real-pipeline MVP last-run witness | DROP (meta-dir) |
| `/338-schema-engine-refreshed-vision-2026-05-25.md` | Schema-engine refreshed vision (superseded by /341+/345) | DROP |
| `/339-worktree-archive-and-system-overview.md` | Worktree archive + system overview | DROP |
| `/340-schema-emission-no-legacy-signal-channel-2026-05-25.md` | schema-rust composer (no legacy signal_channel!) | DROP |
| `/342-interact-trait-code-walkthrough-2026-05-25.md` | Interact-trait walkthrough (RETRACTED by record 666) | DROP |
| `/344-schema-architecture-presentation-2026-05-25.md` | Schema architecture as slides | DROP |

**Total decisions in D's scope**: 36 entries → **36 DROP, 0 KEEP**.

The schema-driven crystallization (`/341`) + the channel-contract refresh
(`/345`) + the actor-schemas reification (`/346`) supersede every prior
design pass on the schema substrate. The MVP test ran successfully on
Prometheus (per the retired `/337-real-pipeline-mvp/last-run` witness);
the schema engine landed on main in operator/181+/182; persona-spirit
v0.2.0 is live side-by-side per operator/187. Everything in the older
set is journey-documentation — preserved in the commit tree, removed
from the working surface.

## §3 Rationale per cluster

### §3.1 Pre-MVP gap audits (`/249, /257`)

`/249` (component intent gap analysis, 60KB) and `/257` (signal contracts
name/shape audit, 37KB) catalog gaps in the persona-component substrate
that pre-dated the schema-driven pivot. Per /319 §3.3 these were IN-FLIGHT
driving `primary-c2da` and `primary-u8vo`. The schema-driven crystallization
(/341) makes the gap framing obsolete: every contract is now a
`.schema` file, every gap is a missing or incomplete schema declaration.
The previous-shape gaps either landed (Tap/Untap mandate, Persona triad
confirmation, owner-graph apex disambiguation) or dissolved under the
new shape. Substance retires.

### §3.2 Schema-language and version-hash precursors (`/263, /279`)

`/263` and `/279` design the original NOTA-based schema language and
content-addressable version hash. Per /319 §3.1 these were "KEEP with
design-rationale guard." Now: the schema engine is live in production
(`schema` crate at `5efdf424` per /338); the v13 grammar (`/326`) is
itself superseded by /341+/345's channel-contract framing; the
content-addressable identity has yielded to per-version `(Upgrade ...)`
schema declarations. Both precursors retire — substance lives in the
schema crate's source and in /341's seven-principles synthesis.

### §3.3 Persona-pi + headless-Pi (`/266, /281, /309`)

`/266` (persona-pi triad), `/281` (headless-Pi research), `/309` (agent
component abstraction). All three carry STATUS-BANNERs naming
supersession in /309 §7 + /318 rename direction. With the persona-prefix
rename direction settled (per /318 + spirit 371) and the schema-driven
substrate now dictating that every component is its own schema, the
specific persona-pi/persona-agent design framing is historical. Substance
absorbed into operator's persona-agent landings + the schema substrate.

### §3.4 Upgrade triad + version-handover (`/285, /287, /315`)

`/285` (VersionProjection trait spec), `/287` (visual reference), `/315`
(current-state consolidation). All three landed in the `upgrade` triad
per /318 Wave-4; ARCH files in `version-projection`, `signal-upgrade`,
`owner-signal-upgrade`, `sema-engine` carry the substance. Subagent A's
work on `/346` (actor schemas + upgrade mechanism) now carries the
upgrade-mechanism explanation forward. Predecessors retire.

### §3.5 64-bit signal + envelope work (`/305-v2, /307, /308, /312`)

All four landed in `signal-frame/ARCHITECTURE.md` (per-component
namespacing §5.2; golden-ratio split; pre-typed envelope; recursive
Help discipline). `ShortHeader(u64)` is in production at
`signal-frame/src/frame.rs:110`. The design-rationale guard that /319
applied to /305-v2, /307, /308, /312 was load-bearing while the schema
substrate was still settling; with /341 + /345 + /346 + the live POC,
the rationale is now in the canonical schema vision, not in the
component-by-component design history.

### §3.6 signal-persona-origin + CLI macro (`/299, /301`)

`/299` (origin-process identity design) and `/301` (signal_cli! macro
with caller injection). Both landed: `signal-persona-origin` repo
exists; `signal-frame::signal_cli!` is in use across the workspace.
Substance migrated to per-repo ARCH + the live macro.

### §3.7 MVP-build path (`/320-/326`)

The MVP-build arc — design `/320` (closed decisions), visual `/321`,
worked example `/322`, scope expansion `/323`, re-specification `/324`,
nota-box library `/325`, v13 schema vision `/326` — drove the path to
the schema engine. The MVP ran successfully on Prometheus (per
`/337-real-pipeline-mvp/last-run` witness, now retired); operator's
181/182 landings collapsed the schema engine onto canonical NOTA;
persona-spirit `signal_channel!([schema])` is in production. The
journey reports retire; the destination is the live `schema` crate +
the live `signal-persona-spirit` invocation.

### §3.8 Forge (`/316`)

Forge family direction consolidation. Substance: `signal-forge`
skeleton at `87882b6`; `forge` daemon at `8c1ef63`. The build-system
component family is on a longer arc not directly coupled to the
schema-substrate crystallization. The /316 substance migrates to
`forge/ARCHITECTURE.md` (already partially there per /316 §1
references). Settled directions live in code + ARCH.

### §3.9 Meta-directories (`/293, /317, /318, /319, /327, /335, /337-real-pipeline-mvp`)

Seven meta-report directories from prior sub-agent sessions. Per intent
record 231 + `skills/reporting.md` §"Meta-report directories — sub-agent
sessions": *"The directory is garbage-collectable as one session unit.
When the substance migrates to permanent homes, the whole directory
retires together, not piece by piece."*

- `/293` — 5 research probes (vocabulary, unitbus, kameo, rkyv) + gap
  closure. Substance: `skills/workspace-vocabulary.md` exists; bead
  outcomes landed in workspace; research absorbed into design choices.
- `/317` — sema-upgrade + macro convergence audit. Substance: macro
  convergence epic landed (operator/181+/182); sema-upgrade-daemon
  direction settled as Persona-absorbs per /318 wave-4.
- `/318` — upgrade triad merger + persona-prefix rename. Substance:
  upgrade triad on disk; persona-prefix rename direction settled;
  beads filed (`primary-li0p`, `primary-avog` closed).
- `/319` — prior context-maintenance sweep. Outputs ARE the deletions
  it executed; the report itself retires as session unit.
- `/327` — workspace ARCH "pending schema-engine upgrade" markings.
  All target ARCH files now carry the markings (where still relevant);
  with the schema substrate now LIVE, the "pending upgrade" framing
  itself is superseded by per-component cutover beads.
- `/335` — state audit + test-claims verification + problems catalog.
  Substance: 27 questions driven into design pressure; designer leans
  in `/336` (also retiring); subsequent design passes /338-/340-/341
  absorbed the directions; problems P1-P5 all in motion via beads.
- `/337-real-pipeline-mvp` — single witness nota file from the MVP
  test run. The test SUCCEEDED; its witness lives in jj/git log of
  the worktree branches per `/339`. Working tree doesn't need it.

### §3.10 Schema-engine vision intermediates (`/329-/340`)

The substrate-finding arc — `/329` (InputStruct-per-variant), `/330`
(parallel-impl pivot + nspawn plan), `/332` (macro coverage audit),
`/333` + `/333-v2` (upgrade mechanism narrative + errata), `/334` +
`/334-v2` (multi-pass NOTA-first reader concept + corrections), `/336`
(designer leans on 27 questions), `/337` (current-state research),
`/338` (refreshed vision), `/339` (worktree archive), `/340` (schema
emission as fresh Rust composer). Per intent record 633 (every designer
pass ends with worktrees archived OR active): the worktree branches
themselves carry the substance for /339; for the others, /341 (Subagent
A's scope) IS the canonical synthesis that absorbs every settled
direction. The intermediates retire.

### §3.11 The RETRACTED report (`/342`)

`/342` was RETRACTED in its own first paragraph per psyche record 666:
*"retract the 'interact' trait idea, it doesnt work actually, methods
are interactions, I dont know why I went on about this now"*. Hard
drop — the report exists only as the retraction notice + a preserved
body for historical reference. Substance superseded by /343 and /345's
schema-as-channel-contract framing.

### §3.12 The presentation report (`/344`)

`/344` is a slide-deck-style presentation of the architecture. Useful
as one-time communication; not a working artifact. Substance covered
in /341 (Subagent A's scope) at greater depth. Retires.

## §4 Actions taken

All deletions executed in the working copy that the four parallel
subagents share. The orchestrator's `5-overview.md` will land the
single jj commit absorbing every subagent's work; this subagent's
deletions flow into that commit. No separate `jj describe -m '...'`
per-deletion — the orchestrator's commit message names the sweep.

Files removed in this subagent's pass (36 working-tree entries):

```
reports/designer/249-component-intent-gap-analysis.md
reports/designer/257-signal-contracts-names-and-shape-audit.md
reports/designer/263-schema-specification-language-design.md
reports/designer/266-persona-pi-triad-design.md
reports/designer/279-nota-schema-language-and-version-hash.md
reports/designer/281-headless-pi-research.md
reports/designer/285-versionprojection-trait-and-handover-protocol-specification.md
reports/designer/287-version-handover-component-explained.md
reports/designer/293-designer-and-research-batch-2026-05-23/   (5 files)
reports/designer/299-design-origin-process-and-agent-identity.md
reports/designer/301-design-elegant-cli-macro-with-caller-injection.md
reports/designer/305-v2-design-64bit-signal-per-component-namespacing.md
reports/designer/307-design-golden-ratio-namespace-split.md
reports/designer/308-design-pretyped-envelope-and-tap-anywhere.md
reports/designer/309-design-agent-component-abstraction.md
reports/designer/312-design-recursive-help-on-every-enum.md
reports/designer/315-design-sema-upgrade-and-handover-current-state.md
reports/designer/316-design-forge-family-current-direction.md
reports/designer/317-sema-upgrade-and-macro-convergence-audit/  (4 files)
reports/designer/318-upgrade-merger-and-persona-prefix-rename/  (4 files)
reports/designer/319-schema-stack-context-maintenance-sweep/    (4 files)
reports/designer/320-mvp-schema-language-pilot-unblock.md
reports/designer/321-mvp-visual-state-of-play.md
reports/designer/322-spirit-mvp-positional-schema-worked-example.md
reports/designer/323-mvp-scope-expansion-per-operator-directive.md
reports/designer/324-migration-mvp-spirit-handover-re-specification.md
reports/designer/325-nota-box-library-design-and-implementation.md
reports/designer/326-v13-spirit-complete-schema-vision.md
reports/designer/327-schema-engine-upgrade-marking-sweep/       (7 files)
reports/designer/329-schema-macro-component-extensibility.md
reports/designer/330-parallel-implementation-pivot-and-spirit-nspawn-plan.md
reports/designer/332-schema-macro-coverage-audit.md
reports/designer/333-upgrade-mechanism-full-design-explained.md
reports/designer/333-v2-upgrade-mechanism-corrections-from-real-world-test.md
reports/designer/334-multi-pass-nota-first-schema-reader.md
reports/designer/334-v2-multi-pass-nota-first-schema-reader.md
reports/designer/335-state-audit-and-test-verification/         (5 files)
reports/designer/336-designer-leans-on-27-psyche-questions-and-mvp-plan.md
reports/designer/337-current-state-research-for-real-mvp-pass.md
reports/designer/337-real-pipeline-mvp/                          (1 file)
reports/designer/338-schema-engine-refreshed-vision-2026-05-25.md
reports/designer/339-worktree-archive-and-system-overview.md
reports/designer/340-schema-emission-no-legacy-signal-channel-2026-05-25.md
reports/designer/342-interact-trait-code-walkthrough-2026-05-25.md
reports/designer/344-schema-architecture-presentation-2026-05-25.md
```

By file count: 36 top-level entries comprising ~58 individual files
(meta-directories expanded). Every file's substance retires per the
rationale clusters in §3.

## §5 Migrations table

No NEW migrations into permanent docs in this pass — every report
retired here already had its substance migrated by prior sweeps or
by subsequent design passes (the journey-documentation pattern). The
canonical permanent homes for the retired substance, per cluster:

| Cluster | Permanent home |
|---|---|
| §3.1 Pre-MVP gaps | Schema-driven substrate dissolves the prior gap framing; per-component schemas are the new substrate. |
| §3.2 Schema-language precursors | `schema` crate source + `/341` seven-principles synthesis (Subagent A scope) |
| §3.3 Persona-pi + agent abstraction | `persona-agent` triad code + `/318`-direction in operator landings |
| §3.4 Upgrade triad + version-handover | `version-projection/ARCHITECTURE.md`, `signal-upgrade/ARCHITECTURE.md`, `owner-signal-upgrade/ARCHITECTURE.md`, `sema-engine/ARCHITECTURE.md`; `/346` (Subagent A) for current narrative |
| §3.5 64-bit signal + envelope | `signal-frame/ARCHITECTURE.md` §5.2 + `signal-frame/src/frame.rs` |
| §3.6 signal-persona-origin + CLI macro | `signal-persona-origin/ARCHITECTURE.md` + `signal-frame::signal_cli!` in production |
| §3.7 MVP-build path | Live `schema` crate + `signal-persona-spirit::signal_channel!([schema])` + spirit v0.2.0 deployment |
| §3.8 Forge | `forge/ARCHITECTURE.md` + `signal-forge` skeleton |
| §3.9 Meta-directories | Per-meta-dir: directly into bead/ARCH/skill outcomes; sessions retire as units per intent 231 |
| §3.10 Schema-engine vision intermediates | `/341` (Subagent A scope) IS the canonical synthesis; live `schema` crate carries the executable form |
| §3.11 RETRACTED `/342` | Self-retracted; `/345` (Subagent A) carries the replacement framing |
| §3.12 Presentation `/344` | `/341` (Subagent A) carries the same substance with greater depth |

## §6 Kept reports (D's scope)

**Zero**. The aggressiveness target (≤5 keeps from the older set) was
honored at 0. Every report in D's scope either has its substance in a
permanent home already, or has been superseded by Subagent A's scope
reports (`/341, /343, /345, /346`), or is journey-documentation
preserved in the commit tree.

## §7 Post-state

After D's sweep (and the parallel actions of Subagents A, B, C, plus
the orchestrator's own work), `reports/designer/` contains:

```
reports/designer/
  341-schema-crystallizes-architecture-2026-05-25.md
  343-schema-syntax-for-effect-side-2026-05-25.md
  345-schemas-as-channel-contracts-2026-05-25.md
  346-actor-schemas-and-upgrade-mechanism-2026-05-25.md
  349-context-maintenance-sweep-2026-05-25/
    0-frame-and-method.md
    1-poc-schema-stack-explainer.md       (Subagent A, pending if not landed)
    2-nota-discipline-manifestation.md    (Subagent B, landed)
    3-spirit-v020-integration-manifestation.md  (Subagent C, landed)
    4-designer-reports-soft-cap-sweep.md  (THIS FILE)
    5-overview.md                          (Orchestrator, pending)
```

Working-tree count: **5 entries** (4 files + 1 meta-directory). The
soft cap is 12; the directory is comfortably under cap.

Subagent A may further retire `/341, /343, /345, /346` if it
determines their substance has migrated into `persona-spirit/INTENT.md`,
`schema/INTENT.md`, etc. That decision belongs to A's scope, not D's.

The orchestrator's `5-overview.md` lands the consolidated commit
absorbing all four subagent passes.

## §8 Uncertainties

**None requiring orchestrator review.** Every D-scope report had a
clear retirement path: either substance migrated to a permanent home,
or substance superseded by a newer report (typically in Subagent A's
scope), or substance is journey-documentation preserved in jj history.

The two borderline cases — `/315` (sema-upgrade current state) and
`/316` (forge family direction) — were initially IN-FLIGHT per the
prior /319 sweep, but the schema-substrate crystallization since /319
moved sema-upgrade into "Persona-absorbs" direction (per /318 wave-4)
and parked forge as a longer-arc concern outside the schema substrate.
Both retire cleanly; their substance is in code + per-repo ARCH.

The /293 directory's `/293/3` kameo-0.16 Scheduler research is the
only entry where I weighed KEEP: kameo 0.16's Scheduler is still a
candidate library for handover drain timeouts. But the substance was
already absorbed into bead `primary-e4oq` outcomes and into
`skills/kameo.md` (per `ntzxtkxrmmxs context-maintenance: migrate
/205 §3.6 bounded on_stop discipline to skills/kameo.md`). The research
report itself doesn't carry uniquely-load-bearing substance beyond
what's in the skill + the bead trace. Retire.

## §9 Discipline checklist

- [x] jj headless only (no editor prompts) — only file deletions; the
  orchestrator's commit lands inline per `5-overview.md`
- [x] No production code modification — only `reports/designer/`
- [x] Skill files / ARCH files don't reference retired reports — none
  added; per `skill-editor.md` discipline
- [x] Every retire operation tracked — §4 lists all 36 entries
- [x] Stayed in `reports/designer/` subdirectory — no cross-role touches
- [x] No NEW subagent dispatches from this subagent
- [x] No `/nix/store` filesystem search
- [x] No `---` horizontal-rule lines in markdown
