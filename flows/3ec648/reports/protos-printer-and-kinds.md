# protos owns the vertical print; capability inputs name their kinds

Repositories, each started from remote main: protos (2f9c63c), datom-codec
(58474fd), ethos-zero (2db764d, 14.1.0). Orchestrate lock 11492 held on the
three repositories.

## Commits (on main, pushed)

- protos 1cf4e63: Own the canonical vertical print; name the Spendable kind. **0.32.0**.
- protos 109797e: Keep angles tight after a headed element. **0.32.1**.
- datom-codec 60b08d8: Name the kinds in capability inputs; take the vertical print from protos. **0.32.0**.
- datom-codec 06e5c93: Repin protos 0.32.1. **0.32.1**.
- datom-codec 0930abc: Give the kinds one home; check the anatomy with the pinned ethos-zero.
- ethos-zero 06d73e0: Print through protos; repin protos 0.32.1 and datom-codec. **14.2.0**.
- protos e4e3019, datom-codec 522897c: Pin ethos-zero 14.2.0 (06d73e0) for the kinds and anatomy checks.

## 1. The print lives in protos

- `protos::Textualizable::textualize` writes the vertical canonical print.
  It runs on protos' iterative rendering machine, which gains `Mark`, `Hang`
  and `Unmark` steps and a column count. The layout facts (column, element
  grouping, next layer) are in the new `src/layout.rs`.
  `canonicalize` assigns the extents of that print.
- The one-line print is still available as the compact alternative
  `Compactable::compact`. I kept it, not removed it, for consumers that read
  one line at a time. The ethos-zero CLI replies use it, so they are
  unchanged.
- I changed two rules from ethos-zero's printer:
  - An empty `[]` or `{}` is a leaf, because it has no next layer.
  - An angled enclosure stays tight after an element only when the
    element's last leaf does not end on `.`, `!` or `:`. When it does, a
    tight `a.<b>` would read back as a head with constraints.
- ethos-zero's `printing.rs` now handles only the sweet form: the root head,
  then each section printed by protos. Its own layout copy is removed.
  `Printable` is unchanged as an API.
- The four Flow Nexus fixtures still round-trip byte-identical (print.rs 9/9).
  `ethos-zero.ethos` is still canonical.
- datom-codec had a second layout writer: its projection measured
  one-line extents itself. It now builds the tree unplaced and protos
  canonicalizes it, so a projected datom carries the extents of the text it
  prints.

## 2. The kinds, for the living's review

| concrete input | kind | owner | why this name |
|---|---|---|---|
| `ReaderBudget` | `Spendable` (`spend![ Boolean ]`) | protos | the reader's only demand is to spend one node at a time and learn whether it could |
| `Path` | `Branchable` | datom-codec | a datom's place, whose capability is branching to a child's place |
| `Budget` | `Budgeted` | datom-codec | what composing is charged against, at a path; distinct from Spendable, whose spend differs |
| `Positions` | `Positional` | datom-codec | the source of a struct form's positions, read in turn; distinct from `Compositional` (the type built from them) |
| `Datom` (in `Composing.compose:`) | `Composable` | datom-codec (existing) | a datom is what composes; the kind already existed |

- Each kind is the hand-written Rust trait renamed, so each meaning has one
  home:
  - `ReaderBudgeting` → `Spendable` (now exported);
  - `Pathing` → `Branchable`;
  - `Budgeting` → `Budgeted`;
  - `Positioning` → `Positional`.

  The derive emits the new names.
- The associations state the bearing: `[ ReaderBudget.[ Spendable ] ]` and
  `[ Path.[ Branchable ] Budget.[ Budgeted ] Positions.[ Positional ] Datom.[ Composable ] ]`.
- `Branchable`, `Budgeted` and `Positional` have empty capability lists in
  ethos. ethos-zero 14 refuses what they would need, so their capabilities
  stay Rust surface:
  - an `Integer` index input: `KindWanted.Integer`;
  - a unit yield;
  - a kind inside `Result<…>` in a yield: `Role.Composing`.
- The hand-written signatures still take the concrete types. I tried a
  generic `protosize_with<B: Spendable>`, but the reader refunds budget when
  it backtracks the angled lookahead, so the kind would also need a
  snapshot/restore capability.
- The anatomy file `datom-codec/datom-codec.ethos` redeclared the kinds, with
  `Path` in an input, and **ethos-zero 14.x already refused it**
  (`KindWanted.Path`). That means ethos-zero's own `dependency-ethos` check
  was red, and the 14.0.0 scan in UPGRADES missed it. Its kinds section is
  now empty, and UPGRADES is corrected. `protos.ethos` still repeats
  `Textualizable` and `Canonicalizable` from the kinds file; it is accepted,
  and I left it alone.
- The generated Rust is committed as `generated/protos-kinds.rs` and
  `generated/datom-codec-kinds.rs`. It is compiled by `tests/kinds.rs`
  against the crate's types, where the generated associations are
  compile-time assertions. New Nix checks:
  - `generated-kinds` regenerates the file with the pinned ethos-zero and
    `cmp`s it against the committed one;
  - `checked-anatomy` runs `Check` on the anatomy file.

## Test evidence

- Seen failing:
  - protos `tests/vertical.rs`: 5 of 7 failed against the one-line printer.
    A later case failed against the first layout (`Generated.Vector`, then
    `<String>` on its own line).
  - protos `tests/kinds.rs` against the 14.1.0 output of the old ethos:
    `E0404 expected trait, found struct crate::ReaderBudget`.
  - datom-codec `tests/kinds.rs`: `E0404` for `crate::Path` (2), `crate::Budget`
    (4), `crate::Datom`, `crate::Positions`.
  - datom-codec `nested_projection_carries_the_extents_of_its_vertical_print`:
    one-line extents (end 41) where the print ends at 59.
  - ethos-zero, after repinning:
    - 7 CLI tests failed on vertical replies, until they were sent through
      `compact` and the angled fix landed;
    - `generated_sema_records_round_trip_as_datom_text` failed, and its
      expectation is now the vertical `{ root\n  [ { first 1 } ] }`.
  - `checked-anatomy.sh` run on the old `datom-codec.ethos` exits 1 with the
    `KindWanted.Path` refusal.
- Then passing:
  - protos: deep 4, delineation 15, kinds 1, protos 18, textualization 13,
    vertical 8.
  - datom-codec: composition 13, core 33, hygiene 1, kinds builds.
  - ethos-zero: lib 18, cli 14, ethos 24, freshness 3, generated 18,
    print 9, signal-without-datom 2.
  - `cargo fmt --check`, `clippy --all-targets -D warnings` and
    `doc -D warnings` are clean in all three.
  - Both generated kinds files are byte-identical to the output of the
    ethos-zero 14.2.0 build.

## Gates

`nix flake check -L` was run once per repository, in parallel, with a
45-minute timeout, on the trees that became the final commits. Builds ran on
prometheus.

- ethos-zero 06d73e0: **exit 0**. All checks green, including
  `dependency-ethos`, which generated protos.rs, protos-kinds.rs,
  datom-codec.rs and datom-codec-kinds.rs. This answers the coordinator's
  witness `witnesses/ethos-zero-14-nix-check.md`: the 14.1.0 failure on
  `KindWanted.Path` is gone.
- protos e4e3019: **exit 0**. All checks green, including `generated-kinds`
  and `checked-anatomy`.
- datom-codec 522897c: **timed out (exit 124)**. It was still building its
  pinned `rust-nightly-complete-2026-06-19` toolchain. These checks had
  finished green: `generated-kinds`, `checked-anatomy`, and the four source
  guards. build, test, fmt, clippy and doc did not run under Nix. I did not
  repeat the run, as the brief allowed one. Locally, cargo test, fmt, clippy
  and doc were green.

## Open questions

- Should `compact` stay, or go as the vision suggests? Should ethos-zero's
  CLI replies go vertical? Today they stay on one line.
- A deeply nested enclosure tree prints with indentation that grows
  quadratically with depth. The datom composition depth bound (4096) caps it.
- Downstream consumers pinning protos/datom-codec get the vertical
  `textualize` and the renamed kinds on repin (see each UPGRADES.md). The
  vendored copies in `primary-next/tools/messaging-codec/vendor/` were not
  touched.

## Sources

- /home/li/primary/flows/3ec648/reports/ethos-zero-kinds-and-print.md
- vision-ethos, knowledge-ethos, protos, datom, versioning, breaking-upgrades, testing skills
- The commits above; UPGRADES.md in protos, datom-codec, ethos-zero
- Failing outputs: scratchpad protos-kinds-failing.txt, datom-kinds-failing.txt
