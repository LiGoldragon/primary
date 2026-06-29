# Design + Proof: per-store `ContentAddressing` policy refusing digest-mismatched bodies at append

Bead `primary-p0gg` — "mirror: refuse digest-mismatched body at append via typed
per-store `ContentAddressing` policy." This file is the DESIGN deliverable plus
the embedded RUN-IT determinism proof. It lands nothing: no tracked-file feature
edits, no commit, no push. The determinism spike is a throwaway in
`/tmp/p0gg-determinism-spike` (outside every tracked repo).

## Ground-truth rev (verify-this-first)

The bead's path:line anchors (`readback.rs`, `LandedBody::content_address`, the
`decision.rs` digest-compare sites) do NOT match the on-disk worktree at
`/home/li/wt/github.com/LiGoldragon/mirror/criome-auth-witness` — that worktree
is an OLDER cut with no `readback.rs`. They match the cargo git checkout

```
/home/li/.cargo/git/checkouts/mirror-c6db31b88119a19c/5102f5e
  rev 5102f5ed87d10d6a7386358b3b10214a04fdf89d
  "mirror: in-VM landed-body verifier re-hashes the restored body to the head"
```

All `mirror/src/*` anchors below are at `5102f5e`. Its `Cargo.lock` pins the
exact deps this design and the proof compile against:

- `sema-engine` `73eea24b294a2bdcac470111afc387e7ce06608e` (branch `main`)
- `signal-mirror` `34ed3fdd429b10722902b01264c17dcda0bcc482` (branch `main`)
- `meta-signal-mirror` `9d2aeddf11d0a87ff23fbcc7f22a55869ffe06b2` (branch `main`)

Cargo checkouts read for this design: `signal-mirror/.../34ed3fd`,
`sema-engine/.../73eea24`, `meta-signal-mirror/.../9d2aedd`.

Implementation note: the implementer should land this on the mirror's working
branch whose HEAD is `5102f5e` (or its descendant `main`), NOT on the stale
`criome-auth-witness` worktree, and re-confirm the sema-engine/signal-mirror pins
have not moved under branch `main`.

## The gap (verified)

`mirror/src/decision.rs` `CheckedAppend::into_decision` (decision.rs:27-101)
runs three linkage guards — `suffix_inconsistency` (decision.rs:118, the
internal previous-digest chain), `expected_head_violation` (decision.rs:135),
`known_divergence` (decision.rs:177). Every digest comparison in them
(decision.rs:125, :153, :162-166, :182) compares one CARRIED or STORED digest
to another. None recomputes the digest from the body bytes. Confirmed by grep:
no `blake3`/hash call exists in `decision.rs`, `store.rs`, or `engine.rs`. So a
body whose carried `EntryEnvelope.digest` (signal-mirror schema/lib.rs:160)
chains correctly but whose `payload` (signal-mirror schema/lib.rs:161) does not
hash to it is accepted: `into_decision` returns `AcceptSuffix`
(decision.rs:100), the engine commands `PersistSuffix` (engine.rs:262-264), and
it LANDS. Today the only detector is post-landing:
`bin/mirror_landed_body_verifier.rs` (re-hashes a RESTORED body, exit-code
witness) and `tests/landed_body_readback.rs` (in-process restore re-hash). Both
recompute through the SAME primitive this design hooks into the append path:
`mirror/src/readback.rs:42-54` `LandedBody::content_address()`.

## The recompute primitive that already exists (reuse, do not reinvent)

`mirror/src/readback.rs:27-55` `LandedBody<'octets>` borrows the body slice and
exposes `content_address(&self) -> Result<EntryDigest>` (readback.rs:42):

1. `rkyv::from_bytes::<VersionedCommitLogEntry, rancor::Error>(self.octets)` →
   maps decode failure to `Error::LandedBodyDecode` (mirror error.rs:19-20).
2. reconstructs through the PUBLIC `sema_engine::VersionedCommitLogEntry::new`
   (sema-engine versioning.rs:414), which recomputes the digest internally via
   the crate-private `EntryDigest::from_entry_fields` (versioning.rs:257 — a
   domain-separated blake3 over store_name, schema_hash, commit_sequence,
   snapshot, previous_entry_digest, and each operation; the `entry_digest` field
   is the OUTPUT, never a hash input).
3. returns the re-derived `sema_engine::EntryDigest` (32 bytes,
   versioning.rs:246).

The carried wire digest `signal_mirror::EntryDigest` is `FixedBytes<32>`
(signal-mirror schema/lib.rs:106); `as_bytes() -> &[u8; 32]`. The comparison is
`rederived.bytes() == entry.digest.as_bytes()` — exactly the two-VM verifier's
check at `mirror_landed_body_verifier.rs:126`.

## Design

### Acceptance criterion 1 — typed `ContentAddressing` in contract/meta + storage, set at registration

The established precedent in this exact codebase is RETENTION: a meta-layer enum
(`meta-signal-mirror schema/lib.schema:57` `RetentionRule [...]`) that is carried
on a meta op and mapped to a SELF-CONTAINED local storage enum
(`mirror schema/sema.schema:93` `RetentionRule [...]`) at the store boundary
(`store.rs:245-260` `RetentionSetting::from_order`). `ContentAddressing` follows
this precedent verbatim.

(a) META / CONTRACT layer — `meta-signal-mirror`, the registration plane.
Registration is a meta op: `meta_signal_mirror::Input::RegisterStore(StoreRegistration)`
(handled at mirror engine.rs:84). In `meta-signal-mirror/schema/lib.schema`:

```
;; new enum, beside RetentionRule (lib.schema:57)
ContentAddressing [Opaque SemaVersionedLog]
;; lib.schema:48 changes from the transparent newtype
;;   StoreRegistration StoreName
;; to a record carrying the policy:
StoreRegistration { store.StoreName addressing.ContentAddressing }
```

`Opaque` is the first variant so it is the natural default. This is a wire-shape
change to the meta plane (see Versioning below). The owner CLI that emits
`RegisterStore` supplies `addressing` (default `Opaque`); the thin CLI gets one
new optional argument, not a new verb.

(b) STORAGE layer — `mirror/schema/sema.schema`. Per the schema's own rule
("Stored rows are SELF-CONTAINED local declarations: the mirror's durable shape
must not move when the wire contract churns", sema.schema:12-14), declare a LOCAL
enum and a per-store policy row + family, mirroring the retention family:

```
ContentAddressing [Opaque SemaVersionedLog]
StorePolicy { store.String addressing.ContentAddressing }
...
PolicyFamily (Family { record.StorePolicy table.store-policies key.Domain })
```

This emits a fifth `RecordFamily` arm (generated sema.rs RecordFamily,
sema.rs:1060-1095 today has four families + `versioning_policy()` at
sema.rs:1069) — `RecordFamily::policy_family()` registered in `Store::open`
(store.rs:282-285) exactly like `entry_family()` / `retention_family()`.

(c) CHECK / READ surface — the value `into_decision` reads. Add the local enum
to the looked-up ledger record (`mirror/schema/sema.schema:62-66`):

```
RegisteredLedger {
  LedgerHead.(Optional HeadMark)
  KnownEntries.(Vector KnownEntry)
  LatestCheckpoint.(Optional CheckpointReceipt)
  Addressing.ContentAddressing            ;; new
}
```

### Why a SEPARATE policy family, not a field on `StoredHead` (chosen, with the rejected alternative)

Rejected alternative: add `addressing` to `StoredHead`
(sema.schema:77 `StoredHead { store StoredHeadStamp }`). Two costs:

1. `Store::advance_head` (store.rs:426-438) rewrites the WHOLE `StoredHead` row
   on every append via `Mutation` with `StoredHead::new(store, Some(stamp))`. To
   keep the policy it would have to thread `addressing` from the ledger through
   `into_decision` → `NovelSuffix` → `persist_suffix` → `advance_head`, coupling
   the policy into the high-frequency head-advance path.
2. Changing `StoredHead`'s shape changes its family `SchemaHash`, so EXISTING
   mirror databases hit `RecordFamilyError::SchemaHashMismatch` (sema.rs:1112) —
   a storage migration of live head rows.

Chosen: a separate `StorePolicy` family is purely ADDITIVE. Existing families
keep their hashes; the head-advance path is byte-identical for every store; and
absence-of-row defaults to `Opaque`, so a store registered before this feature
behaves exactly as today with ZERO new stored state. This is the
"special case dissolves into the normal case" shape: `Opaque` is not a branch to
remember, it is the absence of policy.

### Acceptance criterion 2 — `into_decision` recomputes for `SemaVersionedLog`, `Opaque` provably unchanged

Read side, `store.rs`:

- `load_ledger` (store.rs:334-360) reads the `StorePolicy` row for the store
  (new `policy_row(store)` private reader, sibling of `head_row` store.rs:295)
  and passes its addressing to `RegisteredLedger::new(...)`; a missing row ⇒
  `ContentAddressing::Opaque`. `RegisteredLedger::new` (store.rs:97-107) gains
  the `addressing` parameter; a new `addressing(&self) -> ContentAddressing`
  accessor beside `head()`/`known()` (store.rs:109-119).
- `register_store` (store.rs:466-479) gains the policy: `register_store(&mut
  self, store: &StoreName, addressing: ContentAddressing)` asserts a
  `StorePolicy` row alongside the existing `StoredHead` assertion. The
  meta→local map sits beside `RetentionSetting::from_order` (store.rs:245).

Decision side, `decision.rs` — a FOURTH guard, uniform with the existing three.
Add to `impl RegisteredLedger` (beside `known_divergence`, decision.rs:177):

```rust
/// For a SemaVersionedLog store, every body must content-address to its
/// carried digest; an Opaque store is payload-blind (today's behavior).
fn body_addressing_violation(
    &self,
    entries: &[EntryEnvelope],
) -> Option<AppendRejectionReason> {
    match self.addressing() {
        ContentAddressing::Opaque => None,
        ContentAddressing::SemaVersionedLog => entries
            .iter()
            .find(|entry| {
                !LandedBody::new(entry.payload.as_slice()).addresses_to(&entry.digest)
            })
            .map(|_| AppendRejectionReason::DigestMismatch),
    }
}
```

and one new method on the data-bearing `LandedBody` (readback.rs), so the
verb lives on the type that owns the octets:

```rust
/// Whether this body content-addresses to `digest`. A body that fails to
/// decode addresses to nothing — false, never a panic.
pub fn addresses_to(&self, digest: &signal_mirror::EntryDigest) -> bool {
    self.content_address()
        .is_ok_and(|rederived| rederived.bytes() == digest.as_bytes())
}
```

This collapses BOTH failure modes into one normal case: a body that decodes but
recomputes to a different digest, and a body that does not decode at all, both
yield `addresses_to == false` ⇒ `DigestMismatch`. No side path.

Hook in `into_decision` — one line after the existing `known_divergence` guard
(decision.rs:55-57), before the novel filter and before any `AcceptSuffix`:

```rust
if let Some(reason) = ledger.body_addressing_violation(&entries) {
    return refuse(reason, request.store, ledger.head().cloned());
}
```

`Opaque` proof-of-no-op: `body_addressing_violation` returns `None` on its first
match arm without touching `entries`; combined with absence-of-row ⇒ `Opaque` in
`load_ledger`, an `Opaque` (and every pre-existing) store traverses the
identical decision and persist path it does today. `decision.rs` gains one
import (`crate::readback::LandedBody`, already in-crate) and the local
`ContentAddressing`; it stays a pure in-memory projection (no IO, no storage
access), preserving the module's "no storage access here" contract
(decision.rs:9-11).

Placement note (scope/perf): the guard runs over all `&entries`, uniform with
the other three guards, so an idempotent re-send re-hashes too — strictly safer,
catching a tampered re-send whose carried digest still matches the stored row.
If the implementer prefers to pay blake3 only on the to-be-landed set, move the
call after the `novel` computation (decision.rs:74-81) and pass `&novel`;
correctness is unchanged because already-known entries were digest-verified
against stored rows by `known_divergence`.

### The refusal path produces `DigestMismatch` BEFORE landing/fsync (verified)

`AppendRejectionReason::DigestMismatch` already exists (signal-mirror
schema/lib.rs:221) and is reused — no new wire variant, no nexus schema change.
The flow proving "before landing": `into_decision` returning `RefuseAppend`
maps at engine.rs:268-269 to `Output::AppendRejected` and replies directly; the
durable write `WriteInput::PersistSuffix` is reached ONLY on `AcceptSuffix`
(engine.rs:262-264 → `apply_inner` store.persist_suffix, engine.rs:422-426 →
the two redb transactions at store.rs:403-438). A refusal never enters
`apply_inner`, so nothing is committed or fsynced. The acknowledge boundary is
ack-after-durable-write (store.rs:8-11); a refused append produces no receipt
and no row.

### Acceptance criterion 3 — one Nix flake check witnessing BOTH refusal-not-persisted AND match-lands

Fixture template already exists: `tests/landed_body_readback.rs`
`real_genesis_envelope` (builds a REAL versioned sema-engine genesis entry and
returns `(EntryEnvelope, sema_engine::EntryDigest)` with body =
`rkyv::to_bytes(genesis)`) and `Mirror::with_registered`. New test
`mirror/tests/append_addressing_refusal.rs`, one `#[tokio::test]`:

1. Register store `spirit` with `ContentAddressing::SemaVersionedLog`
   (`Mirror::with_registered` extended to take the addressing; it already drives
   `handle_meta(RegisterStore(StoreRegistration::new(...)))` — the new
   `StoreRegistration` record carries `addressing`).
2. Build `(faithful, real_head)` via `real_genesis_envelope`. Build a TAMPERED
   genesis: sequence 1, `previous_digest = None`, carried `digest = real_head`
   (so all three linkage guards pass), but `payload` = the rkyv body of a
   DIFFERENT genuine entry — the canonical attack: a carried digest that chains,
   a payload that does not hash to it.
3. Append TAMPERED ⇒ assert `Output::AppendRejected` with reason
   `DigestMismatch`. Assert NOT PERSISTED: `engine.store().landed_entries(&store)`
   (store.rs:550) is empty AND `Output::HeadsObserved` reports head `None`.
4. Append FAITHFUL ⇒ assert `Output::Appended`. Assert LANDED:
   `landed_entries` now holds the genesis and its body re-hashes to `real_head`
   (reuse `LandedBody::content_address`).
5. Control proving criterion 2 at the witness level: register a SECOND store
   with `ContentAddressing::Opaque`, append the SAME tampered body ⇒
   `Output::Appended` (payload-blind, unchanged).

Flake check (`mirror/flake.nix`, beside `mirror-restore-hands-back-landed-body`
at flake.nix:132-139, same `craneLib.cargoTest` shape):

```nix
mirror-append-refuses-digest-mismatch = context.craneLib.cargoTest (
  commonArgs // {
    inherit (context) cargoArtifacts;
    cargoTestExtraArgs =
      "--test append_addressing_refusal refuses_mismatched_body_and_lands_matching_body -- --exact";
  }
);
```

This is a pure (no-VM) flake check — the daemon logic runs in-process through
`Engine::handle`, exactly like the existing `landed_body_readback` check — so it
satisfies the testing/Nix discipline (pure tests as flake checks; the `-test`
suffix is for test-only BINS, which this is not).

### Methods-on-types shape (Rust discipline)

- recompute+compare verb on `LandedBody` (`addresses_to`), the type owning the
  octets — not a free helper.
- policy guard `body_addressing_violation` on `RegisteredLedger`, beside its
  three sibling guards — the type owning the looked-up ledger state.
- meta→local map beside `RetentionSetting::from_order`, the established seam.
- the policy is a typed two-variant enum (`Opaque`/`SemaVersionedLog`), not a
  bool flag — the variant set lives in the type system (typed-records-over-flags).
- schema-emitted nouns ARE the types: `ContentAddressing`, `StoreRegistration`,
  `StorePolicy`, `RegisteredLedger.addressing` are authored in the `.schema`
  files and regenerated; no hand-written parallel structs.

### Versioning awareness (required, behavior changes a wire + storage surface)

- Meta wire: `StoreRegistration` changes from `StoreName` newtype to a record →
  a `meta-signal-mirror` version bump; every component that pins
  `meta-signal-mirror` and emits `RegisterStore` (the mirror CLI / operator
  path) recompiles against the new shape. Old encoded `RegisterStore` payloads
  do not decode under the new record shape — coordinate the bump with the
  operator CLI.
- Storage: adding `StorePolicy`/`PolicyFamily` is additive (a new redb table; old
  DBs simply have no policy rows ⇒ `Opaque`). Confirm against sema-engine's
  open/register semantics whether registering a 5th family under the existing
  `SchemaVersion::new(1)` (store.rs:279) is a compatible evolution or wants
  `SchemaVersion::new(2)`; the conservative path bumps the version. No existing
  family's `SchemaHash` changes, so existing head/entry/checkpoint/retention rows
  are untouched.
- Wire reject reason: unchanged (`DigestMismatch` already exists). Nexus
  decision schema: unchanged.

## RISK / TRADEOFF — payload-blindness (Spirit 0yx5)

`SemaVersionedLog` makes the mirror PAYLOAD-AWARE for that one store: to recompute
the address it must decode the body as a `sema_engine::VersionedCommitLogEntry`
and understand sema-engine's content-addressing. This BENDS the mirror's stated
"payload-blind append-ingest" posture (mirror Cargo.toml description;
readback.rs:3 "The mirror is payload-blind"). Concretely, for a
`SemaVersionedLog` store the mirror now (a) couples to the sema-engine body
format and digest scheme — a sema-engine change to `from_entry_fields`
(versioning.rs:257) or the rkyv layout would change what the mirror accepts; and
(b) refuses any body that is not a decodable versioned-log entry, so that store
can carry ONLY sema-engine versioned bodies, never arbitrary octets.

`Opaque` as the default preserves the current posture exactly: payload-blind,
format-agnostic, accepts any carried octets, identical decision path. The policy
is opt-in per store, so the architectural bend is scoped to stores whose owner
explicitly asks for content-address enforcement (e.g. the `spirit` store the
two-VM witness already re-hashes post-landing). This is a real architectural
decision, recorded here as a tradeoff for the accepting authority — the bead
directs it, but it touches the 0yx5 payload-blind decision and should be
acknowledged when accepted.

## Determinism PROOF (RUN IT — actual command + real output)

Claim under test: recomputing the body digest at append (from the carried
`payload` rkyv bytes, via the `LandedBody::content_address` path) is byte-stable
and matches the producer's carried digest for a faithful body, and DIFFERS for a
tampered body — against the EXACT sema-engine rev the mirror compiles against.

Throwaway spike: `/tmp/p0gg-determinism-spike` (NOT in any tracked repo). Its
`Cargo.toml` pins `sema-engine` `rev = 73eea24b294a2bdcac470111afc387e7ce06608e`
(the mirror's locked rev) and copies the mirror's exact rkyv feature set
(`mirror/Cargo.toml:42`: `default-features = false`, `std bytecheck
little_endian pointer_width_32 unaligned`) so the archived layout matches the
body the shipper produces. The spike replicates `real_genesis_envelope`: opens a
real versioned sema-engine store, commits records in one atomic commit, pulls the
genesis `VersionedCommitLogEntry` from `versioned_commit_log()`, rkyv-encodes it,
then decodes and reconstructs through the public `VersionedCommitLogEntry::new`
(the same call `LandedBody::content_address` makes).

Build:

```
$ cd /tmp/p0gg-determinism-spike && CARGO_NET_OFFLINE=true cargo build --offline
   Compiling sema-engine v0.6.2 (...sema-engine.git?rev=73eea24b294a2bdcac470111afc387e7ce06608e#73eea24b)
   Compiling p0gg-determinism-spike v0.0.0 (/tmp/p0gg-determinism-spike)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 11.28s
```

Run (`cargo run --offline --quiet`), real output:

```
genesis operations = 2
carried digest      = f899a56b625a55780c2c60a34831ad6712496ff295309efb61f5028cbc0c7748
rederived digest    = f899a56b625a55780c2c60a34831ad6712496ff295309efb61f5028cbc0c7748
[PASS] faithful body recomputes to the carried digest
[PASS] rkyv re-encode is byte-identical
[PASS] recompute is identical across encode rounds
[PASS] substituted genuine body recomputes to a DIFFERENT digest
[PASS] byte-mutated body fails to decode (also a refusal)
[PASS] garbage body fails to decode

DETERMINISM VERDICT: ALL CHECKS PASS — recompute is byte-stable and tamper-sensitive.
=== EXIT CODE: 0 ===
```

Cross-process stability (the producer and the mirror are different processes):
three separate `cargo run` invocations all printed the SAME digest
`f899a56b625a55780c2c60a34831ad6712496ff295309efb61f5028cbc0c7748`, confirming
the address is a pure function of the entry's structured fields — independent of
process state, allocator addresses, or run order.

Scout-flagged open risks, each addressed by the run:

- `NonEmpty<VersionedLogOperation>` ordering — the genesis was a 2-OPERATION
  commit (`genesis operations = 2`); the recompute reproduced the carried digest,
  so the operation order survives the rkyv round-trip byte-stably
  (`from_entry_fields` iterates `for operation in operations`, versioning.rs:281).
- `SnapshotIdentifier`/`StoreSchemaHash`/`VersionedStoreName` round-trip — these
  are exactly the fields `VersionedCommitLogEntry::new` re-hashes
  (versioning.rs:422-429); their faithful round-trip is precisely what
  "faithful body recomputes to the carried digest" proves.
- exact sema-engine rev — the spike pins `73eea24`, the mirror's locked rev
  (`5102f5e`'s `Cargo.lock`), not a floating `branch = main`.

Tamper sensitivity (so the refusal actually fires): the substituted-genuine-body
case proves a body that DECODES but recomputes to a different digest (the exact
chain-consistent-carried-digest-with-wrong-payload attack the bead describes);
the byte-mutated and garbage cases prove an undecodable body is also refused.
Both collapse to `addresses_to == false` in the design.

DETERMINISM VERDICT: HOLDS, unconditionally on this rev. Caveat (not a failure):
determinism is contingent on the body being a real `rkyv(VersionedCommitLogEntry)`
under the same rkyv feature set, and on sema-engine's `from_entry_fields`
domain-separation scheme not changing — both true at `73eea24`; a future
sema-engine bump that alters either would require re-running this proof (this is
the payload-awareness coupling named in the RISK section).

## Are all three acceptance criteria satisfiable as designed?

Yes.

1. typed `ContentAddressing` in contract/meta (`meta-signal-mirror`
   `StoreRegistration`) + storage (`mirror` sema `StorePolicy`/`RegisteredLedger`),
   set at registration — satisfied, on the existing retention precedent.
2. `into_decision` recomputes for `SemaVersionedLog` and refuses `DigestMismatch`
   before landing; `Opaque` is a default-path no-op (absence-of-row ⇒ Opaque,
   first match arm returns None) — satisfied, and the recompute is proven
   deterministic.
3. one in-process Nix flake check witnessing both refusal-not-persisted and
   match-lands (plus an Opaque control) — satisfied, on the existing
   `landed_body_readback` check shape.

## Deviations from the bead

- The bead pointed at `RecordFamily::versioning_policy()` (store.rs:280) as the
  per-family shape to reuse. That call is the mirror's OWN-store engine-wide
  `VersioningPolicy` (dogfooding), NOT a per-mirrored-store policy. The design
  instead reuses the truer in-repo precedent — the RETENTION per-store policy
  family (meta enum + local enum + separate family + boundary map) — which is a
  better structural fit and avoids perturbing existing family schema hashes. The
  generated `RecordFamily` surface is still extended (a 5th `policy_family()`),
  honoring the spirit of "fit the existing generated-family shape."
- The bead anchors are at mirror rev `5102f5e` (cargo checkout), which is AHEAD
  of the on-disk `criome-auth-witness` worktree; the implementer must target the
  `5102f5e`/`main` line, not that worktree.

## Unknowns / follow-ups for the implementer

- Confirm sema-engine open/register semantics: is registering a 5th family under
  `SchemaVersion::new(1)` a compatible additive evolution, or does it want a
  version bump? (Conservative: bump to `new(2)`.)
- Confirm `meta-signal-mirror` is regenerated from `schema/lib.schema` via the
  schema-rust flow and bumped; identify every consumer that pins it and emits
  `RegisterStore` so the wire-shape change is landed coherently (producers before
  consumers).
- Decide guard scope: all `&entries` (uniform, safer, re-hashes idempotent
  re-sends) vs `&novel` (cheaper). Design recommends all-entries; either is
  correct.
- Re-run the determinism spike if the sema-engine pin under branch `main` has
  moved past `73eea24` by implementation time.

## Cleanliness

Tracked repos carry no feature changes from this work: `git -C
/home/li/primary status --porcelain` is empty except this report under
`agent-outputs/`; the determinism spike lives only in `/tmp/p0gg-determinism-spike`.
No commit, no push, no edits to any mirror/signal-mirror/sema-engine source.
