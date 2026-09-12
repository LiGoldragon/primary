# Substrate repin — protos 0.30.0 through datom-codec and ethos-zero

Subflow of main flow f6db8d. Two repositories touched, one after the other,
producers before consumers.

## Revisions

| repo | before | after | version |
|---|---|---|---|
| protos | 0.29.1 `b543678cfc8609529cea7174eb4af8a64daa54ad` | 0.30.0 `e8701521a37c698d6a2eb933618b9d5d1c6f6ffb` | unchanged (already released by the protos subflow) |
| datom-codec | 0.26.0 `99a9e8c9`…`196d0e290ad6149b847963dbd4c63e77c2cba040` | **0.26.1** `18129314966c5043ee659de452b6f976fa319b21`, pushed to `main` | patch |
| ethos-zero | 7.0.0 `c8a68369` | **7.0.1** `212b359045cc07fc74993a59a039678f4d56b8bd`, pushed to `main` | patch |

Locks: 1119 `DatomCodecProtosRepin` over `/git/github.com/LiGoldragon/datom-codec`
(acquired, released); 1125 `EthosZeroProtosDatomCodecRepin` over
`/git/github.com/LiGoldragon/ethos-zero` (acquired, released). `Observe.Locks`
before each acquisition showed neither path held.

## datom-codec

- `Cargo.toml`: `protos` rev repinned to `e8701521a37c698d6a2eb933618b9d5d1c6f6ffb`.
  `Cargo.lock` updated by `cargo update -p protos` (protos 0.29.1 → 0.30.0).
- No direct protos flake input exists in `datom-codec/flake.nix` — the only
  `protos` entries in its `flake.lock` are nested inputs of the `ethos-zero`
  flake input (used to build the generator that checks the committed
  `.ethos` contracts), unrelated to the Cargo dependency. Nothing there was
  touched; the brief's "flake input" step does not apply to this repository.
- `tests/composition.rs`, `built_strings_round_trip_at_a_root_and_inside_a_variant`:
  the proptest alphabet regex gained the backslash
  (`"[a-zA-Z0-9 .!:;/«»(){}\\[\\]<>_\\\\-]{0,24}"`), which
  `reports/datom-codec-fix.md` recorded excluded "until the protos writer
  escapes it." It now passes.
- Nothing else broke. `cargo test --offline` (9 + 32 tests), `cargo fmt --all
  --check`, `cargo clippy --offline --all-targets -- -D warnings`,
  `RUSTDOCFLAGS="-D warnings" cargo doc --offline --no-deps`, and
  `nix flake check -L --builders ''` (build, test, fmt, clippy, doc,
  no-production-free-functions, no-production-inherent-methods,
  no-zst-behavior, no-forbidden-vocabulary, generated-contract,
  generated-kinds-contract) all passed, witnessed twice: once before the
  version bump and once after.
- Version: **0.26.1**, patch. `datom-codec`'s own `Datomizable for String`
  writer and reader rules are unchanged; the fix is entirely inside the
  protos dependency it repins. A `String` value that gets delimited into
  guillemets (any that carries whitespace, an enclosure glyph, or a leading,
  trailing, or doubled separator — see `src/composition.rs`) and also
  carries a backslash now round-trips where it previously would not have;
  a bare-written string was never affected because it never enters
  guillemets.

## ethos-zero

- `Cargo.toml`: `protos` repinned to `e8701521a37c698d6a2eb933618b9d5d1c6f6ffb`,
  `datom-codec` repinned to `18129314966c5043ee659de452b6f976fa319b21`.
  `Cargo.lock` updated by `cargo update -p protos -p datom-codec`.
- `flake.nix`: the `protos` and `datom-codec` flake inputs (used to read
  their own `.ethos` declarations in the `dependency-ethos` check) repinned
  to the same two revisions. `flake.lock` updated by
  `nix flake lock --update-input protos --update-input datom-codec`.
- Generated fixtures: `tests/freshness.rs`'s three tests (`the_error_module_is_fresh`,
  `the_contract_module_is_fresh`, `every_fixture_module_is_fresh`) passed
  unchanged under the new pins, so nothing needed regenerating — the new
  protos and datom-codec revisions do not change what the generator emits
  from ethos-zero's own fixtures.
- `cargo test --offline` (17 lib + 7 cli + 11 ethos + 3 freshness + 9
  generated + 2 signal-without-datom = 49 tests, all green — the
  `signal-without-datom` pair build their own throwaway crates and needed
  network to resolve crates.io dependencies, not affected by this repin),
  `cargo fmt --all --check`, `cargo clippy --offline --all-targets -- -D
  warnings`, `RUSTDOCFLAGS="-D warnings" cargo doc --offline --no-deps`, and
  `nix flake check -L --builders ''` (build, test, fmt, clippy, doc,
  dependency-ethos, no-free-functions, no-inherent-methods) all passed.
- Version: **7.0.1**, patch. No public field, generated shape, or wire text
  of ethos-zero's own output changed; the fix is entirely inside the two
  repinned dependencies.

## The "rejected right shape" question

The brief asked whether protos 0.30.0 makes readable the shape that
`reports/ethos-zero-fix.md` §3 said protos would need three things for: a
sourced generic's constraints attached to a bare name with no body (e.g.
the unsplit form of `Vector<Integer>`).

**It does not.** Read, `diff b543678..e8701521 -- src/core.rs` (the only
`src/core.rs` change in the release): the entire diff is the new `Escaping`
trait and its use in the reader's opaque-boundary branch and the writer,
plus the guillemet/parentheses print routine — nothing in `Protos::Headed`'s
shape or in the reader's rewind for an angled enclosure with no following
separator. Specifically, against `reports/ethos-zero-fix.md` §3's three
requirements:

1. **A node for a name bearing constraints and no body.** `Protos::Headed`
   in `e8701521`'s `src/core.rs` still carries `separator: Separator` and
   `body: Box<Protos>` unconditionally (`constraints: Option<Box<Protos>>`
   was already present at `b543678` and is untouched by this release —
   it does not by itself provide a body-less node). Still unmet.
2. **A reader that keeps the constraints on that node instead of rewinding
   past them.** The rewind this refers to is outside the diff entirely; not
   touched.
3. **A writer that prints the constraints against the name with no space.**
   Also outside the diff; not touched.

So the ethos-zero adjacency-scanner unification stands as `ethos-zero-fix.md`
left it: `Vector<Integer>` still reads as two sibling structures, and the
comment on `Constraining` in `ethos-zero/src/conception.rs` recording why is
still accurate. Left as is, per the brief.

## Sources

- `orchestrate 'Observe.Locks'` — read before each lock acquisition; neither
  `datom-codec` nor `ethos-zero` was held.
- `/home/li/primary/flows/f6db8d/reports/protos-fix.md` — the protos release
  this repin follows; the two reading-behaviour changes and the escape rule.
- `/home/li/primary/flows/f6db8d/reports/datom-codec-fix.md` — the pending
  backslash-alphabet note this flow closed.
- `/home/li/primary/flows/f6db8d/reports/ethos-zero-fix.md` §3 — the three
  protos requirements this flow re-checked.
- `/git/github.com/LiGoldragon/protos` at `b543678` and `e8701521`,
  `git diff b543678..e8701521 -- src/core.rs` — read and witnessed, for the
  "rejected right shape" answer.
- `/git/github.com/LiGoldragon/datom-codec` and
  `/git/github.com/LiGoldragon/ethos-zero`, both at the revisions above, and
  the gate output for each (`cargo test`, `cargo fmt`, `cargo clippy`,
  `cargo doc`, `nix flake check -L --builders ''`) — this flow's own
  witnesses, run before and after each version bump.
