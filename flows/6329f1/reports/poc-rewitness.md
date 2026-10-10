# POC Re-witness -- CLI fault datom at orchestrate 61b2245bca54

Independent re-witness of the CLI fault fix claimed at orchestrate
ProtoformStack `61b2245bca54` (signal-orchestrate `e7540192f2b3`,
meta-signal-orchestrate `6401248ab0f2`, CriomOS-home `941898fb71d0`).

Method: fresh `git worktree add --detach` at each target rev, Orchestrate
Lock 622 on the orchestrate worktree and Lock 623 on the signal crate
worktrees, builds and tests from those checkouts, a nexus started from
the orchestrate build with isolated XDG paths
(`XDG_STATE_HOME=/tmp/rw6329f1/state`,
`XDG_RUNTIME_DIR=/tmp/rw6329f1/runtime`), every fault reply captured
verbatim with `od -c` byte-level verification, worktrees removed and locks
released after all checks passed.

## 1. Verbatim stderr, exit codes, and byte-level evidence

**Test 1 -- broken datom (`Lock.{ broken`):**

```
exit: 1
stderr: Unreadable.{ Some.{ 5 13 } Structural.{ { 5 13 } Unclosed(Braced) } }
```

od -c:
```
0000000   U   n   r   e   a   d   a   b   l   e   .   {       S   o   m
0000020   e   .   {       5       1   3       }       S   t   r   u   c
0000040   t   u   r   a   l   .   {       {       5       1   3       }
0000060       U   n   c   l   o   s   e   d   (   B   r   a   c   e   d
0000100   )       }       }  \n
```

`Unclosed(Braced)` uses ASCII parentheses (`(` = 0x28, `)` = 0x29), which is
Rust Debug format for `protos::Problem::Unclosed(Enclosure::Braced)`. Datom
would be `Unclosed.Braced` (dot-separated variant).

**Test 2 -- nonsense request (`Nonsense`):**

```
exit: 1
stderr: Unreadable.{ None Corporal.{ [] Shape.{ Variant Nonsense } } }
```

od -c: all ASCII, dot-separated variants. Clean datom.

**Test 3 -- unreachable socket (`ORCHESTRATE_SOCKET=/no/such.sock`):**

```
exit: 1
stderr: Unreachable.{ /no/such.sock “No such file or directory (os error 2)” }
```

od -c:
```
0000000   U   n   r   e   a   c   h   a   b   l   e   .   {       /   n
0000020   o   /   s   u   c   h   .   s   o   c   k     342 200 234   N
0000040   o       s   u   c   h       f   i   l   e       o   r       d
0000060   i   r   e   c   t   o   r   y       (   o   s       e   r   r
0000100   o   r       2   ) 342 200 235       }  \n
```

`342 200 234` = U+201C (LEFT DOUBLE QUOTATION MARK), `342 200 235` = U+201D
(RIGHT DOUBLE QUOTATION MARK). The quotes are curly, not ASCII. The main
flow's suspicion that these are ASCII double quotes is **disproved**.

**Test 4 -- corporal fault inside a variant (`Release.abc`):**

```
exit: 1
stderr: Unreadable.{ None Corporal.{ [] Value.abc } }
```

od -c: all ASCII, dot-separated variants. Clean datom.

**Test 5 -- arity fault (`meta-orchestrate Configure.{ only-one }`):**

```
exit: 1
stderr: Unreadable.{ None Corporal.{ [] Arity.{ 2 1 } } }
```

od -c: all ASCII, dot-separated variants. Clean datom.

## 2. Round-trip through the datomic reader

Each captured stderr line was fed back through the orchestrate CLI as input.
All five delineate successfully (no structural fault from the reader). Tests
2--5 re-delineate into the same nested structure. Test 1 re-delineates with
`Unclosed(Braced)` split into two forms -- `Unclosed` as a bare and `(Braced)`
as a parenthesized group -- rather than the variant `Unclosed.Braced`. The
round-trip is broken for the `Structural` fault variant.

| Test | Delineates | Conceives as intended datom | Round-trip |
|---|---|---|---|
| 1 Lock.{ broken | yes | NO -- `Unclosed(Braced)` is Debug, not datom | BROKEN |
| 2 Nonsense | yes | yes | clean |
| 3 unreachable socket | yes | yes | clean |
| 4 Release.abc | yes | yes | clean |
| 5 Configure.{ only-one } | yes | yes | clean |

## 3. Location of non-datom formatting

The `Structural` arm of `impl Datomic for Fault` in the datomic crate uses
Rust Debug (`{:?}`) on `protos::Problem` instead of datomizing it:

**File:** `datomic/src/lib.rs` at commit `768426ea5f34`, line 953

```rust
Fault::Structural(f) => Datom::Variant(
    "Structural".to_owned(),
    Separator::Period,
    Some(Box::new(Datom::Struct(vec![
        Datom::Struct(vec![f.extent.0.datomize(), f.extent.1.datomize()]),
        Datom::Bare(format!("{:?}", f.problem)),   // <-- Debug, not datomize
    ]))),
),
```

The `Conceptual` and `Corporal` arms of the same impl correctly call
`problem.datomize()` on `datomic::Problem`. The `Structural` arm cannot call
`.datomize()` because `protos::Problem` does not implement `Datomic` (protos
is unaware of datomic). The datomic crate would need to convert
`protos::Problem` to `Datom` explicitly, as it does for `protos::Extent` via
`f.extent.0.datomize()`.

No other non-datom formatting was found. The orchestrate `ClientFailure::datomize()`
and the `datomize_situated`/`datomize_option_extent` helpers produce clean datom.

## 4. Signal crate cargo test

Both signal crates pass all tests in `nix develop`, including the
regeneration (freshness) tests that failed in the previous witness.
The new revs drive regeneration through the ethos-zero library instead
of requiring the binary on PATH.

**signal-orchestrate e7540192f2b3:**
```
test rkyv_frame_round_trips_with_version_validation ... ok
test spaced_reason_uses_curly_quotes ... ok
test all_datom_roots_round_trip ... ok
test committed_module_matches_ethos_zero_generation ... ok

test result: ok. 4 passed; 0 failed
```

**meta-signal-orchestrate 6401248ab0f2:**
```
test rkyv_frame_version_only_validation ... ok
test all_meta_datom_roots_round_trip ... ok
test committed_module_matches_ethos_zero_generation ... ok

test result: ok. 3 passed; 0 failed
```

**Result: PASS**

## 5. CriomOS-home pin and deployed nexus

**CriomOS-home 941898fb71d0** pins orchestrate at `61b2245bca54`:
```
orchestrate.url = "github:LiGoldragon/orchestrate/61b2245bca54";
```

**Deployed nexus:**
```
Active: active (running) since 2026-08-29 06:37:25 CEST; 5 days ago
Binary: /nix/store/pbjprrhnas2vijypwz87zrnzla92f8d5-orchestrate-0.26.0/bin/orchestrate-nexus
```

Answering: `Observe.Locks` returns current locks. Version is 0.26.0 (the
production binary, not the ProtoformStack branch). The deployed nexus was not
touched by this witness.

**Result: PASS**

## Summary

| Item | Result |
|---|---|
| 1. Verbatim fault capture | 4/5 clean datom; 1 contains Debug format |
| 2. Non-datom location | `datomic/src/lib.rs:953` at `768426ea5f34` -- `format!("{:?}", f.problem)` |
| 3. Signal crate tests | PASS (all tests including regeneration) |
| 4. CriomOS-home pin | PASS (pins 61b2245bca54) |
| 5. Deployed nexus | PASS (0.26.0, active, answering) |

**Overall: PARTIAL PASS.** The fix at 61b2245bca54 converts all `ClientFailure`
variants to datom via `.textualize()`, resolving the previous witness's Finding 2
(unreachable socket now uses curly quotes and typed structure) and most of
Finding 1 (Corporal and Conceptual faults are datom). One residual defect
remains: `Structural` faults (parser errors like `Unclosed(Braced)`) still
render `protos::Problem` in Rust Debug format because `datomic::Fault::datomize()`
uses `format!("{:?}", f.problem)` at `datomic/src/lib.rs:953`.

The main flow's suspicion that curly quotes are ASCII was disproved by byte-level
verification: U+201C/U+201D are present.

## Sources

- Fresh `git worktree add --detach` at target revs for orchestrate, signal-orchestrate, meta-signal-orchestrate
- `nix build` of orchestrate 61b2245bca54 (remote builder ssh-ng://prometheus)
- Orchestrate nexus started from build result with isolated XDG paths
- `orchestrate` and `meta-orchestrate` CLI invocations against witness nexus
- `od -c` byte-level capture of each stderr line
- Round-trip feeding of each stderr line through the orchestrate CLI
- `cargo test` in `nix develop` for signal-orchestrate and meta-signal-orchestrate
- `git show 941898fb71d0:flake.nix` for CriomOS-home pin verification
- `systemctl --user status orchestrate-nexus` and `orchestrate 'Observe.Locks'` for deployed nexus
- Cargo checkout of datomic at 768426ea5f34: `/home/li/.cargo/git/checkouts/datomic-e9a094725c87e3bc/768426e/src/lib.rs`
