# Ethos-audit fixes 5, 6 and 7

Subflow of 38de5b (Opus), 2026-09-25. Repository: ethos-zero, main. The work started from 4bf73ca. It was done in the scratch clone `ethos-zero-f567-opus` under Orchestrate lock 6414, which is now released. Each fix was pushed to `github.com:LiGoldragon/ethos-zero` main, and `git ls-remote` confirmed each push.

| fix | commit | version | cargo test | clippy / fmt / guards |
|---|---|---|---|---|
| 5 unique inline names | b35822d | 10.0.0 -> 10.0.1 | green (before and after) | clean |
| 6 fixtures + generator holes | 89a1ee8 | 11.0.0 -> 12.0.0 | green | clean |
| 7 located errors + Check | 407f938 | 12.0.0 -> 13.0.0 | green (8 suites) | clean |

The fix-3 subflow pushed e599317 and cc3e84f (10.0.1 -> 11.0.0) to main between fix 5 and fix 6. My fix 6 was rebased onto those commits. Fix 3 had already added the per-item `#[rustfmt::skip]`, so fix 6 dropped its own duplicate of that change and kept only a test that holds it.

Versioning: fix 5 is a patch because only output that was already invalid changes. Fix 6 is a major bump because inputs that were accepted before are now refused. Fix 7 is a major bump because the CLI reply changes shape and every error path changes. Final version: **13.0.0**.

## Fix 5: unique derived `_Data` names

- A short derived name `X_Data` that more than one enum would declare is now qualified with the owning enum's name, giving `P_X_Data` and `Q_X_Data`. `Query` and `Response` are included in this rule. A payload nested under a derived enum takes that enum's name as a prefix, as it did before.
- An authored name that equals a derived name is refused as `Duplicate` at the authored declaration.
- The row-15 probe (`P.[ X.{ String } ] Q.[ X.{ Integer } ] X_Data.String`) is now `fixtures/inline-collision.ethos`. It is compiled and exercised in `tests/generated.rs`.
- Negative tests are in `tests/ethos.rs`.
- The README paragraph about `EthosNested` was stale and has been rewritten.

## Fix 6: every fixture compiled, and the generator holes closed

- All 18 fixtures are compiled in `tests/generated.rs`. The kind fixtures get the `super` items they import, and each fixture is exercised by a test.
- `Option` and `Result` in outer positions are now emitted fully qualified.
- New refusals, each with a negative test:
  - A type, kind or associated type named after an intrinsic is refused as `Intrinsic.<name>`.
  - A type or kind name that does not start with a capital is refused as `Case.<name>`.
  - A type with no finite value is refused as `Cycle`. Examples: `S.{ Self }`, `A.{ B } B.{ A }`, `E.[ Only.E ]`. An empty enum is still accepted.
- A test checks that every committed generated module carries the header and `#[rustfmt::skip]` on every item.
- **Finding:** once composition-types was compiled, it showed that datom-codec's derive writes `Box::new` without qualification (`crates/datom-codec-derive/src/lib.rs:151`). Any type named `Box` in a module therefore breaks every enum's datomization in that module. That fixture no longer declares `Box` or `Result`.
- **Consequence:** datom-codec.ethos at the pinned 09e2a9d declares `Meaning.String` (line 11). That declaration is now refused (`Intrinsic.Meaning` at 11:3), so the flake's `dependency-ethos` check will fail until the declaration is removed. The declaration lives in datom-codec, which this subflow did not touch.

## Fix 7: errors located by line and column, and a `Check` query

- Every error path is now the Protos path from the file's root, so conception and checking agree. Before this fix:
  - conception dropped the body step and some head/body steps;
  - checking numbered elements by concept index, even though `Vector<Integer>` is two Protos siblings;
  - checking placed a sourced reference's arguments in its body;
  - checking gave capability inputs an extra step.
- A reference's arguments now sit at the angled enclosure beside it (the `BESIDE` step, which the enclosing list resolves).
- `Locating` (`src/location.rs`) walks the path through the source structure, carries the result back across the sweet-form seam, and reports line and column counted from 1. A library test checks 17 error shapes and confirms each one lands on the offending token.
- `ethos-zero 'Check./abs/file.ethos'` validates the file and writes nothing. It replies `Checked.<file>`. This uses one inline datom and no flags.
- Both queries now reject with `Rejected.{ file { line column } error }`. This replaces `GenerationRejected`, whose datom Path was always empty. A rejected Generate no longer creates the output directory.
- `ethos-zero.ethos` and `error.ethos` (`Location`) are updated.
- CLI tests assert line and column for undeclared (including a case below a comment and nested in arguments), duplicate, arity and structural errors.

## Gates

- `nix flake check --no-build` **passed** with substituters disabled. The configured cache nix.prometheus.goldragon.criome timed out during evaluation.
- The full `nix flake check` was tried once and is **blocked**: "local builds are disabled (max-jobs = 0)".
- In its place I ran the local equivalents: cargo test, clippy `--all-targets`, `cargo fmt --check`, `cargo doc`, and both guard scripts, all green. I also ran the dependency-ethos files through the built binary: protos.ethos, protos-kinds.ethos and datom-codec-kinds.ethos are Generated; datom-codec.ethos is Rejected, as described above.

## Consumers: regenerated at 407f938, without repinning

Each consumer was a fresh clone. Its ethos was generated with the new binary and diffed against its committed `src/generated/signal.rs`. Its build.rs freshness assert was also run once against a local path override that was never committed.

- **signal-flow 5ca97ce: not byte-identical.** 15 diff lines, and build.rs panics at its assert (build.rs:14). There are two causes:
  - six `Option<…>` fields are now `std::option::Option<…>` (fix 6);
  - one item gains `#[rustfmt::skip]` (fix 3's per-item skip).
- **meta-signal-flow 4748cfa: byte-identical.** build.rs passes.

## Estate sweep

I ran all 120 `.ethos` files under /git through the 4bf73ca Generate and the 407f938 Check:

- 74 were Generated and are now Checked.
- 43 were rejected before and are still rejected.
- 3 were Generated before and are now Rejected:
  - datom-codec.ethos (`Intrinsic.Meaning`);
  - its vendored copy in primary-next/tools/messaging-codec (the same error);
  - the stale /git ethos-zero checkout's composition-types fixture (`Intrinsic.Result`, already changed on main).

## Sources

- ethos-zero commits b35822d, 89a1ee8 and 407f938 (github main); fix-3 commits e599317 and cc3e84f.
- flows/e51411/reports/ethos-audit.md: fixes 5, 6 and 7, and rows 12, 14 and 15.
- signal-flow 5ca97ce and meta-signal-flow 4748cfa: build.rs, ethos/signal.ethos, src/generated/signal.rs.
- datom-codec 09e2a9d: datom-codec.ethos, crates/datom-codec-derive/src/lib.rs.
- Estate sweep report: scratchpad `estate-f567/report.txt`, which is not committed.
