# Two-VM witness enablers — implementation evidence (full-body replication)

Builds the three small VM-path enablers so the two-VM criome-auth witness can
forward the REAL record body and read the LANDED body back to re-hash it. The
witness wiring + prometheus two-VM run is the NEXT task; this builds the enablers
and proves each works (inner-loop cargo + durable Nix checks on the prometheus
remote builder).

## Task and scope

Per `agent-outputs/CriomeAuthWitnessFullBody/GeneralCodeImplementer-RealBodyEvidence.md`
§6 "What the two-VM witness next step must do". Three enablers:

1. SPIRIT `ObserveHeadObject` meta op — surfaces the head entry's real body
   (`rkyv(VersionedCommitLogEntry)`) as a HEX `String` newtype.
2. `router-forward-witness` reads the forwarded `Append` body from
   `ENTRY_BODY_PATH`.
3. A mirror readback path the witness can drive to read the LANDED body back out
   of the running mirror daemon and re-hash it.

Witness branches only; pushed; NOT landed on any production main.

## Branches + revisions (all pushed)

| repo | branch | new rev | base |
|---|---|---|---|
| meta-signal-spirit | `criome-auth-witness` | `98704a3573cd22aec80349b6b16b82fb2ada6499` | `783cd502` |
| spirit | `criome-auth-witness` | `57eb6475df2a186455b9749118f96ef2720ef28d` | `7d1b0697` |
| router | `criome-auth-witness` | `2f4e51d57d4671bff0cfb38302e7f29ea6edc5b4` | `5fe8ceef` |
| mirror | `criome-auth-witness` | `0bc196e05b3646aeaf330183f77be8ace3aff415` | `9a72e87e` |

criome `criome-auth-integration` @ `4dc374f2` was not touched.

## No wire split

signal-frame `0.3.0 @ b78c8077` and signal-mirror `0.1.1 @ 34ed3fdd` are
byte-identical pins across spirit, router, and mirror after this work. router and
mirror `Cargo.lock` were not touched at all; spirit's only `cargo update` was
`-p meta-signal-spirit` (1 package). meta-signal-spirit's own version moved
`0.3.0 -> 0.4.0` (its meta contract, not a shared wire crate). Enabler #3 was
deliberately built WITHOUT touching signal-mirror — see the decision note below.

## Enabler 1 — SPIRIT `ObserveHeadObject` meta op

### Files changed

- `meta-signal-spirit/schema/meta-signal.schema`: added the `ObserveHeadObject`
  input verb, the `HeadObjectObserved` output verb, and the types
  `HeadObjectHex String`, `SelectedHeadObject (Optional HeadObjectHex)`,
  `VersionedLogHeadObject { DatabaseMarker SelectedHeadObject }` — a `String`
  newtype exactly like the sibling `HeadDigestHex`, NOT `Bytes`/`FixedBytes`, so
  the lean default meta-signal tree stays free of `nota` (the
  `dependency_boundary` architectural-truth test passes).
- `meta-signal-spirit/src/schema/meta_signal.rs`: REGENERATED via the established
  flow (`META_SIGNAL_SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo build`); not
  hand-written. `Cargo.toml` `0.3.0 -> 0.4.0`.
- `spirit/src/store/mod.rs`: new `Store::versioned_log_head_object(&self) ->
  Result<Option<Vec<u8>>, StoreError>` — read sibling of `versioned_log_head`,
  serializing the head entry with the SAME call the production
  `mirror::ComponentShipper::envelope_for_entry` uses
  (`rkyv::to_bytes::<rkyv::rancor::Error>(entry)`); byte-identical to the shipped
  body, no invented format.
- `spirit/src/engine.rs`: new `Engine::observe_head_object[_async]` — maps the
  store octets to lowercase hex (`format!("{byte:02x}")` per byte) wrapped in the
  generated `HeadObjectHex`/`SelectedHeadObject`/`VersionedLogHeadObject`.
- `spirit/src/daemon.rs`: dispatch arm
  `MetaInput::ObserveHeadObject => engine.observe_head_object_async().await`.
- `spirit/tests/observe_head_object.rs`: new test (rides on `test-nota-text`).
- `spirit/flake.nix`: new named check `spirit-observe-head-object-rehashes-to-head`.
- `spirit/Cargo.lock` + `spirit/flake.lock`: re-pinned meta-signal-spirit to
  `98704a35` (0.4.0).

### Exact op shape the witness uses

- CLI: `SPIRIT_META_SOCKET=<node-a meta socket> meta-spirit "(ObserveHeadObject)"`
  (the `meta-spirit` bin requires the `nota-text` feature; reads
  `SPIRIT_META_SOCKET`, default `/tmp/meta-spirit.sock`).
- Reply NOTA shape:
  `(HeadObjectObserved (<DatabaseMarker> (Some <hex>)))`, or
  `(HeadObjectObserved (<DatabaseMarker> None))` for an empty store.
- `<hex>` is lowercase hex of `rkyv::to_bytes::<rancor::Error>(head
  VersionedCommitLogEntry)` (for the seeded witness record: 320 octets = 640 hex
  chars). Decode with `xxd -r -p` to the binary `ENTRY_BODY_PATH` file.
- Sibling `(ObserveHead)` returns `(HeadObserved (<DatabaseMarker> (Some
  <64-hex-digest>)))`; that 64-hex digest is the `HEAD_DIGEST_HEX` the witness
  forwards. Both come from the same seeded head entry, so body and head are
  consistent by construction.

### Proof (actual output)

Inner-loop `cargo test --features nota-text --test observe_head_object -- --nocapture`:

```
running 2 tests
test empty_store_reports_no_head_object ... ok
OBSERVE_HEAD_OBJECT head digest = 326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a
OBSERVE_HEAD_OBJECT body octets = 320
test observe_head_object_returns_the_real_body_that_rehashes_to_the_head ... ok
test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

The test seeds the EXACT witness `Import` (`witness-record-1`), reads the hex
body, decodes it, and reconstructs through the PUBLIC
`VersionedCommitLogEntry::new(store_name, schema_hash, commit_sequence, snapshot,
previous_entry_digest, operations)` (which recomputes the digest from the decoded
fields). The re-derived `entry_digest()` equals the store's own
`versioned_log_head()` AND equals `ObserveHead`'s hex —
`326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a`, i.e. the
task's `326640ace3…b85a`. The hex also decodes to byte-for-byte the store's
serialized head entry.

Durable Nix (prometheus, release, `--locked`):
`nix build .#checks.x86_64-linux.spirit-observe-head-object-rehashes-to-head -L`
-> `2 passed`, exit 0, out
`/nix/store/63zckysg8zyrcyd8a64x1k9pia7z1a25-spirit-test-0.18.0`.

## Enabler 2 — `router-forward-witness` reads `ENTRY_BODY_PATH`

### Files changed

- `router/src/bin/router_forward_witness.rs`: new typed `EntryBodySource` enum
  (`ForwardedBodyFile(PathBuf)` | `InlineText(String)` | `HeadDigestHex`),
  resolved once from the environment and lowered to octets. New error variant
  `ReadEntryBody { path, detail }`. `from_environment` now builds the payload from
  `EntryBodySource::from_environment().into_octets(&head_hex)`. Unit tests added.
- `router/flake.nix`: new named check `router-forward-witness-reads-entry-body`.

### Exact env shape the witness uses

`ENTRY_BODY_PATH` (new, optional) — a file of the REAL entry body octets (the
hex-decoded `ObserveHeadObject` body). Precedence: `ENTRY_BODY_PATH` (file) >
`PAYLOAD_TEXT` (legacy inline string) > `HEAD_DIGEST_HEX` (default body). The
file octets become the `Append` `PayloadBytes` byte-for-byte (binary-safe). The
carried head digest stays `HEAD_DIGEST_HEX`. All other env vars unchanged
(`CRIOME_SOCKET`, `ROUTER_PEER_ADDRESS`, `NODE_IDENTITY`, `RECIPIENT_ACTOR` default
`mirror`, `MIRROR_STORE` default `spirit`, `FORWARD_NONCE`).

The criome attestation already binds the FULL routed-object octets
(`ForwardContentPreimage::for_forward` feeds every octet), so swapping
placeholder -> real body keeps the signature binding and only strengthens the
gate. No attestation change.

### Proof (actual output)

Inner-loop `cargo test --features witness --bin router-forward-witness`:

```
running 3 tests
test tests::inline_text_and_head_hex_remain_the_legacy_stand_ins ... ok
test tests::missing_body_file_is_a_typed_read_error ... ok
test tests::forwarded_body_file_octets_are_read_verbatim ... ok
test result: ok. 3 passed; 0 failed; 0 ignored
```

`forwarded_body_file_octets_are_read_verbatim` writes a binary file (incl.
`0x00 0xff 0x80`) and asserts `EntryBodySource::ForwardedBodyFile(path)
.into_octets(head_hex)` returns those octets byte-for-byte — binary-safe, since
the rkyv body is binary.

Durable Nix (prometheus, release, `--locked`):
`nix build .#checks.x86_64-linux.router-forward-witness-reads-entry-body -L`
-> `3 passed`, exit 0, out
`/nix/store/n9adpjvfbh8fgrnbp809f8xivb4v3j3s-router-test-0.4.1`.

## Enabler 3 — mirror readback via `Restore`-after-`Checkpoint` (NO wire change)

### Decision: existing wire ops, not a new signal-mirror op

The brief preferred a new `signal-mirror` read op surfacing `Store::landed_entries`.
That is NOT viable under "signal-mirror 0.1.1 — do NOT split": spirit (links
`mirror::ComponentShipper`, names `signal_mirror::RestoreBundle`) and router (the
witness bin + dev-dep) BOTH link signal-mirror directly, so adding an op forces
signal-mirror `0.1.2` into all three Cargo closures — a genuine version split. The
brief's explicit alternative (Restore-after-checkpoint) needs zero wire change, so
that is what I built. The mirror's `into_decision` accepts ANY checkpoint artifact
for a registered store with no prior checkpoint (payload-blind), and `load_restore`
returns the suffix past `covered_end + 1`; a `covered_end = 0` checkpoint therefore
makes Restore hand back the whole chain, genesis included.

### Files changed

- `mirror/tests/landed_body_readback.rs`: new test. Builds a REAL versioned
  sema-engine store's genesis entry (the same fixture shape as the router fast
  test), lands its rkyv body, publishes a zero-coverage checkpoint, `Restore`s,
  and re-derives the restored body's digest, reproducing the head. No production
  code change in mirror (`Store::landed_entries` from the base rev is unused by
  the wire path and stays for the in-process router test).
- `mirror/flake.nix`: new named check `mirror-restore-hands-back-landed-body`.

### Exact CLI shape the witness uses (captured from the real codec, round-trips)

```
MIRROR_SOCKET=<mirror working socket> mirror "(PublishCheckpoint (spirit 1 0 0000000000000000000000000000000000000000000000000000000000000000 []))"
# -> (CheckpointPublished (spirit 1 0))
MIRROR_SOCKET=<mirror working socket> mirror "(Restore spirit)"
# -> (Restored (<store> <checkpoint> [<entry-envelope> ...]))
```

NOTA encodings (verified, round-trip): `CheckpointArtifact` is
`(<store> <sequence> <covered_end> <digest> <artifact>)`; `(Bytes 32)` renders as
64 lowercase hex chars (any 32 bytes — the mirror is payload-blind on the artifact
digest), variable `Bytes` renders as a list (`[]` empty). `(Restore spirit)` takes
the bare store name. The Restored bundle's suffix carries each `EntryEnvelope`
with the FULL landed payload.

### Proof (actual output)

Inner-loop `cargo test --test landed_body_readback -- --nocapture`:

```
running 1 test
RESTORE_READBACK head = 095b6978f074620867b7bdcb421a1bf7e0b4f9bd776bad231d915b03f1491dc0 body octets = 271
test restore_hands_back_the_landed_genesis_body_which_rehashes_to_the_head ... ok
test result: ok. 1 passed; 0 failed; 0 ignored
```

The test lands the real body, publishes a `covered_end = 0` checkpoint, `Restore`s,
asserts the restored suffix body equals the landed body byte-for-byte, decodes it
(`rkyv::from_bytes::<VersionedCommitLogEntry>`), reconstructs through
`VersionedCommitLogEntry::new`, and asserts the re-derived `entry_digest()` equals
this store's head (and that the carried head digest is that content address). The
head here (`095b6978…`) is this test's self-built body, not Spirit's; the point is
the wire-readback + re-hash MECHANISM (the canonical `326640ace3…` body is proven
in enabler 1).

Durable Nix (prometheus, release, `--locked`):
`nix build .#checks.x86_64-linux.mirror-restore-hands-back-landed-body -L`
-> `1 passed`, exit 0, out
`/nix/store/khh9dqv0j97lz8r24riqhvqlkmv4nl70-mirror-test-0.1.1`.

## The precise recipe the two-VM witness must follow

1. SOURCE the real body + head from node-a's seeded spirit daemon:
   - `meta-spirit "(ObserveHead)"` -> extract the 64-hex digest -> `HEAD_DIGEST_HEX`.
   - `meta-spirit "(ObserveHeadObject)"` -> extract the `(Some <hex>)` body hex ->
     `printf '%s' <hex> | xxd -r -p > /run/witness/entry.body` -> `ENTRY_BODY_PATH`.
   - For the seeded `witness-record-1`, `HEAD_DIGEST_HEX` =
     `326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a`.
2. FORWARD via `router-forward-witness` with `ENTRY_BODY_PATH=/run/witness/entry.body`
   and `HEAD_DIGEST_HEX=326640ace3…b85a` (plus the criome/peer/identity/nonce env).
   The receiver criome-verifies and relays the Append (carrying the REAL body) to
   the co-resident mirror; the head lands at sequence 1 with that content address.
3. READ BACK the landed body from the running mirror daemon over its working wire:
   - `mirror "(PublishCheckpoint (spirit 1 0 0000…0000 []))"` (zero-coverage; any
     32-byte digest, empty artifact — payload-blind).
   - `mirror "(Restore spirit)"` -> the Restored bundle's suffix[0] carries the
     landed body.
4. RE-HASH and compare the 32 DIGEST BYTES (NOT a hex/decimal grep against a Debug
   render — prior auditor trap): decode the restored body with
   `rkyv::from_bytes::<VersionedCommitLogEntry>`, reconstruct through
   `VersionedCommitLogEntry::new(store_name, schema_hash, commit_sequence, snapshot,
   previous_entry_digest, operations)`, take `entry_digest().bytes()` (the 32-byte
   array), and assert it equals the 32 bytes of `326640ace3…b85a`. The mirror
   `landed_body_readback` test is the exact reconstruction the witness's re-hash
   step reuses; the restored body should also equal the forwarded `ENTRY_BODY_PATH`
   octets byte-for-byte (durability).

   The re-hash step is Rust (rkyv + sema-engine), so the witness needs a small
   re-hash binary/step; it can decode the rkyv `Output::Restored` wire reply
   directly to get the body octets rather than parsing the NOTA byte-list.

## What the witness / auditor must know

- Re-pin the witness flake inputs to the four new revs above (meta-signal-spirit,
  spirit, router, mirror). spirit's flake.lock already re-pins meta-signal-spirit
  to `98704a35`.
- signal-frame 0.3.0, signal-mirror 0.1.1 are unchanged — verify no split survives
  the flake re-pin.
- Enabler #3 deliberately uses `Restore`-after-`Checkpoint` instead of a new
  signal-mirror op (the cascade/split reason above). If the psyche later accepts a
  coordinated signal-mirror `0.1.2` bump re-pinned across spirit+router+mirror,
  the cleaner single-op `ObserveLandedEntries` read surface remains available; it
  is NOT done here because it would split the pinned wire.
- The remaining spoofing gap from the prior step is unchanged: the mirror still
  trusts the carried digest at ingest (closing it needs the typed per-store
  `ContentAddressing` policy — a separate accepted feature, not in scope).
- Inner-loop checks run with the laptop toolchain; durable evidence is the three
  named Nix checks built on the prometheus remote builder (all green above).

### Checks run

| check | where | result |
|---|---|---|
| `cargo test --features nota-text --test observe_head_object` | spirit, laptop | pass (head `326640ace3…b85a`) |
| `cargo test --features nota-text --test observe_head` | spirit, laptop | pass (no regression) |
| `meta-signal-spirit` default build + `dependency_boundary` + `frame` | laptop | pass (String newtype keeps nota out of default tree) |
| `cargo test --features witness --bin router-forward-witness` | router, laptop | pass (3) |
| `cargo test --test landed_body_readback` | mirror, laptop | pass |
| `spirit-observe-head-object-rehashes-to-head` | prometheus, release | pass (2), exit 0 |
| `router-forward-witness-reads-entry-body` | prometheus, release | pass (3), exit 0 |
| `mirror-restore-hands-back-landed-body` | prometheus, release | pass (1), exit 0 |
