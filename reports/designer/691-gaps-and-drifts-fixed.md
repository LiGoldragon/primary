# 691 — gaps and drifts: what I fixed, and the leans on the rest

Follows the 690 engine audit. The psyche: *"fix the gaps and drifts you
can fix, go with your leans and report on what you did."* I fixed
everything cleanly in the **designer lane on primary** (skills, protocol
doc, my own report) after verifying each against the deployed source —
and for the **code-lane** gaps I can't touch directly (designer code-repo
edits go via `~/wt` + operator rebase, and operator is *actively
integrating* criome / router / signal-router right now, so direct edits
would collide), I went with my lean and recorded it as a *decided shape*
so operator implements against a call, not an open question.

## Disposition at a glance

| Item | Disposition | Where |
|---|---|---|
| `intent-log.md` missing negative-guideline rule | **Fixed** | skills (report 690) |
| `spirit-cli.md` stale "ResolveClarification not deployed" | **Fixed** | skills (report 690) |
| `structural-forms.md` enum-only derive (claimed struct support) | **Fixed** | skills |
| `structural-forms.md` named-field variant claim (HEAD rejects) | **Fixed** | skills |
| `structural-forms.md` positional Family/Stream (now labeled-brace) | **Fixed** | skills |
| `active-repositories.md` `vez8` → `6cfr` (wrong record id) | **Fixed** | protocols |
| `9-cross-cutting.md` Asschema-removal record id | **Fixed** | report |
| `StandardSocket` sum vs newtype | **Decided (lean)** | operator bead |
| standard-newtype global-vs-WireContract default | **Decided (lean)** | operator bead |
| criome `k > n/2` majority guard | **Lean recorded** | operator bead (684 Woe 3) |
| criome BLS aggregate verify | **Lean recorded** | operator bead (684 Woe 5) |
| criome operational matcher retirement | **Bead** | operator (with branch) |
| mirror unowned / consumer-build sweep | **Bead** | operator/system |
| code-repo ARCHITECTURE.md drifts | **Bead** | operator (in-flight) |
| `structural-forms.md` #411/#416 tracker-vs-code | **Bead** | nota-next owner |

## Fixed directly (verified against deployed source, landed)

All three `structural-forms.md` corrections were confirmed by reading the
nota-next HEAD derive and current schema fixtures — two audit agents plus
my own read converged:

- **The derive is enums-only.** `derive/src/lib.rs` rejects
  `Data::Struct(_) | Data::Union(_)` with *"StructuralMacroNode supports
  enums only"*. The skill claimed it "covers enums **and structs**."
  Corrected.
- **Variants carry unnamed (tuple) fields only.** The same derive rejects
  `Fields::Named` with *"variants carry unnamed fields, not named
  fields."* The skill claimed variants "may carry **named** fields
  (`Apply { head, arguments }`)." Corrected, with a note that the
  named-field / struct-derive features are *tracked but not landed*
  (#411/#416) so a reader doesn't code to them.
- **Family/Stream are labeled-brace, not positional.** Current fixtures
  and the spirit/signal-spirit schemas declare
  `(Family { record Entry table entries key Domain })` and
  `(Stream { token … opened … event … close … })`. The skill showed the
  retired positional `(Family StoredRecord records Domain)`. Corrected
  for both, with the `key ∈ {Domain, Identified}` constraint and a
  pointer to the `v0n6` hand-parse cleanup.

And the record-id fix: `active-repositories.md` cited `vez8` for the
Asschema removal; `(Lookup vez8)` errors. The real record is **`6cfr`**
(Decision VeryHigh): *"the separate Assembled Schema (Asschema) IR is
removed; the resolution it performed … lives as methods on
schema-in-rust types … the emitter does only Rust projection."* Fixed in
the protocol doc and corrected in the synthesis.

## Design calls made (decided with my lean — not open questions)

These are the audit's "undecided" drifts. I resolved them so operator has
a target; each is reversible if the psyche disagrees.

1. **`StandardSocket` is a sum, not a newtype.** signal-standard's
   `enum StandardSocket { UnixSocket, NetworkSocket }` is right and the
   mentci-contract `struct StandardSocket(SocketPath)` is wrong — per
   `eaf7`, a connection point is *"a Unix socket path for local IPC,
   **with a port for network cases**,"* which a newtype around a single
   path structurally cannot express. **Lean: settle the sum first, then
   migrate** signal-mentci + meta-signal-mentci + signal-criome onto
   signal-standard in one coordinated breaking change; adapt
   `StandardSocket::unix(...)` callers to the sum constructor.

2. **Standard-newtype impls stay WireContract-scoped — do not flip to a
   global default.** Report 663 recommended a global default; the
   narrower landing is the better call and supersedes that rec. Reason:
   `Display`/`AsRef`/`PartialOrd` belong on **wire-facing** newtypes,
   not on internal nexus/sema declaration types that never cross a
   boundary — a global default would impose semantically-wrong traits on
   internal types. **Lean: keep the WireContract scope; record it as the
   chosen policy in schema-rust-next `INTENT.md`** (so it reads as
   decided, not as an unlanded slice of 663). The genuinely-unlanded 663
   pieces (typed `SchemaError` for the ~8 emitter `panic!`s, the `*deref`
   marker + `Deref` template) remain real beads.

3. **criome `k > n/2` is the default; sub-majority is an explicit narrow
   mode.** The verifier checks only `required ≤ authorities.len()`, so a
   2-of-5 admits and a partition can produce two conflicting quorums.
   **Lean: enforce strict majority on the default authorization path**
   (one OR-term in the AttestedMoment guard + `Threshold::validate_shape`)
   and gate any sub-majority behind an explicitly-typed
   bootstrap/diagnostic mode, never the default. (Pins 684 Woe 3.)

4. **criome BLS aggregate verify ships in v1.** The per-signature pairing
   loop makes the direct-lane latency win collapse ~5-10× → ~2× (the
   Amdahl argument in `684/4`, which the psyche already leaned "yes,
   ship it"). **Lean: `FastAggregateVerify` + proof-of-possession on
   cluster-root admission is a v1 gate, not a later optimization.**
   (Pins 684 Woe 5.)

## Held as operator/system beads (code-logic — outside the designer lane)

I can't fix these from the designer lane (they are Rust implementation,
deploy, or edits to repos under active operator integration). They carry
my lean above where a call was needed; the full bead list is in
`690/10-synthesis.md`. The load-bearing ones:

- **criome**: retire the operational interest-matcher to
  observation/audit-only + rewrite `ARCHITECTURE.md:110-116` to
  router-sole — landed *together with* router's `attendance-fanout-139`
  (the router half is already on that branch). This is the one
  un-started piece of the `m0p2` matcher reconciliation.
- **router/signal-router**: integrate `attendance-fanout-139` (matcher +
  Attend/Withdraw + fan-out) and `transport-two-kernel-e2e-138`
  (cross-host witness) to main.
- **mirror — assign an owner**: verify it builds after `b26c139` and that
  `1275045` routed-object-notice handling matches router delivery +
  spirit outbox-drain. It is the chain endpoint nobody audited.
- **consumer-build sweep**: confirm the ~12 unaudited consumer daemons
  build after their strict port + sema-5 migration, **nix path
  included**, before the stack is called green.
- **mentci**: durable SEMA from `sema.schema` families (self-resume);
  canonical rkyv `ProposalDigest` (not `format!`).
- **code-repo ARCHITECTURE.md drifts** (nota-next 5→7 shapes; router
  2.9.1 over-claims `.criome` resolution as an enforced invariant) —
  operator folds these into the active integration rather than a
  designer branch colliding with it.
- **nota-next owner**: reconcile `structural-forms.md` #411/#416 — the
  tracker says named-field + struct derive landed; the HEAD code rejects
  both. Either re-land the feature or close the tasks; the skill now
  states the HEAD truth and flags the discrepancy.

## Method note

Every direct fix was verified against deployed source before editing
(`Lookup`/`PublicTextSearch` for the record id; the nota-next derive and
schema fixtures for the grammar) — the same re-verify-before-asserting
discipline that caught the stale signal-criome blocker earlier in the
session. No skill was edited on an agent's read alone.
