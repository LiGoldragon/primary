# Orchestrate onto signal 7.0.0's exchange layer

Flow 3ec648, 2026-10-02. Two of three repositories are on main with green
gates. orchestrate 0.36.0 is finished and passes locally, but it sits on
branch `3ec648-orchestrate-wip`. Its one `nix flake check` hit the 30-minute
bound while Prometheus was still building the dependency derivations. No check
had reported a failure when it stopped.

## Per repository

| Repo | Version | Commit | Where | Gate | Duration |
|---|---|---|---|---|---|
| signal-orchestrate | 4.0.0 | `4e683453` | main | `nix flake check` green, 25 checks | 805 s |
| meta-signal-orchestrate | 4.0.0 | `972a3b03` | main | `nix flake check` green, 17 checks | 1538 s |
| orchestrate | 0.36.0 | `b56f2644` | branch `3ec648-orchestrate-wip` | `nix flake check` timed out at 1800 s while building `orchestrate-deps` and `orchestrate-nexus-deps`; `cargo test --workspace`, clippy `-D warnings`, `cargo fmt --check` and `cargo doc -D warnings` green locally | n/a |

### signal-orchestrate

- The f6db8d work was committed as found in the tree (`7a2cde30`) and pushed
  as branch `f6db8d-exchange`.
- `4e683453` sits on top of it and moves the ethos-zero pin from 10.0.0
  `4bf73cae` to 13.0.0 `cf7dd128`. I generated `ethos/signal.ethos` with 13.0.0
  and compared the result to the committed file: they are byte-identical, so
  13.0.0 is used. UPGRADES says so.
- `cargo test`: 10 passed, and 12 with `--features datom`.

### meta-signal-orchestrate

- Repinned to signal-orchestrate 4.0.0, signal 7.0.0 `66e7b153`, protos 0.31.0,
  datom-codec 0.31.0 and ethos-zero 13.0.0. `src/generated/signal.rs` was
  regenerated; only the derives changed (`Eq` and `Hash` added, `Composing` in
  place of `Compositional`).
- Added `impl signal::Contracted for Query` with `ETHOS` as the source, plus an
  exchange-layer paragraph in the ethos text.
- New `tests/exchange_envelope.rs` (3 tests) with its own flake check
  `test-exchange-envelope`. The digest oracle was computed outside the crate
  with FNV-1a in Python. Two of the three tests were seen failing when the
  impl pointed at the ordinary contract's source.
- **mind:** its manifest pins this crate with `branch = "main"`. Its lock still
  holds 0.4.0 `a8659aa4`, so it breaks only on its next `cargo update`. I did
  not touch mind, whose tree has uncommitted work. Instead, the 4.0.0 UPGRADES
  entry says mind must repin, either to a revision whose signal it speaks or
  to 3.0.2 `4279ad05`, before it updates.

### orchestrate 0.36.0

- The single-file `transport/session.rs` became `transport/session/`. Each
  piece is a type that carries data and has its behaviour in traits; there
  are no new free functions and no zero-sized namespaces:
  - `GreetingGate<Q>` (`Gating`) handles the one greeting per connection.
  - `SessionLedger` (`Ledgering`) wraps signal's `ExchangeLedger` and adds the
    abort handle of each subscription's feeder.
  - `SocketContract` is implemented on `OrdinaryQuery` and `MetaQuery`. It
    yields `Opened::Answered` or `Opened::Streaming`.
  - `Announcements` (`Following`) yields `Changed`, `Lagged` or `Closed`.
  - `Inbound` (`Listening`) is the reader task, `Feeder` (`Feeding`) feeds one
    subscription, and `Exchanges<Q>` (`Dispatching`, `Delivering`) is one
    connection.
- An `Open` is accepted while an `Observe` stream runs on the same connection.
  `Abandon` stops that exchange's feeder and releases it.
- A subscriber that falls behind gets `End(Lagged)`, and `Overtaking` was
  removed from the core. The feeder channel holds one frame, so a peer that is
  not reading holds the core's stream back and is found lagging.
- An unreadable frame is answered `UnreadableQuery` against the connection.
  A refusal from the meta socket goes out as an answer on exchange 0.
- Both CLIs greet once, send `Dispatch::Open` and read `Delivery::Answer`. The
  failure vocabulary gained `GreetingRefused` and `ExchangeFaulted`. The
  generated client files now use `Composing`.
- Tests:
  - New session unit tests cover a foreign greeting refused, `Open` before the
    greeting, and a repeated greeting.
  - `live_nexus.rs` now runs on temporary XDG sockets. One test covers
    greeting, `Observe` with the state on open even with no Locks, a `Lock`
    opened beside the stream and told apart by exchange, a release seen on the
    stream, and `Abandon` followed by a reopen. A new test drives a subscriber
    behind with quarter-mebibyte changes until it receives `Lagged`, then
    reopens it for the state on open.
  - `stopping.rs`, `second_user_peer.rs` and both client tests were moved to
    the exchange layer. Each client gained a refused-greeting test.
  - Seen failing:
    - The repeated-greeting check removed: the repeated-greeting test failed.
    - `Lagged` swallowed and the `Abandon` release removed: three `live_nexus`
      tests failed.
    - The client's refusal mapping removed: the client test failed.
  - All restored: workspace green. `live_nexus` passed 16 of 16 on five
    consecutive runs.
- Lock graph: exactly one protos (0.31.0 `1febca78`) and one datom-codec
  (0.31.0 `09e2a9d5`). nexus 0.5.0 and sema-engine 0.15.1 are unchanged. Two
  ethos-zero versions remain, both build-only: 13.0.0 directly and 10.0.0
  through signal 7.0.0's own build dependency. `cargo tree` for the Nexus
  shows neither datom-codec nor protos.

## Where it stopped

orchestrate `b56f2644` is on `3ec648-orchestrate-wip`, not on main. The only
missing step is a green `nix flake check`. To land it:

1. Run `nix flake check 'git+file:///git/github.com/LiGoldragon/orchestrate?rev=b56f2644600ffc58fedf4b83639b8b39e615ff2b' -L`
   with a longer bound. The vendor derivation is already on Prometheus.
2. If green, run `jj bookmark set main -r b56f2644` and `jj git push --bookmark main`.

## Deploy steps for the morning

These apply only once orchestrate `b56f2644` is on main with a green gate.

1. In CriomOS-home, repin `orchestrate.url` in `flake.nix`, currently
   `github:LiGoldragon/orchestrate/9070cbb8…`, to the landed 0.36.0 revision,
   and update `flake.lock` for that input only.
2. Build the home configuration through Lojix as the operating-system skill
   directs. Its `orchestrate-service-path` and `orchestrate-wrapper-fallback`
   checks must pass.
3. Switch while no Lock is held. First check that
   `orchestrate 'Observe.Locks'` answers `Observed.Locks.[]`, using the old
   CLI against the old Nexus. The Nexus and both CLIs are one package, so one
   switch moves every client together. The store needs no migration.
4. Verify:
   - `orchestrate 'Observe.Locks'` answers `Observed.Locks.[]` from the new
     pair.
   - One meta call:
     `orchestrate-meta 'Configure.{ «$XDG_RUNTIME_DIR/orchestrate-nexus/orchestrate.sock» «$XDG_RUNTIME_DIR/orchestrate-nexus/orchestrate-meta.sock» }'`
     answers `Configured.{ { … } True }`.
   - A `GreetingRefused` from either CLI means the CLI and the Nexus came from
     different builds.

## Sources

- signal 7.0.0 `66e7b153`: `src/exchange.rs`, `src/accord.rs`,
  `ethos/signal.ethos`
- ethos-zero history `4bf73cae`..`2db764d2`, and the byte comparison of
  generated output under 10.0.0 and 13.0.0
- mind `Cargo.toml:50` and `Cargo.lock`
- CriomOS-home `flake.nix:181` and `modules/home/profiles/min/orchestrate.nix`
- `nix flake check` logs for each repository, run by this subflow
