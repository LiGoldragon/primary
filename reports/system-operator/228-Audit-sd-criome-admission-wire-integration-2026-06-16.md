# 228 — Audit: SD criome admission gate wire integration

Source under audit:

- `signal-criome` worktree:
  `/home/li/wt/github.com/LiGoldragon/signal-criome/criome-admission-gate`
- `signal-criome` branch head:
  `783cc2fa` (`signal-criome: cluster-root admission contract additions`)
- `criome` worktree:
  `/home/li/wt/github.com/LiGoldragon/criome/criome-auth-pilot`
- `criome` branch head:
  `47b1dd0d` (`criome: admission gate checks the envelope scheme (SO audit 227 P2)`)

## Findings

### P1 — `signal-criome` does not pass its own Nix check

SD's summary says `signal-criome` artifacts were regenerated and the branch
builds clean. That is not true under the repo's Nix contract.

`nix flake check` in
`/home/li/wt/github.com/LiGoldragon/signal-criome/criome-admission-gate`
fails in `checks.x86_64-linux.clippy-nota-text` because the `nota-text`
test targets still construct the old four-field `IdentityRegistration`:

- `tests/canonical_examples.rs:166` constructs `IdentityRegistration` without
  the new `admission` field.
- `tests/round_trip.rs:251` constructs `IdentityRegistration` without the
  new `admission` field.
- `examples/canonical.nota:22` still shows
  `(RegisterIdentity ((Persona alice) public-key-1 fingerprint-1 PersonaRequest))`,
  also missing the new fifth positional field.

The failing Nix log reports:

```text
error[E0063]: missing field `admission` in initializer of `signal_criome::IdentityRegistration`
```

Plain `cargo test --offline` does not catch this because it runs no tests for
the default feature set. The failing path is the branch's real build contract:
the flake's `nota-text`/all-target checks.

Required fix before merge:

- Add `admission: None` to the two Rust fixture constructors.
- Update `examples/canonical.nota` to include the optional admission slot.
- Re-run `nix flake check` in `signal-criome`.

### P2 — the production self-admission ceremony is not enforced yet

The external registration path is gated correctly when a cluster root is
configured:

- `src/actors/registry.rs:96` starts `register`.
- `src/actors/registry.rs:101` gates on `self.cluster_root`.
- `src/actors/registry.rs:102` requires `registration.admission`.
- `src/actors/registry.rs:104` returns
  `RejectionReason::UnauthorizedRegistration` before storing.

But the daemon's own `Host("criome")` identity bypasses the gate even when
`cluster_root` is configured:

- `src/actors/root.rs:283` builds `cluster_root` from startup arguments.
- `src/actors/root.rs:288` starts `IdentityRegistry` with that root.
- `src/actors/root.rs:320` writes directly to `StoreKernel`.
- `src/actors/root.rs:326` stores the self identity with `admission: None`.

SD names the production ceremony as remaining work: the cluster-root signs
each node's criome master key. The current code has no field in
`CriomeDaemonConfiguration` for that self-admission, and startup does not
verify one. That means the ceremony is not yet enforceable by code. A fresh
daemon with a configured `cluster_root` can still self-register its own
`Host("criome")` key without a cluster-root admission.

This does not reopen the external self-asserted-registry gap; external
`RegisterIdentity` is gated. It does mean the claim "last thing between the
auth core and trustworthy auth" is still too strong unless "trustworthy"
explicitly excludes root-of-daemon provisioning. For production, either:

- add a startup self-admission field and require it when `cluster_root` is
  configured, or
- make the local self-owned exception explicit as a deliberate trust boundary
  and keep the provisioning ceremony outside registry admission.

### P3 — daemon-level admission tests cover the happy path, not the adversarial matrix

`tests/daemon_skeleton.rs:561` proves the important baseline:

- missing admission under configured root is rejected;
- valid cluster-root admission is accepted.

Unit tests in `src/admission.rs` cover wrong root, relabelled identity,
malformed signature, and wrong scheme. The daemon-level path should still
gain at least the two most important negative integration cases:

- registration with a valid signature from a non-root key is
  `UnauthorizedRegistration`;
- registration with a valid min-pk signature but `Bls12_381MinSig` in the
  envelope is `UnauthorizedRegistration`.

That keeps the previous scheme-confusion defect from reappearing at the
actor boundary.

## Confirmed Good Work

The core runtime wiring is real:

- `signal-criome/src/schema/lib.rs:317` adds
  `CriomeDaemonConfiguration.cluster_root`.
- `signal-criome/src/schema/lib.rs:603` adds
  `IdentityRegistration.admission`.
- `signal-criome/src/schema/lib.rs:293` adds
  `RejectionReason::UnauthorizedRegistration`.
- `criome/src/daemon.rs:38` reads `cluster_root` from
  `CriomeDaemonConfiguration`.
- `criome/src/daemon.rs:79` threads it into `RootArguments`.
- `criome/src/actors/root.rs:288` threads it into `IdentityRegistry`.
- `criome/src/actors/registry.rs:101` gates external registrations.

The previous audit's P2 scheme-confusion issue is fixed:

- `criome/src/admission.rs:93` rejects unsupported admission schemes.
- `criome/src/admission.rs:186` tests that a valid min-pk signature claiming
  `Bls12_381MinSig` is rejected.

The end-to-end test SD cited exists and passes:

- `tests/daemon_skeleton.rs:561` starts a root with configured
  `cluster_root`.
- `tests/daemon_skeleton.rs:574` verifies unadmitted registration is refused.
- `tests/daemon_skeleton.rs:589` creates a cluster-root-signed admission.
- `tests/daemon_skeleton.rs:598` verifies the admitted registration is accepted.

`criome` also repins to the pushed `signal-criome` branch:

- `Cargo.toml:35` uses
  `signal-criome = { git = "...", branch = "criome-admission-gate" }`.
- `Cargo.lock` pins commit `783cc2fa`.

## Verification

Run in `signal-criome/criome-admission-gate`:

- `cargo test --offline` — passed, but this is weak because it runs no tests.
- `cargo clippy --offline --all-targets -- -D warnings` — passed for default
  features.
- `cargo fmt --check` — passed.
- `nix flake check` — failed in `clippy-nota-text` on stale
  `IdentityRegistration` fixtures.

Run in `criome/criome-auth-pilot`:

- `cargo test --offline` — passed, 32 tests.
- `cargo clippy --offline --all-targets -- -D warnings` — passed.
- `cargo fmt --check` — passed.
- `nix flake check` — passed, with the standard note that `aarch64-linux` was
  omitted.

## Recommendation

Do not merge `signal-criome/criome-admission-gate` yet. Fix the stale NOTA
feature fixtures and make the contract branch pass `nix flake check` first.

After that, `criome/criome-auth-pilot` is a good integration branch for the
external admission gate. Before calling production auth complete, decide and
implement the daemon self-admission stance: either enforce cluster-root
admission for `Host("criome")` at startup, or explicitly define local
self-registration as outside the cluster-root admission model.
