*Kind: Mockup Report · Topic: spawn-envelope-and-durable-identity · Date: 2026-05-24 · Lane: second-designer (sub-agent D)*

# 172 · 4 — SpawnEnvelope `parent_authority` + DurableIdentity via SO_PEERCRED

## §1 Locator

- **Worktree:** `/tmp/mockup-d-durable-identity`
- **Repo:** `/git/github.com/LiGoldragon/signal-engine-management`
- **Branch:** `feature/durable-identity-via-peercred`
- **Commit short id:** `0eeae13e`
- **Bead:** `primary-p0ke` ("[mockup] SpawnEnvelope parent_authority + DurableIdentity via SO_PEERCRED (second-designer/172 slice D)")
- **Pushed to origin:** yes (`https://github.com/LiGoldragon/signal-engine-management/pull/new/feature/durable-identity-via-peercred`)
- **Recommendation:** operator integrate as-is, with one operator decision (see §7): where the new identity types should ultimately live — in this crate, in `signal-persona-origin`, or split.

## §2 What changed

### §2.1 New module `src/identity.rs`

Exposes the stable durable identity surface. Public API:

- `ProcessIdentifier(u32)` — newtype around the kernel PID returned by `SO_PEERCRED`. `NotaTransparent` so it round-trips as a bare integer.
- `UnixGroupIdentifier(u32)` — newtype around the kernel GID. `NotaTransparent`.
- `ParentAuthority { parent_process_identifier, parent_unix_user_identifier }` — record carrying the supervisor's verifiable identity. `NotaRecord` so it round-trips as a two-element positional tuple.
- `PeerCredentials { process_identifier, unix_user_identifier, unix_group_identifier }` — kernel-supplied credentials read from `SO_PEERCRED`. `NotaRecord`, three-element positional tuple. `Copy` so the verifier can pass it by value without disturbing borrow patterns.
- `DurableIdentity { engine_identifier, peer_credentials }` — the bound identity. `NotaRecord`.
- `IdentityError` — `ProcessIdentifierMismatch { expected, actual }`, `UnixUserIdentifierMismatch { expected, actual }`, `PeerCredentialsReadFailed(String)`. Implements `std::error::Error` + `Display`.
- `PeerCredentialsSource` — trait abstracting the `SO_PEERCRED` read. Supervised daemons supply the implementation (the contract crate stays I/O-strategy agnostic; see §3).
- `verify_spawn_envelope_origin(source, stream, envelope) -> Result<DurableIdentity, IdentityError>` — the combined read + verify + bind step.
- `verify_peer_credentials_against_envelope(envelope, peer) -> Result<(), IdentityError>` — pure verification, exposed for callers that already hold a `PeerCredentials` value.

### §2.2 New field `parent_authority` on `SpawnEnvelope`

```rust
pub struct SpawnEnvelope {
    pub engine_identifier: ...,
    // ... existing fields ...
    pub engine_management_protocol_version: EngineManagementProtocolVersion,
    // DESIGN-DECISION-REVIEW (second-designer/172 §3.4)
    pub parent_authority: identity::ParentAuthority,
}
```

Positional NOTA encoding appends one trailing record. Concrete change to the existing canonical wire form:

```text
old: "(... 1)"
new: "(... 1 (4242 0))"
```

(`(4242 0)` = `parent_process_identifier`, `parent_unix_user_identifier`.)

### §2.3 Architecture documentation

`ARCHITECTURE.md` gets a new section "Stable Durable Identity (`identity` module)" explaining the field semantics and the bind-and-verify flow.

### §2.4 Nix check

`flake.nix` gains a `test-durable-identity` derivation matching the existing per-test crane pattern.

## §3 Why `PeerCredentialsSource` is a trait, not a concrete implementation

The crate sets `unsafe_code = "forbid"`, and the only way to read `SO_PEERCRED` without unsafe on stable Rust today is `std::os::unix::net::UnixStream::peer_cred` — which is gated behind the unstable `peer_credentials_unix_socket` feature. Stable callers either flip the unsafe lint, depend on `rustix` / `nix`, or wait for stabilisation.

A contract crate should not pick that for the consumer. So `PeerCredentialsSource` is a trait, and supervised daemons supply the implementation. A daemon's typical implementation (documented in the trait's rustdoc and reproduced here):

```rust
struct RustixPeerCredentialsSource;

impl PeerCredentialsSource for RustixPeerCredentialsSource {
    fn read_peer_credentials(&self, stream: &UnixStream)
        -> Result<PeerCredentials, IdentityError>
    {
        let raw = rustix::net::sockopt::socket_peercred(stream)
            .map_err(|error| IdentityError::PeerCredentialsReadFailed(error.to_string()))?;
        Ok(PeerCredentials::new(
            ProcessIdentifier::new(raw.pid.as_raw_nonzero().get() as u32),
            UnixUserIdentifier::new(raw.uid.as_raw()),
            UnixGroupIdentifier::new(raw.gid.as_raw()),
        ))
    }
}
```

The trait gives tests a fixture point that does not require a real Unix-stream pair from two different processes with controlled PID / UID — which is what makes the mockup's verifier tests deterministic.

## §4 Test that demonstrates the change works

Nine new tests live in `tests/durable_identity.rs`. Highlights:

- `round_trip_envelope_and_peer_to_durable_identity` — envelope declares `parent_process=100`, `parent_uid=1000`; fixture peer credentials match; `verify_spawn_envelope_origin` mints `DurableIdentity { engine_identifier: "default", peer_credentials: (100, 1000, 1000) }`.
- `verification_rejects_process_identifier_mismatch` — peer reports PID 200, envelope expects 100; verifier returns `IdentityError::ProcessIdentifierMismatch { expected: 100, actual: 200 }` and refuses to mint a `DurableIdentity`.
- `verification_rejects_unix_user_identifier_mismatch` — same shape for UID.
- `process_identifier_mismatch_takes_precedence_over_user_mismatch` — when both disagree, the verifier reports the process-identifier mismatch first. Pins the diagnostic order so refactors do not silently reshuffle it.
- `pure_verification_step_does_not_require_a_stream` — exercises the `verify_peer_credentials_against_envelope` helper directly with three peer-credentials cases (match, process mismatch, user mismatch).
- `parent_authority_round_trips_through_nota_text` — encodes/decodes via `nota_codec`; asserts canonical wire form `(4242 0)`.
- `peer_credentials_round_trip_through_nota_text` — canonical form `(100 1000 1000)`.
- `durable_identity_round_trips_through_nota_text` — canonical form `(default (100 1000 1000))`.
- `spawn_envelope_with_parent_authority_round_trips` — full envelope encodes, decodes, recovers the new field with the expected `(4242 0)` suffix.

The existing tests in `tests/spawn_envelope.rs` and `tests/round_trip.rs` still pass with the fixture extended to set `parent_authority`. Total: **16 tests passing** (3 spawn_envelope + 4 round_trip + 9 durable_identity), 1 doc-test ignored (the trait's `ignore`-marked usage example).

All four checks ran green inside the worktree:

| Check | Result |
|---|---|
| `cargo test` | 16 passed, 0 failed, 1 ignored |
| `cargo fmt -- --check` | clean |
| `cargo clippy --all-targets -- -D warnings` | clean |
| `nix flake check --option max-jobs 0` (run from parent workspace against `git+file:///git/github.com/LiGoldragon/signal-engine-management?ref=feature/durable-identity-via-peercred`) | all checks passed |

## §5 Reference to operator's existing implementation

Before this mockup, the current `SpawnEnvelope` at `src/lib.rs` lines 247-260 carries everything you need to find the supervisor's *sockets* (`manager_socket`) but does NOT carry the supervisor's *identity*. The crate has no SO_PEERCRED-related types and no verifier. The corpus reports `designer/249`, `/299`, `/301`, `/307` describe the design intent; this mockup lands it as code.

What operator can do:

- `git checkout feature/durable-identity-via-peercred` to see the working mockup
- diff against current `main`'s `src/lib.rs` to see exactly what was added
- run `cargo test --test durable_identity` to watch the verifier reject mismatches
- compare to any operator-side work-in-progress: if operator has already started on this slice, the comparison is the value; if operator has done it differently, see §7 for the open decision

If operator integrates as-is, this slice unblocks the receiving-side handshake in every supervised daemon — the daemon caches the envelope, plugs in its preferred `PeerCredentialsSource` (probably backed by `rustix`), and calls `verify_spawn_envelope_origin` from the `accept()` handler.

## §6 Why peer-cred-bound spawn envelope = stable durable ID

The psyche directive: *"stable, durable ID, like you say, peer cred. Yeah, dig deeper into the spawn envelope mechanism."*

The reason the binding gives a stable durable ID:

- **The envelope provides the long-lived identity.** `engine_identifier` is set by the supervisor and survives restarts — the same engine that crashed and got respawned still carries the same `engine_identifier`. So does `component_name`. These names are the *stable* axis: they're what other components reference when they talk about "the mind daemon" or "the spirit daemon."
- **SO_PEERCRED provides kernel-verified per-session credentials.** Every `accept()` carries credentials the connecting peer did not choose — the kernel writes them based on the connecting process's actual identity. The peer cannot spoof. These are the *verifiable* axis.
- **The combination is what makes the identity stable AND verifiable.** `DurableIdentity { engine_identifier, peer_credentials }` ties the long-lived envelope-declared name to the per-session kernel-supplied proof. The engine identifier doesn't change across restarts (stable); the peer credentials prove who is talking right now (verifiable).
- **Without the binding, an attacker who got the envelope content (e.g. from disk state or a leaked debug log) could impersonate.** With the binding, they ALSO need to be running as the declared supervisor PID + UID — which is unforgeable from userspace. The kernel's bookkeeping is the trust root.

The bind-and-verify flow, end to end:

1. **Spawn.** `persona-daemon` (pid `X`, uid `0`) constructs a `SpawnEnvelope` and sets `parent_authority = ParentAuthority::new(ProcessIdentifier::new(X), UnixUserIdentifier::new(0))`. It spawns `mind-daemon` via systemd or fork-exec, passing the envelope (via standard input, environment variable, or a well-known path — orthogonal to this slice).
2. **Receive.** `mind-daemon` decodes the envelope and caches it in process memory. It now knows: "the supervisor that owns me has PID X and UID 0; I will only accept supervisor connections from that pair."
3. **Bind.** `mind-daemon` binds its `engine_management_socket_path` and starts listening.
4. **Connect.** `persona-daemon` connects to that socket (perhaps to send a `Stop` operation or check `ReadinessStatus`).
5. **Accept + verify.** `mind-daemon`'s accept loop wraps the new stream and calls:
   ```rust
   let identity = signal_engine_management::verify_spawn_envelope_origin(
       &rustix_peer_credentials_source,
       &accepted_stream,
       &cached_envelope,
   )?;
   ```
   Internally: the trait reads `SO_PEERCRED` via `rustix::net::sockopt::socket_peercred`; the verifier compares the kernel-reported PID against `parent_authority.parent_process_identifier` and the kernel-reported UID against `parent_authority.parent_unix_user_identifier`; on match it returns `Ok(DurableIdentity { engine_identifier, peer_credentials })`.
6. **Accept or reject.** On `Ok`, the connection IS the trusted supervisor and the daemon proceeds with the engine-management exchange. On `Err(ProcessIdentifierMismatch { .. })` or `Err(UnixUserIdentifierMismatch { .. })`, the daemon closes the connection — somebody else is claiming to be the supervisor but isn't.

After a `mind-daemon` crash and respawn, the cycle is the same with new ephemeral PIDs but the SAME `engine_identifier`. The stable axis survives; the verifiable axis re-anchors on every connection.

The result: every accepted supervisor connection produces a `DurableIdentity` value the daemon can carry through the rest of its request processing. The identity is one record. It is stable across restarts. Its trustworthiness is kernel-guaranteed.

## §7 Open psyche-question for orchestrator / operator

`ProcessIdentifier`, `UnixGroupIdentifier`, `PeerCredentials`, and `DurableIdentity` could conceptually live in `signal-persona-origin` (which already hosts `UnixUserIdentifier`, `OwnerIdentity`, `EngineIdentifier`). They live in this crate in the mockup because they are introduced for `SpawnEnvelope` verification and adding them in-tree keeps the mockup self-contained.

The decision belongs to operator + orchestrator:

| Option | Effect |
|---|---|
| Keep in `signal-engine-management` | self-contained crate, simpler; but couples the identity vocabulary to engine-management |
| Move all four types to `signal-persona-origin` | unified identity vocabulary; can be reused by `owner-signal-persona` and any future origin-aware crate; one more inter-crate change to thread through |
| Split: move `ProcessIdentifier` + `UnixGroupIdentifier` + `PeerCredentials` to `signal-persona-origin`; leave `ParentAuthority` + `DurableIdentity` + verifier here | identity primitives shared, contract surface local |

The third option is probably the cleanest long-term shape, but landing it requires a coordinated PR across the two crates. The mockup defers this choice so the verifier mechanics ship as one digestible diff.

## §8 Recommendation

**Operator integrate as-is**, with two follow-ups operator can sequence:

1. **Add a real `PeerCredentialsSource` implementation in the consuming daemons** (likely `rustix::net::sockopt::socket_peercred`-backed). The mockup's trait + verifier are usable today; only the daemons need to plug in.
2. **Resolve §7** at leisure. The wire format does not change either way — `ParentAuthority` encodes as `(PID UID)` whether the types live here or in `signal-persona-origin`.

If operator has already done this differently (e.g., put the verifier in a separate `persona-handshake` crate, or used `std::os::unix::net::UnixStream::peer_cred` with a `#![feature(...)]` flag on nightly), the mockup is a critique point: the contract crate should not depend on a specific I/O strategy, and the verifier belongs near the types it validates.

## §9 Files changed

| File | Change |
|---|---|
| `src/identity.rs` | new file — types + trait + verifier |
| `src/lib.rs` | re-export `identity::*`; add `parent_authority` to `SpawnEnvelope` |
| `tests/durable_identity.rs` | new file — 9 tests |
| `tests/spawn_envelope.rs` | extend fixture with `parent_authority`; update canonical wire string |
| `ARCHITECTURE.md` | new section "Stable Durable Identity" |
| `flake.nix` | add `test-durable-identity` check |

## §10 References

- `reports/second-designer/172-design-mockup-dispatch/0-frame-and-method.md` §3.4 — slice frame
- `reports/designer/249-component-intent-gap-analysis.md` — SpawnEnvelope + SO_PEERCRED corpus
- `reports/designer/299-design-origin-process-and-agent-identity.md` — accept-time identity
- `reports/designer/301-design-elegant-cli-macro-with-caller-injection.md` — IngressContext composition
- `reports/designer/307-design-golden-ratio-namespace-split.md` — per-message SO_PEERCRED uid checks
- `signal-engine-management` `ARCHITECTURE.md` — refreshed in this branch
