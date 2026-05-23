# 306 — Intent manifestation sweep round 2 — 2026-05-23

*Kind: Synthesis · Topic: round-2 intent manifestation pass · 2026-05-23*

Designer subagent dispatched in parallel with the prime designer's
ongoing `/305-v2` (signal-namespacing rewrite per intent 326).
Manifests Spirit records 311-326 that landed AFTER subagent A
(`reports/designer/303`), subagent B (`reports/designer/304`), and
second-designer's parallel `/159`, `/160`, `/161` work. Subtracts
prime designer's in-flight `/305-v2` substance (records 314-318
verb-namespacing, 323 next-design-focus, 326 PER-COMPONENT
correction). Subtracts second-designer/161/5's manifestation slate
(records 211/288/289/290/292/293/299/300/302/303/305/306/307/308/310).

Net new substance manifested: 8 records (311, 312, 313, 319, 320,
321, 322, 325) across 5 workspace/ARCH files; 4 beads filed
(3 P1, 1 P2) covering audit-surfaced gaps and one P1 lojix scope
expansion.

## §1 Frame

Spirit holds records 1-326 as of this sweep. Round-2 scope window
is **records 311-326** (this session's net-new layer), with three
record clusters explicitly subtracted:

- **Prime designer's `/305-v2`** owns intents 314-318 (signal
  namespacing — 64-bit header bit layout, partition, SignalCore
  primitives), 323 (next-design focus on 64-bit small-object
  signal type), and 326 (PER-COMPONENT correction to /305-v1).
  This sweep does NOT touch those records or any related ARCH
  surface.
- **Second-designer's `/161/5`** manifested intents 211, 288, 289,
  290, 292, 293, 299, 300, 302, 303, 305, 306, 307, 308, 310 — all
  AFTER subagent A's pass. Their slate is settled (jj changes
  `kxruxrzs`, `opyoyqlt`, `mxruwqsm`). Sweep skips re-manifestation.
- **Subagent A's `/303`** manifested intents 247, 254, 255, 256,
  229, 259, 263. Subagent B's `/304` audit catalogued classification
  through record 277 with one (c) bead filed as `primary-8r1j`.

That leaves the round-2 window of records 311-322 + 324 + 325 (the
non-namespacing records of the post-310 layer) as the actionable
surface for this sweep. Eight of those records carried decided
substance suitable for manifestation without further psyche turn:

- **311** cloud Mutate/Query channel split
- **312** content-addressable per-domain authority
- **313** third stable branch deferred
- **319** ARCA cascade migration discipline
- **320** atomic real-time engine upgrades
- **321** domain-criome runtime excludes provider APIs/CLI store
- **322** domain-criome runtime work uses separate worktree
- **325** cloud plan preparation on owner signal

Record 324 (lojix-daemon GitHub auth) has its full design at
`reports/system-designer/32`; the manifestation here is a P1
operator bead (no ARCH-manifest yet — design is in flight, the
crate doesn't exist).

## §2 Per-intent manifestation log

| Record | Title | Target file | Edit summary |
|---|---|---|---|
| 311 | Cloud Mutate/Query channel split | `signal-cloud/ARCHITECTURE.md` §"Public Operations" + new §"Ordinary vs owner split" | Removed `Plan(DesiredState)` from public ops; added the workspace generalization (component reflecting external state exposes read on ordinary + mutation on owner); cited intents 311 + 325 |
| 311 + 325 | Plan moves to owner contract as PreparePlan | `owner-signal-cloud/ARCHITECTURE.md` §"Public Operations" + new §"Ordinary vs owner split" | Added `PreparePlan(PlanPreparation)` to public ops; new §"Ordinary vs owner split" naming the same generalization |
| 312, 321, 322 | Domain-criome per-domain authority + runtime constraints | `domain-criome/ARCHITECTURE.md` new §§"Content-addressed per-domain authority" + "Runtime hard constraints" | Added the TLD-delegation model (each .criome domain = own authority server; cached delegation per domain); excluded provider APIs and direct CLI store access; runtime feature work uses separate worktree |
| 313 | Optional third stable branch deferred | `INTENT.md` new §"Optional third 'stable' branch is deferred" | Documented carry-the-deferral with the two preconditions named (architecture-discovery cascades to all components; each component bootstraps from own architecture discovery) |
| 319 | ARCA cascade migration discipline | `arca/ARCHITECTURE.md` new §"Cascade migration discipline" placed between Invariants and Cross-cutting context | Named: migration target is the redb index (blobs are content-addressed-immutable); cascade flows along SCHEMA_DEPENDENCIES; composes with persona §1.6.7 continuous-runtime invariant; cited /23/4 design report |
| 320 | Atomic real-time engine upgrades | `persona/ARCHITECTURE.md` §1.6.7 (extended) | Added explicit citation of record 320; named Design D FD-handoff as the lossless substrate, continuous-runtime as the discipline flowing down to ARCA cascade work + per-consumer quarantine semantics |

Total: 5 distinct ARCH files + 1 workspace file (INTENT.md) =
6 substantive edits manifesting 8 intent records.

## §3 Beads filed

| Bead | Title | Scope | Parent / deps |
|---|---|---|---|
| `primary-kbmi.4` | cloud: move Plan from signal-cloud ordinary to owner-signal-cloud as PreparePlan | Mechanical contract refactor: 1 variant moves; tests/runtime.rs reroutes Plan through owner client; Plan type stays in signal-cloud as shared public type | Parent: `primary-kbmi` (cloud + domain-criome runtime daemons); cites Spirit 311 + 325 |
| `primary-kbmi.2.1` | domain-criome: add NotAuthoritative(Delegation) reply for off-daemon Resolve | Per intent 312: NotAuthoritative(Delegation) variant + AuthorityEndpoint field; widen Record enum beyond Vec<Address>; add RegisterAuthority owner op | Parent: `primary-kbmi.2` (domain-criome runtime); cites Spirit 312 + audit /23/5 §2 |
| `primary-srmq` | lojix-daemon: authenticated Nix flake resolution via nix-auth crate | New nix-auth Rust crate (SecretBackend trait + GopassBackend + NixAuthEnvironment + Auth facade); lojix-daemon integration at NixInvocationActor slot; gopass-based GitHub PAT injection via NIX_CONFIG access-tokens | No parent (standalone P1); cites Spirit 324, design report system-designer/32, coordinates with system-designer/28 Gap 5 + /31 Open Question 7.2 |
| `primary-0xn7` | arca-daemon: add schema_header redb table + read-on-boot | Foundation slice for the ARCA cascade discipline manifested in arca ARCH this sweep: schema_header redb row + boot-time version check + refuse-to-serve on mismatch | No parent (foundation slice from /23/0 §4.1); cites Spirit 319 + arca ARCH update |

All four beads carry the originating Spirit record number in their
body per `skills/beads.md` discipline. The first three close
audit-surfaced gaps from `reports/third-designer/23-*` and
`reports/system-designer/32`; the fourth is a foundation slice
that was on the "can start now" pile but unfiled.

## §4 Skipped (with reason)

| Record | Title | Reason for skipping |
|---|---|---|
| 314 | 64-bit signal root-level macro header | **Prime designer's `/305-v2`** in flight |
| 315 | Signal namespace partition (system + component zones) | **Prime designer's `/305-v2`** in flight |
| 316 | SignalCore as workspace data table of universal basic types | **Prime designer's `/305-v2`** in flight |
| 317 | Criome identity as SignalCore primitive | **Prime designer's `/305-v2`** in flight |
| 318 | Sub-ID as SignalCore primitive | **Prime designer's `/305-v2`** in flight |
| 323 | Next design work focuses on 64-bit small-object signal type | **Prime designer's `/305-v2`** is that next design work |
| 326 | The 64-bit signal root-verb namespace is PER-COMPONENT | **Prime designer's `/305-v2`** is rewriting per this correction |
| 324 | lojix-daemon authenticated flake resolution | ARCH-manifest deferred; nix-auth crate doesn't exist yet. Substance lives in design report `reports/system-designer/32`; operator bead `primary-srmq` filed this sweep. ARCH-manifest happens when nix-auth + lojix integration land (then moves to `nix-auth/ARCHITECTURE.md` + `lojix/ARCHITECTURE.md`). |

## §5 Cross-cutting observations

### §5.1 The cloud-domain-criome runtime carries a clean operator-feedback loop

Three artefacts from the same session braid together cleanly: the
system-specialist's birth design (`reports/system-specialist/160`)
landed 6 contract+runtime repos; third-designer's `/22` and `/23`
audited them against the new intent layer (311, 312, 283); the
operator's first runtime slice (`primary-kbmi.1` + `primary-kbmi.2`)
was caught by `/23/5` with two architecture-shape violations
(Plan-on-ordinary, Resolve-without-delegation). This sweep
manifested both intents into ARCH and filed the corrective beads
(`primary-kbmi.4` for Plan, `primary-kbmi.2.1` for Delegation).

The intent → ARCH manifestation → audit → bead → operator loop
ran in ~6 hours within one psyche session — a strong proof-point
for the ESSENCE engine ("intent and design — the engine's dance").
Worth carrying forward to the prime designer's next session-status
report.

### §5.2 ARCA + Persona compose into the continuous-runtime substrate

Intents 319 (ARCA cascade) + 320 (atomic engine upgrade) name two
halves of the same invariant: **the workspace is a continuous
runtime; format changes flow through the cascade without
interrupting service**. Both manifestations in this sweep
explicitly cross-reference each other (`arca/ARCHITECTURE.md`
§"Cascade migration discipline" cites `persona/ARCHITECTURE.md`
§1.6.7; persona §1.6.7 now cites arca's cascade discipline). The
substrate has a name now even if the implementation slate (e.g.,
the new arca schema_header bead `primary-0xn7` + the Migration
trait beads from /23/4) is still operator-side work.

The third leg — per-consumer **quarantine on Migration failure** —
is named in both manifestations as the steady-state failure mode
(persona keeps the failing consumer on its old version
indefinitely while the rest of the fleet moves). This is a
Decision, not a transient: continuous-runtime invariant beats
fleet-uniformity. Worth surfacing in the next prime-designer
status report as a load-bearing position the workspace has
adopted.

### §5.3 The "external state mirrored as daemon-internal" pattern

Intent 311's generalization — "a component whose state surface is
a reflected external resource exposes read on ordinary + mutation
on owner" — is now manifested in both `signal-cloud/ARCHITECTURE.md`
and `owner-signal-cloud/ARCHITECTURE.md`. The pattern is broader
than cloud; it applies to any component that reflects external
state (provider APIs, OS facts, network state, etc.). The
manifestation explicitly notes "this is a workspace
generalization", so future components reflecting external state
inherit the discipline without re-deriving it.

Worth a follow-up: a sentence in `skills/component-triad.md`
naming the pattern alongside the existing ordinary-vs-owner
discussion. Not done this sweep (scope discipline — that's
better picked up by the next manifestation pass once the cloud
implementation lands and the pattern proves out).

### §5.4 What this sweep did not touch

- **Prime designer's `/305-v2`**: the entire signal-namespacing
  cluster (records 314-318, 323, 326) is the prime designer's
  active work; this sweep stayed clear per the dispatch contract.
- **Operator implementation work**: `primary-kbmi.4` and
  `primary-kbmi.2.1` are filed but not implemented; that's the
  operator pickup phase.
- **`skills/component-triad.md`** generalization of intent 311's
  external-state-mirror pattern: noted in §5.3 as a follow-up
  rather than landing this sweep.
- **The PreparePlan / Plan / PlanPreparation type naming**: the
  ARCH manifestation says "PreparePlan(PlanPreparation)" — the
  operator may pick a different field name when implementing; the
  ARCH text uses the suggested-shape vocabulary per discipline.

## §6 See also

Within this directory:
- `reports/designer/303-intent-manifestation-sweep-2026-05-23.md` —
  subagent A's round-1 manifestation (records 247/254/255/256/229/259/263)
- `reports/designer/304-unimplemented-intent-audit-2026-05-23.md` —
  subagent B's audit through record 277 + the `primary-8r1j` (Help) bead
- `reports/designer/305-nota-user-guide-and-codec-architecture/` —
  prime designer's NOTA user-guide work (parallel; non-overlapping)
- prime designer's `/305-v2` (in flight) — signal namespacing rewrite
  per record 326 (DO NOT TOUCH)

Sibling directories' parallel work:
- `reports/second-designer/161-design-cascade-and-context-sweep/5-intent-manifestation-gap-audit.md`
  — manifested records 211/288/289/290/292/293/299/300/302/303/305/306/307/308/310
- `reports/third-designer/23-architecture-update-2026-05-23/` —
  designed records 311-320 with bead-shape lists; this sweep manifested
  the ARCH consequences and filed two of the §4.2 beads
- `reports/third-designer/23-architecture-update-2026-05-23/5-audit-of-operator-runtime-slices.md`
  — caught the two R1/R2 violations this sweep's beads close
- `reports/system-designer/32-design-lojix-authenticated-flake-resolution.md`
  — design for record 324; this sweep filed the operator bead

Files edited this sweep:
- `/git/github.com/LiGoldragon/signal-cloud/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/owner-signal-cloud/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/domain-criome/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/arca/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md`
- `/home/li/primary/INTENT.md`

Spirit records this sweep manifests:
- 311 (cloud, Decision, Maximum, 2026-05-23)
- 312 (domain, Decision, Maximum, 2026-05-23)
- 313 (version-control, Decision, Maximum, 2026-05-23)
- 319 (component-shape, Principle, Maximum, 2026-05-23)
- 320 (workspace, Decision, Maximum, 2026-05-23)
- 321 (domain-criome, Constraint, Maximum, 2026-05-23)
- 322 (domain-criome, Constraint, Maximum, 2026-05-23)
- 325 (cloud, Decision, Maximum, 2026-05-23)

Beads filed this sweep:
- `primary-kbmi.4` P1 task (cloud Plan-to-owner per intent 311 + 325)
- `primary-kbmi.2.1` P1 task (domain-criome NotAuthoritative per intent 312)
- `primary-srmq` P1 feature (lojix-daemon authenticated flake resolution per intent 324)
- `primary-0xn7` P2 task (arca schema_header foundation per intent 319)
