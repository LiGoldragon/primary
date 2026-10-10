# Spirit `ObserveHead` — Real Versioned-Log Content Head for the criome-auth Witness

## Task and scope

Let the criome-auth witness forward the REAL content-addressed head of the
seeded Spirit record — the head criome authenticates and the mirror durably
lands — instead of the synthetic stand-in the audit caught.

The prior witness (`CriomOS-test-cluster` branch `criome-auth-witness`,
`lib/mkCriomeAuthWitnessTest.nix`) computed the forwarded head as:

```
head = printf '%s' 'witness-record-1:criome auth witness record' | sha256sum | cut -c1-64
```

That is a sha256 of two Nix string literals — never read from the Spirit
daemon, never tied to the stored record, and not Spirit's content-addressing.

This change adds a minimal Spirit meta op that returns the store's actual
versioned-log head, in the exact hex form the router-forward-witness ingests.

## What was added (op + design)

A new owner-only meta verb `ObserveHead` on Spirit's meta plane (the same
owner-only socket that already carries `Configure` and `Import`).

Design rationale: the meta plane is where the mirror target AND the local criome
gate are already configured (`Configure`). The versioned-log head is exactly
what the configured `CriomeGate` authorizes for fan-out and the configured
mirror durably lands, so the head read is the coherent read sibling of the head
fan-out config — owner-only, on the same plane the witness's node-a already
drives with `meta-spirit`. It is a pure read (no SEMA write, no guardian), so the
witness's guardian-compiled, fail-closed daemon answers it (reads bypass the
guardian exactly as `Marker`/`Version` do).

Reply shape: `HeadObserved VersionedLogHead { DatabaseMarker SelectedHeadDigest }`
where the head is an optional `HeadDigestHex` (a `String` newtype carrying the
`EntryDigest`'s own lowercase-hex `Display`). An empty log reports no head.

The head is NOT re-hashed: it is `sema_engine::EntryDigest::to_string()` of the
store's current `versioned_log_head()` — Spirit's own content-addressing, the
same `EntryDigest` `CriomeGate::LocalHeadCapture::spirit_head` authorizes.

## Files changed

### meta-signal-spirit (wire contract) — branch `criome-auth-witness` @ `783cd5024507bbf339bd92dad3bba38cd64cb40d`
- `schema/meta-signal.schema`: appended `ObserveHead` input verb and
  `HeadObserved` output verb (appended last → existing wire indices preserved);
  added types `HeadDigestHex String`, `SelectedHeadDigest (Optional HeadDigestHex)`,
  `VersionedLogHead { DatabaseMarker SelectedHeadDigest }`.
- `src/schema/meta_signal.rs`: regenerated artifact (schema-rust, via
  `META_SIGNAL_SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo build`).
- `Cargo.toml`: version `0.2.0` → `0.3.0`.
- `tests/round_trip.rs`: updated the verb-list architectural-truth test; added
  `observe_head_input_round_trips` and `head_observed_output_round_trips`
  (present + absent head).

Base for the branch: `83415f2` (the rev spirit a6d69b46 pinned).

### spirit (daemon/engine) — branch `criome-auth-witness` @ `7d1b069718a0ddede6e3928ecef272f25caaee6b`
- `src/store/mod.rs`: `versioned_log_head()` is no longer `#[cfg(feature = "mirror-shipper")]`
  — the head is a fundamental property of the durable log, now read by both the
  criome-gate fan-out path and the meta query, so it is available in the default
  (offline) daemon build. `EntryDigest` moved to the always-on sema-engine import.
- `src/engine.rs`: added `observe_head` / `observe_head_async` producing
  `MetaOutput::head_observed(...)` from `store().versioned_log_head()`.
- `src/daemon.rs`: dispatch the new `MetaInput::ObserveHead` arm.
- `Cargo.toml`: `meta-signal-spirit` pinned to branch `criome-auth-witness`.
- `Cargo.lock`: resolves meta-signal-spirit `0.3.0` @ `783cd502`.
- `flake.nix`: `meta-signal-spirit-source` input → `.../criome-auth-witness`;
  the vendor-source `substituteInPlace` match string updated to the new branch.
- `flake.lock`: `meta-signal-spirit-source` re-locked to `783cd502`.
- `tests/observe_head.rs` (new): the evidence witness.
- `tests/meta_configure.rs`: added the `HeadObserved` arm to an exhaustive match.

Base for the branch: `a6d69b467e80f4c61c0d2e345e80c3b0023098b3` (the "offline
default build" commit, per the task instruction; note the test-cluster witness
flake.lock currently still pins the older `4fce1c5f` — see Notes).

Wire generation kept at signal-frame 0.3.0 (not split): no GenerationPlan
version strings were changed.

## Evidence — real daemon invocation (gold standard)

A real default-build `spirit-daemon` was started over a unix meta socket;
`meta-spirit` seeded the witness's EXACT record and queried the head. Exact
invocations and actual output:

```
$ meta-spirit '(ObserveHead)'                       # empty store, before seeding
(HeadObserved ((0 0) None))

$ meta-spirit '(Import [(witness-record-1 ([(Technology (Software (Programming CodeGeneration)))] Decision [criome auth witness record] High Low Zero []))])'
(Imported (1 (1 11590050586725752087)))

$ meta-spirit '(ObserveHead)'                       # after seeding
(HeadObserved ((1 11590050586725752087) (Some 326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a)))
```

The real content head of the seeded `witness-record-1` is:

```
326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a
```

This is NOT the old synthetic value
`cdc1c22fea273efbade8385bfa0e5c73899bb66632b96949e0952fc77891b718`.

## Evidence — test (`spirit/tests/observe_head.rs`, `--features nota-text`)

```
running 3 tests
test empty_store_reports_no_head ... ok
test observe_head_returns_the_real_stored_content_head ... ok
test the_head_is_content_deterministic ... ok
test result: ok. 3 passed; 0 failed
```

The load-bearing assertion: the op's head equals byte-for-byte the engine's own
`store().versioned_log_head().to_string()` for the witness's exact seeded record
(parsed from the same `Import` NOTA the witness sends) — so it is genuinely tied
to the stored content, not recomputed; it is 64 lowercase hex; it differs from
the synthetic stand-in; and it is content-deterministic across fresh stores
(same spirit build + same record ⇒ same head, so the witness daemon forwards
this same value).

### Other checks run
- meta-signal-spirit: `cargo test --features nota-text` — 9 passed (incl. the new
  round-trips); `cargo test --test dependency_boundary` — 2 passed (the default
  tree stays free of `nota` — see Notes on the encoding choice).
- spirit: `cargo build` (default), `cargo build --features agent-guardian`
  (witness daemon mode), `cargo build --features mirror-shipper` — all compile.
  `cargo test --features nota-text --test meta_configure --test observe_head
  --test daemon_command` — pass. `cargo fmt --all --check` — clean (both repos).
- Nix witness build: `nix build .#packages.x86_64-linux.default` SUCCEEDED — the
  combined `spirit` package (with `meta-spirit` + `spirit-daemon` bins) built from
  the vendored tree, confirming the flake input + vendor-source + substituteInPlace
  wiring resolves and the meta-signal-spirit 0.3.0 contract compiles under Nix in
  the witness's exact package build. This is the durable, Nix-owned evidence.

## Wire / encoding form (auditor's explicit concern)

The head is 32 raw bytes (`sema_engine::EntryDigest([u8; 32])`, a blake3 digest).
The encoding everyone must compare on is **64-character lowercase hex**:

- Spirit reports it as hex via `EntryDigest`'s own `Display` (`{byte:02x}`),
  carried in the `HeadDigestHex` String. The meta reply renders
  `(Some 326640ace3...b85a)`.
- `router-forward-witness` ingests `HEAD_DIGEST_HEX` as exactly 64 hex chars and
  decodes them to the 32 bytes (`ForwardWitness::decode_digest`).
- criome's `ObjectDigest::from_bytes` is the blake3-hex of those same bytes — the
  same hex string — so the authorized object reference matches by construction.
- The mirror's `signal_mirror::EntryDigest` is `FixedBytes<32>` whose NOTA
  encoding (`nota::FixedByteSequence::to_nota`, pinned nota-next `96e64bcd`) is
  ALSO lowercase hex, and `mirror`'s CLI prints replies via `to_nota()`. So
  `mirror '(ObserveHeads (Some spirit))'` renders the landed head as the SAME
  64-char hex — directly comparable to the forwarded `HEAD_DIGEST_HEX`.

The auditor's "32 DECIMAL bytes, not hex" warning is the trap to avoid: do NOT
surface the head via `Debug` (`EntryDigest([185, 23, ...])`) or as a raw byte
vector — those render decimal and would not match. Everything here is hex.

## Branch + revision (deliverable)

- spirit: branch `criome-auth-witness` @ `7d1b069718a0ddede6e3928ecef272f25caaee6b`
  (base `a6d69b46`). Pushed to origin. NOT landed on main.
- meta-signal-spirit: branch `criome-auth-witness` @ `783cd5024507bbf339bd92dad3bba38cd64cb40d`
  (base `83415f2`). Pushed to origin. NOT landed on main.

## Notes for the witness / auditor (follow-up)

1. **Witness testScript change** (`CriomOS-test-cluster` `criome-auth-witness`,
   `lib/mkCriomeAuthWitnessTest.nix`): replace the synthetic `head = ... sha256sum`
   block with a read from the seeded daemon over the meta socket, e.g.:

   ```python
   head_reply = node_a.succeed(
       "SPIRIT_META_SOCKET=${spiritMeta} ${spiritPackage}/bin/meta-spirit '(ObserveHead)'"
   ).strip()
   match = re.search(r"\(Some ([0-9a-f]{64})\)", head_reply)
   assert match, f"ObserveHead must report the real seeded head: {head_reply!r}"
   head = match.group(1)
   ```

   Run this AFTER the meta Import seeds `witness-record-1` (the head is `None`
   before seeding). The forwarded `HEAD_DIGEST_HEX=` + the mirror-landing
   assertion then compare against this real head. The recorded value for the
   witness's record is `326640ace3...b85a` (will match the live daemon since the
   head is content-deterministic for the same spirit build + record).

2. **Re-pin spirit**: the witness flake.lock currently pins spirit `4fce1c5f`
   (stale, before the offline-default-build commit). Re-pin
   `spirit-source`/`spirit` input to spirit `criome-auth-witness`
   (`7d1b0697`). That branch already re-pins its own meta-signal-spirit input, so
   no separate meta-signal-spirit pin is needed by the test-cluster.

3. **Encoding choice rationale (provisional, for review)**: the head digest is a
   `HeadDigestHex` String, not `(Bytes 32)`/`FixedBytes<32>`. `FixedBytes` wraps
   `nota::FixedByteSequence`, which would force `nota` into meta-signal-spirit's
   default (rkyv-only) dependency tree — forbidden by that crate's
   `dependency_boundary` architectural-truth test (the lean offline daemon
   invariant). A hex `String` newtype keeps the default tree nota-free while
   matching criome's own `ObjectDigest` hex convention and `HEAD_DIGEST_HEX`. If
   the psyche/auditor prefers a shared typed digest, the right move is a separate
   non-nota digest newtype in the schema stack, not pulling nota into the lean
   tree.

4. **Durable-landing gap unchanged**: this work only makes the FORWARDED head
   real. The router inbound-delivery gap the witness already documents (verified
   `ForwardAccepted` but the carried `Append` is not yet relayed to the mirror's
   `ComponentSocket`) is untouched and still owned by the router leg.
