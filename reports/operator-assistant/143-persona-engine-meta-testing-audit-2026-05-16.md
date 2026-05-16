# 143 - Persona engine meta-testing audit and implementation pass

Date: 2026-05-16
Role: operator-assistant
Scope: Persona meta repo, Persona engine tests, Kameo lifecycle impact

## 0. Summary

I audited Persona's engine-level testing against the current actor-heavy,
Nix-owned test discipline and implemented a first meta-testing layer.

The implementation landed in `/git/github.com/LiGoldragon/persona`:

- `tests/meta_testing.rs` now checks that architecture/test documents name
  live Nix check outputs, reject bare `cargo test --...` review commands,
  reject invalid `nix flake check .#name` named-check commands, and keep
  multi-thread Tokio actor tests narrow.
- `flake.nix` now exposes named check outputs for previously load-bearing
  engine witnesses and for the new meta-test witness.
- `ManagerStore::close_and_stop` now performs a close-through-mailbox step
  before graceful actor stop so the redb handle is released before callers
  treat shutdown as complete.
- `tests/manager_store.rs` now has a redb lock-release witness:
  `constraint_manager_store_close_protocol_releases_redb_lock_before_shutdown`.
- Persona test and architecture docs now point to valid
  `nix build .#checks.x86_64-linux.<name>` commands for named witnesses.
- Existing `wait_for_shutdown().await` test call sites now explicitly bind
  `_shutdown_completion`, matching the Kameo lifecycle report's direction
  that ignored terminal outcomes should be intentional.

## 1. Research Pattern

Actor-system test practice is not one test shape.

- Akka Typed distinguishes isolated synchronous behavior tests from
  asynchronous tests using a real `ActorSystem`; its docs say interaction
  between multiple actors belongs in the more realistic asynchronous form.
  Source: https://doc.akka.io/libraries/akka-core/current/typed/testing.html
- Akka's async testing model uses a procedure that drives stimuli, one or
  more actors under test, and receiving actors/probes; larger systems apply
  stimuli at different ingress points and check different emission points.
  Source: https://doc.akka.io/libraries/akka-core/current/typed/testing-async.html
- Erlang Common Test treats both black-box target-system testing and
  white-box direct module testing as normal; it also supports parallel
  connections to target systems, which matches Persona's daemon/CLI/socket
  harness direction.
  Source: https://www.erlang.org/docs/20/apps/common_test/basics_chapter
- Tokio's test guidance matters for Rust actor systems: time-based async
  behavior should use paused/controlled time rather than slow sleeps where
  possible.
  Sources: https://tokio.rs/tokio/topics/testing and
  https://docs.rs/tokio/latest/tokio/time/fn.pause.html

The Persona translation is:

- unit-ish contract tests for pure reducers/schema;
- actor-path tests for every stateful noun;
- daemon/socket/CLI black-box tests for component boundaries;
- stateful Nix checks for named architecture witnesses;
- meta-tests that stop docs from publishing dead commands or stale check
  names;
- resource-release tests for actors that own files, sockets, child
  processes, or redb/sema handles.

## 2. What Was Ugly

The worst finding was self-inflicted documentation debt: Persona's
architecture table was using `nix flake check .#name` for named checks.
That command is invalid. The correct single-witness command is a build of
the check derivation, for example:

```sh
nix build .#checks.x86_64-linux.persona-engine-meta-testing-docs-are-nix-backed
```

The new meta-test now rejects the invalid form.

The second ugly part is Kameo 0.20's current `spawn_in_thread` behavior.
`ManagerStore::start` still needs Tokio's multi-thread test runtime today.
The meta-test allows that exception only for files that exercise
`ManagerStore::start`. This is intentionally narrow, but it is still a
workaround until the Kameo lifecycle branch becomes the workspace runtime.

The third weak spot is the new Nix-check parser. It is a small string
scanner, not a Nix parser. That is acceptable for a meta witness whose
contract is "docs name check outputs in the canonical visible command
form", but it is not a general flake parser.

The fourth weak spot is that this pass built the new named witnesses and
evaluated the whole flake with `--no-build`; it did not build the entire
Persona flake check set. That would be the next broader verification step
when the tree is quiet.

## 3. Verification

Run in `/git/github.com/LiGoldragon/persona`:

```sh
nix develop -c cargo fmt
nix develop -c cargo test
nix build .#checks.x86_64-linux.persona-engine-meta-testing-docs-are-nix-backed -L
nix build .#checks.x86_64-linux.persona-manager-store-close-protocol-releases-redb-lock-before-shutdown -L
nix flake check --no-build
```

All passed. `nix flake check --no-build` evaluated the x86_64-linux
packages, checks, apps, dev shell, and formatter successfully; it warned
only about app outputs lacking `meta` and omitted `aarch64-linux` unless
`--all-systems` is requested.

## 4. Follow-Up Work

The next high-signal testing work is to repeat the resource-release witness
pattern in the other resource owners:

- `persona-terminal` supervisor/control socket/session state;
- `terminal-cell` child process and control socket cleanup;
- `persona-router` store/channel state once its Sema path is fully real;
- `persona-mind` StoreKernel once the supervised `spawn_in_thread`
  lifecycle question is settled in Kameo.

The next meta-test improvement is to make the architecture witness parser
less x86_64-specific without weakening the command examples that humans can
actually run.
