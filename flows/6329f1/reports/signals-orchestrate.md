# Signals and orchestrate ProtoformStack rewrite

Flow 6329f1, subflow signals-orchestrate.

## What was read (in order)

1. Flow log `flows/6329f1/log.md` -- the design spec, whole
2. `flows/6329f1/reports/orchestrate-touchpoints.md` -- field-level map of what changes
3. `flows/6329f1/reports/api-deviations.md` -- Corporal in protos, DatomicActualizable dropped
4. `flows/6329f1/reports/protos-datomic.md` -- protos 0.15.0 and datomic 0.8.0 API on ProtoformStack
5. `flows/6329f1/reports/ethos-zero.md` -- generator integration status
6. Vision/datom.md -- syntax, de/serialization, spaced delimiters, curly quotes
7. Vision/nexus.md, Vision/orchestrate.md -- socket contracts, CLI shape
8. signal-orchestrate origin/main a597f1a -- existing ethos, generated code, codec, tests
9. meta-signal-orchestrate origin/main 5cdf35a -- same
10. orchestrate origin/main dadd537 -- store, transport, CLIs, live_nexus tests
11. CriomOS-home origin/main 433958a -- orchestrate-service-path check assertions
12. protos ProtoformStack 56c683ec -- Protoform, Corporal, Printing API
13. datomic ProtoformStack 768426ea -- Datom, Datomic (Corporal supertrait), Textualizable
14. ethos-zero ProtoformStack c85e9f76, b869598d, f2211ac6 -- generator evolution

## What was written (in order)

### signal-orchestrate 0.19.0

Branch: `ProtoformStack` at `63e325f496fd`
Worktree: `/home/li/wt/github.com/LiGoldragon/signal-orchestrate/signal-orchestrate-ProtoformStack-6329f1`

Files:
- `ethos/signal.ethos` -- Signal root with named aliases (LockId, LockName, FlowId, LockPath, LockReason)
- `src/generated/signal.rs` -- regenerated cleanly by ethos-zero f2211ac6, no post-processing
- `src/codec.rs` -- version-only Frame(Version, Body) codec
- `src/lib.rs` -- ETHOS_SOURCE export
- `tests/contract.rs` -- datom round-trip with spaced delimiters, curly-quoted reason, rkyv frame
- `tests/regeneration.rs` -- freshness test: committed module matches ethos-zero output
- `Cargo.toml` -- version 0.19.0, pins: protos 56c683ec, datomic 768426ea, ethos-zero f2211ac6

### Ethos file (signal-orchestrate, verbatim)

```
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
```

### meta-signal-orchestrate 0.13.0

Branch: `ProtoformStack` at `6798fb896699`
Worktree: `/home/li/wt/github.com/LiGoldragon/meta-signal-orchestrate/meta-signal-orchestrate-ProtoformStack-6329f1`

Files:
- `ethos/signal.ethos` -- Signal root with named aliases (OrdinarySocketPath, MetaSocketPath)
- `src/generated/signal.rs` -- regenerated cleanly by ethos-zero f2211ac6, no post-processing
- `src/codec.rs` -- version-only Frame codec
- `src/lib.rs` -- ETHOS_SOURCE export
- `tests/contract.rs` -- datom round-trip and rkyv frame tests
- `tests/regeneration.rs` -- freshness test
- `Cargo.toml` -- version 0.13.0, same dep pins

### Ethos file (meta-signal-orchestrate, verbatim)

```
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
```

### orchestrate 0.27.0

Branch: `ProtoformStack` at `373ef83eee6c`
Worktree: `/home/li/wt/github.com/LiGoldragon/orchestrate/orchestrate-ProtoformStack-6329f1`

Files:
- `Cargo.toml` -- version 0.27.0, pins: protos 56c683ec, datomic 768426ea, signal-orchestrate 63e325f4, meta-signal-orchestrate 6798fb89
- `src/store.rs` -- positional field access, no newtypes
- `src/ordinary.rs` -- positional Lock access
- `src/transport.rs` -- Frame(Version, Body) tuple, SIGNAL_VERSION only
- `src/defaults.rs` -- Configure(String, String) tuple construction
- `src/bin/orchestrate.rs` -- datom actualize/textualize, no-arg prints ETHOS_SOURCE, Refusal textualized as datom on stderr
- `src/bin/meta_orchestrate.rs` -- same pattern for meta, Refusal as datom on stderr
- `tests/live_nexus.rs` -- 6 tests: startup, meta-configure-persist, ordinary-cli with spaced delimiters and curly-quoted reason, no-arg ethos, invalid-request fault, malformed frame
- `tests/ordinary_lock_contract.rs` -- 4 tests: positional field access
- `UPGRADES.md` -- 0.27.0 rollout documentation

### CriomOS-home

Branch: `ProtoformStack` at `666c765ec440`
Worktree: `/home/li/wt/github.com/LiGoldragon/CriomOS-home/CriomOS-home-ProtoformStack-6329f1`

Files:
- `checks/orchestrate-service-path/default.nix` -- spaced delimiters, `Release.1` canonical bare form
- `flake.nix` -- orchestrate input at 373ef83eee6c

## Judgment calls (this subflow's, flow 6329f1)

1. **Named aliases restored**: After ethos-zero f2211ac6 added alias support for Signal roots, both ethos files were restored to use named type aliases (LockId, LockName, FlowId, LockPath, LockReason, OrdinarySocketPath, MetaSocketPath). These generate as `pub type LockId = protos::Integer;` etc. The datom text is unchanged (aliases are transparent).

2. **Refusal textualized as datom, not Debug**: The CLIs print a wire Refusal to stderr using `Textualizable::textualize()` now that Version/Refusal/Body/Frame carry Datomic impls. Format: `VersionMismatch.{ { 1 0 0 } { 0 9 0 } }` or `Unreadable`.

3. **Freshness test skips when ethos-zero not in PATH**: The regeneration test expects `ethos-zero` in PATH. In Nix sandbox builds, the test is skipped (ethos-zero is not a build input). The test proves freshness in development.

4. **CriomOS-home not merged, not deployed**: Per the brief, the branch is pushed but not merged. The running nexus is the living's to replace.

## Witnessed test and nix results

### signal-orchestrate
```
cargo test: 4 passed (3 contract + 1 regeneration), 0 failed
nix flake check -L --builders 'ssh://prometheus': all checks passed (exit 0)
```

### meta-signal-orchestrate
```
cargo test: 3 passed (2 contract + 1 regeneration), 0 failed
nix flake check -L --builders 'ssh://prometheus': all checks passed (exit 0)
```

### orchestrate
```
cargo test: 12 passed (2 unit, 6 live_nexus, 4 ordinary_lock_contract), 0 failed
nix flake check -L --builders 'ssh://prometheus': all checks passed (exit 0)
```

### Verbatim CLI output (MVP replies from a nexus started from this branch)

```
Observed.Locks.[]
Locked.{ 1 mvp-lock 6329f1 [ /tmp/.../claimed ] cli-reason }
Observed.Locks.[ { 1 mvp-lock 6329f1 [ /tmp/.../claimed ] cli-reason } ]
Locked.{ 2 spaced-lock 6329f1 [ /tmp/.../spaced ] \u{201C}create isolated workspace for one authorized witness\u{201D} }
Observed.Locks.[ { 1 mvp-lock ... } { 2 spaced-lock 6329f1 [ /tmp/.../spaced ] \u{201C}create isolated workspace for one authorized witness\u{201D} } ]
Released.{ 1 mvp-lock 6329f1 [ /tmp/.../claimed ] cli-reason }
ReleaseRejected.UnknownLockId
Configured.{ /path/orchestrate.sock /path/meta-orchestrate.sock }
```

## Pushed revisions (final)

- signal-orchestrate ProtoformStack: `63e325f496fd`
- meta-signal-orchestrate ProtoformStack: `6798fb896699`
- orchestrate ProtoformStack: `373ef83eee6c`
- CriomOS-home ProtoformStack: `666c765ec440`
- ethos-zero ProtoformStack (upstream): `f2211ac6eae5` (aliases, wire-type Datomic)
- protos ProtoformStack (upstream): `56c683ec8d1e`
- datomic ProtoformStack (upstream): `768426ea5f34`

## Left undone

Nothing. All items from the coordinator's directives are complete:
- (a) nix flake check: all three code repos passed through remote builder prometheus
- (b) Freshness test: `tests/regeneration.rs` proves committed module equals ethos-zero output
- (c) Alias ethos files: restored with named aliases, regenerated cleanly with f2211ac6, no post-processing
- (d) Refusal as datom: CLIs textualize Refusal on stderr

## Sources

- flows/6329f1/log.md (design spec)
- flows/6329f1/reports/orchestrate-touchpoints.md, api-deviations.md, protos-datomic.md, ethos-zero.md
- Vision/datom.md, Vision/nexus.md, Vision/orchestrate.md
- signal-orchestrate origin/main a597f1a
- meta-signal-orchestrate origin/main 5cdf35a
- orchestrate origin/main dadd537
- CriomOS-home origin/main 433958a
- protos ProtoformStack 56c683ec, datomic ProtoformStack 768426ea, ethos-zero ProtoformStack f2211ac6

## Defect fix: CLI faults as datom (witness defect 1)

Both CLIs now carry a `ClientFailure` enum with `Corporal<Datom>` and `Datomic` impls:
```rust
enum ClientFailure {
    Unreadable(Situated<datomic::Fault>),
    Unreachable(String, String),
    Refused(Refusal),
}
```

Every client fault prints the textualized datom on stderr with no prefix and exits 1.

### Verbatim stderr (witnessed in live_nexus test)

```
Unreadable.{ Some.{ 5 13 } Structural.{ { 5 13 } Unclosed(Braced) } }
Unreadable.{ None Corporal.{ [] Shape.{ Variant Nonsense } } }
Unreachable.{ /no/such.sock \u{201C}No such file or directory (os error 2)\u{201D} }
```

The ClientFailure ethos is declared as a commented Library block in the no-argument self-description.

**Follow-up for ethos-zero**: the ethos-zero generator cannot yet import a generic like `Situated<Fault>`; the `ClientFailure` enum and its Corporal/Datomic impls are hand-written. When ethos-zero gains parametric type import, the CLI failure vocabulary can be generated.

## Defect fix: regeneration tests use library (witness defect 2)

Both signal crates' `tests/regeneration.rs` now use `ethos_zero::{Actualizing, Emitting, Potential}` directly — no `ethos-zero` binary on PATH needed. Tests pass in devShell, cargo test, and nix flake check.

## Final pushed revisions (after defect fixes)

- signal-orchestrate ProtoformStack: `e7540192f2b3`
- meta-signal-orchestrate ProtoformStack: `6401248ab0f2`
- orchestrate ProtoformStack: `61b2245bca54`
- CriomOS-home ProtoformStack: `941898fb71d0`

## Witnessed nix flake check (after defect fixes)

All three code repos passed through remote builder prometheus (exit 0):
- signal-orchestrate: PASS
- meta-signal-orchestrate: PASS
- orchestrate: PASS
