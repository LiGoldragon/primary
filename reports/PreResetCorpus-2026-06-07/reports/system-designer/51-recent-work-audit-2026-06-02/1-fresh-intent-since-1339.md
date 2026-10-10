# Sub-report 1 — Fresh Spirit intent (1339-1375) status audit

## Frame

Window: Spirit records 1339-1375 (inclusive). Records 1366-1369 do
not exist (gap in sequence; only 1365 and 1370+ in mid-range).
Predecessor audit (report 57, retired) covered 1307-1338.

Method: for each natural cluster, classify status as IMPLEMENTED
(code/config landed), MIGRATED (in a skill or per-repo
ARCHITECTURE.md / INTENT.md), or IN-SPIRIT-ONLY. Verification by
grep against `/git/github.com/LiGoldragon/<repo>/` source +
`/home/li/primary/skills/*.md` + workspace `AGENTS.md` / `INTENT.md`
+ relevant repo `ARCHITECTURE.md` / `INTENT.md`. Records about
local AI / Prometheus / pi / cloud / cluster ops are out-of-scope
for this audit and bucketed at the end.

## Cluster A — Positive-grep deployment checks forbidden (1340, 1341, 1342)

Substance: a positive `grep -R "Type"` block is not architecture
proof; only narrow negative grep (proving a retired symbol is
absent) is allowed. Architectural claims must be witnessed at
compile / runtime / fixture / integration layers.

Status: **MIGRATED**.

Evidence:
- `/home/li/primary/skills/testing.md:39-50` "No positive grep
  deployment checks" — matches 1340/1341/1342 substance directly
  with the same allowed-narrow-negative carve-out.
- `/home/li/primary/skills/architectural-truth-tests.md:112` reads
  "grep is NOT a Layer 1 witness" reinforcing the same boundary
  from the truth-test side.

The carve-out language in `testing.md` mirrors 1341 nearly
verbatim. Capture is complete.

## Cluster B — Engine-trait architecture LIVE in spirit-next (1357)

Substance: SignalEngine + NexusEngine + SemaEngine (Spirit
1326-1336) are live in `spirit-next` main. SemaEngine split into
`apply` + `observe` per Spirit 1332 (parallel reads) landed at
`d29dc6c`.

Status: **IMPLEMENTED + MIGRATED**.

Evidence:
- `/git/github.com/LiGoldragon/spirit-next/src/schema/lib.rs:1526`
  `pub trait SignalEngine`; `:1557` `pub trait NexusEngine`;
  `:1576` `pub trait SemaEngine`. Generated module on main.
- `/home/li/primary/skills/component-triad.md:746-820`
  "Runtime triad engine traits" formalizes the triad with
  cited Spirit records 1330/1331/1332.
- `/git/github.com/LiGoldragon/spirit-next/ARCHITECTURE.md` +
  `INTENT.md` carry the triad narrative.
- spirit-next `main` head is `b5ced5c` (HEAD = main confirmed);
  the d29dc6c reference is reachable on main via the chain
  `d29dc6c -> b53f4fc -> e4e5035 -> 5fc9639 -> 5ac8b16 -> b5ced5c`.

Cluster fully landed; no migration debt.

## Cluster C — Testing trace as runtime witness (1343, 1344, 1345, 1346, 1347, 1349, 1350)

Substance: schema-derived runtime gets an optional testing-build
log surface so SignalEngine / NexusEngine / SemaEngine usage emits
structured trace events to a logging socket. The CLI is the log
surface — testing trace flows back through the same wire substrate
as production interaction. Trace becomes the workspace canonical
Layer 2 runtime witness (1349 explicit), and each engine self-
verifies via entry/exit hooks (1350).

Status: **IMPLEMENTED** in code. **PARTIALLY MIGRATED** at the
spirit-next repo layer; workspace-level capture is weak.

Evidence (implemented):
- Schema-rust-next emitter at
  `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:1825-1907`
  emits `trace_signal_activation`, `trace_signal_admitted`,
  `trace_signal_triaged`, `trace_signal_replied`,
  `trace_nexus_entered`, `trace_nexus_decided`,
  `trace_sema_write_applied`, `trace_sema_read_observed` as
  default-no-op methods on the engine traits themselves.
- `/git/github.com/LiGoldragon/spirit-next/src/lib.rs:29-56`
  `#[cfg(feature = "testing-trace")] pub mod trace;` exports
  `TraceError, TraceEvent, TraceLog, TraceObjectName,
  TraceSocketListener, TraceSocketPath`.
- `/git/github.com/LiGoldragon/spirit-next/src/config.rs:12-58`
  `trace_socket_path: Option<ConfigurationPath>` is part of
  the binary `Configuration` struct (matches 1348 — config-as-
  data).
- `/git/github.com/LiGoldragon/spirit-next/tests/instrumentation_logging.rs`
  + `tests/process_boundary.rs` form the Layer 2 witness.
- `/git/github.com/LiGoldragon/spirit-next/flake.nix:100-147`
  emits `packages.trace`, `packages."trace-cli"`,
  `packages."trace-daemon"` separate from the lean
  `packages.cli` / `packages.daemon` (matches 1371).

Evidence (migrated at repo layer):
- `/git/github.com/LiGoldragon/spirit-next/ARCHITECTURE.md:35-43`
  describes the `testing-trace` surface, the rkyv `TraceEvent`
  frame, and the trace-socket round-trip as runtime proof rather
  than deployment grep.
- `/git/github.com/LiGoldragon/spirit-next/ARCHITECTURE.md:284`
  + `:358` cover the in-process witness sites.
- `/git/github.com/LiGoldragon/schema-rust-next/ARCHITECTURE.md:116-123`
  + `INTENT.md:77-84` explain trace hooks belong to the
  engine traits themselves (closes 1365 correction at the
  schema-emit repo).

Gap (workspace-level):
- `skills/architectural-truth-tests.md` does NOT yet name the
  testing-trace log surface as the workspace canonical Layer 2
  witness for engine-trait usage — 1349's Maximum-certainty
  claim. The skill talks about Layer 2 witnesses abstractly
  but does not point at the spirit-next testing-trace pattern
  as the reference realisation.
- `skills/component-triad.md` (the Runtime triad engine traits
  section, lines 746-820) does NOT mention the trace hook
  default methods or the testing-build feature-gate pattern as
  part of the engine-trait contract, even though they now live
  alongside the engine-trait methods in emitted Rust.

## Cluster D — Single-NOTA-argument extends to build config (1348)

Substance: build configuration is itself a NOTA struct;
testing-build is a configurable field. The single-NOTA-argument
rule governing daemon/CLI input also governs build configuration.

Status: **IN-SPIRIT-ONLY** at the discipline layer.
**IMPLEMENTED-AS-FEATURE-FLAG** in code.

Evidence (in-code, partial):
- `flake.nix:100-147` switches between lean and trace packages
  via Cargo feature flags (`--features testing-trace`). This is
  ad-hoc Cargo-flag plumbing, not a NOTA-struct shape.
- `skills/component-triad.md:366-401` "The single argument rule"
  covers runtime CLI / daemon argv but does NOT extend the rule
  to build configuration as 1348 (Maximum) requires.

Gap: 1348's Maximum-certainty claim that build config itself is
a NOTA struct hasn't crystallised in code (still Cargo feature
flags) or skill (no §"Build config is NOTA" in component-triad
or nix-discipline). Worth migrating.

## Cluster E — Engine method count matches wire event count (1361)

Substance: SignalEngine has two methods (triage + reply) because
Signal handles two wire events. NexusEngine has one (execute).
SemaEngine has two (apply + observe per Spirit 1332). Resolves
the divergence between designer 454's uniform-execute spec and
the b53f4fc2 implementation.

Status: **IMPLEMENTED + MIGRATED**.

Evidence:
- `/home/li/primary/skills/component-triad.md:761-763` table
  explicitly states "triage + reply" for SignalEngine, "execute"
  for NexusEngine, "apply + observe" for SemaEngine, with
  per-row Spirit citations.
- Generated trait method count in
  `schema-rust-next/src/lib.rs:1825-1907` matches the discipline
  exactly.

## Cluster F — Trace hooks belong to engine traits, not side enums (1365, 1370, 1374)

Substance: testing trace traceability is on traits of the
schema-derived engine actors, not a hand-written / generated event
enum living beside them (1365 Correction). Trace runs live through
the daemon and comes back to the CLI as a human-facing log
surface (1370). In a trace/debug build, CLI defaults to printing
decoded trace logs to stdout (1374).

Status: **IMPLEMENTED + MIGRATED at repo layer**.

Evidence:
- `schema-rust-next/src/lib.rs:1825-1907` — trace hooks emitted
  AS METHODS on the engine traits, with default no-op bodies.
  Implementors who want trace override the hooks; non-trace
  consumers get the no-op default. Closes 1365 directly.
- `schema-rust-next/ARCHITECTURE.md:116-123` documents the
  engine-trait-owned trace hooks.
- `spirit-next/tests/process_boundary.rs` (referenced from
  `flake.nix:174-176`) drives CLI-receives-trace-events-from-
  daemon-trace-socket — proves the 1370 live round-trip.

Gap: workspace-level skill capture (similar to Cluster C). The
"engine-trait correction" insight (1365) is not in
`skills/component-triad.md` or `skills/architectural-truth-tests.md`
as a stated principle — instrumentation belongs to the
interface/actor contract, not a local side vocabulary. Worth
migrating because it's a general design rule, not a
spirit-next-specific tactic.

## Cluster G — Optional-at-compile-time trace + differentiated Nix packages (1371)

Substance: trace code must be optional at compile time; Nix
exposes differentiated packages for normal lean builds versus
trace-enabled testing builds.

Status: **IMPLEMENTED**.

Evidence: `spirit-next/flake.nix:114-147` — `traceDaemonPackage`,
`traceCliPackage`, `traceCombinedPackage` are separate Cargo
builds with `--features testing-trace`, exposed as
`packages.trace`, `packages."trace-cli"`,
`packages."trace-daemon"`. The lean `packages.cli` /
`packages.daemon` compile without trace. The Cargo feature
`testing-trace` is the compile-time gate.

Workspace skill capture absent (no `skills/nix-discipline.md`
§"Trace vs lean package shape") — but this is component-level
boilerplate. 1375 explicitly proposes extracting the boilerplate
into a Nix library "once the spirit-next shape proves out", so
1371 + 1375 together are at the "let the shape stabilise, then
crystallise into a shared library" stage. Status of 1375 is
deliberately IN-SPIRIT-ONLY (Clarification, future-oriented).

## Cluster H — No-NOTA-between-components binary protocol rule (1373)

Substance: there should be NO NOTA between components. Daemons
and components exchange binary protocol data. The CLI is the
translation/debugging surface that may wrap a normal call in a
debugging request (e.g. where logs go). Maximum certainty.

Status: **IN-SPIRIT-ONLY** at the workspace-skills layer.
**IMPLEMENTED IN PRACTICE** in spirit-next (the wire is rkyv-
encoded `signal-*` records, not NOTA strings).

Evidence (in code):
- `spirit-next` wire substrate is rkyv-encoded across the trace
  socket and Signal/Nexus/SEMA round-trips (see TraceEvent rkyv
  framing referenced in `ARCHITECTURE.md:38`). Components
  exchange binary frames per the in-code reality.

Gap (workspace-level):
- `skills/component-triad.md:366-401` "The single argument rule"
  covers CLI and daemon argv accepting NOTA-or-rkyv per the
  hardcoded boundary — but the broader claim "NO NOTA between
  components, full stop" is NOT stated. The closest existing
  language conflates "single argument" with "translation
  boundary" without naming the binary-only-between-components
  principle. 1373 is Maximum; this is a load-bearing gap.

## Cluster I — Rkyv emitter discipline (1358, 1359, 1360)

Substance: schema-rust-next emitter should automatically (1358)
wrap recursive enum variants in `Box`, (1359) consolidate same-
shape sibling variants under a semantic-family parent carrying
the original variant name as data, and (1360) sub-divide
closed-sum enums past ~10 variants into sub-enums grouped by
semantic kinship. Audit Suggestions 1, 2, 3 from designer 452.

Status: **IN-SPIRIT-ONLY**. Audit branch exists but did not
land in main.

Evidence (miss):
- `grep -n "Box\|recursive\|family\|consolidate\|sub.divide" schema-rust-next/src/lib.rs` returns no emitter logic for
  these patterns (only trace-related emissions).
- `schema-rust-next` main HEAD is `d3ec9f9` — no commit message
  mentions Box/family/sub-divide.
- `schema-next` carries `97fde52 designer/452: audit rkyv enum-
  wrapping presumption on MacroPatternObject pilot` and an
  `audit-rkyv-enum-wrapping-presumption` branch, but the
  emitter-side implementation hasn't propagated into
  `schema-rust-next` main.
- No mention of recursive-Box or family-consolidation in
  `schema-rust-next/ARCHITECTURE.md` or `INTENT.md`.

These three are Maximum/High decisions with concrete audit
verification cited in the records themselves (1358 explicitly
references "eight pilot tests on the audit-rkyv-enum-wrapping-
presumption schema-next branch"). They are ready to manifest;
nothing technical is blocking. Recommend operator pull-through
to `schema-rust-next` main as a discrete work item.

## Cluster J — Designer worktree, operator main (1352, 1354, 1355)

Substance: operator integration lands on main; designer work for
new design/prototype proceeds in worktrees rebased on main,
reusing past work where appropriate, continuing one
design/prototype at a time around what the prototype is meant to
prove. 1355 generalises: depth-first single-capability proving,
not breadth-first design fan-out.

Status: **MIGRATED** (operator/designer skills + AGENTS.md).
1355 (the methodology principle in isolation) is **PARTIALLY**
migrated.

Evidence:
- `/home/li/primary/AGENTS.md:384-390` "Designers work on
  feature branches in `~/wt`; operators own main + rebase"
  captures the lane split with the 515 cross-reference.
- `/home/li/primary/skills/operator.md:243-301` covers operator
  integration on main, harvesting from designer worktrees,
  retaining the designer branch as evidence.
- `/home/li/primary/skills/designer.md:269-302` covers designer
  branches not being mainline authority.

Gap: the "one capability proved at a time, depth-first not
breadth-first" methodology of 1355 (High) is not stated as a
named principle in `skills/designer.md`. The closest content
("pilot one slice, ship one slice") is in the report tradition
but not formalised. Worth adding as a §"Prototype-proving
methodology" subsection. Lighter-touch than 1373 because it's
High certainty, not Maximum.

## Cluster K — Context-maintenance after impl rounds (1353)

Substance: after active implementation/prototype subagent work,
run context maintenance and a fresh-intent audit over recent
reports and code before deciding what to address. Main operator
synthesises returned work, picks sensible immediate fixes,
implements rather than letting stale context drive the next slice.

Status: **MIGRATED in practice** (this very meta-report
directory + earlier `50-cross-lane-context-maintenance-2026-05-30`
both realise the discipline). Not named as a skill section.

Evidence:
- `/home/li/primary/reports/system-designer/50-cross-lane-context-
  maintenance-2026-05-30/` shows the audit-then-act pattern.
- `/home/li/primary/skills/designer.md:635+` covers the
  orchestrator-synthesises-and-decides flow for sub-agent
  outputs but doesn't name "post-implementation context
  maintenance" as its own step.

High certainty, generic across roles — worth a one-line
addition to both `skills/operator.md` and `skills/designer.md`
naming "After substantive impl work, run a fresh-intent +
recent-reports audit before picking the next slice."

## Cluster L — Cross-pollination intent-gap method (1364)

Substance: intent gaps are filled by cross-pollinating patterns
established elsewhere in the intent. When one area lacks a
clear design, look for an analogous pattern already established
and project it onto the gap. Used during intent-clarity audits
of recent work. Medium certainty.

Status: **IN-SPIRIT-ONLY**. No skill captures this method.

Evidence (miss):
- `grep cross.pollinat\|gap.fill\|analog` across
  `skills/intent-maintenance.md`, `skills/intent-clarification.md`
  returns no matches.
- `/home/li/primary/skills/human-interaction.md:46` has a
  "gap-fill" pattern for inter-agent coordination but it is
  NOT the design-pattern-cross-pollination method 1364
  describes.

Medium certainty + a method-rather-than-a-rule pattern — fine to
leave IN-SPIRIT-ONLY for now but a natural fit for
`skills/intent-clarification.md` if it stabilises through use.

## Cluster M — Agent memory as queryable tool-call trace (1356)

Substance: persistent memory for tool-using agents is the
queryable tool-call trace, not the model context window. Expose
`query_history` back to the agent. MCP-first architectural
property — structured tool protocols give perfect recall by
construction. High certainty, applies generically.

Status: **IN-SPIRIT-ONLY**.

Evidence (miss):
- No skill mentions `query_history` or MCP-first agent memory.
- Note: workspace already has the harness-memory rule
  (`AGENTS.md:425+` "No harness-dependent memory; session-scoped
  tools land in workspace files"). 1356 is adjacent but
  different — it's about HOW a tool-using agent's persistent
  memory should be architected, not where workspace truth
  lives.

Worth a `skills/agent-memory-architecture.md` or section in
`skills/library.md` IF the workspace is heading toward building
tool-using agents. Pure principle right now; defer unless
implementation work picks up.

## Cluster N — No-parallel-legacy-API discipline (1339)

Substance: don't keep old design convenience APIs after the
working interface exists. Keep ONE active working API moving
forward; remove legacy/convenience surfaces rather than
maintaining parallel ways to express the same runtime path.
Maximum certainty.

Status: **IMPLEMENTED in recent schema-rust-next commits**.
**IN-SPIRIT-ONLY at the workspace-skills layer**.

Evidence (implemented):
- `schema-rust-next` recent commits explicitly retire legacy
  surfaces: `06a7797 schema-rust: remove legacy single sema
  surface`, `febde07 schema-rust: retire generated NexusMail
  convenience`, `35baaf7 schema-rust: remove retired enum
  spelling from docs`, `d8006b6 schema: remove legacy
  declaration compatibility`.

Gap: no skill states the discipline as a named principle. Closest
language is `skills/architecture-editor.md`'s removal discipline
(don't search; this is a general pattern). Worth a one-line
addition to either `skills/architecture-editor.md` or
`skills/component-triad.md`.

## Out-of-scope bucket (noted, not audited)

These records are about local AI / Prometheus / pi / cluster /
cloud-deploy and lie outside this lane's area. Per the brief:

- **1362, 1363** — local AI toolkit (curated best/latest models
  per capability; Prometheus prefetch). cloud-designer /
  cluster-operator territory.

## Cross-cutting findings

### F1 — Schema-rust-next emitter is the propagation engine

Engine-trait + trace-hook emission both live in
`schema-rust-next/src/lib.rs:1825-1907` as schema-emitted code.
The rkyv emitter discipline (1358-1360) is the next layer of
emitter work and is currently audit-branch-only. This is the
single highest-leverage repo for the next slice — three Maximum/
High records (1358 Maximum, 1359 High, 1360 High) are waiting on
emitter implementation that has been verified on a pilot branch.

### F2 — Workspace-skill-level capture lags repo-level capture

The pattern across Clusters C, F, H is: insight lands in code and
in the relevant repo's `ARCHITECTURE.md` / `INTENT.md`, but the
workspace-level skill (the generalisation across components) is
not updated. Spirit's Maximum-certainty general claims (1349,
1365, 1373) name "workspace canonical X" / "interface/actor
contract" / "component-triad rule" — these are explicitly
workspace-level statements that should land in skills/, not just
in spirit-next/ARCHITECTURE.md.

### F3 — Testing-trace is the single most landed insight from this window

Clusters C + F + G all converge on the testing-trace + engine-
trait-hooks pattern. It is implemented in schema-rust-next
(emission), spirit-next (consumption + tests), flake.nix
(packaging), and captured at both repos' ARCHITECTURE/INTENT.
The missing piece is naming it as the workspace canonical Layer
2 witness in `skills/architectural-truth-tests.md`.

### F4 — Several Maximum-certainty records still IN-SPIRIT-ONLY at workspace layer

1348 (build-config-is-NOTA), 1349 (testing-trace = workspace
canonical Layer 2 witness), 1365 (trace belongs to engine-trait
contract, not side vocabulary), 1373 (NO NOTA between
components). All Maximum certainty. All currently lack workspace-
skill-level capture. F4 is the report's largest finding.

## Recommendations

These are the IN-SPIRIT-ONLY entries worth migrating NOW. Ordered
by certainty + leverage.

1. **1373** Maximum — Add §"No NOTA between components — binary
   protocol is the wire" to `skills/component-triad.md` after
   §"The single argument rule". State: NOTA is for argv at the
   process boundary; between live components the wire is binary.
   CLI is the human-facing translation/debugging layer. Cite
   spirit-next's rkyv signal-protocol as the worked example.

2. **1349** Maximum — Add §"Testing-trace as the workspace
   canonical Layer 2 witness for engine-trait usage" to
   `skills/architectural-truth-tests.md` after the existing
   Layer 2 discussion. Cite the schema-rust-next emitter +
   spirit-next consumer + flake.nix package split as the
   reference realisation; cite designer 459's proof-of-usage
   ladder as upstream.

3. **1365** Maximum — Add to `skills/component-triad.md` §Runtime
   triad engine traits a paragraph: instrumentation belongs to
   the engine-trait contract itself as default-no-op hook
   methods, not to a parallel local trace enum. Cite the
   schema-rust-next emission at `src/lib.rs:1825-1907`.

4. **1358** Maximum — Operator pull-through item: bring the
   `audit-rkyv-enum-wrapping-presumption` recursive-variant
   `Box<T>` wrapping into `schema-rust-next` main. Eight pilot
   tests already verified per the record body.

5. **1348** Maximum — Migration is two-step. (a) Add §"Build
   configuration is itself a NOTA struct" to
   `skills/component-triad.md` after §"The single argument
   rule". (b) Refactor `spirit-next/flake.nix` ad-hoc Cargo
   feature flags into a typed build-config NOTA struct read at
   build time. Step (a) is cheap; step (b) is operator work.

6. **1339** Maximum — One-paragraph addition to
   `skills/architecture-editor.md` (or `skills/component-triad.md`
   wherever it lands closer) stating: when a working interface
   exists, retire the legacy convenience API; do not maintain
   parallel ways to express the same runtime path. Cite the
   recent schema-rust-next removal commits as examples.

7. **1355** High — One-paragraph addition to `skills/designer.md`
   naming "depth-first single-capability prototype-proving" as
   the methodology. Pair-cite with the existing pilot-one-slice
   guidance.

8. **1353** High — One-line addition to `skills/operator.md`
   (and mirror in `skills/designer.md` for the orchestrator
   protocol) naming "after substantive impl work, run a fresh-
   intent + recent-reports audit before picking the next slice"
   as a standing discipline.

Records that are appropriate to leave IN-SPIRIT-ONLY for now:
1356 (Medium-leverage agent-memory architecture — wait for
tool-using-agent work to pick up), 1364 (Medium method —
stabilise through use first), 1372 + 1375 (Decision +
Clarification about Nix package shapes; 1375 explicitly says
"once the spirit-next shape proves out").
