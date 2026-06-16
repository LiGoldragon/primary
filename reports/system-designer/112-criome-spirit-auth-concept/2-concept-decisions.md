# 112.2 — concept and decisions (the deliverable)

The critique-corrected concept, then the decisions the psyche asked to make. This
file supersedes the raw synthesis where the critic found it wrong (noted inline).

## Three corrections the critic forced

The raw synthesis recommended a *witness-first* design with a synchronous
before-commit gate. The adversarial critic showed three load-bearing errors, all
confirmed in code:

1. **The recommended default did not meet the goal.** A chain-head *witness* binds the
   LOG to criome's key — it authenticates nothing about the submitter. The psyche's
   goal is [bind WHO submitted it]; the witness fails it. The part that meets the goal
   (per-caller binding) was deferred as "heaviest cost." Backwards.
2. **The before-commit gate is not on the wire.** criome's `AuthorizeSignalCall`
   **always returns `AuthorizationPending`**; grants are observed via
   `ObserveAuthorization`, never returned synchronously (`authorization.rs:120` +
   criome `ARCHITECTURE.md`). So a synchronous "commit on the grant reply" gate does
   not exist — it needs a deferred-commit state machine spirit lacks, plus
   `meta-signal-criome` (unbuilt) for the human-approval path.
3. **Denial ≠ unavailability.** A criome `AuthorizationDenied` (a policy verdict) must
   ALWAYS reject the write; criome being *unreachable* is a separate posture choice.
   Collapsing them is a security bug, not a knob.

## The corrected concept — "out-of-band caller-attestation, criome's tempo"

The pilot's shape that actually meets the goal, honors criome's disciplines, and
needs no unbuilt machinery is the **fourth cell** the synthesis hid:

> After the guardian accepts and the operation commits, spirit asks its local criome
> to mint an **out-of-band `Attestation`** that binds the **kernel-vouched caller
> principal** (the SO_PEERCRED uid threaded from `daemon.rs:142`, resolved to a
> registered Identity) **to the exact committed operation digest** (`Sign` over a
> `ContentReference{digest, purpose, schema_version}`). The attestation is a separate
> record keyed by the operation digest — no proof field is embedded in any intent
> record. The write never blocks on criome.

Why this is the pilot:

- **It meets the goal.** The attestation binds *who submitted* each operation to *the
  exact bytes committed* — per-operation, per-caller. The witness-only default did
  not.
- **It is on the wire today (modulo criome's BLS core).** `Sign` is synchronous and
  takes a free `ContentReference`; no `ObserveAuthorization` deferral, no
  deferred-commit state machine, no `meta-signal-criome`.
- **It honors "criome verifies; Persona decides."** The guardian keeps the entire
  content verdict; criome only signs the bytes + principal. Three authorities stay
  separate (per operator `223`): socket/filesystem = can-this-process-reach-this-tier;
  criome = is-this-principal-bound-to-these-exact-bytes; guardian = is-this-admissible.
- **It honors out-of-band-only.** The `Attestation` is a separate record; the intent
  `Entry`/`StoredRecord` gains no proof field, mirroring spirit's own
  guardian-verdict-out-of-log discipline.

A **chain-head integrity witness** (P3) is a cheap optional add-on for whole-log
tamper-evidence, and a **before-commit gate** (P2) is a later hardening for a tiny
sensitive set (Remove/Supersede/privacy-elevated) — *once* criome's async
authorization path and `meta-signal-criome` exist. Neither is the pilot.

The single hard blocker for the whole thing is criome's real `blst` sign/verify path
(today the placeholder `criome-skeleton-bls-signature`). So the deepest framing of the
pilot: **spirit is the forcing function that makes criome grow its real cryptographic
core** — which is exactly why the psyche called it "a perfect pilot."

## Decisions for the psyche

Four are genuinely the psyche's (A–C, E); D is a values-call worth a recommendation.
The agent-level choices the critic flagged as padding (the `ContentPurpose` variant;
the 0.4.0-vs-0.6.x read-cost) are lane decisions, noted under "Agent-level" below.

### A — Who does criome authenticate in the pilot?

The foundational, currently-unasked question; everything else follows from it.

- **The submitter / caller** — binds WHO wrote each operation to the bytes. *Meets the
  goal.* **(recommended)**
- **The log itself** — criome's key witnesses log integrity (tamper-evidence); binds
  nothing about the submitter.
- **Both** — caller-binding + a log-integrity witness on top.

*Recommendation: the caller* — it is the recorded goal ([bind WHO submitted it]); the
log witness is a cheap add-on, not the headline.

### B — When does criome act, and is it on the write's critical path?

- **After-the-fact, out-of-band, non-blocking** — criome attests the committed
  operation; the write never waits; matches the psyche's draft and criome's
  async + out-of-band design. **(recommended)**
- **Before-commit gate, blocking** — commit only on authorization (true prevention),
  but criome's authorization is async-by-design, so this needs a deferred-commit state
  machine + `meta-signal-criome`, both unbuilt.
- **Hybrid** — non-blocking default; blocking gate only for sensitive ops.

*Recommendation: after-the-fact* for the pilot; revisit the gate once criome's
authorization path exists.

### C — What exactly does criome sign?

- **Per-operation digest** — the exact bytes of each accepted operation. Matches the
  psyche's "signature on the content-addressed log *entry*"; binds each submission
  individually. **(recommended)**
- **Per-commit chain-head (`EntryDigest`)** — one signature witnesses the whole log;
  cannot isolate one record inside a multi-operation commit.
- **Periodic checkpoint only** — cheapest; coarse integrity, not per-operation.

*Recommendation: per-operation digest* (with an optional chain-head witness for
whole-log tamper-evidence — they compose).

### D — Failure posture: criome unavailable vs criome denying (recommendation, not a fork)

Denial and unavailability are different. **A criome `AuthorizationDenied`/invalid
signature must ALWAYS reject** — that is the mechanism working. The only real choice is
the *unavailable* case, and silent fallback is rejected by both lanes. Recommended:
for the pilot, **unavailable → attest-later with a visible `unauthenticated`/`unwitnessed`
provenance class** (never silent), tightening to fail-closed per op-class (mirroring
`guardian_required`) as criome hardens. Surfaced here for the psyche to veto.

### E — (Deferred) Intent substrate: move intent off `INTENT.md` files into Spirit?

Independent of criome; the psyche raised it ("read intent should mean read spirit… I
want to agglomerate intent in spirit and not in files so that we only search one
place… emphasize the architecture file… but the intention to live in spirit"). It
overturns the active contract (`cdd3`; AGENTS.md "INTENT.md first"), so it is
explicit-only. My premature `15df` is zeroed pending this call.

- **Yes — Spirit is the single intent source**; `ARCHITECTURE.md` keeps architectural
  state; per-repo `INTENT.md` migrates off gradually (opportunistically, when a repo
  is touched).
- **Hybrid** — Spirit is source-of-truth; `INTENT.md` becomes a *generated /
  architecture-adjacent summary* (the operator's likely-end-state framing).
- **No / not yet** — keep per-repo `INTENT.md` canonical per the current contract.

No recommendation: this is a contract-level call the psyche owns. If Yes/Hybrid, it
cascades into AGENTS.md, `skills/intent-log.md`, `skills/repo-intent.md`, and every
repo's `INTENT.md` — a deliberate rollout, not a one-session edit.

## Dependencies (the build order)

1. **criome real `blst` sign/verify** — the single biggest blocker for every layer.
2. **criome master keypair lifecycle** (generation, mlock/zeroize custody, passphrase)
   — tied to the not-yet-existing `meta-signal-criome`.
3. **trustworthy `RegisterIdentity`** — must verify the Developer/master signature
   (`registry.rs:90`); until then the registry is self-asserted.
4. Spirit-side (buildable ahead of crypto, against the placeholder):
   stop discarding `ConnectionContext` (`daemon.rs:142`); a `CriomeAuthority` client
   (methods on a data-bearing noun, modeled on `AgentGuardian::call_agent`); a `Store`
   accessor returning the real `EntryDigest`; an out-of-band attestation ledger (a new
   SEMA family, or pushed to criome's attestations family — **never** an embedded
   field); binary `SpiritDaemonConfiguration` fields for the criome socket path + master
   public key.
5. **Deploy coordination** (system-operator): both source trees pin sema-engine 0.6.x
   while deployed spirit runs 0.4.0-era — the pilot is effectively 0.6.x-coupled; the
   criome daemon must run for spirit's Unix user with a configured key.

## Risks

- Spirit-side work completes against a placeholder signature; integration bugs surface
  only at crypto-enable time.
- "uid-asserted" caller binding is OS authorization, not cryptographic authentication —
  if the psyche reads "authenticated" as "caller proved a BLS key," the first cut
  under-delivers unless caller-signed is the explicit hardening target.
- Domain-tag coupling: every signature is bound to
  `sema-engine-versioned-commit-log-entry-v2`; an engine bump to `-v3` invalidates the
  witness chain — re-attest after any engine migration.
- Surfacing the real 32-byte `EntryDigest` on the wire (replacing the truncated u64
  `StateDigest`) breaks every `signal-spirit` consumer/CLI/test — pre-production
  allows it, but the break surface needs an operator integration pass.
- A multi-operation commit bundles several operations under one `EntryDigest`, so a
  chain-head witness is per-commit, not per-record (another reason C → per-operation).

## Resolution — decisions taken (2026-06-16)

The psyche ratified the critique-corrected concept in full and took the deferred
substrate decision:

- **A — principal = the submitter/caller.** The pilot binds WHO wrote each operation,
  not merely the log. (The witness-only default the first synthesis recommended is
  rejected as failing the goal.)
- **B — timing = after-the-fact, non-blocking.** No before-commit gate in the pilot;
  it is deferred until criome's async authorization path and `meta-signal-criome`
  exist.
- **C — signed = per-operation digest.** The exact bytes of each accepted operation;
  matches [signature on the content-addressed log entry].
- **E — Yes, Spirit is the single intent source.** `ARCHITECTURE.md` keeps
  architectural state; per-repo `INTENT.md` migrates off into Spirit gradually.

Captured intent: **`2st7`** (Decision High) — the settled pilot mechanism (A+B+C),
extending the operator's `w2g3`; **`15df`** restored to High (the substrate decision,
E) and **`cdd3`** zeroed (explicitly superseded). Failure posture D stands as the
recommendation (denial always rejects; unavailable → visible `unwitnessed`
provenance, never silent).

Tracked work: **`primary-kr40`** (criome real blst Sign/Verify + signed
RegisterIdentity + master key lifecycle — the hard blocker), **`primary-5zur`** (the
spirit-side pilot build, gated on kr40), **`primary-ebev`** (the intent-substrate
rollout — contract docs + gradual `INTENT.md` migration). The message/criome
`INTENT.md`/`ARCHITECTURE.md` manifestation and the criome-repo crypto work land on
their own branches in the criome/operator lanes, not this coordination repo.

## Agent-level (not psyche decisions)

- **`ContentPurpose`**: the gate path can reuse the existing `PrivilegeElevation`;
  the witness can reuse `SignedObject` or `Archive`; a dedicated `SpiritIntentLog`
  variant is a nice-to-have for domain separation but not required first. Designer/
  operator coordination call.
- **0.4.0 vs 0.6.x head read**: O(n) vs O(1) over 1258 records is negligible and
  swappable behind one `Store` method. An operator sequencing note, not a strategic
  choice — but the *deploy* coordination in dependency 5 is real and operator-owned.
