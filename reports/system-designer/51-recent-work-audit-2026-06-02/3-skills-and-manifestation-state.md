# Skills and workspace-manifestation state — system-designer audit 3

## Frame

This audit covers the state of workspace-level manifestation surfaces —
`skills/*`, `AGENTS.md`, `INTENT.md`, `ESSENCE.md` — against recent
intent and design work (window 2026-05-26 → 2026-06-02). Focus
dimensions:

1. What landed in skills in the last 7 days?
2. Per-skill detailed state on the surfaces called out by the brief.
3. Orphan-chain `ukxxvstt + xrtmsqtp` analysis — content, rebase-as-is or
   revise?
4. Workspace-wide intent (Spirit 1327) propagation status across the
   AGENTS / INTENT / ESSENCE / skill stack.
5. Capture-to-architecture lag patterns visible in the Spirit landscape.

Read-only audit. Per `AGENTS.md` rule, no `---` horizontal rules below;
all section boundaries via headings.

## Recent skill landings (2026-05-26 → 2026-06-02)

`git log --since='2026-05-26' --name-status` against
`skills/ AGENTS.md INTENT.md ESSENCE.md`. The substantive landings in
this window, newest first:

| Commit | Date | Surface(s) | What |
|---|---|---|---|
| `a45c395a` | 2026-06-01 | INTENT.md, architectural-truth-tests.md, component-triad.md, designer.md | designer 461 cross-lane migration: proof-of-usage ladder + runtime triad engine traits + sub-agent dispatch shapes |
| `20af8c88` | 2026-06-01 | architectural-truth-tests.md, testing.md | operator: no-positive-grep-as-deployment-proof (1340-1341) |
| `3fd66cdd` | 2026-06-01 | designer.md, rust/methods.md | designer 461 pre-cursor: typestate-vs-borrow-rule retirement (rust/methods.md §"Typestate retires when borrow rules enforce its invariant") + designer.md worked-instances section |
| `8964c0b3` | 2026-06-01 | spirit-cli.md | system-operator: spirit verbal depth queries (1338) |
| `9d985bf9` | 2026-06-01 | architectural-truth-tests.md | designer: next-stack audit + porting research + upgrade-as-sema + wrapper-audit |
| `7716b855` | 2026-06-01 | mermaid.md | operator: macro library nota types |
| `52d38380` | 2026-05-31 | INTENT.md, mermaid.md | operator: strict schema syntax closure |
| `9cf5995c` | 2026-05-31 | operator.md | operator: require async subagent workflow |
| `e8958562` | 2026-05-31 | INTENT.md | operator: programmable nota schema stack |
| `d130776a` | 2026-05-30 | designer.md, nota-design.md, reporting.md | path-as-locator anti-example, audit-precision, hand-codec-vs-derive |
| `180e6f2b` | 2026-05-30 | spirit-cli.md | production spirit recency queries |
| `94b15cf1` | 2026-05-30 | INTENT.md | operator: live asschema implementation |
| `8d562232` | 2026-05-30 | mermaid.md | Mermaid edge label notation trap |
| `26af086d` | 2026-05-29 | AGENTS.md, INTENT.md, nix-discipline.md, secrets.md (new), skills.nota | workspace: context maintenance + skill updates + secrets skill |
| `08bfc6bc` | 2026-05-29 | intent-log.md, intent-maintenance.md | tombstone-before-remove; removal supersedes append-only |
| `f73ca004 / e71b03e1 / be1d98b1 / 01ec3b34 / f8d66bf3` | 2026-05-29 | spirit-cli.md, nix-usage.md | spirit query family: certainty filters, topic-set queries, zero-certainty removal candidates; nix-usage requires pushed github witnesses |
| `d69f3f39 / 657d5693 / 4bc98d26 / 423dea6e` | 2026-05-28 | spirit-cli.md, intent-maintenance.md | spirit query mechanics: record removal, range queries + negation, summary observation surface, record-identifier queries |
| `3a652ae8` | 2026-05-28 | context-maintenance.md | "context maintenance sweep discipline" (NOT the §3a rewrite — that gap remains) |
| `0a028b70` | 2026-05-28 | mermaid.md, reporting.md | Mermaid graph readability |
| `8ec26c8e` | 2026-05-27 | INTENT.md | SEMA as durable database work |
| `e3e6795f / e8202c50` | 2026-05-27 | INTENT.md, architectural-truth-tests.md, testing.md | schema-at-heart test discipline; schema-object witness requirement |
| `eefc0457` | 2026-05-27 | actor-systems.md, rust/methods.md | recurring patterns A-F named at top |
| `ea3733e0` | 2026-05-27 | INTENT.md, actor-systems.md, component-triad.md, rust/methods.md, skills.nota | async mail actor object patterns |
| `25203da5` | 2026-05-27 | INTENT.md, component-triad.md, naming.md | manifest records 951 + 952 (REST wire architecture; schema/Rust mirror naming) |
| `8f57f71f / efe8dc20 / 8a99a2af` | 2026-05-27 | INTENT.md, component-triad.md, enum-contact-points.md, report-naming.md, reporting.md, rust/methods.md | Nexus mail keeper consolidation; three-schema-types triad + signal-protocol mail (963/964/965) |
| `67e0f807` | 2026-05-27 | AGENTS.md, architecture-editor.md, repo-intent.md | continuous manifestation discipline per-repo (record 944) |
| `0c6c9310` | 2026-05-27 | context-maintenance.md | clean lingering assistant terminology per record 920 |
| `e1a5de2a / 293e9269 / 19f48717 / ecb5196e / c7dbf5ee / 4bdc75de` | 2026-05-27 | AGENTS.md, context-maintenance.md, role-lanes.md, mermaid.md, nota-design.md, rust-discipline.md + sub-skills, reporting.md, double-implementation-strategy.md | lane context discipline tightening; Rust discipline tightening (record 882); status banners cleanup |
| `e2504e07` | 2026-05-27 | AGENTS.md, ESSENCE.md, INTENT.md, plus 9 skills | rename system-specialist → system-operator |
| `78bea1e3` | 2026-05-26 | abstractions.md, component-triad.md | /371 signal/executor/SEMA runtime triad + federation framing |

Density: 30+ commits in 7 days touching skills/INTENT.md/AGENTS.md. The
manifestation cadence is strong; the chunky landings (designer 461,
designer-operator engine-trait family, record-882 method discipline,
record-944 continuous-manifestation discipline, record-920 role rename)
are all visible. Two-thirds of commits touch a single file; the
chunkier multi-file commits (designer 461, record 920 rename) match the
psyche-intent migrations they manifest.

## State of specific skills

### `skills/component-triad.md`

Confirmed: the Runtime-triad-engine-traits section is present at
`/home/li/primary/skills/component-triad.md:746-825`. The section
carries:

- Three-engine table at lines 759-763 with **SignalEngine = 2 methods**
  (`triage` + `reply`), **NexusEngine = 1 method** (`execute`),
  **SemaEngine = 2 methods** (`apply` + `observe`). Method counts
  match the brief's expectation.
- Interface-direction mermaid at lines 765-777 — 5 nodes (Signal,
  Nexus, Sema, Wire, plus the Wire arrow). Stays under the §"Graphs
  are short" budget.
- Origin-route invariant named at line 793-799 — "Origin identifier
  protocol (Spirit 1336)" plus the "preserved across all six plane
  envelope hops" line citing Spirit 1329.
- Pipeline-shape section at lines 784-791 (Spirit 1335 cited).
- Spirit-record citations: 1326, 1327, 1330, 1331, 1332, 1333, 1334,
  1335, 1336 — all the records 1330-1336 the brief named. Plus 1329
  for the six-hop preservation property. Not cited: 1337 (Nexus
  signal-message-embedding brainstorm — that's a Clarification still
  too early for skill landing).
- The "What this pattern is — and is not" sub-section (lines
  801-817) explicitly closes "not a fourth-plane substrate"; rules
  out "validation engine," "queue engine," "audit engine" trait
  proliferation. Good guardrail.

The section's worked example (lines 819-824) cites `spirit-next` and
its ARCHITECTURE.md §"Runtime triad"; per the schema-arc audit
(sibling sub-agent), the live landing as of 2026-06-01 is
`spirit-next` at commit `d29dc6c` (Spirit 1357). component-triad.md
does not cite the commit ID inline; the worked-example line just
points at the repo. That's appropriate for a skill (skills don't
chase commits); the per-repo ARCHITECTURE.md owns the moving
commit-id witness.

Verdict: this skill is the canonical workspace landing for the
engine-trait pattern. Substance complete and aligned with intent.

### `skills/architectural-truth-tests.md`

Read fully (638 lines). Four major sections constitute the
truth-tests apparatus:

1. **§"No positive grep as deployment proof"** (lines 47-71) — bans
   `grep -R "SemaWriteInput"`-style proofs; permits grep only as
   **negative guards**. Spirit 1340-1341 anchoring.
2. **§"Proof-of-usage ladder — choose cheapest sufficient"** (lines
   73-220) — three-layer model (STATIC → RUNTIME → BEHAVIORAL),
   per-layer witness catalogue with cost/strength, worked examples.
   This is the designer-461 migration from designer reports 459's
   substance. The forbidden case (positive grep) sits explicitly
   below Layer 1.
3. **§"Constraints first"** (lines 222-238) — the
   architecture-constraint → test-name pattern with worked
   constraint→test mapping table.
4. **§"Pair-rule sweeps — valid patterns and adjacent
   anti-patterns"** (lines 281-324) — the rule that every
   positive-and-negative-shape discipline gets BOTH greps in the
   same audit scope.

Plus §"Schema-chain witnesses use schema objects" (lines 345-377),
§"Live boundary witness for vocabulary widening" (lines 379-406),
§"Nix-chained tests — the strongest witness" (lines 408-500),
§"Examples (from the persona messaging stack)" (lines 502-518),
§"Rule of thumb — the test name pattern" (lines 520-545),
§"Actor-density tests" (lines 547-580), §"When to use which witness"
(lines 582-596), §"What this skill is NOT" (lines 598-611), §"See
also" (lines 613-637).

Four truth-tests, in the sense the brief asks:

- **TT-1 Architectural witness > behavior-only test.** Lines 32-45.
- **TT-2 Forbid positive grep as proof.** Lines 47-71. Spirit
  1340-1341.
- **TT-3 Choose cheapest sufficient witness on the proof-of-usage
  ladder.** Lines 73-220. Spirit 1349 (Layer-2-runtime-witness
  principle) substance covered though not explicitly cited.
- **TT-4 Witnesses use schema-emitted objects when the chain is
  schema-derived.** Lines 345-377. Spirit 1345 anchoring (signal-
  nexus-sema trace witnesses).

These line up with current intent. The skill is well-developed and
the proof-of-usage ladder reads as the canonical reference.

One absence worth flagging: §"Live boundary witness for vocabulary
widening" cites a worked example (`fixture.reply_text` against a
StoreFixture) but no Spirit record number anchors the pattern. The
substance is sound; future audit could pin it to a specific record
when one lands.

### `skills/designer.md`

Designer-461 added 68 lines (commit `a45c395a` lines 668-741):

- **§"Worked instances — the pattern in shape"** (lines 671-707) —
  four sub-agent dispatch shapes from the 2026-06-01 session:
  closed-claim verification, falsifiable specs for open claims,
  design-fidelity audit against a commit, remnant retirement
  refactor. Substance is concrete (cites specific repos and the
  240-to-72-line collapse).
- **§"Three-way convergence as correctness signal"** (lines 710-737)
  — convergence-on-isolated-dispatch is evidence; divergence reveals
  hidden judgement calls. Worked example: designer 446 next-stack
  porting meta-report where three sub-agents converged on
  spirit-fold as the right first slice.

Redundancy check: these sit inside the parent §"Designer sub-agents
land code witnesses" (line 607). They are refinements of the
parent's pattern, not duplications. The role-discipline files
(`role-lanes.md`, `AGENTS.md` "Roles") do not cover sub-agent
dispatch shape — that's designer's job. No redundancy with existing
discipline.

Earlier in the session, commit `3fd66cdd` added 64 lines to
designer.md under the same parent section about sub-agent code-
witness dispatch. The chained additions in `3fd66cdd` (commit at
15:19) and `a45c395a` (commit at 16:12) form a coherent expansion;
the second wave (worked-instances + convergence) builds on the
first. Reading the file end-to-end confirms the additions read as
one coherent block, not two stitched-together chunks.

Verdict: designer.md additions are substance-bearing, well-placed,
and not redundant with role-discipline files. The skill's overall
length (884 lines) is getting large — eventually some sub-topics may
warrant their own files — but no concrete split is needed yet.

### `skills/context-maintenance.md` — GAP CONFIRMED

The brief named this as a known gap; verified at
`/home/li/primary/skills/context-maintenance.md:172-191`:

The §3a section currently on main says:

> ### 3a · Design-rationale guard against premature DELETE
>
> A report carrying **competing design alternatives** ... do NOT DELETE
> such a report when its chosen-design substance migrates. Add a
> STATUS-BANNER naming the permanent-doc landing instead ...

Per Spirit 1323 (Correction Maximum, 2026-05-31): "closed reports
should not be kept merely for rationale or history" — STATUS-BANNER
preservation is the superseded shape; "Migrate live patterns first,
then retire" is the new shape. The Spirit record is authoritative;
the skill on main is stale.

The orphan commit `ukxxvstt` (skills: nix build-time compilation
discipline (1322) + apply 1323 to context-maintenance §3a + capture
F8 method-count-per-wire-events clarification) carries the rewrite
(51 insertions / 16 deletions). The rewrite:

- Renames §3a from "Design-rationale guard against premature DELETE"
  to "Migrate live patterns first, then retire".
- Names migration targets for competing-alternatives substance
  (architecture file / Spirit record / git history).
- Explicitly retires the previous STATUS-BANNER pattern, naming the
  failure mode it caused (preserved contradictions, search noise).
- Cites Spirit 1323 inline.

Verdict: ukxxvstt's context-maintenance §3a rewrite is the correct
shape. Recommend rebasing onto main as-is. No conflicts expected
since no other commit has touched §3a's region since the orphan.

### `skills/nix-discipline.md` — GAP CONFIRMED

Read `/home/li/primary/skills/nix-discipline.md` end of §"Build, run,
and deploy from the remote — never a local checkout" at line 237. The
next section is §"Lock-side pinning" at line 239. **No "Compiled
artefacts at build time, never JIT" section exists on main between
those.**

Per Spirit 1322 (Principle High, 2026-05-31): when a Nix derivation
builds a config/script/module for a runtime with JIT or AOT
compilation (Emacs Lisp .eln, Python bytecode, Common Lisp FASLs,
TypeScript .d.ts, sass/SCSS), produce the compiled artefacts AT
BUILD TIME inside the derivation. Don't let them appear lazily at
runtime. The principle: a Nix-built artefact is content-hashed and
store-shipped; runtime JIT caches invalidate on every Nix rebuild,
so build-time compilation eliminates the invisible regression.

Orphan commit `ukxxvstt` carries the addition (45 insertions) at
nix-discipline.md after §"Build, run, and deploy" and before §"Lock-
side pinning". The new section names the worked example
(`CriomOS-home`'s `initElCompiled` derivation),
`modules/home/profiles/med/emacs.nix:678-738`, and includes a smell
test ("if first-use after rebuild is slow, the runtime JIT cache is
doing the work").

Verdict: ukxxvstt's nix-discipline.md addition is the correct shape.
Recommend rebasing onto main as-is. Check whether any subsequent
nix-discipline edit has touched the insertion point — verified by
running `git log --since='2026-06-01 14:00' -- skills/nix-discipline.md`:
zero commits since the orphan was authored. Clean rebase.

### `skills/intent-maintenance.md` — GAP CONFIRMED

The brief calls out orphan `xrtmsqtp` claiming to migrate
"tombstone-discipline" to this skill (~13 lines). Verified at
`/home/li/primary/skills/intent-maintenance.md:93-98`:

On main:

> Paste the result into a tombstone appendix (the model is
> `reports/system-designer/45` §"Appendix — full text of removed
> records"); the report then IS the provenance of what was removed.
> The 1157–1175 loss (`reports/system-designer/46`) happened precisely
> because records were removed without this step; report 45's 19
> survive because they were tombstoned first.

The reference to `reports/system-designer/45` is now problematic
since `xrtmsqtp` retires that report (`reports/system-designer/45`
is among the files xrtmsqtp deletes). The orphan's rewrite at the
same location:

> Paste the result into a tombstone appendix in the removing agent's
> report; the report then IS the provenance of what was removed.
> The discipline emerged from a known loss: an undocumented removal
> of records 1157–1175 (no tombstone) proved unrecoverable because
> redb's copy-on-write page reuse overwrote the freed bytes within
> hours; an earlier removal of 19 psyche-approved records that WAS
> tombstoned first preserved their full text. Capture first, then
> remove.

The migration is essential — without it, intent-maintenance.md cites
a deleted report. The new shape inlines the principle (no report
reference); the discipline survives the retirement.

Verdict: xrtmsqtp's intent-maintenance.md migration is correct and
urgent (current main has a dangling reference). Recommend rebasing
as-is. The skill file region is otherwise unmodified since the
orphan; clean rebase.

### `skills/rust/storage-and-wire.md` — GAP CONFIRMED

Verified at `/home/li/primary/skills/rust/storage-and-wire.md:277-280`.
The bulleted list ends with:

- No silent backward compatibility.
- Version-skew guard.
- Treat schema changes as coordinated upgrades.

The orphan `xrtmsqtp` adds a fourth bullet immediately after:

- **Enum variant evolution: append at the end, express semantic order
  separately.** Discriminant-stability rule: new variants append LAST
  under `#[repr(u8)]`. Semantic ordering via manual `Ord` /
  `order_rank` impl, never via `#[derive(Ord)]` on declaration order.
  Worked example: `Magnitude::Zero` appended after `Maximum` to keep
  `Minimum=0..Maximum=6` stable; manual `order_rank` returns `Zero=0`
  for semantic-bottom. Cites Spirit record 1249 and `sema`
  ARCHITECTURE §"Schema evolution".

This is load-bearing rkyv discipline for any persisted enum. Without
it, an agent introducing a new variant at top-of-enum for "semantic
order" silently shifts every persisted byte by one. Per Spirit 1249
this discipline emerged from real workspace experience (the Magnitude
widening).

Verdict: xrtmsqtp's storage-and-wire.md addition is correct and the
gap is real. Recommend rebasing as-is. Clean rebase (no other commit
has touched that bullet list since the orphan).

## Orphan-chain analysis — `ukxxvstt + xrtmsqtp`

Confirmed via `jj log -r 'main..ukxxvstt' --no-graph`:

- Orphan tip: `ukxxvstt` (commit `23c9b21`, 2026-06-01 16:00 UTC).
- Orphan parent: `xrtmsqtp` (commit `a6c041a`, 2026-06-01 15:52 UTC).
- Neither is reachable from main.
- `jj log -r 'ukxxvstt..main' --no-graph` returns 17+ commits — main
  has moved forward considerably since the orphan was authored.

### `xrtmsqtp` — system-designer retire-and-migrate

Files touched (17, mostly deletions):

- 15 report-file deletions across `reports/system-designer/`
  (`34-mvp-and-sandbox-audit/*`, `43-spirit-signal-surface-168-review.md`,
  `48-intent-removal-implementation-audit-and-consolidation-2026-05-29.md`,
  `49-recent-context-schema-arc-and-spirit-search-2026-05-30.md`,
  `50-cross-lane-context-maintenance-2026-05-30/*`) — total 4579
  lines deleted.
- 2 skill files modified:
  - `skills/intent-maintenance.md` — 13-line rewrite at lines 93-98
    (described above).
  - `skills/rust/storage-and-wire.md` — 17-line addition at line 280
    (described above).
- Net: 24 insertions / 4579 deletions.

Risk on rebase as-is: low. Main has not deleted any of the 15
reports the orphan would delete (verified by listing
`reports/system-designer/` — `34-mvp-and-sandbox-audit/`, `43-…`,
`48-…`, `49-…`, `50-cross-lane-context-maintenance-2026-05-30/` are
all present). Main has not touched the intent-maintenance §93-98
region. Main has not touched the storage-and-wire bullet-list region.

Recommendation: **rebase `xrtmsqtp` onto main as-is.** No revision
needed. The system-designer lane (this lane) owns the retire-and-
migrate authority for system-designer reports per Spirit 1323.

### `ukxxvstt` — skills migration chain

Files touched (2):

- `skills/context-maintenance.md` — §3a rewrite (51 insertions / 16
  deletions; described above).
- `skills/nix-discipline.md` — new §"Compiled artefacts at build
  time, never JIT" section (45 insertions; described above).
- Net: 80 insertions / 16 deletions.

The commit description mentions "F8 method-count-per-wire-events
clarification" — that's Spirit 1361 capture work that the orphan
chain authored. Verified via Spirit query: 1361 is in the store
(`engine-trait method-count wire-events signal-nexus-sema`
Clarification). The capture is preserved by Spirit; only the skill
migrations are the unlanded part of ukxxvstt.

Risk on rebase as-is: low. context-maintenance.md has not been
touched since 2026-05-28 (`3a652ae8` for sweep discipline elsewhere
in the file; not §3a). nix-discipline.md has not been touched since
2026-05-29 (`26af086d` for the context-maintenance sweep batch).
Clean insertion points.

Recommendation: **rebase `ukxxvstt` onto main as-is.** No revision
needed. The migrations are correct and the rebase target is clean.

### Chain integrity

`ukxxvstt`'s parent is `xrtmsqtp`. Rebasing the chain preserves
`xrtmsqtp` first (retire-and-migrate batch), `ukxxvstt` second
(skills migration). The two commits are logically independent of
each other but were authored sequentially in one session. Rebasing
either alone is safe; rebasing both as the chain is the cleanest
shape since it preserves the authorship intent.

### Authority

System-designer lane (this lane) owns the migrations. xrtmsqtp's
report deletions are within system-designer scope (all 15 deleted
files are under `reports/system-designer/`). ukxxvstt's skill
edits are workspace-wide; per Spirit 921+ the system-designer lane
manifests workspace-wide structural shape, so this is in-lane.

Operator lane will execute the rebase per the designer/operator
boundary (`AGENTS.md` §"Hard overrides", record 515). The
recommended operator handoff: cherry-pick or rebase
`xrtmsqtp → ukxxvstt` onto main; verify no merge conflicts; push.

## Workspace-wide intent (Spirit 1327) propagation status

Spirit 1327 (Principle Maximum, 2026-06-01): "every component triad
defines Signal/Nexus/SEMA in schema; runtime is composition of
schema-emitted trait impls". Workspace-wide scope.

Propagation per surface:

### `INTENT.md` — YES, manifested

`/home/li/primary/INTENT.md:553-585` carries Pattern B "Three
execution centers (Signal + Nexus + SEMA)" with explicit anchor
records: "371 (Executor → Nexus per 964), 964, 970, 981, 982,
**1326, 1327, 1330-1336**". Lines 569-584 explicitly call out 1327
Principle Maximum workspace-wide and name the three engine traits
(`SignalEngine`, `NexusEngine`, `SemaEngine`) with their methods and
borrow rules. Worked example cited: spirit-next at `d29dc6c`.

### `skills/component-triad.md` — YES, manifested

`/home/li/primary/skills/component-triad.md:746-825` carries the
canonical landing. Confirmed above. The skill is the workspace's
canonical reference for the engine-trait pattern.

### `AGENTS.md` — NOT explicitly manifested

`/home/li/primary/AGENTS.md` does not cite Spirit 1327. The
"Component triad means daemon + working signal + policy signal"
hard override (lines 176-184) names the triad repository shape
(daemon + signal-* + owner-signal-*) but not the runtime engine
trait shape. The §"Where to look for more" pointer to INTENT.md
covers it indirectly.

Recommendation: **acceptable absence**. AGENTS.md is the compact
every-keystroke contract; record-882 (no free functions) is named
explicitly because every Rust authoring moment touches it.
Engine-trait pattern is referenced through component-triad.md and
INTENT.md is one read away. Adding a hard override for 1327 would
inflate AGENTS.md without proportional discipline payoff. Keep as
is; reconsider if agents start hand-writing engine bodies without
reading component-triad.md.

### `ESSENCE.md` — NOT manifested, appropriate

ESSENCE.md is the "gold of the gold" — only the most universal
psyche intent at maximum certainty stated with force. Engine traits
are workspace-wide architecture; they don't rise to the essence bar.
The §"Intent is the cornerstone" + §"Intent and design — the
engine's dance" + workspace-essence framing is what ESSENCE carries.

Recommendation: no change. The 1327 propagation correctly lives one
layer below ESSENCE in INTENT.md and skills/component-triad.md.

### `skills/rust/methods.md` and `skills/abstractions.md` — partial

methods.md cites the schema-emitted-traits pattern via §"Methods on
types, not free functions" + §"Schema-generated objects are the
method surface" (per INTENT.md line 597-598 pointer). The shape:
"behaviour lives as a method on the schema-emitted noun" — the
Rust-side complement of 1327. Not explicitly Spirit-1327-anchored
but the discipline is consistent.

abstractions.md: cited from `AGENTS.md` line 211 ("verb belongs to
noun"). Carries the noun-discipline that 1327 enforces at the
trait-method level.

Recommendation: no change needed. The Rust-side surfaces are
upstream of 1327 (they enforce the method-on-noun discipline; 1327
applies it to engine traits). The cross-references work.

### Where else might 1327 need to land?

Two candidates worth tracking:

1. **Per-repo `ARCHITECTURE.md` files** in triad-component repos
   (`sema`, `sema-engine`, `nexus`, the persona-* triads). Per
   `AGENTS.md` lines 22-29 (record 944 continuous manifestation),
   per-repo ARCHITECTURE.md should reflect 1327 as each repo adopts
   the engine-trait pattern. The schema-arc sub-agent audit (sibling
   sub-agent 2) will name which per-repo files are caught up.
2. **`skills/architectural-truth-tests.md`** — §"Schema-chain
   witnesses use schema objects" (line 345) already cites the
   schema-emitted-trait surface (`SignalEngine`, `NexusEngine`,
   `SemaEngine`) but does not explicitly anchor to Spirit 1327.
   Adding one inline citation would tighten the
   skill→intent traceability without changing substance.

## Workspace lag patterns — capture-to-architecture gaps

Spirit records since 2026-06-01 went up to 1395+ (queried via
`(Observe (Records ((Any []) None (AtLeast High) (Since (2026-06-01
00:00:00)) DescriptionOnly)))`). 80+ records in the window. Lag
patterns visible:

### Lag-1 — Schema upgrade family (1305-1314) — 7+ days open

Records: 1305 (upgrade-as-sema-operation Principle Maximum), 1306
(upgrade testing daemon Decision), 1307 (nota schema implementation
explanation Constraint), 1308 (upgrade sema schema Decision), 1309
(schema-daemon self-editing editor Decision), 1310 (sema
transitory-database upgrade-runtime Decision), 1311 (upgrade
compilation binary-spawn Constraint), 1312 (nota schema
correspondence goal Principle), 1313 (upgrade schema-edit examples
Clarification), 1314 (self-editing design-now Decision).

This is a coherent Maximum-certainty intent cluster about
**upgrade-as-SEMA-operation** — schema upgrades flow through SEMA
write operations; the daemon self-edits its schema. Eight records,
five Decision-class, two Principle-class, one Constraint-class.

Skills citation status: zero topic-skill landing. Only `component-
triad.md:763` says "Database upgrades flow through SEMA per Spirit
1308" inline in a table cell — that's the lone citation.

Target surface: this needs a **new topic skill or major
component-triad section** — e.g. `skills/sema-upgrade.md` or
component-triad.md §"Sema as the upgrade mechanism". The substance
is large enough (8+ records covering principle, mechanism,
testing, daemon-spawning) to warrant its own discipline file.

Why open: the cluster landed in Spirit on 2026-06-01 morning; the
designer/operator session afterward focused on engine-trait
manifestation (designer 461) which pulled the next 1326-1336
cluster into skills. The upgrade-as-sema cluster has no carrying
designer report yet — the operator-side `next-stack` repos
(`schema-next`, `schema-rust-next`) have working code (per sibling
sub-agent 2) but no design report has surfaced the pattern into a
durable skill landing.

### Lag-2 — Testing-trace + runtime-witness family (1343-1351) — open

Records: 1343 (schema runtime instrumentation testing log-socket
Decision), 1344 (testing cli trace configuration nota Decision),
1345 (signal nexus sema trace witnesses Clarification), 1346
(schema-emitted-objects optional-logging testing-build feature-gate
Decision), 1347 (cli log-socket testing-mode debug-observation
Decision), 1348 (build-config nota-struct testing-build feature-
flags Decision), 1349 (testing-build runtime-witness layer-2 proof-
of-usage Principle), 1350 (engine-self-verification signal-engine
nexus-engine sema-engine testing-build Decision), 1351 (signal-
engine signal-reply sema-identifier acknowledgement-shape
Clarification).

This is the **runtime-witness as Layer-2 proof-of-usage** cluster
that the designer-461 proof-of-usage ladder partially absorbed (Layer
2 witnesses including "Actor trace assertion (recorder actor)" and
"Process-boundary test"). The cluster is partially manifested:
proof-of-usage-ladder substance is in `architectural-truth-tests.md`,
but the **testing-build feature-gate + cli-log-socket + engine-self-
verification mechanics** (1346-1350) are not in any skill.

Target surface: `skills/testing.md` or a new `skills/runtime-witness.md`
extending the proof-of-usage ladder with the Layer-2-via-feature-gate
mechanism. Also possibly `skills/spirit-cli.md` for the cli log-socket
testing-mode (1347).

Why open: same session-pacing reason. The engine-trait family soaked
the designer attention; the runtime-witness substrate (one layer
down from engine-trait) is the next migration wave.

### Lag-3 — Nexus inner/outer-world architectural vocabulary (1388) — fresh, open

Record 1388 (Principle): "nexus inner-world outer-world signal-
boundary sema-boundary architectural-vocabulary". The principle
captures Nexus as the "inner world / outer world" semantic — the
Signal-boundary and SEMA-boundary as the two world-edges Nexus
straddles. This is workspace-wide architectural vocabulary worth
anchoring in `skills/component-triad.md` §"Runtime triad" alongside
the engine-trait substance.

Lag: ~1 day. Not late yet but visible — should land in the next
manifestation wave.

### Lag-4 — Spirit binary-protocol CLI debugging (1373) — open

Record 1373 (Principle): "component-triad binary-protocol cli-nota
debugging". The principle captures that any component-triad CLI is
the debugging surface for the daemon (CLI sends NOTA, daemon replies
NOTA; that's the debugging substrate). This naturally extends
`AGENTS.md` line 176-184 "Component triad means daemon + working
signal + policy signal" or sits in `skills/component-triad.md` §"The
single argument rule" / a new §"Debugging via the CLI".

Target surface: component-triad.md addition.

Lag: ~24 hours.

### Lag-5 — Agent-memory queryable / MCP architecture (1356) — open

Record 1356 (Principle): "agent-memory tool-call-log queryable
mcp-architecture". The principle that agent tool-call logs should be
queryable as memory through an MCP-like architecture. Workspace-wide
implication for how agents introspect their own histories.

Target surface: could land in `skills/context-maintenance.md` as a
forward-looking carry-uncertainty note, or in INTENT.md as an
emerging-pattern note.

Lag: ~24 hours. Lower urgency since it's directional rather than
operational.

### Lag-6 — Schema-rust-next interface-trait + macro family (1386-1398) — fresh

Records: 1386, 1387, 1390, 1391, 1392, 1393, 1394, 1395, 1396, 1397,
1398. Many Decision-class; mostly about schema-rust-next emitting
default trait implementations for actor tracing, generated interfaces
with macros, root-enum help, introspect-via-tracing.

Target surface: per-repo ARCHITECTURE.md (`schema-rust-next`,
`spirit-next`). Some general-pattern substance may eventually rise
to `skills/component-triad.md` or a new `skills/schema-emission.md`.

Lag: <12 hours. Too fresh to call lag yet; the design is still
firming.

### Lag-7 — Worktree-prototype + designer-operator workflow refinement (1352-1355) — open

Records: 1352 (Clarification), 1354 (Clarification), 1355 (Principle
"design-methodology prototype-proving worktree-discipline").

Designer.md and operator.md already have worktree-prototype landing
from earlier sessions (verified via grep). 1355 specifically posits
worktree-prototype as a **design methodology** for proving design.
This may warrant a tighter inline citation in designer.md
§"Designer authority" or §"Working pattern". Not a major migration —
substance is there, the spirit-record anchoring is missing.

Lag: tracking. Lower priority.

### Lag-8 — Context-maintenance §3a (orphan-carried) — known critical gap

Already covered above. Spirit 1323 (Correction Maximum, 2026-05-31)
on main since two days. The orphan chain has the rewrite.

### Lag-9 — nix-discipline JIT (orphan-carried) — known gap

Spirit 1322 (Principle High, 2026-05-31). Orphan-carried. Two days
open.

### Lag-10 — intent-maintenance.md tombstone (orphan-carried) — dangling reference

Two days open. Currently main cites a report (`reports/system-
designer/45`) that the same orphan chain retires; if the orphan's
retirement landed before the orphan's intent-maintenance rewrite, the
reference would dangle. Recommend rebasing the orphan chain as one
unit to avoid partial-state dangling references.

### Pattern summary

Workspace pattern: **a designer report carries the migration but
only one migration per session**, so capture-to-architecture lag
accumulates roughly in proportion to Spirit-record cadence. Recent
cadence: 30+ records/day; manifestation cadence: 1-2 sessions/day
each landing 2-3 records. Net: a backlog of 5-10 records per day
that don't yet have a target migration.

The orphan chain represents a single migration that simply hasn't
been integrated to main. Rebasing it closes 3 of the open gaps
above (Lag-8 §3a, Lag-9 nix JIT, Lag-10 intent-maintenance).

## Recommendations

Concrete small moves, ordered by impact and ease:

### R1 — Operator rebases the orphan chain onto main (HIGH IMPACT, EASY)

Cherry-pick or rebase `xrtmsqtp → ukxxvstt` onto current main.
Verified clean rebase (no conflicts). Closes Lag-8, Lag-9, Lag-10.

Designer / system-designer lane authorises the migration; operator
lane executes per `AGENTS.md` line 381-393 (designer/operator
boundary).

### R2 — Author a `skills/sema-upgrade.md` topic skill (HIGH IMPACT, MEDIUM EFFORT)

The schema-upgrade-as-SEMA-operation family (Lag-1, 8 records) is
the largest open capture-to-architecture gap. Substance is rich
enough to warrant its own skill. Anchoring records: 1305, 1306,
1308, 1309, 1310, 1311, 1312, 1313, 1314. Skill outline:

- The principle (upgrade flows through SEMA write operations).
- The daemon-self-editing mechanism (1309).
- The transitory-database for upgrade runtime (1310).
- Upgrade compilation as binary-spawn (1311).
- Testing-daemon spawning shape (1306).

Owner: designer or system-designer (this lane), depending on
psyche-prioritisation.

### R3 — Extend `skills/component-triad.md` with inner/outer-world vocabulary (LOW EFFORT)

Spirit 1388 — Nexus as inner-world / outer-world Principle. Add a
short sub-section under §"Runtime triad engine traits" or §"Three
schema types, three runtime planes". Adds the vocabulary alongside
the engine-trait substance.

Plus Spirit 1373 — CLI as binary-protocol debugging substrate.
Short addition to §"The single argument rule" or new §"Debugging via
the CLI".

Owner: designer or system-designer.

### R4 — Add Layer-2 runtime-witness mechanics to `architectural-truth-tests.md` or `testing.md` (MEDIUM EFFORT)

Records 1346-1350 are the testing-build feature-gate +
engine-self-verification mechanism — operational shape that
complements the proof-of-usage ladder. Extend the existing ladder
with a "Layer 2 via feature-gated trace recorder" sub-section
naming the build-config + cli-log-socket pattern.

Owner: designer.

### R5 — Verify per-repo ARCHITECTURE.md adoption of engine-trait pattern (system-designer task)

`spirit-next/ARCHITECTURE.md` cited as the worked example. Verify
the other triad-component repos (`sema`, `sema-engine`, `nexus`,
the persona-* triads) have caught up. Per `AGENTS.md` lines 22-29
(record 944 continuous manifestation), this is on-going work.
Sibling sub-agent 2 (schema-arc audit) names the per-repo state.
System-designer drafts the migrations; designer lanes execute.

### R6 — Track the schema-rust-next interface-macro family for an emerging skill (LOW URGENCY)

Records 1386-1398 are too fresh to migrate now (the design is still
firming). Watch the cluster; if it stabilises in the next 3-5 days,
spawn a `skills/schema-rust-emission.md` or extend
`skills/component-triad.md`.

### R7 — Inline Spirit-1327 citation in `architectural-truth-tests.md` (TINY)

Section §"Schema-chain witnesses use schema objects" (line 345)
currently cites the schema-emitted-trait surface without explicit
Spirit 1327 anchoring. Add one inline citation. Low effort, sharpens
intent traceability.

## See also

- `0-frame-and-method.md` — orchestrator frame for this audit
- `1-fresh-intent-since-1339.md` — sibling sub-agent on the recent
  Spirit landscape
- `2-schema-arc-and-engine-triad-state.md` — sibling sub-agent on
  per-repo state in the schema arc
- `4-lane-coordination-and-recent-reports.md` — sibling sub-agent on
  cross-lane convergence and stale-report retirement
- Orphan commit lineage:
  - `xrtmsqtp` (commit `a6c041a`, 2026-06-01 15:52)
  - `ukxxvstt` (commit `23c9b21`, 2026-06-01 16:00)
- Anchoring Spirit records: 1322, 1323, 1327, 1340-1341, 1330-1336.
