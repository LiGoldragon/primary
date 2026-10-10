# Real-body criome forward: the LANDED body re-hashes to the record's real head

Implementation evidence. Closes residual #1 from the audit: the forwarded
`Append` carried a PLACEHOLDER body (`b"criome-verified durable append"` under a
synthetic `[0x5a;32]` digest) and the mirror trusted the carried digest without
recomputing it. This change forwards the REAL content-addressed record body and
proves, independently of the mirror's trust, that re-deriving the digest from
the LANDED body reproduces the record's real head.

## Task and scope

Prove the real-body mechanism in a fast Rust integration test FIRST (before VM
work): a criome-verified forward carrying the REAL record body durably lands in
a real mirror, AND re-deriving the digest from the LANDED body reproduces the
record's real head (the value Spirit's `ObserveHead` returns). Build on the
witness branches; do not regress verify-gating; no polling; hardwired grants
only; witness branches only, no production main.

## (1) DESIGN DECISION

### What real content is shipped

The body is `rkyv::to_bytes(VersionedCommitLogEntry)` — the whole sema-engine
versioned-log entry — and the carried digest is that entry's own
`entry_digest()`. This is NOT an invented format: it is byte-for-byte what the
production `ComponentShipper::envelope_for_entry` ships
(`mirror/src/shipper.rs:150-166`), which is the same machinery Spirit uses for
mirror fan-out. The fast test sources it through that exact production method.

### How the head is reproduced from it

The head digest is a domain-separated blake3 over the entry's STRUCTURED fields
(store name, store schema hash, commit sequence, snapshot, previous digest, and
the operation set) — `EntryDigest::from_entry_fields`
(`sema-engine/src/versioning.rs:257-285`), NOT a hash of the rkyv bytes. The
re-derivation therefore decodes the landed body
(`rkyv::from_bytes::<VersionedCommitLogEntry>`), then reconstructs through the
PUBLIC `VersionedCommitLogEntry::new(store_name, schema_hash, commit_sequence,
snapshot, previous_entry_digest, operations)` — which recomputes the digest
internally — and asserts the result equals the source store's head. This uses
only public sema-engine API (the hashing constructor `from_entry_fields` is
`pub(crate)`; `::new` reaches it). No sema-engine change.

### Self-validating mirror vs test re-derive — and WHY

Chosen: the TEST re-derives from the LANDED body (the brief's explicit
fallback), and the mirror append path is UNCHANGED. Reason, with evidence:

- Mandatory mirror self-validation (`hash(body) == carried_digest`) is
  mirror-semantics surgery, not a finishing piece. The mirror is **payload-blind
  by design** (`mirror/Cargo.toml:8`); making the append decision payload-aware
  would break (a) the entire synthetic-body linkage suite
  `mirror/tests/daemon_logic.rs` (it ships `digest=[seed;32]` +
  `PayloadBytes(vec![0xaa, seed])` to exercise sequence-gap/fork/crash-window
  logic) and (b) the EXISTING router landing test itself (it ships
  `b"criome-verified durable append"` under `[0x5a;32]`). Per the brief's
  boundary ("if it forces mirror-semantics surgery, STOP and report"), this is
  out of scope for a non-regressing step.
- The realness is instead proven WITHOUT trusting the mirror: the test reads the
  bytes the mirror durably committed (new `Store::landed_entries`) and re-hashes
  them through sema-engine's own content-addressing. A tampered body would
  re-derive to a different digest and fail the assertion.
- Self-validation IS feasible later with no new dependency (the mirror already
  depends on sema-engine; the `DigestMismatch` refuse reason already exists). The
  clean shape that does NOT regress payload-blindness is a typed per-store
  `ContentAddressing` policy (`Opaque` default vs `SemaVersionedLog`) — see (7).

## (2) Files changed

### mirror — branch `criome-auth-witness` @ `9a72e87` (base `d30cd180`)
- `src/store.rs`: new public `Store::landed_entries(&self, store: &StoreName) ->
  Result<Vec<EntryEnvelope>>` — the read sibling of `persist_suffix`/`load_heads`:
  returns every durably-stored entry for a store as its wire envelope (sequence,
  previous, digest, FULL payload), reusing `ReceivedEntry::to_envelope`. Additive
  read surface only; the payload-blind append path and chain-linkage validation
  are unchanged.
- `Cargo.toml`: version `0.1.0` -> `0.1.1` (additive public API).
- Mirror linkage + arc suites still green (no regression): `cargo test --test
  daemon_logic --test end_to_end_arc` — all pass.

### router — branch `criome-auth-witness` @ `5fe8cee` (base `221b5fb0`)
- `tests/criome_forward_lands_in_mirror.rs`: NEW test
  `criome_verified_forward_lands_the_real_record_body_which_rehashes_to_the_head`.
  Builds a REAL source sema-engine versioned store (asserts one `WitnessRecord`),
  reads its genesis `VersionedCommitLogEntry` + head via the production
  `ComponentShipper::envelope_for_entry`, forwards it criome-verified through
  router B into the co-resident mirror, then reads the LANDED body back
  (`observe_landed_body` -> `Store::landed_entries`) and re-derives its content
  address, asserting it equals the source head and the carried head digest.
  `MirrorBehindComponentSocket` restructured to share the engine
  (`Arc<Mutex<Engine>>`) so the relay's serving task and the test's read drive
  the SAME durable store. Existing landing test untouched and still green.
- `flake.nix`: NEW check `router-criome-forward-lands-real-body-in-mirror` runs
  that test (Nix-owned durable evidence).
- `Cargo.lock`: mirror dev-dep re-pinned `0.1.0` `d30cd180` -> `0.1.1`
  `9a72e87`. Shared wire pins UNCHANGED: signal-frame 0.3.0 (b78c8077),
  signal-mirror 0.1.1 (34ed3fdd), sema-engine 0.6.x — the wire is NOT split.

No sema-engine, signal-mirror, signal-frame, criome, or spirit source changed.

## (3) Test command + actual output (the deliverable)

Inner-loop (laptop cargo), both tests in the file:

```
$ cargo test --test criome_forward_lands_in_mirror
running 2 tests
test criome_verified_forward_lands_an_append_in_the_co_resident_mirror ... ok
test criome_verified_forward_lands_the_real_record_body_which_rehashes_to_the_head ... ok
test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.14s
```

The new test's load-bearing assertions (all passed):
- the forwarded body `!=` the old placeholder `b"criome-verified durable append"`;
- `ForwardAccepted` (criome-verified);
- mirror head advanced empty -> sequence 1 with the entry's real content address;
- the LANDED payload bytes equal the forwarded body byte-for-byte (intact);
- `rkyv::from_bytes::<VersionedCommitLogEntry>(landed body)` decodes;
- `VersionedCommitLogEntry::new(decoded fields).entry_digest() == source head`
  (re-derived from the LANDED body == the value `ObserveHead` returns);
- the carried head digest equals that re-derived content address.

Durable Nix check (built on the prometheus remote builder, release mode):

```
$ nix build ".#checks.x86_64-linux.router-criome-forward-lands-real-body-in-mirror" -L
router-test> +++ command cargo test --release --locked --test criome_forward_lands_in_mirror criome_verified_forward_lands_the_real_record_body_which_rehashes_to_the_head -- --exact
router-test> running 1 test
router-test> test criome_verified_forward_lands_the_real_record_body_which_rehashes_to_the_head ... ok
router-test> test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out; finished in 0.22s
```
out: `/nix/store/25i70iy8yw91zdykjdkvz2nfbpq50k5h-router-test-0.4.1` (exit 0)

## (4) Existing named router checks (inner-loop cargo, all PASS)

```
router_accepts_forward_under_real_criome_bls_attestation ... ok
router_refuses_forwards_without_a_valid_criome_attestation ... ok
router_configuration_carries_listen_identity_and_criome_socket ... ok
router_bootstrap_carries_hardwired_peers_and_actor_homes ... ok
```
Plus the existing landing test (not regressed):
`criome_verified_forward_lands_an_append_in_the_co_resident_mirror ... ok`.
`cargo fmt --all --check` clean for the changed test file (pre-existing
formatting drift in unrelated files `router_forward_witness.rs`,
`configuration_text_edges.rs`, `criome_forward_attestation.rs` was left
untouched — not in scope).

## (5) Branches + revisions

- mirror: `criome-auth-witness` @ `9a72e87e843f8ed12ea94700a3183639088cdedc`
  (base `d30cd180`). PUSHED.
- router: `criome-auth-witness` @ `5fe8ceefb7d80a7edb24d328100a8a15faf767a5`
  (base `221b5fb0`). PUSHED.
- NOT landed on any production main.

## (6) What the two-VM witness (next step) must do

1. **Re-pin** the witness flake: mirror input -> `9a72e87` (0.1.1, has
   `landed_entries`); router input -> the new router rev.
2. **SOURCE the real body from Spirit.** Spirit has the body in-process
   (`Store::versioned_log()` -> `Vec<VersionedCommitLogEntry>`,
   `spirit/src/store/mod.rs`) but NO wire/meta op exposes it. Add a meta op
   `ObserveHeadObject` (extending `ObserveHead`) returning
   `rkyv::to_bytes(head entry)` as a hex/base64 `String` — a String newtype, NOT
   `Bytes`, because `Bytes`/`FixedBytes` pull `nota` into meta-signal-spirit's
   lean default tree (forbidden by its `dependency_boundary` test, exactly the
   constraint the `HeadDigestHex` choice already navigates). The witness calls it
   AFTER the `Import` seeds `witness-record-1`, decodes the hex to a file.
3. **CARRY.** Teach `router-forward-witness` (the sender bin,
   `src/bin/router_forward_witness.rs`) to read the body from an `ENTRY_BODY_PATH`
   env (the file from step 2) as the `PayloadBytes`, keeping `HEAD_DIGEST_HEX`
   (from `ObserveHead`) as the carried digest. Head and body are consistent by
   construction (both from the same Spirit entry). This ~10-line additive change
   was DEFERRED from this step (it is VM-path and cannot be tested without the
   Spirit SOURCE op above; the fast Rust test already proves the mechanism).
4. **ASSERT full-body landing.** The head assertion must compare the 32 digest
   bytes of `326640ace3…b85a` (64 hex or 32 decimal — NOT a hex grep against a
   Debug/decimal render; prior auditor trap). For the BODY itself: the deployment
   wire has no read-one-entry op (`Restore` needs a checkpoint). Either publish a
   checkpoint then `Restore` to fetch the suffix bodies, OR add a `signal-mirror`
   read op surfacing `Store::landed_entries` over the wire (future surface). The
   re-derivation proof itself is already carried by the fast Rust test here.

## (7) Surprises / remaining spoofing gap / scope notes

- **Surprise:** the residual was purely sender-side. Spirit's fan-out and the
  mirror's shipper ALREADY ship the real `rkyv(VersionedCommitLogEntry)` body;
  only the WITNESS senders (the router test + the `router-forward-witness` bin)
  fabricated a placeholder. The body format needed no invention.
- **Criome binding unchanged and intact:** the attestation digest already binds
  over every routed object's octets (`ForwardContentPreimage` /
  `content_digest`), so swapping placeholder -> real body keeps the signature
  binding with zero attestation change — the verify gate only gets stronger
  (the real body is signed). Verify-gating is not regressed.
- **Remaining spoofing gap (honest):** the mirror still trusts the carried
  digest on the append path. A criome-AUTHORIZED but malicious sender could ship
  a body whose digest it lies about; the mirror would land it (the carried digest
  becomes the head) without noticing. The fast test detects this by re-derivation
  AFTER landing, but the mirror does not refuse it at ingest. Closing it cleanly
  needs the typed per-store `ContentAddressing` policy (`Opaque` default |
  `SemaVersionedLog` self-validating), stored at `RegisterStore` (a
  meta-signal-mirror contract + storage change) and read in
  `CheckedAppend::into_decision` (refuse `DigestMismatch` on a re-derive
  mismatch). That is a real feature spanning signal/meta/storage/decision and a
  design choice not yet accepted — recommended as the next scoped step, NOT
  forced here per the brief's stop-and-report boundary.
