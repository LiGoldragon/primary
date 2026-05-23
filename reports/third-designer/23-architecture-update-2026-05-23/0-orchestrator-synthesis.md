# 0 — Orchestrator synthesis: architecture update after 2026-05-23 psyche prompt

*Third-designer's orchestrating report for the parallel design wave
on the 10 new psyche intent records (311-320, this session) plus
system-specialist's freshly-landed cloud + domain-criome triads.
Four subagents produced numbered reports 1-4; this synthesis names
the cross-cutting findings, reconciles a brief-assumption issue
flagged by subagent D, and produces the consolidated operator bead
list the psyche asked for.*

## 0. TL;DR

10 intent records captured (311-320): cloud Mutate/Query channel
split; content-addressable domain authority; stable-branch deferred;
64-bit signal-message header; partitioned namespace (SignalCore +
component zone); SignalCore as basic-types data table; Criome
identity primitive; Sub-ID primitive; ARCA migration cascade;
continuous-runtime atomic upgrade.

System-specialist landed 6 contract+runtime repos for cloud +
domain-criome with passing tests, correctly NOT executing the
unaffirmed meta-signal rename. Four design subagents produced:
audit + revision (subagent A); 64-bit header bit layout +
partitioned namespace (subagent B); SignalCore primitives catalogue
(subagent C); ARCA cascade + atomic upgrade flow (subagent D).

**Three load-bearing design positions:**

1. **Persona binds the stable public socket per component; uses
   `SCM_RIGHTS` to hand accepted FDs to the active daemon version.**
   Selector flip changes only the NEXT accept; in-flight clients
   keep their FDs until close. Lossless + client-transparent (intent
   245) falls out naturally. (Subagent D.)

2. **64-bit message header: 1-bit partition + zone-specific
   allocations.** System zone (P=0): 7-bit Core type + 3-bit variant
   kind + 5-bit sub-discriminator + 48 reserved. Component zone
   (P=1): 16-bit component identifier + 16-bit per-component type +
   3-bit variant kind + 5-bit sub-discriminator + 23 reserved.
   Unit-variant messages = 8 bytes on the wire. Constant-time
   dispatch via bitfield + array lookup. (Subagent B.)

3. **SignalCore is 10 primitives** (Identity, SubId, Magnitude,
   Timestamp, MonotonicOffset, ComponentName, ContractVersion,
   Slot, Revision, plus 2 promotion-candidates Topic/Summary).
   `Identity` = BLS12-381 G1-compressed 32 bytes; existence-verified
   via Criome `Verify(Identity)`. `SubId` = Blake3 of canonicalised
   SubIdSpec; minted by closest daemon to launch; canonical record
   in ARCA. (Subagent C.)

Subagent A audit verdict: system-specialist's 6 landed repos are
clean against foundation discipline. 16 beads decomposed (6
immediate additive, 5 Q4/Q8-gated, 5 peer-subagent-gated).
Subagent D produced 11 ARCA/Persona beads.

## 1. Brief-assumption correction (subagent D's flag)

Subagent D surfaced a meaningful correction: **the brief I sent
referenced `/284` (per-type Migration trait) and `/278` (multi-version
daemon coexistence), but these report numbers don't currently
exist as separate reports.** Their substance lives in:

- **`/285`** — explicitly supersedes `/284`'s framing per its TL;DR.
  The Migration trait spec is here.
- **`/287`** — likely the multi-version daemon coexistence substance
  (subagent D's report cross-refs both).

Also: **PeerCheck is retired per spirit record 196.**
`signal-version-handover` is the sole discovery contract; the
equivalent function lives in Persona's control connection. My
brief's "PeerCheck + CoordinateBack" reference is historical.

Implication for subagents A and B: their reports may carry stale
`/284` / `/278` / PeerCheck references too. Picking-up agents
should re-resolve to `/285` + `/287` + `signal-version-handover`
when reading.

## 2. Cross-cutting design convergences

### 2.1 — Identity-no-op cascade still touches every consumer's schema_header

Subagent D: when a workspace type changes (e.g., Sub-ID encoding
bumps), every consumer's `CONTRACT_VERSION` changes because
cross-schema refs hash by value per `/279` §3d. Even identity-no-op
consumers (whose bytes don't change) must update their
`schema_header` row. Four-line redb header write per consumer.

Implication: the cascade is **mandatory through the hash graph**,
not optional based on whether the consumer's surface changed
visibly. Affects bead sequencing in §4.

### 2.2 — Closest-daemon-to-launch mints Sub-IDs

Subagent C: Sub-IDs are minted by the closest daemon to the launch
event. Parent agent's daemon for LLM calls. Orchestrate for spawned
processes. Persona-listen for STT-extracted spans. This means
**every persona-ecosystem daemon needs to know how to mint Sub-IDs**
— SignalCore primitive is a workspace-wide capability, not a
single-component concern. Composes with the 64-bit header's system-zone
allocation (subagent B): SubId gets a stable system-zone type code.

### 2.3 — Quarantine + partial-fleet steady state

Subagent D: when a per-consumer Migration fails during cascade,
Persona quarantines that one consumer on its old version while
the rest of the fleet moves to the new schema. ARCA is **NOT
rolled back**. The continuous-runtime invariant (record 320) wins
over fleet-uniformity. This is a Decision (acceptable steady
state, not transient).

### 2.4 — TLD-daemon-with-delegation > pure federation-of-equals

Subagent A: the landed `signal-domain-criome` assumes a central
registry. Applied R2's content-addressed authority correctly =
TLD-daemon-with-delegation model (not pure federation-of-equals
from /22's earlier sketch). Each .criome domain's daemon answers
its own resolution; top-level `domain-criome` is the .criome TLD
registry but delegates to per-domain daemons via `NotAuthoritative(Delegation)`
replies carrying `AuthorityEndpoint`. Designer lean recorded;
psyche affirmation requested.

## 3. The four subagent reports — one-line each

- **1-cloud-domain-criome-audit-and-revision.md** — 6 landed repos
  pass foundation hygiene; R1 + R2 land as additive changes. `Plan`
  moves to owner; `NotAuthoritative(Delegation)` adds to ordinary;
  `Delegation` carries `AuthorityEndpoint`; `Record` widens beyond
  `Vec<Address>`. Sub-ID + Criome identity integrate additively
  once 317-318 land. 16-bead list.
- **2-signal-64bit-header-and-partition.md** — 1-bit partition
  selector + zone-specific layouts; 3-bit variant kind = 8 classes;
  unit-variant = 8 bytes on wire. Constant-time dispatch. Macro
  gains `component_identifier` line; registry in signal-frame.
  Layout-version annotation propagates via /279's hash chain.
- **3-signalcore-basic-types-table.md** — 10 primitives in
  SignalCore: Identity (BLS12-381), SubId (Blake3 of SubIdSpec),
  Magnitude (with Unknown), Timestamp (i64 UTC seconds),
  MonotonicOffset, ComponentName, ContractVersion, Slot<T>,
  Revision, + Topic/Summary as promotion candidates. Two surfaces:
  NOTA registry + Rust crate (Nix arch-truth check syncs).
  ExistenceVerdict {Exists/DoesNotExist/Suspended/Pending} via
  Criome `Verify(Identity)` with 30s TTL cache + revocation
  invalidation.
- **4-arca-cascade-and-atomic-upgrade.md** — ARCA stores 4 type
  families (build artefacts, Job specs, user attachments, sub-id
  rolls); migrates redb index only (blobs immutable). sema-upgrade
  orchestrates cascade; Persona owns the swap. `SCM_RIGHTS` FD
  handover preserves in-flight clients. Quarantine on per-consumer
  failure; partial-fleet success is acceptable steady state.
  11-bead list.

## 4. Consolidated operator bead list

The psyche asked for "a final list of beads that you're going to
actually fill for operators to start either testing or implementing
further." This is the consolidated set from subagents A and D plus
implied beads from B and C. Grouped by gate.

### 4.1 — Foundation beads (can start now)

These don't depend on further psyche decisions; they're concrete
follow-up work on already-settled architecture.

| Bead | Title | Owner |
|---|---|---|
| `bead-arca-schema-header` | Add `schema_header` redb table + read-on-boot to arca-daemon | system-specialist or operator |
| `bead-arca-inspect-socket` | Add pre-bind inspect socket to arca-daemon for hash discovery (per /279 §6c) | system-specialist or operator |
| `bead-arca-component-schema` | Author arca's component schema file (per `signal-X-schema.nota` pattern) | system-specialist |
| `bead-persona-stable-public-socket` | Implement Persona's per-component stable public socket + `SCM_RIGHTS` FD handover (Design D from persona/ARCH §1.6.7) | operator |
| `bead-component-identifier-registry` | Author `signal-frame/component-registry.nota` enumerating workspace components with 16-bit IDs | designer (mine or any structural) |
| `bead-arca-typed-store-vocabulary` | Migrate arca's stored types to the four-family discipline (build artefacts, Job specs, attachments, sub-id rolls) | operator |
| `bead-cross-version-failure-tap-dashboard` | persona-introspect operator dashboard surfacing failed cross-version messages | operator-assistant |

### 4.2 — Cloud + domain-criome revision beads (gated on Q1/Q2)

These are subagent A's category (a) — additive revisions to
system-specialist's landed repos. Gated on Q1 (Plan as Mutate or
Query) and Q2 (TLD-daemon-with-delegation or pure federation).

| Bead | Title | Owner |
|---|---|---|
| `bead-cloud-move-plan-to-owner` | Move `Plan(DesiredState)` from signal-cloud to owner-signal-cloud as `PreparePlan(PlanPreparation)` | system-specialist (in-place) |
| `bead-domain-criome-not-authoritative` | Add `Reply::NotAuthoritative(Delegation)` to signal-domain-criome; extend `Delegation` with `AuthorityEndpoint` | system-specialist |
| `bead-domain-criome-typed-record-kinds` | Widen `Record` enum beyond `Vec<Address>` to typed kinds (AAAA, MX, TXT, CAA, redirect, criome-attested-cloud-projection) | system-specialist |
| `bead-domain-criome-register-authority` | Add `RegisterAuthority(AuthorityRegistration)` to owner-signal-domain-criome | system-specialist |
| `bead-cloud-domain-criome-arch-update` | Update both runtime repos' ARCHITECTURE.md to reflect R1 channel split + R2 per-domain authority | system-specialist |
| `bead-cloud-domain-criome-witness-tests` | Add NOTA round-trip + signal-frame envelope tests for the new variants | system-specialist |

### 4.3 — 64-bit header + SignalCore primitive beads (gated on B/C psyche review)

These depend on psyche affirmation of subagent B's bit layout and
subagent C's primitive catalogue.

| Bead | Title | Owner |
|---|---|---|
| `bead-signal-frame-64bit-header` | Implement the 64-bit header in signal-frame (envelope, bit-extract macros, dispatch table generation) | operator |
| `bead-signalcore-crate` | Create signal-core crate with the 10 SignalCore primitives + Rust trait + NOTA registry | operator |
| `bead-criome-identity-existence-verify` | Implement `Verify(Identity)` on criome contract + cached client wrapper (30s TTL) | operator |
| `bead-sub-id-mint-pilot` | Pilot Sub-ID minting in one daemon (persona-spirit, as it's the canonical pilot) | operator |
| `bead-sub-identifier-cross-component-pilot` | Cross-component Sub-ID consumption: persona-spirit mints, persona-mind reads | operator |
| `bead-magnitude-unknown-widening` | Add `Unknown` variant to signal-sema Magnitude (per intent 165 + spirit record bead `primary-gjs5` if not already filed) | operator |

### 4.4 — ARCA cascade + Persona atomic upgrade beads (gated on D psyche review)

Subagent D's beads, distilled.

| Bead | Title | Owner |
|---|---|---|
| `bead-dep-catalogue-derived` | sema-upgrade aggregates each component's `SCHEMA_DEPENDENCIES` into derived dep catalogue | operator |
| `bead-persona-fleet-upgrade-owner-op` | Add `AttemptFleetUpgrade` op to `owner-signal-version-handover` (the Persona-driven fleet swap entry point) | operator |
| `bead-handover-mirror-payload-apply` | Implement Mirror-payload-apply path in version-handover so mirrored messages decode + replay correctly | operator |
| `bead-quarantine-gate-fleet` | Add per-consumer quarantine state to Persona + `owner-signal-version-handover`; partial-fleet success | operator |

### 4.5 — Deferred / parked

| Bead | Title | Reason |
|---|---|---|
| `bead-cloud-watch-subscribe` | Add Watch/Unwatch to signal-cloud (v2) | Gated on Q4 (cloud op split confirms direction) |
| `bead-domain-criome-criome-attestation` | criome-attested-signed resolution | Gated on Q8 (domain-criome v1 dimensions) |
| `bead-domain-criome-trust-graph` | Trust-graph-constrained filtering | Gated on Q8 |
| `bead-meta-signal-rename-phase-0` | Psyche affirmation of meta-signal rename at Maximum | Still Minimum certainty per records 290 + 299 |
| `bead-signal-real-time` | persona-listen + persona-speak + signal-real-time | Parked per intent 166 (designer pivots to /249 gap-closure) |
| `bead-persona-llm-client` | Workspace-native LLM client library | Parked per intent 166 |

## 5. Open questions for psyche (consolidated, prioritized)

Subagents A + B + C + D each surfaced open questions; consolidating
to the high-leverage subset.

### 5.1 — Blocks the revision wave

- **Q1 — Is `Plan` Mutate or Query?** Subagent A designer lean:
  Mutate (mutates daemon's plan store) → move to owner-signal-cloud.
  Affects bead `bead-cloud-move-plan-to-owner`.
- **Q2 — TLD-daemon-with-delegation or pure federation-of-equals
  for domain-criome?** Subagent A lean: TLD-daemon-with-delegation
  (matches intent 312's content-addressed-per-domain). Affects
  `bead-domain-criome-not-authoritative` + `bead-domain-criome-register-authority`.
- **Q3 — Do the §4.2 immediate-additive beads route to system-specialist
  in-place or to operator lanes?** Subagent A's question. The
  6 repos already shipped under system-specialist; in-place
  amendments by them are the cleanest path. But the workspace
  beads pattern says operator implements designer-bridged work.
  Lean: system-specialist for in-place since the repos are theirs.

### 5.2 — Blocks the foundational architecture

- **Q4 — 64-bit header bit layout** (subagent B). 1-bit partition
  + zone-specific allocations is the proposal; provisional sizes
  (16-bit component ID, 16-bit per-component type) generous.
  Affirm or override.
- **Q5 — Component-identifier registry location** (subagent B
  Q1). Lean: `signal-frame/component-registry.nota`. Confirm.
- **Q6 — Reserved-bit layout-version-tag allocation** (subagent
  B Q3). Lean: reserve 4 bits explicitly. Confirm.

### 5.3 — Blocks SignalCore + identity

- **Q7 — SignalCore primitive catalogue** (subagent C). 10 entries
  proposed. Topic + Summary as promotion candidates pending
  second-consumer evidence. Affirm.
- **Q8 — Mixed-enum NOTA shape for SubIdSpec** (subagent A §6.6).
  Defer or land now? Lean: land if the codec already supports mixed
  enums (it does, per intent 21).
- **Q9 — SubId → Identity promotion model** (subagent C). Explicit,
  one-directional, triggered when entity needs to sign. Lean:
  affirm.

### 5.4 — Blocks the cascade + atomic upgrade

- **Q10 — Quarantine-on-failure as steady state** (subagent D
  §7). Persona keeps the failing consumer on old version
  indefinitely (until owner action) while the rest moves. Lean:
  yes — continuous-runtime invariant wins.
- **Q11 — Identity-no-op cascade triggers schema_header write
  even without bytes changing?** (subagent D §6). Designer lean:
  yes — for hash-binding integrity. Confirm.

### 5.5 — Strategic / cross-cutting

- **Q12 — Spirit record 196's PeerCheck retirement** —
  `signal-version-handover` is the canonical post-/285 discovery
  contract. Confirm subagents A and B can update their reports'
  stale references.
- **Q13 — Meta-signal rename at Maximum certainty?** Records 290
  + 299 still Minimum. The 6 landed cloud + domain-criome repos
  use `owner-signal-` correctly. Defer or rename?
- **Q14 — Promotion model for Topic + Summary** (subagent C). These
  are workspace-relevant types but only one consumer today (spirit).
  Promote when a second consumer appears, or now?

## 6. Disposition

The picking-up agent has 23 beads in §4 plus 14 open questions in
§5. Suggested sequencing:

1. **Psyche triage**: Q1, Q2, Q3 (gates the cloud + domain-criome
   revision wave) + Q4, Q5 (gates the 64-bit header). Without
   these, half the bead list waits.
2. **Foundation-bead pickup**: §4.1's 7 beads can start immediately;
   they're foundation work nobody is gated on.
3. **Revision wave**: §4.2's 6 beads (after Q1 + Q2).
4. **Architecture cascade**: §4.3 + §4.4 (after Q4-Q11).
5. **Park §4.5** until the parked design intent 166 lifts.

The synthesis itself retires when Q1-Q5 land and the foundation
beads start moving in the operator queue.

## 7. References

- **Spirit records this turn (311-320)**: cloud Mutate/Query split,
  content-addressed domain authority, stable branch deferred,
  64-bit message header, partitioned namespace, SignalCore basic-
  types data table, Criome identity primitive, Sub-ID primitive,
  ARCA migration cascade, continuous-runtime atomic upgrade.
- **Subagent reports**: `1-cloud-domain-criome-audit-and-revision.md`,
  `2-signal-64bit-header-and-partition.md`,
  `3-signalcore-basic-types-table.md`,
  `4-arca-cascade-and-atomic-upgrade.md` (this directory).
- **System-specialist landed work**:
  `reports/system-specialist/160-cloud-domain-criome-birth-design.md`;
  repos `signal-cloud`, `owner-signal-cloud`, `signal-domain-criome`,
  `owner-signal-domain-criome`, `cloud`, `domain-criome`.
- **Spirit record corrections to source from**: 196 (PeerCheck
  retirement), 285 (Migration trait spec, supersedes /284), 287
  (multi-version daemon coexistence, supersedes /278), 290 + 299
  (meta-signal rename, Minimum certainty).
- **Prior orchestrator synthesis**:
  `reports/third-designer/22-cloud-criome-design-research/0-orchestrator-synthesis.md`.

This synthesis retires when the picking-up agent has triaged
Q1-Q5 and the §4.1 foundation beads start moving.
