# A5 — Intent-refresh proposals (Horizon / Logix rewrite agglomerations)

Read-only cloud-designer sweep. Applies the agglomeration principle
(record 1zd6v86uo9ycvuqnk3k): find clusters of overlapping records —
especially Medium / Cert-Zero / near-duplicate ones — that belong
together and could be fused into a single fresh higher-certainty
record, shrinking how much future agents must read. The fused records
all carry convergent direction from three independent sweeps (A1
Horizon-side, A2 Logix/triad-side, A3 legacy substrate), so the
certainty raise is justified by cross-lane corroboration, not by my
opinion.

IMPORTANT: every proposal below is PROPOSE-ONLY. The spirit Record
calls are copy-pasteable but I do NOT run them — the psyche reviews and
applies. Each proposal also lists the originals to retire under
explicit supersession so the corpus actually shrinks rather than grows.

NOTA reminder followed throughout: bracket forms only, no quotation
marks inside any record text; records are positional (Record then
[topics] then Kind then [text] then Certainty then Privacy).

## How to read each proposal

Each proposal carries: (a) the source-record cluster it replaces;
(b) the fresh record as a spirit Record call; (c) the proposed
certainty + the convergence that justifies it; (d) the originals to
retire under explicit supersession.

## Proposal 1 — Horizon minimalism (fuse the two minimal Principles)

The two Horizon-minimalism Principles are distinct facets (semantic
boundary vs type-count) of one intent: Horizon stays minimal. Both
are High, both crisp, no contradiction — A1 already flagged them as a
keep-both-but-could-be-one-record pair, and A3 shows both are faithful
restatements of 2026-05-20 Maximum Principles in horizon.nota
(horizon.nota:15-20 + :57-62 for what-not-how;
horizon.nota:64-69 for in/out reuse). Fusing collapses two reads into
one and lets the legacy lineage retire cleanly.

### (a) Source cluster
- 7ggswqdxqqz97za6o7w (Principle, High) — express WHAT not HOW;
  complexity stays out of Horizon, Nix composes the facts.
- 10v4744869xt5spwnam (Principle, High) — no parallel in/out types;
  reuse the input type as the output type.

### (b) Proposed fresh record
spirit "(Record ([horizon cluster-data nix-composition what-not-how input-output-reuse minimal] Principle [Horizon and its cluster-data are minimal on two axes that reinforce one intent. First, at the semantic boundary: Horizon expresses only WHAT the psyche as cluster user wants the cluster to do — simple typed facts — never HOW and never decision-making; Nix consumes those facts and composes them into the more complex decisions, so all composition and decision-complexity stays downstream in Nix and out of Horizon. Second, at the type-count level: Horizon data types do not repeat across inputs and outputs — where the input type can also serve as the output type, reuse it rather than defining parallel in and out types. Fewer, reused types keep the model small. This is the upstream design principle for the Horizon rewrite: minimal at the boundary AND minimal in the type count.] VeryHigh Zero))"

### (c) Certainty + convergence
Propose VeryHigh (raise from High). Justified: the same direction
arrives from three independent places — the two session High records,
the Maximum-certainty legacy Principles in horizon.nota that they
restate, and the horizon-rs/horizon-leaner-shape/INTENT.md sections
(Beautiful horizon over beautiful Nix; No input/output type
duplication) that already synthesise both verbatim. Triple corroboration
across session + legacy + per-repo INTENT raises certainty above the
component records.

### (d) Retire under supersession
7ggswqdxqqz97za6o7w and 10v4744869xt5spwnam, both marked superseded by
the fused record. The legacy horizon.nota lines stay as file history
(not Spirit), unchanged.

## Proposal 2 — Horizon/Logix split + cutover goal (the rewrite charter)

The three records that define the rewrite's shape and goal are tightly
coupled and always read together: the split (Horizon stays simple
projection, Logix gets the triad), the cutover goal (retire dual
stacks), and the immediate-port directive. A1 and A2 both treat
1bok2 + 75auhtr + 6pmein as the rewrite charter, and A2 notes 1bok2
itself names the supersession of the open trichotomy. Fusing gives one
charter record. Note: 1bok2 already RESOLVED 1vymk533 — see Proposal 3
for the trichotomy retirement, kept separate because 1vymk533 carries
a surviving mechanical nugget.

### (a) Source cluster
- 1bok2bxvu3beswif9mv (Clarification, High) — Horizon = simple
  projection hack-for-now; Logix = full triad-engine + schema-based
  component port.
- 75auhtr308tgt4kaa9a (Decision, High) — finish to cutover, retire
  dual production / next deploy stacks.
- 6pmeinb6tqtdotsgi4u (Decision, High) — port high-confidence
  production CriomOS changes into the next stack immediately, then test.

### (b) Proposed fresh record
spirit "(Record ([horizon lojix rewrite cutover retire-dual-stack runtime-shape triad-port charter] Decision [The Horizon and Logix rewrite charter. Horizon is a hack for now and that is acceptable — it stays the simple projection surface, NOT a full triad component; Logix, the lojix component, is the more traditional component that receives the full triad-engine and schema-based-component port. Horizon leans pure-and-simple projection; Logix carries the runtime triad. The goal is to finish the lean rewrite to the point of cutover and retire the dual deploy stacks — the standing burden of maintaining Stack A production and Stack B next in parallel should end; the rewrite is prioritized to reach parity then switch over. Along the way, port high-confidence production CriomOS changes into the next Lojix and Horizon stack immediately where the correct change is clear, then test those builds.] VeryHigh Zero))"

### (c) Certainty + convergence
Propose VeryHigh (raise from High). Justified: A1, A2, and A3 all
independently identify these three as the inseparable rewrite charter;
A3 shows the cutover posture is also grounded in deploy.nota:50-55
(per-node not flag-day cutover) and codified in
protocols/active-repositories.md. The split half (1bok2) is the newer
resolution of a long-open question (cloud-operator/11 finding #7 and
system-operator/167 Next-Best-Step #2 both asked it) — a resolution
that closes prior uncertainty earns a certainty bump.

### (d) Retire under supersession
1bok2bxvu3beswif9mv, 75auhtr308tgt4kaa9a, 6pmeinb6tqtdotsgi4u — all
superseded by the fused charter record.

## Proposal 3 — Retire the open Horizon-trichotomy (clean supersession, no fuse)

This is a clean single-record retirement, not a fuse. 1vymk533
(Medium) framed Horizon's runtime shape as an open trichotomy
(signal-only / triad / pure-library). 1bok2 (and the charter in
Proposal 2) closes it: Horizon = pure-and-simple projection. Both A1
and A2 flag 1vymk533 as already-superseded-but-not-yet-marked. The one
surviving nugget — a pure-projection Horizon needs a types-only-module
schema shape (the report-39 finding that a 4-position document forces a
signal plane) — is a mechanical design constraint worth carrying
forward, so I propose lifting it into a small fresh record rather than
losing it on retirement.

### (a) Source cluster
- 1vymk533gmb43v78e46 (Clarification, Medium) — the open trichotomy
  (now closed) PLUS the types-only-module nugget (still live).

### (b) Proposed fresh record (carries only the surviving nugget)
spirit "(Record ([horizon schema types-only-module projection-surface pure-library] Clarification [A pure-projection Horizon — settled as the runtime shape by the rewrite charter — needs the types-only-module schema shape. The report-39 finding is that a 4-position schema document forces a signal plane; a Horizon that is a pure projection library with no runtime triad therefore needs a types-only-module schema variant so the datatypes generate without forcing an Input/Output signal plane onto Horizon. This is the surviving mechanical constraint from the now-closed Horizon-runtime-shape trichotomy.] High Zero))"

### (c) Certainty + convergence
Propose High for the surviving-nugget record (raise from the original
Medium). Justified: the trichotomy is dead, but the types-only-module
constraint is a concrete mechanical requirement that follows directly
and necessarily from the now-High charter decision (Horizon = pure
projection). A constraint that is entailed by a High decision inherits
High. The Medium original conflated a now-resolved open question with a
durable mechanical finding; splitting them lets the open part retire
and the durable part stand at proper certainty.

### (d) Retire under supersession
1vymk533gmb43v78e46 — superseded; its trichotomy framing is dead
(closed by the Proposal-2 charter), its mechanical nugget re-captured
above at High.

## Proposal 4 — Prototype discipline (fuse the prototype-must-be-real trio)

The three prototype-discipline records all express one theme: a
rewrite prototype must be real, complete, and shown working — not
prose, not bypassed shims. A1 explicitly flags 3zue + 5wo8 as
near-duplicates in spirit and proposes the trio could agglomerate.
ifcmomo is the weak member — A1 and A2 both read it as a one-time
handoff working order (operator inspects the frame before deciding),
closer to a working order than durable intent. I propose fusing the
two durable Constraints and DROPPING ifcmomo as a completed working
order rather than folding it in.

### (a) Source cluster
- 3zue95xkt8gzui12cao (Constraint, High) — Horizon pure-schema work
  shown through a working end-to-end prototype (imports, assembled
  schema, generated data types), not design prose.
- 5wo8xmt0qpl6u6t10md (Constraint, High) — prototype audits must use
  the designed components fully; develop an incomplete component rather
  than bypass it.
- ifcmomoobjs4f3vaw7 (Constraint, High) — one-time handoff: operator
  inspects the system-designer Horizon schema-pipeline frame before
  converging. (Working-order smell — propose retire, do not fold in.)

### (b) Proposed fresh record (fuses the two durable Constraints)
spirit "(Record ([horizon lojix criomos prototype working-pipeline use-components-fully discipline] Constraint [Prototype discipline for the CriomOS, Lojix, and Horizon rewrite. A prototype must be shown through a working end-to-end pipeline — imports, assembled schema, generated data types, tests exercising schema-emitted values — not through design prose. And a prototype must use the designed components FULLY: when a designed component is too incomplete to use, the prototype work develops that component further rather than bypassing it with a hand-written shim. Proof is by working artifact that drives the real components, never by description.] High Zero))"

### (c) Certainty + convergence
Propose High (hold, not raise). Justified: both source Constraints are
already High and crisp; the fuse is about read-count reduction, not new
conviction. A2 corroborates the same discipline applies to the
Spirit/cloud pilots (schema-at-the-heart, no hand-written shims, tests
exercise schema-emitted values), so the principle is workspace-wide —
but I do not raise to VeryHigh because the fuse adds no new
independent source beyond restating the two Highs plus the cloud-pilot
echo.

### (d) Retire under supersession
3zue95xkt8gzui12cao and 5wo8xmt0qpl6u6t10md — superseded by the fused
record. ifcmomoobjs4f3vaw7 — retire as a completed one-time working
order (NOT folded into the fuse; the handoff it ordered has occurred,
so it no longer guides — the working-orders-are-not-intent test).

## Proposal 5 — Triad plane-schema shape (fuse the four-angle plane-shape cluster + the Cert-Zero record)

Four records assert the SAME plane-schema-files-inside-the-daemon-crate
shape from different angles. A2 explicitly flags this: 2bgatqufm9m0dktxkv5
prints at Cert Zero (likely an unset default capture) but is
corroborated by three higher-certainty records, so the shape is settled
despite the lone Zero. Fusing collapses four reads into one and
eliminates the dangling Cert-Zero record, which would otherwise mislead
a future agent skimming certainties.

### (a) Source cluster
- 7joz3dmegqiptqgra5p (Correction, VeryHigh) — each plane has its own
  schema file inside the daemon crate; plane schemas are not separate
  crates.
- 1up1ufia24c2opn3mqn (Decision, High) — daemon owns nexus.schema +
  sema.schema as separate files inside the daemon crate, each importing
  wire-contract Signal IO; planes are not separate crates/repos.
- 2auv4uvj4cr71iy2emj (Correction, High) — triad is not one daemon
  schema with Signal/Nexus/SEMA sections; at least three separate plane
  schemas; contract stays wire-only; all-in-one Spirit pilot is a
  bootstrap exception.
- 2bgatqufm9m0dktxkv5 (Correction, Cert Zero) — each plane its own
  schema; component = 3 schemas min; generator emits per plane.

### (b) Proposed fresh record
spirit "(Record ([schema component-triad daemon plane-schema component-shape contract-daemon-split] Correction [The schema-derived component triad is NOT one daemon schema file with Signal, Nexus, and SEMA sections. A component is at least three separate plane schema files. The Signal wire contract lives in the contract repos and stays wire-only. The Nexus and SEMA plane schemas are separate schema files INSIDE the component daemon crate — for example cloud/schema/nexus.schema and cloud/schema/sema.schema — each declaring its own imports, exports, input, output, and namespace, and each importing the wire-contract Signal IO. Plane schemas are NOT separate crates and NOT separate repos; per-plane crate split is not the triad shape. The daemon runtime composition imports and connects the separate plane schemas rather than embedding Nexus and SEMA sections inside the contract or inside a single all-in-one daemon schema. The current all-in-one Spirit pilot is a named bootstrap exception and must not be treated as the canonical split shape.] VeryHigh Zero))"

### (c) Certainty + convergence
Propose VeryHigh (the level of the strongest source, 7joz3dme).
Justified: four records from four angles converge on the identical
shape, and the workspace-wide r59l2td3o6pvq9vhl3 (VeryHigh) corroborates
the schema-emitted-traits foundation. The lone Cert-Zero member is the
strongest argument FOR agglomeration — folding it into a VeryHigh fused
record removes a misleading low-certainty artifact while losing none of
its substance (its per-plane-generator detail is preserved in the fused
text).

### (d) Retire under supersession
7joz3dmegqiptqgra5p, 1up1ufia24c2opn3mqn, 2auv4uvj4cr71iy2emj,
2bgatqufm9m0dktxkv5 — all superseded by the fused plane-shape record.

## Proposal 6 — Schema actor base-enum principle (fuse the near-identical duplicate pair)

A2 flags z2b9f2 and 4yhbegi02 as near-duplicate Principles, same
substance, no conflict. Confirmed by reading both: they state the
identical idea (schema base enums define the reaction/action types an
actor receives and emits; execution matches variants to select replies
and route work) in slightly different words. This is the cleanest
duplicate in the corpus — a one-to-one merge.

### (a) Source cluster
- z2b9f2nekb560v67ga (Principle, High) — schema base enums define
  actor reaction/action types; execution matches variants to select
  replies + route work.
- 4yhbegi02q5q97a2qcl (Principle, High) — schema creates base
  input/output enums for actor reaction types; execution matches
  variants to choose reply + state action.

### (b) Proposed fresh record
spirit "(Record ([schema actor execution base-enum reaction-action] Principle [Schema-created base input and output enums define the reaction and action types an actor can receive and emit. Execution logic matches those schema-created variants to select the right reply and route the work or state action. The schema defines the actor IO vocabulary; the handwritten execution is the match over schema variants.] High Zero))"

### (c) Certainty + convergence
Propose High (hold). Justified: both originals are already High and
say the same thing — this is pure de-duplication, no new conviction to
raise. Holding at High is the honest level; a duplicate-merge should
not inflate certainty.

### (d) Retire under supersession
z2b9f2nekb560v67ga and 4yhbegi02q5q97a2qcl — both superseded by the
fused principle.

## Proposal 7 — meta-signal rename (fold the stale owner-signal holdout)

A2 flags 3i3hed0a6790r2clvo3 (Medium — owner-signal stays active until
rename lands) as superseded by three High rename records: the rename is
now active work, not tentative. The three High records overlap heavily
(3lchri = rename is active work + deep pass; 2hstvjvbx = fleet rename
all 13 repos; 1n5b0k32 = policy repos use meta-signal prefix, owner is
stale). Fusing the three actives into one fleet-rename record and
retiring the stale Medium holdout collapses four reads into one and
removes the contradicting Medium that says the opposite of the Highs.

### (a) Source cluster
- 3lchri1gcxm3mc7ltm3 (Decision, High) — owner-signal to meta-signal
  rename is active work; deep rename pass across guidance + contract
  repos.
- 2hstvjvbxb8z0tp0xsp (Decision, High) — fleet rename all 13
  owner-signal-* repos to meta-signal-*; uniform standard; future
  components born meta-signal-.
- 1n5b0k32jjw75rhgkb6 (Correction, High) — policy signal repos use the
  meta-signal- prefix; owner- is stale.
- 3i3hed0a6790r2clvo3 (Clarification, Medium) — owner-signal remains
  active naming until rename lands. (Contradicts the Highs — retire,
  do not fold.)

### (b) Proposed fresh record (fuses the three actives)
spirit "(Record ([component-triad naming meta-signal owner-signal fleet-rename policy-contract] Decision [The owner-signal to meta-signal rename is active work, not tentative. The workspace policy-contract naming standard is meta-signal-<component> uniformly; the owner-signal- prefix is stale. Run a deep rename pass that audits and updates the workspace guidance and the affected contract repositories. As a fleet operation, all existing owner-signal-* contract repos rename to meta-signal-* — the 13 affected repos: owner-signal-agent owner-signal-cloud owner-signal-domain-criome owner-signal-mind owner-signal-orchestrate owner-signal-persona owner-signal-persona-spirit owner-signal-repository-ledger owner-signal-router owner-signal-sema-upgrade owner-signal-terminal owner-signal-upgrade owner-signal-version-handover. Future components are born meta-signal- from inception. For the Logix rewrite specifically: the policy contract must be born meta-signal-lojix, never owner-signal-lojix.] High Zero))"

### (c) Certainty + convergence
Propose High (hold at the level of the three active sources).
Justified: the three actives are already High and convergent; this is
read-count reduction plus removal of a contradicting Medium. I do not
raise to VeryHigh because no new independent source corroborates beyond
the three already-High records. The Logix-specific clause is added
because A2 found meta-signal-lojix is not yet captured at all — folding
the rename intent down to the named component is a useful concretion.

### (d) Retire under supersession
3lchri1gcxm3mc7ltm3, 2hstvjvbxb8z0tp0xsp, 1n5b0k32jjw75rhgkb6 —
superseded by the fused fleet-rename record. 3i3hed0a6790r2clvo3 —
retire as stale/contradicted (it asserts owner-signal stays active,
which the three Highs reverse); do NOT fold its substance in.

## Cross-proposal notes

### Records I deliberately did NOT agglomerate
- The triad-runner / engine-mechanism cluster (5pcw3e6, 75ccxoaj,
  1mttcjcn, 4ffjo8wt) reads as overlapping but each carries a DISTINCT
  decision (extract the runner; carry the engine mechanism in schema
  source as baseline; ratify report 482 as direction; minimal
  lifecycle hooks only). They reinforce but do not duplicate — fusing
  would lose granularity. Left as-is.
- The contract-wire-only cluster (4b5gisiz, 394s6ikh, 5vy3adk1,
  6jh9823) each fixes a different wire-boundary error (no engine traits
  in contract; signal repo carries only wire schema; six Sema words
  forbidden on the wire; no NOTA between components). Distinct
  corrections, not duplicates. Left as-is.
- 431pfi7l1akuu22b01b (typed-source-first anti-pattern correction)
  stands alone — it is the single sharpest record in the Horizon corpus
  and the live driver behind the cutover. Not a fuse candidate.

### The agglomeration arithmetic
The seven proposals replace 21 source records (6 fuses consuming 2+3+1+2+4+2+3, plus 2 clean retirements of working-order / contradicting-Medium records: ifcmomo and 3i3hed0) with 7 fresh records — a net reduction from roughly 21 reads to 7, while raising certainty on three of them (Proposals 1, 2, 5 to VeryHigh; Proposal 3 nugget Medium to High) and removing one Cert-Zero artifact (2bgatquf) and one contradicting Medium (3i3hed0) that would otherwise mislead a certainty-skimming agent.

### Apply order suggestion (for the psyche, if accepted)
Capture the seven fresh records first, then issue the supersession /
retirement on the originals — so the corpus is never momentarily
missing the intent. Proposals 1, 2, 3 are the highest-value (the
Horizon charter agents read first); 5 and 7 remove the misleading
low-certainty / contradicting artifacts; 4 and 6 are pure read-count
hygiene.
