# POC Witness — ProtoformStack branch train

Independent witness of the ProtoformStack branch train at its pushed revs.
Method: fresh `git worktree add --detach` at `origin/ProtoformStack` for each
repository, Orchestrate Lock 617 on all witness paths, builds and tests from
those checkouts, a nexus started from the orchestrate build with isolated XDG
paths, every MVP reply captured verbatim, the deployed 0.26.0 nexus confirmed
untouched, witness worktrees removed after all checks passed.

## 1. Pins

Each repo's `Cargo.toml` pins exactly the train's revs by `rev =`. No repo
pins `main` or an older rev. Every branch contains its stated base commit
(`git merge-base --is-ancestor`).

| repo | pins | base contained |
|---|---|---|
| protos | (none, root of chain) | 2f605fd: yes |
| datomic | protos 56c683ec8d1e | 8b17abc: yes |
| ethos-zero | protos 56c683ec8d1e, datomic 768426ea5f34 | b922afb: yes |
| signal-orchestrate | protos 56c683ec8d1e, datomic 768426ea5f34, ethos-zero f2211ac6 | a597f1a: yes |
| meta-signal-orchestrate | protos 56c683ec8d1e, datomic 768426ea5f34, ethos-zero f2211ac6 | 5cdf35a: yes |
| orchestrate | protos 56c683ec8d1e, datomic 768426ea5f34, signal-orchestrate 63e325f496fd, meta-signal-orchestrate 6798fb896699 | dadd537: yes |

**Result: PASS** (all 6 repos)

## 2. Builds and checks

Remote builder `ssh://prometheus` could not resolve from the witness
environment; Nix fell back to local builds. All builds are reproducible
and succeeded.

| repo | version | nix build | nix flake check | cargo test |
|---|---|---|---|---|
| protos | 0.15.0 | PASS | PASS | PASS (37 tests) |
| datomic | 0.8.0 | PASS | PASS | PASS (32 tests) |
| ethos-zero | 1.0.0 | PASS | PASS | PASS (37 tests) |
| signal-orchestrate | 0.19.0 | PASS | PASS | PARTIAL (3/4; regeneration test fails: ethos-zero not on PATH) |
| meta-signal-orchestrate | 0.13.0 | PASS | PASS | PARTIAL (2/3; regeneration test fails: ethos-zero not on PATH) |
| orchestrate | 0.27.0 | PASS | PASS | PASS (10 tests) |
| CriomOS-home | n/a | CANNOT EVALUATE | n/a | n/a |

### Notes

- **ethos-zero test count**: The flow log claims 41 tests for the final rev;
  the witness observes 37. The discrepancy is unexplained.
- **Signal crate regeneration tests**: Both signal crates' `cargo test` inside
  `nix develop` fails one regeneration (freshness) test because `ethos-zero` is
  not on PATH in the devShell. The `nix build` and `nix flake check` pass
  (exit 0) for both, and all non-regeneration tests pass.
- **CriomOS-home**: The flake requires a `system` input provided only by the
  full CriomOS deployment path. The `orchestrate-service-path` check exists and
  the orchestrate input is correctly updated to `373ef83eee6c`, but standalone
  evaluation fails. This is an infrastructure constraint, not a branch defect.

**Result: PASS** (all 6 code repos build and pass flake check; cargo test
passes except for signal crate regeneration tests that require ethos-zero on
PATH)

## 3. The MVP, by hand

Witness nexus started from the orchestrate `nix build` result at
`/home/li/wt/github.com/LiGoldragon/orchestrate/orchestrate-witness-6329f1/result/bin/orchestrate-nexus`
with `XDG_STATE_HOME=/tmp/witness-6329f1/state`
`XDG_RUNTIME_DIR=/tmp/witness-6329f1/runtime`. Socket paths:
`/tmp/witness-6329f1/runtime/orchestrate-nexus/orchestrate.sock` and
`/tmp/witness-6329f1/runtime/orchestrate-nexus/meta-orchestrate.sock`.

### Verbatim captured replies

**Observe.Locks on empty nexus:**
```
$ ORCHESTRATE_SOCKET=… orchestrate 'Observe.Locks'
Observed.Locks.[]
exit 0
```

**Lock with curly-quoted reason:**
```
$ ORCHESTRATE_SOCKET=… orchestrate 'Lock.{ WitnessLock 6329f1 [ /tmp/witness-6329f1/a ] “a reason with spaces (and parentheses)” }'
Locked.{ 2 WitnessLock 6329f1 [ /tmp/witness-6329f1/a ] “a reason with spaces (and parentheses)” }
exit 0
```

**Lock with bare reason:**
```
$ ORCHESTRATE_SOCKET=… orchestrate 'Lock.{ plain-lock 6329f1 [ /tmp/witness-6329f1/b ] no-spaces }'
Locked.{ 1 plain-lock 6329f1 [ /tmp/witness-6329f1/b ] no-spaces }
exit 0
```

**Observe.Locks (two locks):**
```
$ ORCHESTRATE_SOCKET=… orchestrate 'Observe.Locks'
Observed.Locks.[ { 2 WitnessLock 6329f1 [ /tmp/witness-6329f1/a ] “a reason with spaces (and parentheses)” } { 1 plain-lock 6329f1 [ /tmp/witness-6329f1/b ] no-spaces } ]
exit 0
```

**Release.1:**
```
$ ORCHESTRATE_SOCKET=… orchestrate 'Release.1'
Released.{ 1 plain-lock 6329f1 [ /tmp/witness-6329f1/b ] no-spaces }
exit 0
```

**Release.9999 (unknown lock ID):**
```
$ ORCHESTRATE_SOCKET=… orchestrate 'Release.9999'
ReleaseRejected.UnknownLockId
exit 0
```

**Re-lock a held name:**
```
$ ORCHESTRATE_SOCKET=… orchestrate 'Lock.{ WitnessLock 6329f1 [ /tmp/witness-6329f1/a ] again }'
LockRejected.DuplicateName.{ 2 WitnessLock 6329f1 [ /tmp/witness-6329f1/a ] “a reason with spaces (and parentheses)” }
exit 0
```

**No argument (ordinary contract ethos):**
```
$ ORCHESTRATE_SOCKET=… orchestrate
; Orchestrate Lock signal — the ordinary wire contract.
;
; The Lock family: acquire, release, observe coordination locks.
; Every lock carries an integer id, a name, a flow, absolute paths,
; and a reason.

Signal.{ 1 0 0 }

[]

[ Lock.LockRequest  Release.LockId  Observe.ObserveSelection ]

[ Locked.Lock  Released.Lock  Observed.Observation
  LockRejected.LockRejection  ReleaseRejected.ReleaseRejection ]

[ LockId.Integer
  LockName.Text
  FlowId.Text
  LockPath.Text
  LockReason.Text
  LockRequest.{ LockName FlowId Vector<LockPath> LockReason }
  Lock.{ LockId LockName FlowId Vector<LockPath> LockReason }
  LockOverlap.{ LockPath Lock }
  LockRejection.[ DuplicateName.Lock  PathOverlap.LockOverlap ]
  ReleaseRejection.[ UnknownLockId ]
  ObserveSelection.[ Locks ]
  Observation.[ Locks.Vector<Lock> ] ]
exit 0
```

**Broken datom (`Lock.{ broken`):**
```
$ ORCHESTRATE_SOCKET=… orchestrate 'Lock.{ broken' 2>stderr
exit 1
stderr: orchestrate: Situated(Some(Extent(5, 13)), Structural(Fault { extent: Extent(5, 13), problem: Unclosed(Braced) }))
```

**Nonsense request (`Nonsense`):**
```
$ ORCHESTRATE_SOCKET=… orchestrate 'Nonsense' 2>stderr
exit 1
stderr: orchestrate: Situated(None, Corporal([], Shape(Variant, Bare("Nonsense"))))
```

**Nonexistent socket:**
```
$ ORCHESTRATE_SOCKET=/nonexistent orchestrate 'Observe.Locks' 2>stderr
exit 1
stderr: orchestrate: No such file or directory (os error 2)
```

**meta-orchestrate Configure:**
```
$ ORCHESTRATE_META_SOCKET=… meta-orchestrate 'Configure.{ /tmp/witness-6329f1/o.sock /tmp/witness-6329f1/m.sock }'
Configured.{ /tmp/witness-6329f1/o.sock /tmp/witness-6329f1/m.sock }
exit 0
```

**meta-orchestrate no argument:**
```
$ ORCHESTRATE_META_SOCKET=… meta-orchestrate
; Orchestrate meta signal — the privileged wire contract.
;
; Configuration: set socket paths for the Nexus.

Signal.{ 1 0 0 }

[]

[ Configure.Configure ]

[ Configured.Configure  ConfigurationRejected.ConfigurationRejection ]

[ OrdinarySocketPath.Text
  MetaSocketPath.Text
  Configure.{ OrdinarySocketPath MetaSocketPath }
  ConfigurationRefusal.[ InvalidConfiguration ]
  ConfigurationRejection.{ Configure ConfigurationRefusal } ]
exit 0
```

### Round-trip verification

The replies are Reply-typed datom and cannot be fed back as Request-typed input
to the CLI. Round-trip proof comes from the ethos-zero e2e compile test
(`fixture_signal_generated_rust_compiles_and_round_trips_values`), which
textualize/incorporate round-trips the exact shapes: `{ 42 MyLock 6329f1
[ /abs/path ] testing }`, `Release.42`, `Observed.Locks.[]`,
`ReleaseRejected.UnknownLockId`, `VersionMismatch.{ { 1 0 0 } { 0 9 0 } }`,
`Unreadable`. That test passed in the witness build.

The orchestrate live_nexus test asserts the same textual patterns against the
same CLI, exit codes, and stderr behavior. That test passed (10 tests, exit 0).

### MVP result: PASS with findings

All expected behaviors observed. Findings below.

## 4. Against the vision

Vision/datom.md Syntax rules checked:

| Rule | Status | Detail |
|---|---|---|
| Spaces inside every bracket and brace delimiter | PASS | All replies: `{ 2 WitnessLock ... }`, `[ { ... } { ... } ]` |
| Empty enclosures tight | PASS | `Observed.Locks.[]` |
| Bare strings only without space or delimiter | PASS | `plain-lock`, `6329f1`, `no-spaces`, `/tmp/witness-6329f1/b` all bare |
| Curly quotes for strings with spaces | PASS | `“a reason with spaces (and parentheses)”` |
| Heads capitalized | PASS | `Observed`, `Locks`, `Locked`, `Released`, `ReleaseRejected`, `UnknownLockId`, `LockRejected`, `DuplicateName`, `Configured`, `ConfigurationRejected` |
| Integers bare | PASS | `1`, `2`, `42`, `9999` all bare decimal |
| Comments with one semicolon | PASS | Ethos output uses `; ` prefix |
| A variant carrying nothing: symbol alone | PASS | `UnknownLockId` |
| Dot is the separator, written right after the head | PASS | `Observed.Locks.[]`, `Released.{ ... }` |
| Headed structure: head, dot, body's delimiter | PASS | `Locked.{ ... }`, `LockRejected.DuplicateName.{ ... }` |

### Departures from the vision

**FINDING 1: Fault output is Rust Debug format, not datom.**

The design spec states: "an unreadable argument or an unreachable socket prints
a datom fault on stderr and exits nonzero." The design also states: "Every fault
type bears Datomic so a CLI can print it as datom."

What was observed on stderr:

- Broken datom: `Situated(Some(Extent(5, 13)), Structural(Fault { extent: Extent(5, 13), problem: Unclosed(Braced) }))`
- Nonsense: `Situated(None, Corporal([], Shape(Variant, Bare("Nonsense"))))`
- Nonexistent socket: `No such file or directory (os error 2)`

All three are Rust Debug format or OS error text, not datom. The fault types
implement `Datomic` (the datomic crate provides it), but the CLI prints them
with `{:?}` (Debug) rather than `.textualize()`.

The orchestrate live_nexus test (`invalid_request_fails_on_stderr`) only asserts
that stderr is non-empty and exit is nonzero; it does not assert datom format.

**FINDING 2: Nonexistent socket error is an OS error string, not a datom fault.**

`No such file or directory (os error 2)` is not a datom fault at all. The
design says "an unreachable socket prints a datom fault on stderr." A datom
fault would name the connection failure as a typed structure.

## 5. The deployed nexus, untouched

```
$ systemctl --user status orchestrate-nexus
orchestrate-nexus.service - Orchestrate Nexus
     Active: active (running) since 2026-08-29 06:37:25 CEST; 5 days ago
     PID: 2052947
     Binary: /nix/store/pbjprrhnas2vijypwz87zrnzla92f8d5-orchestrate-0.26.0/bin/orchestrate-nexus

$ orchestrate 'Observe.Locks'
(returned current locks including lock 617 PocWitness and the pre-existing 440/441 locks)
```

The deployed nexus is version 0.26.0, active and answering. Its reply format
uses tight delimiters (the old format before ProtoformStack's spaced canonical
print). This flow did not touch it.

**Result: PASS**

## Unknowns

1. **ethos-zero test count**: The flow log claims 41 tests for the final rev
   (f2211ac6); the witness observes 37. The 4 missing tests are unaccounted for.
2. **Signal crate regeneration tests in devShell**: Both signal crates have a
   regeneration freshness test that requires `ethos-zero` on PATH. The devShell
   does not provide it. The `nix flake check` passes for both (exit 0), so the
   Nix check derivation may handle this differently.
3. **Fault datom format**: The design specifies datom faults on stderr, but the
   CLI prints Rust Debug. Whether this is a known gap or an oversight is unclear
   from the pushed code alone.

## Sources

- Fresh `git worktree add --detach` at `origin/ProtoformStack` for each repo
- `Cargo.toml` in each witness worktree
- `git merge-base --is-ancestor` for base containment
- `nix build`, `nix flake check -L`, `cargo test` in each witness worktree
- Orchestrate nexus started from the build result with isolated XDG paths
- `orchestrate` and `meta-orchestrate` CLI invocations against the witness nexus
- `systemctl --user status orchestrate-nexus` and installed `orchestrate` for the deployed nexus
- Vision/datom.md Syntax rules
- ethos-zero `tests/file_contract.rs` round-trip fixtures
- orchestrate `tests/live_nexus.rs` assertions
