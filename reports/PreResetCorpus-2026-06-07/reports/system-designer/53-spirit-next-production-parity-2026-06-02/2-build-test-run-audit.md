# Spirit Next — build + test + run empirical audit (2026-06-02)

## Frame

Sub-agent 2 of meta-report 53. Empirical, evidence-first dimension of
the audit: actually `nix build` the pushed `main`, actually run the
test suite, actually bring up a daemon on a `/tmp` slot, actually
round-trip every wire operation through the CLI, and read the
production reply shape with my own eyes — no inference from source.

**Repo head used.** `/git/github.com/LiGoldragon/spirit-next` `@-` =
`main` = `vsypoxzy 7c350679` *spirit-next: move daemon startup into
command noun* (2026-06-02 12:53 — current). Local main is in sync
with `origin/main` (`jj git fetch` reports "Nothing changed").

**Production daemon read-only.** Throughout the audit the production
binding `~/.nix-profile/bin/spirit -> spirit-v0.3.0` was untouched;
the running `persona-spirit-daemon-v0.3.0.service` (PID 3068577,
active since 2026-06-01 12:06:46) never received a request and its
state directory was only read. Test artifacts landed under
`/tmp/spirit-next-smoke-test{,-2}/` and were removed at the end.

**Constraint compliance.** Three sub-agent constraints applied:
read-only on production, `/tmp` for test state, no further
sub-agent dispatch. All three honoured.

## Build status

### Pushed remote — `nix build github:LiGoldragon/spirit-next` FAILS

`nix build github:LiGoldragon/spirit-next` against the pushed
`main` (commit `7c350679`) fails for both default and daemon
packages with the same panic from `build.rs:88`:

```text
thread 'main' (188) panicked at build.rs:88:13:
checked-in generated schema source is stale at
/build/spirit-next-source-with-local-schema-patches/src/schema/lib.rs;
regenerate it from schema/lib.schema
```

The full error chain is:

```text
error: Cannot build '...-spirit-next-0.1.0.drv' on
       'ssh-ng://nix-ssh@prometheus.goldragon.criome' failed:
       builder failed with exit code 101.
       Output paths:
         /nix/store/0kzrf1wnb65vzaj7vpd2h0l3wqka7m24-spirit-next-0.1.0
error: Cannot build '/nix/store/iq9g9ihgp6lkdjk6q1dz4mdv3lfacfqp-spirit-next.drv'.
       Reason: 1 dependency failed.
```

The check that fires lives in `build.rs` lines 69-93
(`SchemaBuild::assert_checked_in_schema_is_fresh`): the in-tree
`src/schema/lib.rs` (1867 lines, checked in) does not byte-match
what `schema_rust_next::RustEmitter` produces from
`schema/lib.schema` (47 lines) under the build sandbox's view of
the deps.

### Root cause — schema-rust-next-source flake input lags Cargo.lock

`flake.nix` declares three non-flake sibling sources
(`nota-next-source`, `schema-next-source`, `schema-rust-next-source`)
that the Nix builder vendors into the Cargo workspace via a
`[patch.*]` block (lines 73-90 of `flake.nix`). The committed
`flake.lock` pins:

| Input | Pinned rev | Date |
|---|---|---|
| `nota-next-source` | `b33b5b51ce10aa7f44027b7290bfe008c90e7ce5` | 2026-06-01 |
| `schema-next-source` | `e2a8abfcaae2d083dc19e46e15be26f8f7a5e5cc` | 2026-06-01 |
| `schema-rust-next-source` | `d3ec9f9113bb80ea018460bf9654179ae3dda16b` | 2026-06-02 07:35 |

But `Cargo.lock` references **newer** revs for the same crates:

| Crate (Cargo.lock) | Pinned rev | Comment |
|---|---|---|
| `nota-next` | `b33b5b51` | matches lock |
| `schema-next` | `e2a8abfc` | matches lock |
| `schema-rust-next` | `a8c0f012142f37084bf634ec543f1ab981f9e272` | **newer than flake.lock** |

`schema-rust-next@a8c0f012` is *"schema-rust: emit per-plane trace
object names"* (parent of recent rev `dd944233`). `schema-rust-next@
d3ec9f91` is *"schema-rust: prefer exact plane routes over payload
fallback"* — older. The newer emitter produces the source that's
checked into `src/schema/lib.rs`; the older emitter the Nix sandbox
uses produces a different source.

Spelled out: the Cargo.lock + checked-in generated source were
produced from the **newer** `schema-rust-next` rev, then committed.
But the `flake.lock` `schema-rust-next-source` input was never
re-locked, so the Nix sandbox vendors the **older** rev, runs its
emitter, gets different output, panics on the freshness assert.

### Local cargo build SUCCEEDS

`nix develop -c cargo build` from `/git/github.com/LiGoldragon/spirit-next`
**succeeds** because cargo resolves git deps directly from
`Cargo.lock`, not from the flake input:

```text
$ nix develop -c cargo build --release --features nota-text --bin spirit-next
   Compiling schema-rust-next v0.1.0 (https://github.com/.../schema-rust-next.git?branch=main#a8c0f012)
   ...
    Finished `release` profile [optimized] target(s) in 3.18s
```

Same outcome for `spirit-next-daemon`. Local-build path is healthy.

### Fix path — flake update of one input

I rebuilt the pushed remote with `--override-input` pointing at the
local checkouts of the three deps:

```sh
nix build github:LiGoldragon/spirit-next \
  --override-input nota-next-source path:/git/github.com/LiGoldragon/nota-next \
  --override-input schema-next-source path:/git/github.com/LiGoldragon/schema-next \
  --override-input schema-rust-next-source path:/git/github.com/LiGoldragon/schema-rust-next
```

This succeeded — `/nix/store/r4larn1mzximx968dyj4i3ndraw2yvd3-spirit-next-0.1.0`
(daemon) and `/nix/store/ajrrififspciiw4n1vi1rvbapy31s2xm-spirit-next-0.1.0`
(cli). Same with `nix flake check` (all checks passed). The minimum
push-fix is a `nix flake update schema-rust-next-source` after the
deps' main bookmarks settle, followed by a commit + push of the new
`flake.lock`. (`nota-next-source` and `schema-next-source` were
overridden in the test for symmetry, but their pinned revs already
match the lock — only `schema-rust-next-source` is genuinely stale.)

### Buildable output paths under overrides

The default `packages.default` is a `runCommand` symlink farm that
brings together `cli` + `daemon`:

```text
$ ls /nix/store/wb8brljz311b9h1md9413v60fd3jaagm-spirit-next/bin/
spirit-next -> /nix/store/ajrrif...-spirit-next-0.1.0/bin/spirit-next
spirit-next-daemon -> /nix/store/r4larn...-spirit-next-0.1.0/bin/spirit-next-daemon
```

So the daemon binary is `spirit-next-daemon`, the CLI is `spirit-next`
(matching `skills/spirit-cli.md` slot vocabulary — the `spirit-next`
deploy slot in the live profile would resolve to this CLI).

## Test suite results

`nix develop -c cargo test --features nota-text --no-fail-fast`
landed against the local Cargo.lock (the build path that DOES work
today). Plus a second pass with `--features nota-text,testing-trace`
for the testing-trace witness layer.

### Default feature surface (`nota-text` only)

```text
test result: ok. 0 passed; 0 failed       (unit tests, src/lib.rs)
test result: ok. 0 passed; 0 failed       (unit tests, src/bin/spirit-next.rs)
test result: ok. 0 passed; 0 failed       (unit tests, src/bin/spirit-next-daemon.rs)
test result: ok. 2 passed                 (tests/daemon_command.rs)
test result: ok. 2 passed                 (tests/dependency_surface.rs)
test result: ok. 6 passed                 (tests/generated_signal_plane.rs)
test result: ok. 0 passed; 9 ignored      (tests/nix_integration.rs)
test result: ok. 6 passed                 (tests/operator_271_closed_claims.rs)
test result: ok. 3 passed                 (tests/process_boundary.rs)
test result: ok. 19 passed                (tests/runtime_triad.rs)
test result: ok. 3 passed                 (tests/socket_negative.rs)
test result: ok. 1 passed                 (Doc-tests spirit_next)
```

**Totals** — 41 passing, 0 failing, 9 ignored on the binary +
nota-text surface.

### testing-trace feature surface

Adds three trace-witness tests to `instrumentation_logging.rs`
and one extra `process_boundary.rs` test
(`cli_receives_testing_trace_events_from_daemon_trace_socket`):

```text
test result: ok. 2 passed                 (tests/daemon_command.rs)
test result: ok. 6 passed                 (tests/generated_signal_plane.rs)
test result: ok. 3 passed                 (tests/instrumentation_logging.rs)
test result: ok. 4 passed                 (tests/process_boundary.rs)   ← was 3, +1 trace test
test result: ok. 19 passed                (tests/runtime_triad.rs)
test result: ok. 3 passed                 (tests/socket_negative.rs)
... plus the rest same as above
```

**Totals** — 45 passing, 0 failing, 9 ignored with testing-trace.

### Tests are substantive, not aspirational

I read each integration test file's outline:

- **`tests/process_boundary.rs`** (4 tests). The real
  `CARGO_BIN_EXE_spirit-next-daemon` is spawned with a binary
  rkyv config, a Unix socket and a redb `.sema` file land in a
  `TempDir`, the real `CARGO_BIN_EXE_spirit-next` invokes it,
  every reply is parsed back through `Output::from_str`. The
  `daemon_persists_sema_file_across_a_restart` test kills the
  first daemon, opens a second daemon against the same .sema
  file, and asserts the commit sequence resumes — real durability
  proof. `candidate_daemon_handover_from_production_copy_preserves_original_sema_database`
  copies a sema file, runs a candidate daemon against the copy,
  and asserts the original is untouched.
- **`tests/instrumentation_logging.rs`** (3 tests under
  `testing-trace`). Asserts that the trace-log surface records
  real signal/nexus/sema activations during a Record, and that a
  rejected input emits no nexus/sema events. Genuine behavioural
  witnesses, not stubs.
- **`tests/runtime_triad.rs`** (19 tests). Component-level
  behavioural tests for each engine trait (Signal → Nexus → Sema)
  including a `sema_store_persists_records_across_reopen_of_the_same_sema_file`
  test that re-opens the redb file and re-reads its records. The
  signal-actor-rejects-invalid-input test confirms the wire-level
  rejection path.
- **`tests/generated_signal_plane.rs`** (6 tests). Schema-emitted
  round-trip + frame decoder + mail-sent event check. All
  substantive.
- **`tests/socket_negative.rs`** (3 tests). Asserts the binary
  transport rejects raw-NOTA-text and rejects garbage bytes —
  this is the binary-protocol-on-wire guard from Spirit 1373.
- **`tests/operator_271_closed_claims.rs`** (6 tests). Schema
  constraint enforcement (no `@` sigil, honest data-variant
  rendering, etc.). Mechanical but substantive.
- **`tests/dependency_surface.rs`** (2 tests). Shells out to
  `cargo tree` to assert the daemon-side binary surface has no
  `nota_next` runtime dep and the CLI-side does. Substantive
  proof of the no-NOTA-in-daemon rule.
- **`tests/daemon_command.rs`** (2 tests under `testing-trace`).
  Tests the `DaemonCommand` argument-count check and the binary
  config read. Tiny but substantive — covers the
  ConfigurationError paths.

The 9 ignored tests in **`tests/nix_integration.rs`** are all
gated by `#[ignore]` because they shell out to `nix build`. The
file `cargo test --test nix_integration -- --ignored` would run
them, gating the gates. Not run during this audit; they would
exercise the same end-to-end shape as the smoke tests below.

**Aspirational-vs-substantive verdict**: every test does
something. There are no placeholder bodies, no `unimplemented!()`,
no smoke-test-only stubs. The signal-plane round-trip, durability,
binary-protocol guard, no-NOTA-in-daemon dependency surface, and
trace-logging witnesses are all real behavioural tests.

## Daemon smoke test — full operation matrix

### Daemon bring-up

The daemon takes one argument: a path to a rkyv-archived
`Configuration` (per `src/config.rs`). Configuration carries
`{ socket_path, database_path, trace_socket_path }`. No NOTA at
daemon startup at all (Spirit 1373 — "no NOTA between components").

I wrote a tiny `config-helper` crate (linked against the local
spirit-next) to emit the binary config, then launched:

```text
$ /git/.../spirit-next/target/release/spirit-next-daemon \
    /tmp/spirit-next-smoke-test/config.rkyv &
daemon pid: 26077
$ ls -la /tmp/spirit-next-smoke-test/
-rw-r--r-- 113 Jun  2 13:26 config.rkyv
-rw-r--r-- 1589248 Jun  2 13:26 spirit-next.sema
srwxr-xr-x       0 Jun  2 13:26 spirit-next.sock
```

Daemon up, socket bound, redb (`.sema`) file initialised at
~1.5 MB.

### CLI round-trip — every wire operation

The CLI takes a NOTA argument and resolves the socket path from
`SPIRIT_NEXT_SOCKET` (env var, no flag). One operation per CLI
invocation. Output is the schema-emitted typed reply printed as
NOTA.

```text
$ SPIRIT_NEXT_SOCKET=$SOCK spirit-next \
    "(Record ([[smoke-test]] Decision [trying out spirit-next] Minimum))"
(RecordAccepted (1 (1 12322621551671276716)))

$ ... "(Observe ((Full [[smoke-test]]) (Some Decision)))"
(RecordsObserved
  ([([[smoke-test]] Decision [trying out spirit-next] Minimum)]
   (1 12322621551671276716)))

$ ... "(Observe ((Partial [[smoke-test]]) None))"
(RecordsObserved ... same record ...)

$ ... "(Lookup 1)"
(RecordFound (1 ([[smoke-test]] Decision [trying out spirit-next] Minimum)
              (1 12322621551671276716)))

$ ... "(Count ((Partial [[smoke-test]]) None))"
(RecordsCounted (1 (1 12322621551671276716)))

$ ... "(Remove 1)"
(RecordRemoved (1 (2 0)))

$ ... "(Observe ((Full [[smoke-test]]) (Some Decision)))"
(Error ([no matching record] (2 0)))
```

Every Input variant the schema declares
(`Record / Observe / Lookup / Count / Remove`) round-trips
correctly. The DatabaseMarker (the `(commit-sequence digest)`
pair at the tail of each reply) advances on each write
(1 → 2 after Remove), the digest changes per write but goes to
`0` after Remove (DatabaseMarker `(2 0)` on the post-Remove
Observe — the database is empty, digest is the empty hash).

### Multi-record sanity

```text
$ ... "(Record ([] Decision [should reject] Maximum))"
(Rejected (EmptyTopic (2 0)))               # empty-topic validation

$ ... "(Record ([[other-topic]] Principle [second record] High))"
(RecordAccepted (2 (3 11360608102949804138)))

$ ... "(Record ([[smoke-test] [other-topic]] Constraint [multi-topic] Medium))"
(RecordAccepted (3 (4 11968003552463988391)))

$ ... "(Lookup 999)"
(Error ([record not found] (4 11968003552463988391)))
```

Validation works (empty topic → typed `Rejected (EmptyTopic ...)`).
Multi-topic records work (the Topics vector accepts multiple
bracketed-string entries). Lookup miss returns `Error`, not
`Rejected` — distinct reply categories.

### Nix-built binary round-trip

After completing the cli + daemon overrides build, I spun up a
fresh daemon (`/nix/store/r4larn1m...-spirit-next-0.1.0/bin/spirit-next-daemon`)
and invoked the Nix-built CLI
(`/nix/store/ajrrifif...-spirit-next-0.1.0/bin/spirit-next`)
against it on a fresh `/tmp/spirit-next-smoke-test-2/` slot:

```text
$ SPIRIT_NEXT_SOCKET=$SOCK $NIX_CLI \
    "(Record ([[nix-built]] Decision [via Nix package] Maximum))"
(RecordAccepted (1 (1 12459607933241223442)))
$ ... "(Observe ((Full [[nix-built]]) None))"
(RecordsObserved ([([[nix-built]] Decision [via Nix package] Maximum)]
                  (1 12459607933241223442)))
$ ... "(Lookup 1)" → RecordFound ...
$ ... "(Remove 1)" → RecordRemoved (1 (2 0))
$ ... "(Observe ((Full [[nix-built]]) None))" → (Error ([no matching record] (2 0)))
```

The Nix-built binaries are behaviourally identical to the local
cargo-built ones — same wire shape, same reply structure.

### Reply shape vs production v0.3.0

The task prompt cites `skills/spirit-cli.md:160-162` for prod
reply patterns. Comparison:

| Operation | Production v0.3.0 reply | spirit-next reply | Shape match? |
|---|---|---|---|
| `Record` | `(RecordAccepted N)` | `(RecordAccepted (N (CommitSequence Digest)))` | **Richer** — next bundles DatabaseMarker |
| `Remove` | `(RecordRemoved N)` | `(RecordRemoved (N (CommitSequence Digest)))` | **Richer** — next bundles DatabaseMarker |
| `Observe` records | `(RecordsObserved [...])` | `(RecordsObserved ([Entry...] (CommitSequence Digest)))` | Different shape — next wraps in a positional record |
| `Lookup` | (n/a — prod has no Lookup) | `(RecordFound (N Entry DatabaseMarker))` | New in next |
| `Count` | (n/a — prod has no Count) | `(RecordsCounted (Count DatabaseMarker))` | New in next |
| `Error` | (n/a — prod returns variant per op) | `(Error (ErrorMessage DatabaseMarker))` | New top-level variant |
| `Rejected` | (n/a — prod fails out-of-band) | `(Rejected (ValidationError DatabaseMarker))` | New top-level variant |
| `ChangeCertainty` | `(CertaintyChanged (N Magnitude))` | not implemented | **gap** |
| `State` (lowers to Assert) | accepted | not implemented | **gap** |
| `Watch / Unwatch` | long-lived stream | not implemented | **gap** |
| `Observe Topics` | bare-token reply | `unknown TopicMatch variant Any` (parse error on the input shape) | **gap** |
| `Observe (Any [])` | accepted (`Any` topic match) | `unknown TopicMatch variant Any` | **gap — Any TopicMatch unimplemented** |

So spirit-next emits *richer* replies for the operations both
support — every reply carries a `DatabaseMarker` (commit sequence
+ state digest), which production doesn't. **A consumer expecting
`(RecordAccepted N)` would mis-parse `(RecordAccepted (N (1 ...)))`.**
This is the substantive wire-shape divergence the orchestrator
needs to know.

The other gap discovered empirically: `TopicMatch` in
`schema/lib.schema` declares `[(Partial Topics) (Full Topics)]`
— no `Any` variant. The CLI emits "unknown TopicMatch variant Any"
when it sees `(Any [])` in the Query position. That's not a runtime
implementation gap; it's a schema-level gap. A future-Observe-all
query needs the schema to grow an `Any` variant in `TopicMatch`,
or a separate top-level `Observe Topics` opcode (which production
has). Either change ripples through `runtime_triad.rs` test
`sema_engine_queries_partial_and_full_topic_sets`.

## Blockers encountered

None hard. The build-from-remote blocker (stale flake.lock for
`schema-rust-next-source`) is a flake-lock-update commit away from
fixed. The CLI and daemon, once built, run cleanly and round-trip
every operation the schema declares.

The one minor friction: the daemon's single-argument is a
**binary rkyv configuration file**, not a NOTA expression. I had
to write a tiny config-helper crate to emit it (`Configuration::new(...).write_binary_file(...)`).
This matches the `tests/process_boundary.rs:27` pattern but is
not documented anywhere a fresh agent would find quickly. For a
human deploying spirit-next side-by-side, the home-manager module
that builds the service needs to materialize this rkyv file from
typed Nix at activation time (analogous to how
`persona-spirit-daemon.service` materializes its NOTA argument
directly). The wire-shape sub-agent (Sub-agent 1) and deploy
sub-agent (Sub-agent 3) likely cover the home-manager surface;
flagging it here as the daemon-side gap that surfaces empirically
the moment you try to start the daemon by hand.

## Behavioural verdict

**spirit-next is ALMOST usable as a side-by-side deploy today.**

What works **right now**, end-to-end, from CLI through socket
through daemon through redb and back, both via local cargo and
Nix-built binaries:

- Daemon startup with a binary configuration file
- Unix socket bind, stale-socket cleanup, request handling loop
- Binary protocol (length-prefixed rkyv) on the wire — rejects
  raw NOTA text + garbage bytes
- `Record / Observe / Lookup / Count / Remove` — all five
  schema-declared input ops
- Validation rejections (`EmptyTopic`, `EmptyDescription`,
  `EmptyQueryTopic`) at the input boundary
- Durable storage to a redb `.sema` file; survives daemon
  restart; commit sequence persists; database marker advances
  per write; record identifier sequence monotonic
- Multi-topic records; partial vs full topic-match query
- Testing-trace instrumentation surface (trace socket; cli
  collects events; daemon emits typed phase names)
- Schema-emitted Rust round-trip; binary boundary guards;
  hand-rolled rkyv codec absent

What's **incompatible with production wire shape**:

- Reply shape carries `DatabaseMarker` — every reply is richer
  than production's terse `(RecordAccepted N)`
- No `ChangeCertainty / State / Watch / Unwatch / Tap / Untap`
- No `Observe Topics` (bare-token reply) — only `Observe Query`
- No `Any` TopicMatch — only `Partial` and `Full`
- `Magnitude` schema lacks `Zero` (production has it for
  removal-candidate nomination)
- `Kind` matches (Decision / Principle / Correction /
  Clarification / Constraint — five variants) — parity here

What's **missing or undocumented for deployment**:

- Daemon config is a binary rkyv file with no NOTA-text or
  schema-driven materializer for home-manager to call.
  Side-by-side deploy needs either: (a) a tiny Nix helper that
  emits the rkyv file from typed Nix at home-manager activation
  time, or (b) growing a `Configuration::from_nota_string`
  surface (which would re-add NOTA-text to the daemon — likely
  violates Spirit 1373).

## Recommendations — minimum changes to make spirit-next daily-usable

Ranked by smallness:

1. **Bump `flake.lock` for `schema-rust-next-source`** so the
   pushed-remote `nix build` succeeds. One-line lockfile change,
   one commit, one push. Without this, every Nix user who tries
   `nix build github:LiGoldragon/spirit-next` hits the staleness
   panic on first try.

2. **Add a tiny home-manager activation step** that emits the
   binary configuration rkyv file from typed Nix attrs (socket
   paths, db path, optional trace socket path). This is the only
   piece that's empirically missing on the deploy path. The
   typed-Nix-to-rkyv shape mirrors what
   `persona-spirit-daemon-next.service` already does in NOTA
   text form, except spirit-next has consciously moved the
   text decoder out of the daemon.

3. **Decide the production-parity strategy** as a deliberate
   design call (not implicit drift). Two coherent paths:
   - **Side-by-side, no wire parity**: spirit-next ships in its
     own `spirit-next` slot with its own richer reply shape,
     its own CLI, its own state directory. No agent expects
     spirit-next to answer the same questions as `spirit`.
     Cutover is a deliberate intent-capture event, not an
     invisible alias change. This matches the explicit
     side-by-side discipline of `skills/spirit-cli.md`
     §"Deployment slots".
   - **Side-by-side with reply-shape parity**: spirit-next
     grows a "v0.3 reply mode" (terse `(RecordAccepted N)`,
     bare-token Observe Topics, etc.) gated by a schema-level
     reply-shape selection so existing `spirit` clients can
     point at the spirit-next socket transparently. Richer
     replies become opt-in. Significantly more work; only
     worth it if cutover is intended to be transparent.

4. **Land the missing operations** in priority order if the
   parity path is chosen: `ChangeCertainty` first (most-used
   workflow op after Record), then `State`, then `Watch/Unwatch`.
   `Tap/Untap` is a no-op placeholder even in production.

5. **Grow the schema with an `Any` TopicMatch variant or a
   bare `Topics` top-level Observe**. The current "unknown
   TopicMatch variant Any" parse failure is a small papercut
   for agents that use the production query patterns.

The lockfile bump (item 1) is the absolute minimum: with it, the
pushed remote builds, all flake checks pass, all binaries
produce, and a side-by-side `spirit-next` slot with its own
state and sockets is a CriomOS-home module away. The wire
divergence (items 3-5) is a design decision the orchestrator
synthesises, not a defect.

## Evidence cleanup

- Test daemons killed (PIDs 26077, 27058 — both gone after
  smoke runs).
- `/tmp/spirit-next-smoke-test{,-2}` removed.
- `/tmp/spirit-next-config-helper{,-target}` removed.
- `/tmp/spirit-next-build.log` and `/tmp/spirit-next-lib.rs`
  (scratch files used during diagnosis) removed.
- Production daemon `persona-spirit-daemon-v0.3.0.service`
  still running, same PID 3068577, same start time
  2026-06-01 12:06:46.
- Production state dir `~/.local/state/persona-spirit/v0.3.0/`
  untouched (last mtime on the redb predates this audit).

No commits made. No worktrees created (the audit ran entirely
out of the existing `/git/...` checkout in read-and-build mode,
which is allowed since no source was modified).
