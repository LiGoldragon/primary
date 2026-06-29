# Two-VM criome-auth witness — FULL-BODY replication, prometheus run, v3

Extends `agent-outputs/CriomeAuthWitness/CriomosImplementer-WitnessRunEvidence-v2.md`
(the L1–L6 chain @ `fa449abf`, which proved the carried DIGEST lands). This v3
closes the full-body step: the REAL record BODY (`rkyv(VersionedCommitLogEntry)`)
is forwarded across the criome gate, durably lands in node-b's mirror, and is
read back OUT of the running mirror and RE-HASHED INSIDE THE VM through
sema-engine to reproduce the record's real head — full-body replication, not
just a digest. Re-ran twice on prometheus with real KVM boots; the full chain
(L1–L6 incl. both negatives) PLUS the new L5-body full-body proof GENUINELY
PASSES. Nothing landed on any production main.

Builds on the three enablers in
`agent-outputs/CriomeAuthWitnessFullBody/GeneralCodeImplementer-WitnessEnablersEvidence.md`
and the real-body mechanism in `…-RealBodyEvidence.md`.

## (1) What changed + files

### mirror — branch `criome-auth-witness` @ `5102f5ed` (base `0bc196e0`)
The in-VM full-body verifier and its single-source-of-truth re-hash.

- `src/readback.rs` (NEW): `LandedBody` newtype over the octets a mirror handed
  back, with `content_address(&self) -> Result<EntryDigest>`. Decodes the body
  as `rkyv(VersionedCommitLogEntry)`, reconstructs through the PUBLIC
  `VersionedCommitLogEntry::new` (which recomputes the digest from the entry's
  structured fields), and returns the re-derived sema-engine content address.
  This is the SINGLE source of truth for the re-hash — both the verifier bin and
  the in-process readback test use it.
- `src/bin/mirror_landed_body_verifier.rs` (NEW): the `mirror-landed-body-verifier`
  witness bin (`LandedBodyVerifier`). Reads `MIRROR_SOCKET` / `WITNESS_STORE`
  (default `spirit`) / `EXPECTED_HEAD_HEX`; sends `Input::Restore` over the
  working socket, decodes the BINARY `Output::Restored` reply directly (no NOTA
  byte-list parsing), re-derives the suffix[0] body's content address via
  `LandedBody`, and exits nonzero unless the 32 digest BYTES equal the expected
  head AND the mirror's carried head digest equals it. Prints one evidence line
  `LANDED_BODY_REHASH … MATCH`. Pure-logic unit tests for the digest-hex decode.
- `src/client.rs`: added `DaemonSocket::request(input) -> Result<Output>` (the
  typed binary round-trip the NOTA CLI and the verifier both ride); refactored
  the CLI `run` to use it (removed duplicated encode/decode).
- `src/error.rs`: added `Error::LandedBodyDecode(String)` (typed boundary error
  for a body that is not a versioned-log entry).
- `tests/landed_body_readback.rs`: refactored to re-derive through
  `LandedBody::content_address` — so the existing green Nix check
  `mirror-restore-hands-back-landed-body` now proves the EXACT path the in-VM bin
  uses. Removed the now-unused inline reconstruction + import.
- `Cargo.toml`: version `0.1.1 → 0.1.2`; new `witness = ["nota-text"]` feature;
  new `[[bin]] mirror-landed-body-verifier` (`required-features = ["witness"]`).
- `flake.nix`: new `packages.witness` (`--features witness`, pname
  `mirror-witness` — the daemon + nota-text CLIs + verifier bin node-b installs);
  new check `mirror-landed-body-verifier-builds`.

No `signal-mirror` / `signal-frame` change: the verifier uses the existing
binary `encode_signal_frame`/`decode_signal_frame` surface. signal-mirror 0.1.1
(`34ed3fdd`) and signal-frame 0.3.0 (`b78c8077`) are unchanged — the wire is NOT
split.

### CriomOS-test-cluster — branch `criome-auth-witness` @ `b0b30951` (base `fa449abf`)
The witness now forwards the real body and re-hashes it in the VM.

- `flake.lock`: re-pinned the ROOT inputs to the enabler revs — spirit
  `57eb6475` (its own lock re-pins meta-signal-spirit `98704a35`), router
  `2f4e51d5`, mirror `5102f5ed` (my new rev); criome `4dc374f2` unchanged.
- `lib/mkCriomeAuthWitnessTest.nix`:
  - `mirrorPackage = inputs.mirror.packages.${system}.witness` (was `.default`).
  - `baseNode`: `/run/witness` tmpfiles dir on both nodes; new `witnessBodyPath`.
  - L3: after `ObserveHead`, source the REAL head ENTRY BODY via
    `meta-spirit '(ObserveHeadObject)'`, extract the `(Some <hex>)` body, decode
    with `xxd -r -p` to `/run/witness/entry.body` on BOTH nodes.
  - All THREE forwards (both negatives + the positive) now set
    `ENTRY_BODY_PATH=/run/witness/entry.body`, so every forward carries the
    IDENTICAL genuine body and the registered key stays the ONLY difference
    between refuse and accept.
  - L5-body (NEW): after the head lands, publish a zero-coverage checkpoint
    (`PublishCheckpoint (spirit 1 0 0000…0000 [])`) and run
    `mirror-landed-body-verifier` IN THE VM; assert it succeeds and its output
    carries `MATCH` + the real head.

## (2) Why the cross-component re-hash is sound (the make-or-break)

The body is serialized by spirit (its `versioned_log_head_object`, byte-identical
to the production `ComponentShipper::envelope_for_entry` call) and decoded by the
mirror-crate verifier. Spirit's sema-engine (branch=main, locked `98ba507b` in
spirit's tree) and the mirror's sema-engine (branch=main, locked `73eea24b`)
differ ONLY by the `0.6.2 → 0.6.3` version bump and subscription-export lines:
`git diff 73eea24b 98ba507b -- src/versioning.rs` is EMPTY, and the rkyv feature
set (`std bytecheck little_endian pointer_width_32 unaligned`) is identical. So
`VersionedCommitLogEntry`'s rkyv layout and `EntryDigest::from_entry_fields`
digest derivation are byte-identical across both daemons — the body round-trips
and re-hashes deterministically. The live VM run is the final proof (below).

## (3) Reproduce command + clean rev + forced-boot mechanism

Clean committed rev the witness ran at (pushed):
`CriomOS-test-cluster criome-auth-witness @ b0b309511a7909a6f80918c9572afaa2db0a3a6a`.

```sh
# from a clean checkout of the witness branch (refuses a dirty tree; pins the rev):
scripts/run-criome-auth-on-prometheus
# or the exact command run this session, ON prometheus:
nix run github:LiGoldragon/CriomOS-test-cluster/b0b309511a7909a6f80918c9572afaa2db0a3a6a#test-criome-auth-witness
```

How it forces a REAL boot every invocation: the app's program is the
`runNixOSTest` DRIVER. `nix run` builds/caches only the driver package + the two
node closures; the QEMU boot happens when the driver RUNS, every invocation — a
cached `checks` realisation cannot satisfy it. The boot MUST run natively on
prometheus: ouranos (laptop) is forbidden QEMU, and prometheus's
`/etc/nix/machines` lacks the `nixos-test` feature so the boot cannot be
remote-scheduled — prometheus's LOCAL nix (`system-features = … kvm nixos-test`)
runs it. Forced-boot PROVEN by two consecutive invocations at the SAME committed
rev each booting a DISTINCT fresh QEMU pair:
- Run 1 (`2026-06-29T09:22:43Z`): QEMU `node-b pid 688130`, `node-a pid 688131`.
- Run 2 (`2026-06-29T09:26:20Z`): QEMU `node-b pid 688241`, `node-a pid 688242`.
A store-realized `checks` output never produces fresh distinct QEMU pids.

## (4) Full evidence bundle — PROMETHEUS RUN (rev b0b30951, run 1, 09:22:43Z)

All lines are durable-state / driver-introspection observations (typed CLI
replies, unit states, the verifier's exit code + printed re-hash), not daemon
printlns of internal state.

- **L1 — VM booted on prometheus (KVM).** `RUN_HOST=prometheus`,
  `RUN_KVM=present`, `RUN_SYSTEM_FEATURES=system-features = benchmark big-parallel
  kvm nixos-test`, `RUN_REVISION=b0b30951…`. Driver: `node-a/node-b: starting vm`;
  `node-b: QEMU running (pid 688130)` / `node-a: QEMU running (pid 688131)`;
  `connected to guest root shell` on both.

- **L2 — six daemons active, distinct identities.** `L2 OK: criome+router+spirit
  (node-a) and criome+router+mirror (node-b) active; distinct identities`.

- **L3 — real Spirit record seeded; fail-closed; REAL head + REAL BODY read.**
  `(Imported (1 (1 11590050586725752087)))`; ordinary working-socket Record
  refused `(ReferentGuardianRejected (HarnessUnavailable [] [guardian is required
  but no guardian agent is configured]))`; `ObserveHead =
  326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a`;
  **`L3 OK: real head ENTRY BODY sourced (ObserveHeadObject); body octets = 320`**
  (the rkyv `VersionedCommitLogEntry` body, decoded to a file on both nodes).

- **L5-prep — mirror store registered, head empty.** `(HeadsObserved [(spirit
  None)])`.

- **L6 pre — receiver ingress reachable.** node-b router TCP :7440 reachable
  from node-a.

- **L6a (negative 1, UNREGISTERED signer, carrying the REAL body) — refused with
  reason; mirror empty.** criome B `(LookupIdentity (Host node-a)) → UnknownIdentity`
  before the forward. `WITNESS_PUBLIC_KEY=a6d76b1a…` then `(ForwardRefused
  AttestationInvalid)`. Mirror heads after: `(HeadsObserved [(spirit None)])`.

- **Trust handshake.** `(IdentityReceipt ((Host node-a) Active))`.

- **L6b (negative 2, REGISTERED identity + FOREIGN signature, carrying the REAL
  body) — refused with reason; mirror still empty.** `WITNESS_PUBLIC_KEY=b0a33ce5…`
  (FOREIGN: `b0a33ce5… != a6d76b1a…`, asserted) then `(ForwardRefused
  AttestationInvalid)`. Mirror heads after: `(HeadsObserved [(spirit None)])`.

- **L4 (positive) — verified + accepted.** `WITNESS_PUBLIC_KEY=a6d76b1a…` (the
  SAME registered matching key as negative-1) then `(ForwardAccepted 0)`.

- **L5 (durable mirror landing) — REAL record LANDED.** `L5 mirror heads after
  accept: (HeadsObserved [(spirit (Some (1 326640ace3…b85a)))])`; mirror head ==
  the real forwarded spirit head.

- **L5-body (FULL-BODY proof, the new link) — the landed BODY re-hashes IN THE VM
  to the real head.** Checkpoint: `(CheckpointPublished (spirit 1 0))`. Verifier:
  ```
  LANDED_BODY_REHASH store=spirit octets=320 rederived=326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a carried=326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a expected=326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a MATCH
  ```
  The bin re-derived the digest from the body it read back over `Restore` and
  asserted the 32 digest BYTES equal the real head (exit 0). `rederived` ==
  `carried` == `expected` == `326640ace3…b85a`.

- `WITNESS GREEN (full chain): … the carried Append durably LANDED in the mirror
  with head == the real spirit head. The landed BODY was then read back over
  Restore and RE-HASHED IN THE VM through sema-engine to reproduce the real head
  — full-body replication, not just a digest. The registered matching key is the
  sole gate.`

Driver finish: `(finished: run the VM test script, in 12.37 seconds)`; `test
script finished in 12.44s`; `cleanup` clean; no `Traceback`, no
`RequestedAssertionFailed`, no `AssertionError`. `DRIVER_EXIT=0`.

### Run 2 (same rev, consecutive, 09:26:20Z) — identical pass, fresh boot
QEMU `node-b pid 688241` / `node-a pid 688242` (DISTINCT from run 1). Same chain;
same `LANDED_BODY_REHASH … 326640ace3…b85a … MATCH`; `test script finished in
12.67s`; `DRIVER_EXIT=0`. Per-boot keys DIFFER (run 2 node-a key `844ed875…`,
foreign `a54089a9…`) — fresh per-boot criome identities prove genuine boots, not
a replayed cache; within the run node-a's key is the SAME in negative-1 and the
positive (registered matching key is the sole gate) and the foreign key differs.
The real head `326640ace3…b85a` is IDENTICAL across both runs (content-addressed)
and the landed body re-hashes to it in both — the un-fakeable determinism.

## (5) PASS / FAIL of every link

| Link | Claim | Result |
|---|---|---|
| L1 | VM boots natively on prometheus (KVM) | PASS (QEMU 688130/688131; run 2 688241/688242) |
| L2 | six daemons active, distinct identities | PASS |
| L3 | real Spirit record seeded; fail-closed; REAL head + REAL BODY (320 octets) | PASS |
| L6a (neg 1) | unregistered signer (real body) refused with reason; mirror empty | PASS (`UnknownSigner → AttestationInvalid`) |
| L6b (neg 2) | registered identity + foreign signature (real body) refused; mirror empty | PASS (`InvalidSignature → AttestationInvalid`; `b0a33ce5… != a6d76b1a…`) |
| L4 | registered matching-key forward verified + accepted | PASS (`ForwardAccepted 0`) |
| L5 | carried Append durably LANDS; head == real record head | PASS (`(spirit (Some (1 326640ace3…)))`) |
| **L5-body** | **landed BODY read back + RE-HASHED IN THE VM == real head (32-byte compare)** | **PASS** (`LANDED_BODY_REHASH … MATCH`, octets=320, exit 0) |

Two consecutive real boots at the clean rev, both `DRIVER_EXIT=0`.

## (6) Branches + revisions (all pushed; gated on the re-audit; NOT on any main)

| Repo | Branch | Rev | Role this run |
|---|---|---|---|
| CriomOS-test-cluster | `criome-auth-witness` | `b0b309511a7909a6f80918c9572afaa2db0a3a6a` | the full-body witness + re-pin — the clean rev it ran at |
| mirror | `criome-auth-witness` | `5102f5ed87d10d6a7386358b3b10214a04fdf89d` | NEW: `LandedBody` re-hash + `mirror-landed-body-verifier` bin + witness package (base `0bc196e0`) |
| router | `criome-auth-witness` | `2f4e51d57d4671bff0cfb38302e7f29ea6edc5b4` | pinned (enabler, untouched): `router-forward-witness` reads `ENTRY_BODY_PATH` |
| spirit | `criome-auth-witness` | `57eb6475df2a186455b9749118f96ef2720ef28d` | pinned (enabler, untouched): owner-only meta `ObserveHeadObject`; re-pins meta-signal-spirit `98704a35` |
| meta-signal-spirit | `criome-auth-witness` | `98704a3573cd22aec80349b6b16b82fb2ada6499` | pinned (enabler, untouched, via spirit): `ObserveHeadObject` meta op |
| criome | `criome-auth-integration` | `4dc374f261db5d8d2bb62cb614f42a8592bca86f` | pinned (untouched): configurable node_identity + distinct-identity trust |

ROOT input revs verified from the committed `flake.lock` at `b0b30951` (the lock
also carries unrelated TRANSITIVE sema/mirror/spirit nodes pulled by CriomOS/lojix
— those are NOT the witness daemons). Wire generation unchanged: signal-frame
0.3.0 / signal-mirror 0.1.1 / signal-criome 0.6.0 — NOT split.

## (7) Durable Nix checks (built on the prometheus remote builder)

| check | repo/rev | result |
|---|---|---|
| `mirror-landed-body-verifier-builds` | mirror `5102f5ed` | PASS (exit 0; verifier bin compiles under `--features witness`; digest-hex decode unit tests) |
| `mirror-restore-hands-back-landed-body` | mirror `5102f5ed` | PASS (exit 0; now re-derives through the SAME `LandedBody::content_address` the in-VM bin uses) |

Inner-loop (laptop cargo) before push: `cargo build/test --features witness`
(verifier bin: 3 unit tests pass), `cargo test --test landed_body_readback`
(1 pass), `cargo clippy --all-targets --features witness -- -D warnings` clean,
`cargo fmt --all --check` clean.

## (8) Remaining weaknesses (for the auditor / psyche)

1. **Ingest spoofing gap UNCHANGED (honest).** The mirror still trusts the
   carried digest at ingest: a criome-AUTHORIZED but malicious sender could ship
   a body whose digest it lies about and the mirror would land it. The witness
   detects this AFTER landing by re-hashing (L5-body), but the mirror does not
   refuse it at ingest. Closing it cleanly needs the typed per-store
   `ContentAddressing` policy (`Opaque` default | `SemaVersionedLog`
   self-validating, refusing `DigestMismatch` in `CheckedAppend::into_decision`)
   — a real signal/meta/storage/decision feature, not yet accepted, NOT forced
   here. This is the primary open surface.
2. **The two negatives both surface at the router as `AttestationInvalid`**
   (criome maps `UnknownSigner` and `InvalidSignature` to one router reason). The
   witness distinguishes them structurally: negative-1 runs when criome B
   `(LookupIdentity (Host node-a)) = UnknownIdentity`; negative-2 asserts the
   presented key differs from the registered key. The per-decision branch is
   unit-proven in `criome/tests/distinct_node_identities.rs`. Unchanged from v2.
3. **Sender leg is `router-forward-witness` (a bin), not a router daemon outbound
   forward** (no router ingress attaches a `RoutedContractObject` to an OUTBOUND
   message). The bin uses the router's OWN production `CriomeForwardAttestation`,
   so every signature/verification is real; the RECEIVER is the full daemon.
   Unchanged from v2.
4. **Daemons run as root in throwaway guests** — proves the auth/verify/durable
   landing + full-body re-hash logic, NOT production per-user socket isolation
   (carried by the hardened CriomOS modules, boot-proven separately).
5. **The verifier re-does `Restore` over the wire** (read-only) to decode the
   binary `Output::Restored` directly rather than parsing the NOTA byte-list the
   CLI would print; the testScript publishes the checkpoint via the `mirror` CLI.
   Restore is read-only, so the double call (none here — only the bin restores)
   is safe.
6. **Benign log noise** (unchanged): node-b `router-daemon-tailnet: … early eof`
   is the router logging the forward-witness bin's one-shot TCP close; it does
   not affect any link (the test reads typed replies + the bin's exit code).

## (9) Host safety / boundaries

Every boot was a hermetic `runNixOSTest` driver run on prometheus
(`system-features = … kvm nixos-test`); no production `Switch`, no touching
prometheus live services/network; VMs are throwaway guests. ouranos never fired
QEMU. No secrets in any output (the BLS public keys are public material).
Nothing landed on any production main; all branches pushed and gated on the
independent re-audit.
