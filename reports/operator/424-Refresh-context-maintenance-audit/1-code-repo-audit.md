# 424.1 — Code repo audit

## Verified State

Fetched `origin` for all eight repos with `jj git fetch --remote origin`; every
fetch returned `Nothing changed`. Final `jj status` after tests: all audited
working copies clean. No repo is ahead of or behind `origin/main`.

| Repo | Main commit | Origin | Dirty | Test result |
|---|---:|---|---|---|
| `criome` | `068f9db9` — `criome: port to strict signal-criome contract` | matches | clean | pass |
| `signal-criome` | `521a8ed3` — `signal-criome: expose snapshot collection accessors` | matches | clean | pass |
| `meta-signal-criome` | `16b9a196` — `meta-signal-criome: refresh schema support pins` | matches | clean | pass |
| `signal-standard` | `aa672cc8` — `signal-standard: add typed standard socket vocabulary` | matches | clean | pass |
| `signal-mentci` | `d0fea7bf` — `signal-mentci: return observation token with snapshot` | matches | clean | pass |
| `meta-signal-mentci` | `270cd909` — `meta-signal-mentci: bootstrap daemon configuration contract` | matches | clean | pass |
| `mentci` | `5ddd3b4e` — `mentci: add daemon runtime and thin client` | matches | clean | pass |
| `mentci-lib` | `c5a80852` — `mentci-lib: model edited answers as proposals` | matches | clean | pass |

Cargo tests run with `CARGO_TARGET_DIR=/tmp/primary-audit-424/...`:

- `criome`: `cargo test --all-targets --locked` passed.
- `signal-criome`: `cargo test --all-targets --features nota-text --locked`
  passed.
- `meta-signal-criome`: `cargo test --all-targets --features nota-text
  --locked` passed.
- `signal-standard`: both default and `--features nota-text` test runs passed;
  the `nota-text` run covered 8 round-trip tests.
- `signal-mentci`: `cargo test --all-targets --features nota-text --locked`
  passed.
- `meta-signal-mentci`: `cargo test --all-targets --features nota-text
  --locked` passed.
- `mentci`: `cargo test --all-targets --locked` passed; 10 tests cover daemon
  connection handling, client input, startup configuration, frame codec, and
  state.
- `mentci-lib`: `cargo test --all-targets --locked` passed; 9 approval tests
  passed. Known warning remains: `examples/handshake.rs` is both
  `mentci-handshake-test` and example `handshake`.

Nix verified:

- `signal-standard`: `nix flake check --no-write-lock-file --no-update-lock-file`
  completed successfully.
- `mentci-lib`: same command completed successfully.

Unverified in this bounded pass:

- I did not rerun clippy.
- I did not rerun the heavier existing Nix flakes for `criome`,
  `signal-criome`, or `meta-signal-criome`.
- `signal-mentci`, `meta-signal-mentci`, and `mentci` have no `flake.nix`, so
  there is no Nix gate there yet.

## Dependency Check

Scanned `Cargo.toml`, `Cargo.lock`, `flake.nix`, and `flake.lock` across the
eight repos for forbidden local dependency forms.

Verified:

- no Cargo dependency uses `path = ...`;
- no Nix input uses `path:/git`, `git+file`, `file://`, or `/git/...`;
- `path = ...` hits are target declarations such as `src/lib.rs`,
  binary/test/example paths, or Nix source-filter argument names.

`mentci/Cargo.toml:12-15` uses remote Git dependencies for
`meta-signal-mentci`, `signal-frame`, and `signal-mentci`, matching the
remote-only daemon-runtime discipline.

## Focused Code Facts

`signal-mentci` observation token is correct on current main:

- `signal-mentci/schema/lib.schema:261` defines
  `InterfaceStateObservation { subscriber, interest }`; callers do not supply
  a token.
- `signal-mentci/schema/lib.schema:284` defines
  `InterfaceObservationOpened { token, state }`.
- `signal-mentci/schema/lib.schema:377` makes `InterfaceStateStream` token-keyed
  and closed by `SubscriptionToken`.
- `mentci/src/state.rs:122` mints the token and returns the projected state.
- `mentci/tests/state.rs:47` proves the initial reply carries
  `SubscriptionToken::new("subscription-1")` and the current projection.

Mentci daemon/client runtime is present:

- `mentci/src/command.rs:29` accepts exactly one daemon startup path and rejects
  `.nota`.
- `mentci/src/configuration.rs:21` decodes a binary `meta-signal-mentci`
  `Configure` frame.
- `mentci/src/client.rs:39` accepts exactly one request input: binary frame
  file, `.nota` file, or inline NOTA.
- `mentci/src/client.rs:49` sends the request to the Unix socket and writes a
  binary reply frame to stdout.
- `mentci/src/daemon.rs:41` binds the configured Unix socket, owns state through
  a data-bearing Kameo `StateOwner`, reads one request frame, and writes one
  reply frame.

Criome current main is newer than reports `408`/`410` on one point:

- policy contracts are now persisted across restart. `criome/tests/daemon_skeleton.rs:752`
  restarts `CriomeRoot`, then `:755` looks up the persisted contract and `:769`
  evaluates it after restart.

## Branch Context

Relevant non-main bookmarks:

- `criome` `attested-moment-majority-guard-139` at `ed2f3b5d`: strict-majority
  guard for fork-safe `AttestedMoment` time attestations. Exists locally and on
  origin; not on main.
- `signal-standard` `attendance-fanout-139` at `8befd44e`: lifts
  `AuthorizedObjectInterest::matches_reference`; exists locally and on origin;
  one commit ahead of main.
- Older `criome` / `signal-criome` policy and attested-moment bookmarks remain
  as prototype/design evidence. Main has already absorbed some of that arc.

## Current Blockers

1. `criome` fork-safe time quorum majority guard is not on `main`; integrate
   `attested-moment-majority-guard-139` or explicitly defer it.
2. Router delivery is still open. `criome` can store/filter authorized-object
   snapshots, but router `Attend` / `Withdraw` and socket-level fan-out are not
   in this audited main set.
3. `signal-standard` exists, but consumers have not migrated. `signal-criome`
   still owns local `ComponentKind` / `AuthorizedObjectInterest`; `meta-signal-mentci`
   still owns local `ComponentKind` / `StandardSocket` stand-ins.
4. `mentci` state is executable but in-memory; durable SEMA/redb persistence and
   restart recovery remain.
5. Mentci verdict egress to criome remains blocked on real criome key-custody /
   signing integration.
6. Nix flakes are missing for `signal-mentci`, `meta-signal-mentci`, and
   `mentci`.
