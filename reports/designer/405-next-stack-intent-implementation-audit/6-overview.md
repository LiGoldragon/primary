# 405/6 — Overview: where the next-stack vocabulary outruns the code

*Kind: Meta-report synthesis · Topics: schema, nota, spirit-next, nexus, sema, signal, audit, intent · 2026-05-28*

*Synthesis of the five repo audits (`1-nota-next` … `5-signal-frame`)
against the amalgamated intent in `0-frame-and-method.md` §1. Each
finding below traces to a sibling file with `path:line` evidence; this
file ranks and connects them. The audit targets operator `main` at the
commits pinned in §3 of the frame.*

## 1. One-line verdict

The stack is **honestly built and disciplined where it is built, but the
freshest and highest-certainty architecture intent — three schema
*languages*, three runtime *centers*, Nexus-as-mail-keeper, durable SEMA
— exists as vocabulary, schema-typed events, and emitted method names,
NOT yet as runtime topology or three distinct engines.** This is mostly
**expected lag** (that intent is records 964/970/982/1006/1007 from
2026-05-27, Maximum certainty; the code is one day behind), not concealed
divergence. The audit's job is to make the frontier precise so the next
implementation cycle aims at it — plus a short list of genuine
bugs/doc-drift to fix independent of the frontier.

## 2. Per-repo verdict

| Repo | Layer | State relative to intent |
|---|---|---|
| `nota-next` | 0 raw text | Cleanest. Scope holds, method-only clean, 8/8 green. One correctness bug + a header that is AHEAD of any psyche record. |
| `schema-next` | 1 schema lang | Disciplined single engine. Implements **0 of 3** schema types; import/export resolution absent. 34/34 green. |
| `schema-rust-next` | 2 Rust emit | Real emitted nouns. Mirror-naming reaches file paths only; 3-plane traits are 2-of-3 + self-contradictory + string-tier-proven. 10/10 green. |
| `spirit-next` | 3 pilot | Most honest (docs pre-disclose gaps). Schema-at-heart MET, zero boundary shims, tests genuinely prove via Nix. Three-centers is a flat orchestrator; SEMA in-memory. 16 green / 9 ignored + 9/9 Nix. |
| `signal-frame` | wire | The laggard. Predates the method-only override AND the mail-mechanism intent. Owns the unbuilt database-marker-on-Reply slot; ~80 free-fn violations; orphan+stale concept schema. Workspace green. |

## 3. The central finding — vocabulary outruns runtime, confirmed three times independently

The 2026-05-27 architecture wave (records 964 three schema types, 970
Nexus mail keeper + three execution centers, 982 three symmetric
languages) is the freshest Maximum-certainty intent in the stack. Three
agents, auditing three different repos, each independently found the same
thing: **it is named, not yet realized.**

- **schema-next** (`2-schema-next.md`): `grep -rni "signal|nexus|sema|plane" src/` returns nothing. ONE generic schema language, ONE engine. The three planes survive only as prose added by the pinned commit ("manifest three-plane mail intent" = 17 lines of markdown, 0 code) and as ordinary namespace types in one test whose own comment says "until the plane-specific file split lands."
- **schema-rust-next** (`3-schema-rust-next.md`): the pinned commit emits real `NexusEngine`/`SemaEngine` traits but **no `SignalEngine`** (2 of 3), and the new `NexusEngine::execute` single-method shim contradicts the file's own richer per-variant `*Nexus` dispatch trait — two unreconciled notions of "Nexus trait" coexist, proven only at the "string-contains" tier.
- **spirit-next** (`4-spirit-next.md`): only Signal is a real center. "Nexus" is methods on generated enums (`into_nexus_output`/`into_sema_input`, `engine.rs:240-264`) invoked procedurally by `Engine::handle`, which calls SEMA directly (`engine.rs:49`). **No object holds the mail in a being-processed state while SEMA runs** — `NexusMail` is consumed before the SEMA call. The mail lifecycle EVENTS are schema-typed and logged; the mail-KEEPER ROLE has no runtime topology.

This is the implementation frontier. It is not a failure — it is the gap the engine's intent→design→implement dance is meant to leave open for one cycle. But it is the gap.

## 4. Findings grouped — frontier vs. fix-now vs. psyche-decision

### A. Implementation frontier (expected lag; targets for the next cycle)

These are the freshest Maximum intent not yet in code. They are where the next prototype cycle goes, not bugs to scold.

1. **Three schema types as three typed engines/languages** (records 964/982) — schema-next implements one generic engine. The single largest gap.
2. **Single-colon import/export resolution** (record 982's other half) — MISSING across the stack: schema-next has no export surface or cross-schema import resolution (its own `ARCHITECTURE.md:23` admits it); schema-rust-next never calls `asschema.imports()` so `schema:spirit:Entry` cannot become `spirit::Entry`; spirit-next emits the per-plane Imports/Namespace positions but they are **inert** (only Input/Output are live). The 4-position shape is half-alive.
3. **Nexus mail-keeper as runtime topology** (record 970) — needs an object that owns the mail in a BEING-PROCESSED state across the SEMA call, translating both directions. Today it is procedural orchestration.
4. **Durable SEMA** (records 1007/1008) — spirit-next store is `Vec<StoredRecord>` in `Mutex<Store>` (`store.rs:17`), zero redb/`.sema`/file-write. Confirms bead `primary-q2au`; "not a full SEMA proof" until it writes the durable artifact. The `.redb`→`.sema` rename rides on this.
5. **`SignalEngine` trait** (3rd plane) in schema-rust-next, and reconciliation of the two Nexus-trait notions.

### B. Genuine fixes (independent of the frontier — do regardless)

1. **nota-next `packed_word` corrupts structures with >15 children** (`src/parser.rs:292,305,311`) — child count clamped to a nibble with no overflow marker; lossy round-trip; untested (fixtures are ≤3 children). A correctness bug in the exact artifact the pinned commit ships, and it will mislead schema-next when it triages a wide structure.
2. **Per-repo doc drift — three repos over-claim** (violates the continuous-manifestation discipline, record 944): schema-next `ARCHITECTURE.md:50` says the engine "lowers all three planes uniformly" (true only because it cannot tell them apart); signal-frame `ARCHITECTURE.md` never mentions mail/Nexus and ships an **orphan + stale** `signal-frame.concept.schema` (declares `Frame (ShortHeader Payload)` while the real `ExchangeFrameBody` has four variants); nota-next asserts the 64-bit header as settled. spirit-next is the counter-example — its docs pre-disclose every gap and should be the model.
3. **schema-rust-next build-graph drift** — its `Cargo.lock` pins schema-next at `807c525` while `main` is `e0681f2`; the emitter is validated against a stale lowering layer. (Note: spirit-next's lock correctly pins all three substrate crates at the audited commits — so the drift is schema-rust-next's own test graph, not the pilot's.)
4. **signal-frame method-only debt** — ~11 violations in the runtime crate (`frame.rs` 7, incl. 2 `pub` API; `caller.rs` 3; `namespace.rs` 1) plus ~70 in the generator crates. signal-frame HEAD predates the method-only hard override (records 712/882), so this is catch-up, not regression — but it is the one repo out of step.
5. **spirit-next minor**: `StateDigest` is a `wrapping_mul(31)` toy fold (not content-addressed); `UpgradeFrom`/`AcceptPrevious` traits emitted but unimplemented/untested; `process_boundary.rs` is the one lesser-shape test (cargo-built + raw-string-asserted), now redundant with the Nix tier.

### C. Psyche decisions (the audit cannot resolve these — they need intent)

1. **The nota-next 64-bit "structure header" is AHEAD of any psyche record.** No record in 700-1008 asks for a packed triage word, depth-2/8-slot ceilings, or the `packed_word` round-trip — only the repo's own agent-written `INTENT.md`. Ratify it as real design, or downgrade it to a documented internal detail? Until ratified it is an unaccountable commitment with a live bug (B-1).
2. **Where does brace key/value-ness live — Layer 0 or Layer 1?** nota-next treats a `{}` block as structurally identical to a parens (flat `Vec<Block>`) and never asserts even-length; it has *silently* chosen to defer all key/value semantics to schema-next. Is that the intended boundary, or should Layer 0 structurally reject odd-length brace bodies?
3. **How literally should "Nexus IS the runtime representation that a mail is being processed" (record 970) be implemented?** Is the target a real mail-keeper object that holds the message across the SEMA call (literal reading), or is schema-typed mail events + procedural orchestration an acceptable realization of the same intent? This decides how much of frontier item A-3 is actually in scope.

## 5. The thing to be careful about — the Nix `checks` can be over-credited

spirit-next genuinely meets the record-1006 prove-not-pretend bar at the
test level: honest counts are **9/25 real-Nix-binary, 24/25
schema-emitted-assert, 0/25 synthetic-enum**, and the nix-integration app
launches actual Nix-built binaries exchanging real rkyv over a real Unix
socket. But the flake's `checks` are overwhelmingly **grep-based
structural witnesses** (assert a symbol is present in emitted source),
not behavioral proofs. A reader scanning `nix flake check` output could
over-credit the stack. The real behavioral proof is `cargo test` + the
nix-integration application; the structural checks are scaffolding, and
the synthesis recommends not treating their green as architectural proof.

## 6. Bead candidates (proposed, not yet created)

Confirmed existing: **`primary-q2au`** (durable SEMA) — A-4 is its exact
content; the audit confirms it is still `Mutex<Vec>`. **`primary-lrgj`**
(Nix-integration CI cadence) — still open from /404; the audit confirms
the Nix tier is real and worth gating on.

New candidates to consider (one per frontier/fix item; numbering for
discussion, not yet filed):

- schema-next: implement the three schema types as a discriminated set of typed engines + the 4-position positions wired to plane semantics (A-1).
- schema-next + schema-rust-next: implement single-colon import/export resolution end-to-end (A-2); the cross-namespace round-trip test is the proof.
- spirit-next: build the Nexus mail-keeper object owning BEING-PROCESSED across the SEMA call (A-3) — gated on psyche decision C-3.
- schema-rust-next: emit `SignalEngine`; reconcile the two Nexus-trait notions; promote the 3-plane-trait proof from string-tier to compiled (A-5).
- nota-next: fix `packed_word` overflow + add a >15-child round-trip test (B-1).
- doc-reconciliation sweep across nota-next/schema-next/signal-frame to match the spirit-next honesty standard (B-2).
- schema-rust-next: bump `Cargo.lock` to current schema-next (B-3).
- signal-frame: method-only migration (B-4) + the database-marker-on-Reply slot (record 935 obligation).

## 7. The shape of the whole

Read top to bottom, the stack tells one story: **the lower you go, the
more finished it is; the higher you go, the more the newest intent is
still vocabulary.** nota-next (layer 0) is essentially done bar one bug.
schema-next (layer 1) is a clean single engine waiting to become three.
schema-rust-next (layer 2) emits real nouns but only half-mirrors the
namespace and half-emits the plane traits. spirit-next (layer 3) proves
the pipeline end-to-end with real binaries and zero boundary shims — and
is honest that its Nexus and SEMA are still the procedural/in-memory
placeholders the architecture intends to replace. signal-frame sits to
the side, the oldest repo, lagging two intent waves.

Nothing here contradicts the intent dishonestly; spirit-next in
particular is a model of a repo whose docs match its code. The gap is
that the engine's freshest, highest-certainty design (the three
languages / three centers / mail keeper / durable SEMA) landed ~24 hours
ago and the implementation cycle that closes it has not run yet. This
audit is the design-readiness signal for that cycle.
