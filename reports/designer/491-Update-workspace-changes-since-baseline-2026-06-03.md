---
title: 491 — Workspace update report (since baseline 2026-05-20)
role: designer
variant: Update
date: 2026-06-03
topics: [workspace-update, change-survey, context-maintenance]
description: |
  First workspace update report in the recurring series established
  by Spirit 1530. Baseline picked: 2026-05-20, the two-week window
  covering the engine mechanism ratification, the trace mechanism
  becoming a typed schema-defined interface, the production-orientation
  shift, the 487 meta-report and its three new design directions, the
  YAML front matter migration, and the privacy thread reaching the
  Magnitude-axis decision. Surveys 115 skill-touching commits, ~70
  Spirit captures (records 1326 through 1532), reports across six
  active lanes, and component motion across spirit-next, schema-next,
  schema-rust-next, triad-runtime, persona-spirit, and signal-persona-
  spirit. Names what shifted and what's queued for the next period.
---

# 491 — Workspace update report (since baseline 2026-05-20)

## Baseline and period

This is the inaugural workspace update report. No prior Update report
exists, so the baseline is picked rather than inherited from a
predecessor. The chosen baseline is **2026-05-20**, two weeks back from
today's date.

The rationale: two weeks is long enough to show the shape of motion,
short enough to be tractable in a single read. The window opens just
before the second-designer lane consolidation on 2026-05-22, captures
the rust-method-only override landing on 2026-05-26, runs through the
production-orientation directive at the start of June, and closes on
today's intensive 487-488-489-490 cycle. The next Update report will
take this report's commit as its baseline.

Volume in the period: 115 commits touching `skills/`, 47 reports
landed in `reports/designer/`, ~70 Spirit captures (records 1326
through 1532), substantial code motion across roughly eight component
repositories, and four new lanes registered (`assistant`,
`counselor`, plus `cloud-designer` and `system-designer` continuing
work).

## Headlines

### The triad engine mechanism gets ratified, then sub-ratified four times over

The single most load-bearing shift of the period is the engine
mechanism substrate. Designer 482 (Psyche report 1, since retired
after migration) proposed *NexusWork* / *NexusAction* as the
asymmetric pair driving every component's runner loop. The psyche
ratified it as workspace-canonical: *"Psyche ratifies designer 482
(psyche report 1) substrate as workspace-canonical engine mechanism.
The firm parts — NexusWork/NexusAction asymmetric pair + 5-variant
action set (ReplyToSignal CommandSemaWrite CommandSemaRead
CommandEffect Continue); macro-generated runner loop (triad_main!
emitted from schema-rust-next); effects per-component declared in
schema with Stash as first universal candidate; Continue as in-process
immediate recursion; cross-component invocation via Signal contracts
not Nexus-internal access; inner runtime engine deferred as
future-direction per Spirit 1483; actor traits deferred as
future-direction."* (Spirit 1486, Decision Maximum).

Four sub-substrates followed and each landed in `skills/component-triad.md`:

- **Lifecycle hooks** on the engine traits: *"Generated Signal, Nexus,
  and SEMA engine traits should carry minimal lifecycle hooks: on_start
  and on_stop with typed start and stop failure results."* (Spirit
  1487, Decision High).
- **Schema carries the mechanism**: *"Schema source carries the triad
  engine mechanism as the baseline so schema authors get the runner
  shape, trace plumbing, and continuation substrate through
  generation."* (Spirit 1488, Decision High).
- **Nexus inner-engine deferred**: backpressure, runtime control,
  actor prioritization — all named, all explicitly pushed to
  future-deeper-runtime work (Spirit 1465 + 1483 + 1484).
- **Hidden-non-actor-owner anti-pattern** extended to schema-emitted
  engine traits — engine traits live on real data-bearing types, never
  on ZST namespaces or helper-no-state structs (`skills/actor-systems.md`,
  per Spirit 1487).

The substrate is the load-bearing direction for every component going
forward. Schema-rust-next has already started emitting upgrade
migrations and the Nexus work/action traits (commit `540d572`); spirit-
next now runs the recursive Nexus on a work-action schema (`53e752a`).

### Tracing becomes a typed schema-defined interface

The trace mechanism crossed a substantial threshold in the period.
Tracing was previously a hand-written event enum sprinkled around
spirit-next; the recent corpus reframes it as *"its own schema-defined
interface with closed generated enum vocabularies for trace names and
events, not an ad hoc string log"* (Spirit 1492, Decision Maximum) and
*"Tracing remains typed data until the client display boundary; trace
events and trace logs use generated interface data types, and string
rendering happens only when a client or user-interface surface prints
them"* (Spirit 1490, Principle Maximum).

The reference stack is now spirit-next + triad-runtime + schema-rust-
next: schema-rust-next emits trace hooks on the engine traits and
per-plane trace object names; triad-runtime adds a shared trace runtime
and a generic client display surface; spirit-next consumes both and
renders trace events as NOTA at the client edge. The trace identity
is the canonical SymbolPath (per Spirit 1506), so trace headers, help
identifiers, and config keys all share one machine-readable namespace.

The `eprintln` fallback in the daemon trace path was named as a
violation of the typed-data-strings-only-at-display rule and removed:
*"There is no daemon-side printline. There shouldn't be."* (Spirit
1509, Constraint Maximum). Operator caught this during the cleanup
that crossed the 488 boundary.

### The production-orientation directive shifts the workspace forward

The workspace direction shifted explicitly toward production at the
end of May: *"Workspace direction shifts toward production now —
components actually interacting (schema + persona + spirit + introspect
+ possibly more) rather than single-component pilots. Production-
orientation goals — get components talking; schema-daemon drives
upgrades; persona is the supervisor engine that keeps all components
running; extract maximum code from per-component into schema-macro
emission + a shared runtime library that holds generic SEMA/Nexus/
Signal runtime infrastructure; identify and answer the important
decisions that gate production. The AI/agents need to see what happens
when this runs together — design alone is insufficient; production-
scale interaction is the next validation layer."* (Spirit 1482,
Decision Maximum).

The 484 production-readiness meta-report
(`reports/designer/484-Audit-production-readiness-meta-2026-06-02/`)
ran five parallel sub-agents across schema, persona, spirit, shared
runtime, and deployment. Eight ratifications landed and five operator
slices were named as the first production proof. Sub-agent E surfaced
the deployment chain gap (wrong-target flake input) that
system-designer 53 then audited end-to-end.

### The 487 meta-report and three new design directions

`reports/designer/487-Design-trace-help-config-context-meta-2026-06-03/`
opened with the morning's STT capture (Spirit 1489-1496) and dispatched
four parallel sub-agents:

- Sub-agent A — trace mechanism + daemon string-boundary audit.
- Sub-agent B — Help / description namespace design.
- Sub-agent C — typed NOTA config-by-convention design.
- Sub-agent D — context and intent maintenance sweep.

The overview synthesised the four verdicts plus Spirit 1499-1501,
ratified 11 decisions, and named an 8-step operator slice sequence
plus 5 skill migrations. The three new design directions surfaced are:

- **Help / description namespace** — *"Help and documentation should
  be schema data in a mirror description namespace over the global
  symbol namespace, with generated defaults when no explicit
  description entry exists for a fully qualified symbol."* (Spirit
  1493, Principle High). Every root enum gets a Help variant
  automatically per Spirit 1396.
- **NOTA config-by-convention** — *"Authored workspace data files
  should prefer typed NOTA data: predictable file names and
  directories define the expected root type, usually a struct or
  sometimes a top-level enum selection or vector of records."*
  (Spirit 1494, Principle High).
- **Trace-client library** — *"A trace-client library lives in the
  repo and owns the display plus SEMA-log features. The CLI becomes
  a thin wrapper that enables and calls the library features rather
  than reimplementing trace listener and decoder logic per component."*
  (Spirit 1501, Decision High). The Path B leaning landed at Spirit
  1511, but the conservative-discipline correction at Spirit 1516
  later marked it as *lean-pending-context* rather than ratified —
  one of the most important Corrections of the period.

### The discipline-edit pass: YAML front matter, bracket-quote citations, narrative voice

A cluster of reporting-discipline shifts arrived in the final 24 hours
of the period:

- **YAML front matter for reports** — *"Reports use standard YAML
  front matter for metadata, not the semicolon-bracket pseudo-NOTA
  shape … YAML front matter plugs into standard markdown UI tooling
  (previewers, GitHub rendering, Obsidian, editor frontmatter
  parsers); valid markdown so renderers display reports cleanly; is
  the conventional metadata-on-markdown standard."* (Spirit 1527,
  Decision High). The Correction at Spirit 1528 named the prior
  pseudo-NOTA header shape as drift, not ratified discipline.
- **Bracket-quote citation form** — *"Reference intent records in
  prose markdown by quoting the description summary literally as
  bracketed text — the bracketed form IS the citation — not by the
  record number alone."* (Spirit 1522, Principle Maximum; reinforced
  at 1526). This report itself uses the shape throughout.
- **Psyche-variant code-shown discipline** — *"Psyche reports must
  show actual code, not summarize as line counts or vague references."*
  (Spirit 1515, Principle Maximum). The 488 rewrite added §3a / §4a /
  §5a code excerpts to demonstrate.
- **Narrative-voice psyche reports** — *"Psyche reports talk to a
  human being in a narrative voice — not citation-heavy. Numeric
  Spirit record IDs should be used to mark RANGES when highlighting
  a relevant span of intent, not as constant inline citations on every
  claim."* (Spirit 1521, Principle High).
- **Lean-vs-ratification correction** — *"A psyche statement that
  leans toward a choice while explicitly asking for more information
  is NOT a ratification."* (Spirit 1516, Correction Maximum).
- **Update variant** — Spirit 1530 establishes this report's category.
- **Plain-language open items** — *"Open-work and psyche reports must
  explain opaque unresolved items in plain terms."* (Spirit 1524,
  Correction High).

The 489 audit found 47 reports across designer (44) + operator (3)
lanes carrying the pseudo-NOTA header. Batch 1 (skills) and batch 2
(47-report migration) both landed today. The 490 closeout marks the
migration done.

### The privacy thread reaches the Magnitude-axis decision

A long thread on Spirit privacy ran from Spirit 1429 through 1463 in
the period. The thread started with the assistant/counselor lanes
registering and immediately needing a private-information substrate.
The trajectory walked through public/private boolean (rejected) → a
four-tier audience-register enum Open/Personal/Sensitive/Sealed
(considered) → finally settling on Magnitude reuse: *"Spirit privacy
is a Magnitude on the privacy axis — records gain a privacy field
typed Magnitude where Zero means no privacy (open/public) and Maximum
means sealed. This reuses the existing Magnitude vocabulary instead
of introducing a new audience-register enum like
Open/Personal/Sensitive/Sealed."* (Spirit 1463, Decision Maximum,
explicitly supersedes 1457/1458).

The privacy substance is implemented in persona-spirit source
(commits `189c715`, `9fa4b20`) but not yet deployed. The
`skills/privacy.md` skill was rewritten by the counselor lane to set
the privacy-by-default discipline for personal-affairs work; the
`assistant` and `counselor` lanes were registered with private-repo
isolation (Spirit 1431/1432/1442).

### The 47-report YAML front matter migration

The discipline-edit pass triggered a mechanical migration of 47
reports from the pseudo-NOTA header shape to YAML front matter. This
landed as `designer 489 follow-through batch 2: migrate 46 reports to
YAML front matter` (commit `3db0ca85`, +640/-234). The 490 closeout
(`reports/designer/490-Closeout-pseudo-nota-header-migration-2026-06-03.md`)
marks the operation complete.

### Operator's engine-report skill and the leta LSP tooling

Operator landed `skills/engine-report.md` (commit `e1d229af`) and
report 293 on the engine-report tooling situation. The engine-report
discipline is the standardised situation report for components — code
size, schema size, generated Rust size, interfaces, signatures,
graphs. It uses code-introspection and language-server tools (Spirit
1518/1519/1520). Operator report 294 then refreshed the engine
explanation from basics per Spirit 1529 (*"Psyche reports should let
the psyche follow the line of thought all the way back to the
basics"*).

## Intent captures, grouped by topic

The period saw roughly 200 Spirit records land. Grouped by topic
cluster:

**Engine mechanism / triad substrate** (the substrate ratification
and its consequences): records 1326-1338 (engine-trait pipeline,
origin-rolling-identifier protocol, signal triage + reply method
shape, Nexus inner/outer worlds, slim acknowledgements), 1386-1395
(schema-driven architecture, terse Rust, recursive Nexus
computation, schema-defined trace interface), 1437-1439 (Nexus
decision/effect language refinement), 1485-1488 (ratification
batch), 1532 (triad-engine readability principle).

**Trace mechanism** (typed schema-defined interface): records 1370-
1375 (live daemon trace + optional compile-time + CLI display),
1390-1394 (testing-trace as Layer 2 witness, trace built into the
generated engine traits, name-only recording), 1400-1408 (trace
headers from interface header, extended/compact form distinction),
1489-1492 (typed-data-strings-only-at-display, no recursive
trace-tracing), 1497-1503 (trace renders as NOTA at client edge,
trace-client library lives in triad-runtime), 1505 + 1509 + 1512
(no daemon-side printline), 1510 + 1513 + 1514 (per-crate
enablement discipline).

**Help and Help namespace**: 1396 (every root enum gets a Help
variant automatically), 1493 (Help and documentation are schema
data in a mirror description namespace), 1506-1508 (canonical
SymbolPath generalises beyond help).

**NOTA design** (inline enum payload + config-by-convention): 1411
(beauty as design-standard gate), 1466-1468 (inline enum payload
pattern + sugar resolution), 1494 (authored data files prefer typed
NOTA), 1508 (*"NOTA is at heart a hack on the text user interface
… NOTA is a typed language; everything is read as a known type in
data-type-theory terms."*).

**Privacy** (the thread reaching Magnitude reuse): 1429-1436
(personal-affairs Spain + Canadian citizen + solo-consulting
context), 1431-1434 + 1440-1444 + 1451-1453 (privacy roles +
private repos + read-restricted-by-default), 1445-1463 (typed
access classification → Magnitude reuse).

**Reporting discipline**: 1471 (Psyche-report kind established),
1481 (Variant in filename, capitalized), 1504 (context maintenance
is repair, not survey), 1515 + 1516 + 1521 + 1522 + 1524 + 1526 +
1527 + 1528 + 1529 (the discipline-edit batch), 1530 (the Update
variant establishing this report).

**Production orientation + deferred runtime control**: 1482
(production-orientation directive), 1483 + 1484 (defer
backpressure / inner-engine / actor-prioritization), 1469-1470
(runtime-upgradable schema; implement best-of-latest designs from
main HEADs).

**Component triad pipeline + contract repos**: 1422 (Signal-repo
split — Signal interface in contract repo, Nexus/SEMA in daemon
repo; workspace template), 1427-1428 (spirit triad naming gate
resolved: `meta-signal-` prefix workspace-wide rename across 13
repositories).

**Spirit interface ergonomics**: 1472-1474 + 1476 + 1478 + 1480
(simple-to-complex variant ladder; broad atomic topics; shorthand
interfaces for common operations).

**Workspace ops** (other): 1362-1363 (local-AI model curation on
Prometheus), 1372 (last-version package for upgrade testing),
1396 + 1423-1424 (Playwright browser-extension token via gopass),
1450 + 1409 (VSCodium default editor; Playwright vs browser-use),
1518-1520 (engine-report skill), 1525 (Prometheus-only model
downloads), 1531 (STT mishears `psyche` as `SIDEQ`).

## Skill, ESSENCE, and INTENT evolution

### ESSENCE.md

Three new sections landed:

- **"Strings only at the edges; the system is typed"** — the unified
  typed-boundary principle, anchoring Spirit 1490 + 1492 + 1495 all
  Maximum.
- **"NOTA is a typed text user interface"** — Spirit 1508 Maximum,
  the rationale for NOTA-everywhere.
- **"Symbols are paths through the schema namespace"** — Spirit
  1506 Maximum / 1507 High, naming SymbolPath as the workspace's
  canonical machine-readable universal symbol form.

### INTENT.md

New sections in prose-synthesis form:

- **"Authored data files prefer typed NOTA, by path convention"**
  (Spirit 1494).
- **"Tracing is its own typed schema-defined interface"** (Spirit
  1489/1490/1491/1492).
- **"Help and documentation are schema data in a mirror namespace"**
  (Spirit 1493).
- **"NOTA is a typed text user interface"** (Spirit 1508).
- **"Symbols are paths through the schema namespace"** (Spirit 1506
  / 1507) with worked examples — Help, NOTA config, trace identity
  all reuse the canonical SymbolPath.

### skills/

115 skill-touching commits in the period. The highest-traffic skill
files were `skills/component-triad.md`, `skills/reporting.md`,
`skills/intent-log.md`, `skills/nota-design.md`, and
`skills/architectural-truth-tests.md`. New skills:

- **`skills/workspace-update-report.md`** (this report's discipline).
- **`skills/engine-report.md`** (operator-side, per Spirit 1520).
- **`skills/privacy.md`** rewrite by the counselor lane.

Substantive section additions across the existing skills:

- `skills/component-triad.md` — §Lifecycle hooks on engine traits;
  §Nexus mechanism substrate (NexusWork/NexusAction +
  triad_main! macro + Continue recursion + effects per component +
  Signal-contract cross-component invocation); §Two triads
  distinction; §Help-operations source refinement (Spirit 1493);
  §Trace enablement per-crate documentation (Spirit 1510).
- `skills/actor-systems.md` — §Engine traits live on real data-
  bearing types (extends the hidden-non-actor-owner anti-pattern).
- `skills/nota-design.md` — Rule 4: enum payloads are choices,
  structs are products; inline enum payload + header sugar + type-
  table resolution (Spirit 1466/1467/1468).
- `skills/reporting.md` — §Report header (YAML front matter);
  §Psyche reports — show the code; §Decisions in Psyche reports —
  distinguish lean from ratification; §Psyche reports talk to a
  human — narrative voice (Spirit 1515/1516/1521/1527/1528).
- `skills/intent-log.md` — §Citing intent in prose — bracket-
  quote the summary (Spirit 1522/1526); §The pre-capture gate —
  the after-the-task test; §When a working order slips in anyway
  (record removal).
- `skills/architecture-editor.md` — capture Spirit 1339 (retire
  legacy paths when the working interface exists).
- `skills/architectural-truth-tests.md` — testing-trace as Layer 2
  witness for engine-trait usage; schema-emitted engine traits as
  workspace witness surface; pair-rule-sweep.
- `skills/context-maintenance.md` — split into deep patterns +
  Spirit capture sweep step; clarified staleness (recent intent
  prevails); §Cross-lane meta-report directory.
- `skills/beauty.md` — workspace-shape consequences (terseness,
  symmetry, schema-driven self-describing interfaces-first).
- `skills/component-triad.md` (a second cluster) — capture Spirit
  1373 (no NOTA between components, build-config NOTA),
  Spirit 1348 + 1365 + 1388 (instrumentation on engine-trait
  contract, Nexus inner/outer world vocabulary).
- `skills/report-naming.md` — spec variant in BOTH filename and
  front matter (per Spirit 1481).

### AGENTS.md

The period's AGENTS.md additions were anchored earlier (around
2026-05-22 to 2026-05-26) but worth naming as the substrate of
the current behavior:

- **Rust method-only-no-free-functions** hard override (per Spirit
  712 + 882, both Maximum).
- **JJ inline-message rule** (per Spirit 237).
- **Meta-report directory pattern** + per-response report shape
  (per Spirit 231/232).
- **Subagent dispatch is always non-blocking** (per Spirit 539).
- **Forwarded prompts — don't blind-duplicate, do gap-check** (per
  Spirit 538 / 565-567).
- **Privacy hard override**: private-repos closed by default; only
  the owning psyche can authorise access (per Spirit 1440 + 1443 +
  1453).

## Reports landed, retired, in-flight

### `reports/designer/` (the prime designer lane)

**Landed in period (range 443-491, 47 reports)**: 443 design
improvements audit, 444 stack vision, 445 next-stack audit (the
pseudo-NOTA header originator), 446 next-stack porting research,
447 upgrade-as-SEMA design, 448 single-field-wrapper audit, 449
bead-staleness audit, 450 + 451 operator-271 verification, 452
rkyv-enum-wrapping audit, 458 spirit-triad naming gate decision,
463 operator-trace-implementation audit, 465 recent-decision
landscape, 466 triad-engine-honesty meta-directory, 467
name-only trace research, 468 developed interfaces, 469 introspect
component design, 470 psyche-backlog top-6 visual, 472
context-maintenance, 473 spirit algorithm proposals, 474 spirit
topic-discovery feature, 475 contract-repo pipeline meta-directory,
477 Nexus re-agglomeration, 478 inner-Nexus engine recursive runtime
control, 481 schema-daemon upgradable runtime pilot, 484
production-readiness meta-directory (5 sub-agents + overview), 487
trace/help/config/context meta-directory (4 sub-agents + overview),
488 Psyche-487-overview, 489 audit of report headers and skill
hallucinations, 490 pseudo-NOTA header migration closeout.

**Retired in the 487 follow-through** (substance fully migrated to
skills): 476 (Nexus side-channel), 479 (inline enum payload
pattern), 480 (spirit-next best-of-designs pilot), 482 (engine
mechanism fundamental decision — the psyche report 1), 483
(tracing emission completeness), 485 (engine vs actor traits), 486
(schema-carries engine mechanism).

**Retired in the 472 + 461 context-maintenance sweeps**: 415 + 439
context-maintenance ledgers (superseded), 453 + 454 engine-trait
substance (migrated to `skills/component-triad.md`), 459 proof-of-
usage substance (migrated to `skills/architectural-truth-tests.md`),
plus seven reports retired in the 472 sweep itself.

### `reports/operator/`

**Landed in period (range 246-294, ~49 reports)**: schema-nota-spirit
whole-stack tour (248), schema-asSchema self-audit (251), trace
implementation + audit chain (270 to 280), spirit-next testing-trace
implementation (277), Nexus recursive computation + internal control
interface (287/288/289), tracing mechanism audit + polish (291),
client trace genericization (292), engine-report tools situation
(293), Psyche engine-report refresh from basics (294).

### `reports/system-designer/`

Landed: 51 recent-work audit, 52 workspace skill capture pass, 53
spirit-next production parity (4 sub-agents), 54 spirit privacy
classification research, 55 spirit variant-ladder design research
(881 lines; corpus-mined 1399 records), 56 psyche meta-report on
Spirit recent work (privacy thread + variant-ladder + deployment
chain gap).

### `reports/system-operator/`

Landed: ~50 reports including the spirit-topic-depth-query
implementation (177), local-AI toolkit prefetch chain (178-180,
185), Playwright + Ghostty configurations (181), spirit privacy +
shorthand audit (182), engine-report tooling CriomOS-side (183),
psyche-open-work updates (186), Psyche context-maintenance situation
(187).

### `reports/assistant/` + `reports/counselor/`

Brand-new lanes registered in the period: each has 3 reports
covering role registration, private-repos design, and privacy
operations. Most substance now lives in `private-repos/assistant-
reports/` and `private-repos/counselor-reports/` per the privacy
discipline.

### `reports/cloud-designer/`

Reports 11/13/14/15 — backup network review, Pi-local Gemma
execution, Gemma4 multimodal llamacpp design, lane agglomeration
audit. The lane's focus in the period was AI-side work.

### In-flight

- **Vision architecture report** being written in parallel by another
  designer.
- A.3 (trace-client library Path B) still pending psyche ratification
  per Spirit 1511 + 1516 (the lean-pending-context correction).
- The 11 skill cleanups identified in 489 §C.1 — stale citations of
  retired reports, skill-editor rule violations, drift cleanup —
  queued for follow-up.

## Component and repo state

**spirit-next** — the highest-motion repo in the period. Major
landings: testing trace witness (`e4e5035`), live trace socket
testing surface (`5ac8b16`), generated engine trace hooks (`b5ced5c`),
recursive Nexus on work-action schema (`53e752a`), generated engine
lifecycle hooks (`7a08894`), consume triad-runtime trace surface
(`dc8f16d`), render trace client events as NOTA (`e6a3a70`), privacy
as Magnitude (`8fa8b48`), per-plane trace object names (`f8ab848`).
The repo is currently the canonical reference implementation of the
engine mechanism substrate plus the trace mechanism.

**schema-next** — substantial schema refinement: macro library data
mirrors collapsed (`99078b2`), schema macro source entry types
collapsed (`e2a8abf`), strict key/value data for macro artifacts
(`2d7b41f`), legacy declaration compatibility removed (`d8006b6`),
labeled root enum wrappers rejected (`0732a12`), parenthesized enum
payload signatures required (`0201dec`). The repo also gained the
upgradable runtime daemon pilot under designer 481.

**schema-rust-next** — the emitter side now produces trace hooks on
engine traits (`8264f3d`), exact plane routes by variant name
(`a16fbcc`), typed trace identity from interface routes (`fa3f615`),
upgrade migrations + Nexus work-action traits (`540d572`), engine
lifecycle hooks (`a5bf5c9`), NOTA trace display adapter target docs
(`5632836`). The emitter is closely tracking the substrate
ratification.

**triad-runtime** — newly added to `protocols/active-repositories.md`
(commit `965e131b` in primary). Carries the shared trace runtime
(`cfbcca4`), generic trace client display surface (`524da35`),
default silent recording (`b4e494d`). This is the home of the
trace-client library per Spirit 1501.

**persona-spirit** — privacy infrastructure substantially landed in
source but not yet deployed: filter records by privacy magnitude
(`189c715`), verbal recency depth queries (`df09280`), recorded-time
filter (`c5a3eb9`), certainty change (`830747b`), record removal
(`e89e9bd`), description-only spirit-next (`ba1956d`), schema-driven
next substrate docs (`84b7001`). The deployment chain gap (wrong-
target flake input) is the named blocker.

**signal-persona-spirit** — wire-shape symmetry to persona-spirit:
privacy magnitude filtering, verbal recency depths, recorded-time
queries, certainty-change operation, removable certainty state,
topic-set record queries, record removal verb, summary observation
mode, record identifier queries, topic vector validation.

**signal-spirit** — new contract repo scaffolded per Spirit 1422 +
1427 (commit `8a87870` initial scaffold; `061815f` schema runtime
contract).

**nota-codec** — quoted string delimiters rejected (`f761421`),
double-quoted CLI convention documented (`f348d2c`), block strings
for bracket-safe text (`9e855d4`), structural shape helpers expanded
for schema macros (`a7aa75b`).

## Forward look — what's queued for the next period

The next workspace update report's baseline is **this commit**.
Carryover items into that period:

- **A.3 trace-client library Path B** — pending psyche ratification
  per the lean-pending-context correction at Spirit 1516. The §3a
  code in `reports/designer/488-Psyche-487-overview-context-and-
  decisions-2026-06-03.md` IS the more-context the psyche asked
  for. Ratification fires when the psyche engages with the §3a
  block.
- **8 other open decisions** named in the system-designer 56 psyche
  meta-report on Spirit recent work — privacy thread deployment,
  variant-ladder shape selection from corpus mining, deployment
  chain target redirection, cross-lane convergence questions.
- **11 skill cleanups** from the 489 audit §C.1 — stale citations
  of retired reports, skill-editor rule violations, drift cleanup,
  the four remaining drift findings, the two flagged possible
  drifts.
- **Vision architecture report** being written in parallel today;
  will land in the next period.
- **Update Spirit field for privacy magnitude in the deployed
  daemon** — currently the privacy code is implemented in source but
  not deployed because the flake input is pointed at the wrong
  target. system-designer 53 named this.
- **Help / description namespace implementation** in schema-rust-
  next — Spirit 1493 + 1396 named it; no code yet.
- **NOTA config-by-convention implementation** — Spirit 1494 named
  it; the 487.3 sub-agent C report carries the demo.
- **Spirit shorthand interface** — Spirit 1472 + 1476 + 1477 named
  it; not yet specified.
- **Spirit variant-ladder selection** from the system-designer 55
  research's 7 surfaced questions.
- **The deferred-future runtime stack** — Spirit 1483 + 1484 names
  backpressure, inner-Nexus engine, actor scheduling/prioritization
  as future-deeper-runtime. Production-orientation focuses on the
  substrate and the spirit-next + introspect first pair; these
  resume when overload evidence appears.

The next Update report fires when the psyche requests one, when the
next extended busy period closes, or before a context-loss event.
The chain starts here.
