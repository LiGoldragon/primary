# 423 — Mentci remotes and daemon runtime

## Frame

The psyche explicitly authorized creating the missing GitHub remotes and
continuing implementation. I treated this as an operator implementation task,
not a new intent capture.

## Remotes

Created or confirmed these public GitHub remotes, all with `main` as default:

- `LiGoldragon/signal-standard`
- `LiGoldragon/signal-mentci`
- `LiGoldragon/meta-signal-mentci`
- `LiGoldragon/mentci`
- `LiGoldragon/mentci-lib`

All five local main bookmarks match origin after this pass.

I also added `signal-standard`, `mentci`, `signal-mentci`, and
`meta-signal-mentci` to `protocols/active-repositories.md`, so future active
repo sweeps include the newly landed component surface.

## Landed Code

`signal-mentci` main:

- Commit `d0fea7bf` — `signal-mentci: return observation token with snapshot`.
- Fixed `ObserveInterfaceState` output so the reply carries both the daemon
  subscription token and the projected initial state:
  `InterfaceObservationOpened { token state }`.
- Regenerated contract artifacts and updated round-trip tests.

`mentci` main:

- Commit `5ddd3b4e` — `mentci: add daemon runtime and thin client`.
- Added the runtime crate over remote dependencies only:
  `signal-mentci`, `meta-signal-mentci`, and `signal-frame` all come from
  GitHub remotes.
- Added `mentci-daemon`, which starts from exactly one binary
  `meta-signal-mentci` `Configure(MentciDaemonConfiguration)` frame.
- Added `mentci`, a thin client that takes one request input: a binary
  `signal-mentci` frame file, a `.nota` request file, or inline NOTA. It sends
  the request to the local daemon socket and writes the binary reply frame to
  stdout.
- Added the first daemon state machine: pending questions, decisions,
  edited-answer proposals, subscriptions, revision, status, notifications, and
  panes.
- Added a Unix-socket frame codec and an actor-owned state handler using
  kameo.
- Updated `README.md` and `ARCHITECTURE.md` so they no longer claim the daemon
  binary is missing.

## Testing

Cargo gates:

- `signal-standard`: `cargo test --all-targets`; `cargo clippy --all-targets -- -D warnings`.
- `signal-mentci`: `cargo test --all-targets --features nota-text`; `cargo clippy --all-targets --features nota-text -- -D warnings`.
- `meta-signal-mentci`: `cargo test --all-targets --features nota-text`; `cargo clippy --all-targets --features nota-text -- -D warnings`.
- `mentci`: `cargo test --all-targets`; `cargo clippy --all-targets -- -D warnings`.
- `mentci-lib`: `cargo test --all-targets`; `cargo clippy --all-targets -- -D warnings`.

`mentci` now has 10 tests:

- daemon connection handler returns a real `signal-mentci` reply frame over a
  Unix stream pair;
- client builds request frames from inline NOTA and `.nota` files;
- startup configuration round-trips as a binary meta-signal frame;
- `.nota` startup paths are rejected for the daemon;
- frame codec round-trips a length-prefixed Mentci frame;
- state tests cover question presentation, observation token + projected state,
  defer keeping a question open, and approval closing it against later edits.

Nix gates:

- `nix flake check github:LiGoldragon/signal-standard --no-write-lock-file` passed.
- `nix flake check github:LiGoldragon/mentci-lib --no-write-lock-file` passed.

The other new component repos do not have flakes yet, so their Nix gate is not
available. I did not use local `path:/git/...` Nix overrides.

## Dependency Discipline

I checked the relevant manifests and locks for forbidden local dependency
paths. The only `path = ...` hits are ordinary Cargo target declarations such
as `path = "src/lib.rs"` and test/example target paths. No local dependency
paths or `path:/git/...` overrides were introduced.

## Remaining Work

- Persist Mentci SEMA state. The current daemon state is executable and tested,
  but in-memory.
- Wire notification fan-out beyond request/reply.
- Connect cryptographic verdict egress to criome key custody; this is blocked
  on the real criome key custody path, not on Mentci’s UI/state shape.
- Add flakes to `signal-mentci`, `meta-signal-mentci`, and `mentci` if we want
  a Nix gate per repo.
- Replace any future local duplicated types with imports from `signal-standard`
  once the broader standard-contract migration is ready.
