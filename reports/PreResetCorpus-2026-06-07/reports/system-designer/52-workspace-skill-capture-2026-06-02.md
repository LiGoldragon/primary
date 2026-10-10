# Workspace skill capture pass — 9 IN-SPIRIT-ONLY records → 5 skills — 2026-06-02

Kind: migration report.
Role: system-designer (sub-agent under report 51's orchestrator).
Retires: per Spirit 1323 — once all nine migrations are absorbed into
downstream agent context (next audit cycle confirms).

## Frame

Per the audit synthesis at `reports/system-designer/51-recent-work-
audit-2026-06-02/5-overview.md` §"T2.1 Workspace skill capture pass":
nine Maximum / High certainty Spirit records had been waiting in
IN-SPIRIT-ONLY status for 12 hours to 7 days. The dominant tension
the audit named (F2/C5/F4) is **capture-to-skill lag**: insight
lands in code and per-repo `ARCHITECTURE.md` / `INTENT.md` but the
workspace-level skill (the generalisation across components) lags
behind. Each individual migration is small; the value is landing
them all in one coherent pass rather than opportunistically across
sessions where capture quality varies.

This report records the pass.

## What landed

| ID | Spirit | Magnitude | Kind | Target file | Section |
|---|---|---|---|---|---|
| M1 | 1373 | Maximum | Principle | `skills/component-triad.md` | new §"No NOTA between components — binary protocol is the wire" |
| M2 | 1349 | Maximum | Principle | `skills/architectural-truth-tests.md` | new §"Testing-trace as the workspace canonical Layer 2 witness for engine-trait usage" |
| M3 | 1365 | Maximum | Correction | `skills/component-triad.md` | new §"Instrumentation belongs to the engine-trait contract" |
| M4 | 1348 | Maximum | Decision | `skills/component-triad.md` | new §"Build configuration is itself a NOTA struct" |
| M5 | 1388 | Medium | Clarification | `skills/component-triad.md` | new §"Nexus's inner-world / outer-world vocabulary" |
| M6 | 1339 | Maximum | Principle | `skills/architecture-editor.md` | new §"Retire legacy paths when the working interface exists" |
| M7 | 1355 | High | Principle | `skills/designer.md` | new §"Depth-first single-capability prototype-proving" |
| M8 | 1353 | High | Decision | `skills/operator.md` + `skills/designer.md` | new §"Audit before the next slice" in both |
| M9 | 1327 | Maximum | Principle | `skills/architectural-truth-tests.md` | inline citation in §"Schema-chain witnesses use schema objects" |

All nine landed. Five commits total, grouped by target file:

| Commit | File | Migrations |
|---|---|---|
| `9ce9fe81` | `skills/component-triad.md` | M1, M3, M4, M5 |
| `fa753bf8` | `skills/architectural-truth-tests.md` | M2, M9 |
| `4ffa8dac` | `skills/architecture-editor.md` | M6 |
| `218ad5e7` | `skills/designer.md` | M7, M8 |
| `db88e9d4` | `skills/operator.md` | M8 |

Five commits matches the spec (4-6 expected). Each commit is
path-selective; the audit reports under `reports/system-designer/51-
recent-work-audit-2026-06-02/` and sub-agent A's parallel orphan-
chain work were not swept into any of my commits.

## Per-migration log

### M1 — Spirit 1373 → `skills/component-triad.md:403`

Record body: *"There should be no NOTA between components. Daemons
and components exchange binary protocol data; the CLI is the
translation/debugging surface that can wrap a normal call in a
debugging request with options such as where logs should be
displayed or stored."*

Insertion: AFTER §"The single argument rule" (ends at line 401),
BEFORE §"Help operations". Pairs naturally with M4 (also a
single-argument-rule extension) immediately following.

Substance: NOTA is the BOUNDARY form (argv, stdout, daemon ↔ human).
Between live daemons the wire is BINARY (rkyv-encoded signal-frame
frames), not NOTA. The CLI is the translation/debugging surface that
can wrap calls in debugging requests (e.g. naming where trace logs
flow). Worked example: spirit-next's rkyv-encoded signal-frame +
trace-socket round-trip. Scales to every future inter-component
channel: NOTA at any inter-component boundary is a triad violation
in the same shape as NOTA on a daemon socket (Invariant 2).

### M2 — Spirit 1349 → `skills/architectural-truth-tests.md:137`

Record body: *"The testing-build logging socket is the workspace
canonical Layer 2 runtime witness for engine-trait usage. When
testing build is active and logs flow to the CLI, the agent observes
proof that Signal/Nexus/SEMA engine traits are actually called by
the runtime — not just present in source. This realizes the
proof-of-usage ladder from designer 459 as a deployable feature."*

Insertion: as `#### ` (sub-section) inside §"Layer 2 — RUNTIME
(execution path taken)" (line 117), AFTER the strength paragraph
and BEFORE §"Layer 3 — BEHAVIORAL". Placement names the witness as
a specialization of Layer 2, not a separate layer.

Substance: the testing-trace surface as the workspace canonical
Layer 2 witness for engine-trait usage. Reference realization
across three repos: emission in `schema-rust-next/src/lib.rs`
(1825-1907), consumption in `spirit-next/tests/
instrumentation_logging.rs` + `tests/process_boundary.rs`,
packaging in `spirit-next/flake.nix` (lean vs trace package
split). Cross-references §"Instrumentation belongs to the
engine-trait contract" in component-triad.md (the M3 sister
addition). Witness strength: the trace hook IS the trait's
emission, so a bypass that re-implements the engine outside the
trait loses the witness as a consequence.

### M3 — Spirit 1365 → `skills/component-triad.md:889`

Record body: *"Testing trace must not be modeled merely as a
hand-written or generated event enum in spirit-next. Traceability
should be expressed as traits on schema-derived interfaces and,
where possible, on the Signal, Nexus, and SEMA actor traits
themselves, so instrumentation belongs to the interface/actor
contract rather than to a local side vocabulary."*

Insertion: as `### ` sub-section inside §"Runtime triad engine
traits", AFTER §"What this pattern is — and is not" and BEFORE the
canonical-worked-example paragraph.

Substance: instrumentation is engineering of the trait surface, not
of a parallel side vocabulary. The emitted shape: default-no-op
trace hook methods on the engine traits themselves. Cites the
schema-rust-next emission at `src/lib.rs:1825-1907`. Names the
side-enum pattern this corrects (a hand-written `TraceEvent` enum
next to the engines) and the right shape (hooks on the trait).

### M4 — Spirit 1348 → `skills/component-triad.md:442`

Record body: *"Build configuration is itself a NOTA struct with
fields — the same single-NOTA-argument rule that governs daemon and
CLI input also governs build configuration. Testing-build is a
configurable field on that struct; how the build switches between
production and testing modes is the same NOTA-shaped declaration as
the rest of the build config."*

Insertion: AFTER M1 (also after §"The single argument rule"). The
two extensions of the single-argument rule (runtime / wire and
build) sit together.

Substance: build configuration is itself a NOTA struct. Today's
`spirit-next/flake.nix` realises the runtime intent through Cargo
feature flags — the addition names this as "the correct runtime
behaviour realised through the wrong substrate" and points at the
destination shape (a `BuildConfiguration` record). Open in code
(implementation is feature-flag-shaped today, NOTA-shape is the
direction), captured here as workspace discipline.

### M5 — Spirit 1388 → `skills/component-triad.md:924`

Record body: *"Nexus sits between two worlds — Signal is the OUTER
world (clients wire ingress and egress) SEMA is the INNER world
(durable state mutations and observations). Nexus is the center
making decisions; Signal/SEMA are its peripheries. The inner/outer
vocabulary makes architectural roles explicit and rhymes with
object-oriented original insight of interfaces first. Consistent
with the engine-trait architecture (Spirit 1326-1336) and 1336
origin-route threading through full pipeline."*

Insertion: as `### ` sub-section inside §"Runtime triad engine
traits", immediately after M3 and before the canonical worked
example. Both M3 and M5 sit between the "What this pattern is" list
and the closing canonical-example paragraph; both extend the
trait-pattern picture with additional vocabulary.

Substance: the OUTER world / INNER world vocabulary for Nexus's
peripheries. Signal = outer (process boundary, wire framing,
identity stamping). SEMA = inner (redb, durable state).
Nexus = center. The vocabulary makes architectural roles explicit
and rhymes with object-oriented interfaces-first insight. Cross-
referenced to engine-trait architecture (Spirit 1326-1336) and
origin-route threading (Spirit 1336).

### M6 — Spirit 1339 → `skills/architecture-editor.md:425`

Record body: *"Do not keep old design convenience APIs after the
working interface exists. The stack should keep one active working
API moving forward and remove legacy or convenience surfaces
instead of maintaining parallel ways to express the same runtime
path."*

Insertion: as `## ` section AFTER §"Editing rules" (which contains
the parallel discipline for architecture docs: "Edit in place;
don't fork or version"), BEFORE §"When to create one". The new
section generalises the doc-level rule to the code substrate.

Substance: when the working interface exists, retire the legacy
convenience API. One active working API moving forward. Cites the
recent schema-rust-next + schema-next removal commits (`06a7797`
legacy single sema surface, `febde07` generated NexusMail
convenience, `35baaf7` retired enum spelling from docs, `d8006b6`
legacy declaration compatibility). Worked examples grounded in
real commits I verified exist before citing. Consistency with
`ESSENCE.md` §"Backward compatibility is not a constraint" named.

**Placement note.** The audit suggested either architecture-editor
or component-triad. After reading both end-to-end, architecture-
editor was the cleaner fit because it already carries the parallel
"edit in place" discipline for docs; the new section generalises
that to code. component-triad.md is about API SHAPE (NOTA, single
argument, triad invariants) rather than about API LIFECYCLE.

### M7 — Spirit 1355 → `skills/designer.md:286`

Record body: *"Design work progresses by proving one prototype
capability at a time in a worktree — pick the next thing the
schema-stack prototype needs to prove, prove it in a feature
branch worktree, integrate, then move to the next. Avoid
breadth-first design fan-out; depth-first single-capability proving
keeps the design grounded in working code."*

Insertion: as `### ` sub-section inside §"Working pattern", AFTER
§"Work on feature branches in `~/wt`" and BEFORE §"Reports as
visuals". The worktree-discipline sub-section names the SUBSTRATE;
the new section names the METHODOLOGY that uses it.

Substance: depth-first single-capability proving. Pairs with the
"pilot one slice, ship one slice" pattern. Shape consequences: one
feature branch under proof per design thread; reports pin the
capability under proof (not a fan-out roadmap); integration is the
completion signal. Worked example: the designer 446 → 454 → 461
spirit-pilot session as the recent instance.

### M8 — Spirit 1353 → `skills/operator.md:260` AND `skills/designer.md:557`

Record body: *"After active implementation/prototype subagent work,
run context maintenance and a fresh-intent audit over recent
reports and code before deciding what to address immediately. The
main operator should synthesize the returned work, choose sensible
immediate fixes, and implement them rather than letting stale
context drive the next slice."*

Insertion in operator.md: as `### ` sub-section inside §"Working
pattern", AFTER §"Subagents are asynchronous side work" and BEFORE
§"Work from the designer cascade". Both deal with subagent cadence;
M8 names what happens AFTER the subagent returns.

Insertion in designer.md: as `### ` sub-section at the end of
§"Parallel manifestation + audit pattern", BEFORE §"Working with
operator". The manifestation+audit pattern is one shape of the
discipline; M8 names the general rule.

Substance: after substantive impl/subagent work, run an audit
before opening the next slice. Cites the worked examples in this
lane: `reports/system-designer/50-cross-lane-context-maintenance-
2026-05-30/` and the in-flight `reports/system-designer/51-recent-
work-audit-2026-06-02/`. The two sister sub-sections in operator.md
and designer.md cross-reference each other.

Committed as two separate commits (one per target file) because
the additions are independent and grouped by file per spec.

### M9 — Spirit 1327 → `skills/architectural-truth-tests.md:397`

Record body: *"Every component engine in the workspace triad
architecture defines and uses its Signal, Nexus, and SEMA
interfaces in schema, and conducts core logic through schema-emitted
traits whose methods take and return root types of the concerned
interfaces — adapting Spirit 1326 (spirit-engine-specific) to the
workspace-wide component-triad pattern. The trait surface is
uniform across components; each component's runtime is a
composition of schema-emitted trait implementations."*

Insertion: inline citation in the opening paragraph of §"Schema-
chain witnesses use schema objects" — a single sentence anchoring
the traceability of the truth-test discipline to the workspace-wide
Principle.

Substance: tiny anchor edit. The section already used the
`SignalEngine` / `NexusEngine` / `SemaEngine` vocabulary; the
addition makes the Spirit 1327 link explicit so a reader following
"why are these the witness surface?" arrives at the workspace-wide
Principle, not at an ambient assumption.

## Records NOT migrated and why

The brief named exactly the nine above. I did not surface
additional records for capture in this pass because the audit
recommendations (sub-agent 1's R1-R8 + sub-agent 3's R3+R7) named
exactly this set, and the brief's quality bar emphasises
substance-faithful capture over coverage expansion.

Records the audit deliberately left IN-SPIRIT-ONLY:
- **1356** (Medium-leverage agent-memory architecture) — wait for
  tool-using-agent work to pick up. Audit verdict: pure principle,
  defer until implementation work materialises.
- **1364** (Medium method — cross-pollination intent-gap method) —
  stabilise through use first.
- **1372 + 1375** (Decision + Clarification about Nix package
  shapes; 1375 explicitly says "once the spirit-next shape proves
  out"). Future-oriented; not yet ready.

These four are correctly left in Spirit-only state.

## Methodology observations

### What worked

- **End-to-end reads of target skill files before drafting.** The
  insertion points only revealed themselves after reading the whole
  file shape. component-triad.md's §"The single argument rule"
  paired naturally with M1 and M4 because reading the file end-to-
  end made the "rule extension" cluster visible.
- **Spirit-record-first reading order.** Querying each record's
  full body via `spirit "(Observe (RecordIdentifiers ((Exact N)
  WithProvenance)))"` before drafting forced me to write to the
  record's actual wording, not the audit's interpretation. M5
  (Nexus inner/outer) was a Medium-certainty Clarification, not a
  Maximum — the record's tone informed the addition's tone
  (vocabulary clarification, not load-bearing principle).
- **Cross-citation verification before committing.** I checked
  every commit hash cited (M6's schema-rust-next + schema-next
  retirement commits) against the real jj logs before writing them
  into the skill. Two of the four commits the audit cited
  (`febde07`, `35baaf7`, `06a7797`, `d8006b6`) were beyond a small
  `--limit` window and would have looked hallucinated to a future
  agent reading the log; they exist further back. Always verify.

### What I would do differently

- **Resolve the architecture-editor vs component-triad question
  for M6 earlier.** I drafted half the prose under the assumption
  it'd land in component-triad, then re-read architecture-editor
  and reverted. The right call surfaces by reading both files
  end-to-end before drafting — which IS the methodology, but I
  ran ahead before completing it.
- **The audit's commit-hash citations need verification AS the
  authoring step, not as a quality-check pass after.** Future
  passes: verify every cited locator (commit, line, file path)
  before drafting the addition that cites them.

### Next capture pass — what to do differently

- **Migrate as a single coordinated pass when 8+ records accumulate
  in IN-SPIRIT-ONLY status**, not opportunistically. The audit
  identified this as the dominant tension; this pass confirms that
  one focused session lands all the additions at consistent
  quality. Distributed opportunistic capture leaves capture quality
  variable.
- **Run the audit-then-capture cadence as the standing discipline.**
  Spirit 1353 names this; this pass demonstrates the shape. The
  recent-work audit identifies the IN-SPIRIT-ONLY backlog; one
  migration session closes it; the next audit confirms.
- **Watch for inline-anchor-shaped migrations.** M9 (Spirit 1327
  inline anchor) is the cheapest migration shape — a single
  sentence in an existing paragraph. The audit ranked it 9th but
  it took 60 seconds. Future passes should batch inline-anchor
  edits together; they cost almost nothing each and add up to
  substantial findability.

## Files affected (full paths)

- `/home/li/primary/skills/component-triad.md` — M1, M3, M4, M5
  (4 additions, +130 lines)
- `/home/li/primary/skills/architectural-truth-tests.md` — M2, M9
  (2 additions, +58 lines)
- `/home/li/primary/skills/architecture-editor.md` — M6
  (1 addition, +45 lines)
- `/home/li/primary/skills/designer.md` — M7, M8
  (2 additions, +60 lines)
- `/home/li/primary/skills/operator.md` — M8
  (1 addition, +24 lines)

Total: 9 migrations, 5 files, 5 commits, +315 / -2 lines.

## See also

- `reports/system-designer/51-recent-work-audit-2026-06-02/1-fresh-
  intent-since-1339.md` §"Recommendations" — source of the 8 of 9
  recommendations (R1-R8 — M5 was added by the orchestrator
  synthesis at 5-overview.md).
- `reports/system-designer/51-recent-work-audit-2026-06-02/5-
  overview.md` §"T2.1 Workspace skill capture pass" — synthesis
  that named all nine and the rationale for landing them in one
  pass.
- `skills/spirit-cli.md` §"Operations on the ordinary channel" —
  the query shape used for each record body read.
- `skills/skill-editor.md` — the skill-edit discipline this pass
  followed.
- `ESSENCE.md` §"Backward compatibility is not a constraint" —
  related Principle that M6 (Spirit 1339) explicitly cross-
  references.
