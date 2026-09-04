# Final Witness -- ProtoformStack branch train at final revs

Independent witness of the ProtoformStack branch train after its last
re-pin (datomic a27f9b8e: Corporal/Datomic for protos structural types).
Method: fresh `git worktree add --detach` at each target rev, Orchestrate
Lock 629 on all seven worktree paths, builds and tests from those
checkouts, a nexus started from the orchestrate build with isolated XDG
paths (`XDG_STATE_HOME=/tmp/finalwitness-6329f1/state`,
`XDG_RUNTIME_DIR=/tmp/finalwitness-6329f1/runtime`), every reply captured
verbatim with `od -c` byte-level verification on the structural fault
line and the curly-quoted string, worktrees removed and lock released
after all checks passed.

## 1. Pins

Every rev exists on `origin/ProtoformStack` (verified by
`git merge-base --is-ancestor`).

Orchestrate's `Cargo.lock` resolves exactly one protos and one datomic:

| crate | count | rev |
|---|---|---|
| protos | 1 | 56c683ec8d1ec8f8f80e9e12251fbfd08d27d728 |
| datomic | 1 | a27f9b8e778935f1fb2ec0011620cf44a96ea81b |

`cargo tree -d` shows only `syn` (v2/v3) as a duplicate; no train crate
is duplicated.

Signal crates and ethos-zero all pin datomic a27f9b8e7789:

| repo | Cargo.toml pin |
|---|---|
| ethos-zero | `datomic = { git = "...", rev = "a27f9b8e7789" }` |
| signal-orchestrate | `datomic = { git = "...", rev = "a27f9b8e7789" }` |
| meta-signal-orchestrate | `datomic = { git = "...", rev = "a27f9b8e7789" }` |

CriomOS-home pins orchestrate at e631bad92ef2:

```
orchestrate.url = "github:LiGoldragon/orchestrate/e631bad92ef259e74d59fb83e24d17a9a24e2814";
```

**Result: PASS**

## 2. Builds and tests

Remote builder `ssh://prometheus` could not resolve; Nix fell back to
local builds. The build succeeded.

```
nix build (orchestrate 0.27.0 at e631bad92ef2): PASS
```

Cargo test results:

| repo | tests | result |
|---|---|---|
| orchestrate | 10 (6 live_nexus + 4 ordinary_lock_contract) | ok. 10 passed; 0 failed |
| signal-orchestrate | 4 (3 lib + 1 regeneration) | ok. 4 passed; 0 failed |
| meta-signal-orchestrate | 3 (2 lib + 1 regeneration) | ok. 3 passed; 0 failed |

All regeneration (freshness) tests pass -- the signal crates regenerate
through the ethos-zero library, resolving the earlier witness's
regeneration-on-PATH failure.

### Verbatim test tails

**orchestrate:**
```
test no_argument_prints_ethos_source ... ok
test malformed_frame_is_refused_before_it_reaches_the_store ... ok
test client_failures_are_datom_on_stderr ... ok
test zero_argument_startup_initializes_default_store_and_rejects_extras ... ok
test meta_configuration_persists_and_a_restart_resumes_it ... ok
test ordinary_cli_uses_datomic_request_reply_and_refusal_roots_against_a_live_nexus ... ok

test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out

test locks_are_atomic_complete_and_released_by_durable_id ... ok
test duplicate_names_and_overlapping_paths_are_typed_refusals ... ok
test observe_locks_is_a_name_then_id_ordered_point_in_time_value ... ok
test released_ids_never_reach_a_later_lock_after_restart ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

**signal-orchestrate:**
```
test rkyv_frame_round_trips_with_version_validation ... ok
test spaced_reason_uses_curly_quotes ... ok
test all_datom_roots_round_trip ... ok
test committed_module_matches_ethos_zero_generation ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

**meta-signal-orchestrate:**
```
test rkyv_frame_version_only_validation ... ok
test all_meta_datom_roots_round_trip ... ok
test committed_module_matches_ethos_zero_generation ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

**Result: PASS**

## 3. The MVP, by hand

Witness nexus started from the orchestrate `nix build` result at
`/home/li/wt/github.com/LiGoldragon/orchestrate/orchestrate-finalwitness-6329f1/result/bin/orchestrate-nexus`
with `XDG_STATE_HOME=/tmp/finalwitness-6329f1/state`
`XDG_RUNTIME_DIR=/tmp/finalwitness-6329f1/runtime`. Socket paths:
`/tmp/finalwitness-6329f1/runtime/orchestrate-nexus/orchestrate.sock` and
`/tmp/finalwitness-6329f1/runtime/orchestrate-nexus/meta-orchestrate.sock`.

### Verbatim captured replies

**Observe.Locks on empty nexus:**
```
$ ORCHESTRATE_SOCKET=... orchestrate 'Observe.Locks'
Observed.Locks.[]
exit 0
```

**Lock with curly-quoted reason:**
```
$ ORCHESTRATE_SOCKET=... orchestrate 'Lock.{ FinalWitness 6329f1 [ /tmp/finalwitness-6329f1/a ] "a reason with spaces" }'
Locked.{ 1 FinalWitness 6329f1 [ /tmp/finalwitness-6329f1/a ] "a reason with spaces" }
exit 0
```

**Observe.Locks (one lock):**
```
$ ORCHESTRATE_SOCKET=... orchestrate 'Observe.Locks'
Observed.Locks.[ { 1 FinalWitness 6329f1 [ /tmp/finalwitness-6329f1/a ] "a reason with spaces" } ]
exit 0
```

**Release.1:**
```
$ ORCHESTRATE_SOCKET=... orchestrate 'Release.1'
Released.{ 1 FinalWitness 6329f1 [ /tmp/finalwitness-6329f1/a ] "a reason with spaces" }
exit 0
```

**Broken datom (`Lock.{ broken`):**
```
$ ORCHESTRATE_SOCKET=... orchestrate 'Lock.{ broken' 2>stderr
exit 1
stderr: Unreadable.{ Some.{ 5 13 } Structural.{ { 5 13 } Unclosed.Braced } }
```

od -c of stderr:
```
0000000   U   n   r   e   a   d   a   b   l   e   .   {       S   o   m
0000020   e   .   {       5       1   3       }       S   t   r   u   c
0000040   t   u   r   a   l   .   {       {       5       1   3       }
0000060       U   n   c   l   o   s   e   d   .   B   r   a   c   e   d
0000100       }       }  \n
0000105
```

No parentheses in the byte stream. `Unclosed.Braced` is dot-separated
datom, not Debug format. This resolves the re-witness's residual defect.

**orchestrate with no argument (first ten lines):**
```
$ ORCHESTRATE_SOCKET=... orchestrate
; Orchestrate Lock signal — the ordinary wire contract.
;
; The Lock family: acquire, release, observe coordination locks.
; Every lock carries an integer id, a name, a flow, absolute paths,
; and a reason.

Signal.{ 1 0 0 }

[]

exit 0
```

**meta-orchestrate Configure:**
```
$ ORCHESTRATE_META_SOCKET=... meta-orchestrate 'Configure.{ /tmp/finalwitness-6329f1/o.sock /tmp/finalwitness-6329f1/m.sock }'
Configured.{ /tmp/finalwitness-6329f1/o.sock /tmp/finalwitness-6329f1/m.sock }
exit 0
```

### Byte-level verification of curly-quoted output

The Locked reply for a lock with a curly-quoted reason was captured and
verified by `od -c`. The quote delimiters are `342 200 234` (U+201C) and
`342 200 235` (U+201D). No ASCII double quote (0x22) is present.

```
0000000   L   o   c   k   e   d   .   {       2       B   y   t   e   C
0000020   h   e   c   k       6   3   2   9   f   1       [       /   t
0000040   m   p   /   f   i   n   a   l   w   i   t   n   e   s   s   -
0000060   6   3   2   9   f   1   /   a       ]     342 200 234   q   u
0000100   o   t   e   s       t   e   s   t 342 200 235       }  \n
```

### Debug and quote verification

All stdout and stderr lines were checked for:
- `(`-style Debug formatting (e.g., `Unclosed(Braced)`): **none found**
- ASCII double quotes (0x22) outside curly-quoted content: **none found**

All curly-quoted strings use U+201C/U+201D exclusively.

**Result: PASS**

## 4. The deployed nexus, untouched

```
$ systemctl --user status orchestrate-nexus
orchestrate-nexus.service - Orchestrate Nexus path-reservation service
     Active: active (running) since Sat 2026-08-29 06:37:25 CEST; 5 days ago
     Main PID: 2052947 (orchestrate-nex)
     Binary: /nix/store/pbjprrhnas2vijypwz87zrnzla92f8d5-orchestrate-0.26.0/bin/orchestrate-nexus

$ orchestrate 'Observe.Locks'
Observed.Locks.[{629 FinalWitness ...} {440 WisprAuthWitness ...} {441 WisprEdgeProxy ...}]
exit 0
```

The deployed nexus is version 0.26.0, active and answering through the
installed wrapper. Its reply format uses tight delimiters (the old format
before ProtoformStack's spaced canonical print). This flow did not
touch it.

**Result: PASS**

## Against the vision

Vision/datom.md Syntax rules checked on all witness output:

| Rule | Status | Detail |
|---|---|---|
| Spaces inside every bracket and brace delimiter | PASS | All replies: `{ 2 ByteCheck ... }`, `[ { ... } ]` |
| Empty enclosures tight | PASS | `Observed.Locks.[]` |
| Bare strings only without space or delimiter | PASS | `FinalWitness`, `6329f1`, `Braced` all bare |
| Curly quotes for strings with spaces | PASS | U+201C/U+201D byte-verified |
| Heads capitalized | PASS | `Observed`, `Locks`, `Locked`, `Released`, `Unreadable`, `Structural`, `Unclosed`, `Configured` |
| Integers bare | PASS | `1`, `2`, `5`, `13` all bare decimal |
| Comments with one semicolon | PASS | Ethos output uses `; ` prefix |
| A variant carrying nothing: symbol alone | PASS | `Braced` |
| Dot is the separator, written right after the head | PASS | `Observed.Locks.[]`, `Released.{ ... }`, `Unclosed.Braced` |
| Headed structure: head, dot, body's delimiter | PASS | `Locked.{ ... }`, `Structural.{ ... }`, `Unclosed.Braced` |

No departures from Vision/datom.md or the spec in the flow log.

The re-witness's residual defect (`Unclosed(Braced)` as Debug format) is
resolved: datomic a27f9b8e implements Corporal/Datomic for protos::Fault,
Problem, Enclosure, Boundary, and Separator, so the structural fault now
textualizes as `Unclosed.Braced` (dot-separated variant).

## Summary

| Item | Result |
|---|---|
| 1. Pins: revs on branch, Cargo.lock clean, datomic a27f9b8e pinned, CriomOS-home pins e631bad9 | PASS |
| 2. Builds and tests: nix build + cargo test orchestrate, signal-orchestrate, meta-signal-orchestrate | PASS |
| 3. MVP by hand: all replies clean datom, structural fault fixed, no Debug format, no ASCII quotes | PASS |
| 4. Deployed nexus: 0.26.0, active, answering | PASS |

**Overall: PASS.** All four items pass with no findings or departures.

## Sources

- Fresh `git worktree add --detach` at target revs for all seven repos
- `git merge-base --is-ancestor` for branch containment
- `Cargo.lock` and `Cargo.toml` in each witness worktree
- `cargo tree -d` in `nix develop` for orchestrate
- `nix build --builders 'ssh://prometheus'` of orchestrate (fell back to local)
- `cargo test` in `nix develop` for orchestrate, signal-orchestrate, meta-signal-orchestrate
- Orchestrate nexus started from build result with isolated XDG paths
- `orchestrate` and `meta-orchestrate` CLI invocations against the witness nexus
- `od -c` byte-level capture of structural fault stderr and curly-quoted output
- `systemctl --user status orchestrate-nexus` and installed `orchestrate` for deployed nexus
- Vision/datom.md Syntax rules
- Orchestrate Lock 629 on all seven witness worktree paths, released after checks
