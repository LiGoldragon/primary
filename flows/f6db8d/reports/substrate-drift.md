# Substrate drift — D1, D2, D5, D6 closed

Subflow of main flow f6db8d, acting on `flows/f6db8d/reports/substrate-review.md`.
Two repositories were edited, each under its own Orchestrate Lock, each gated and
pushed. D3 was left to the migration subflow that released ethos-zero 8.0.0
(`da58504`); D4 and the ARITY question were left for the living. ethos-zero was
read and built, never edited.

Everything below marked **witnessed** was run in this session and its output
seen here.

## Released

| repository | revision | version |
|---|---|---|
| protos | `171b21f65337983ab624b7b906397a4f1f92c5a3` | 0.30.1 |
| datom-codec | `5eefe8292433...` (`5eefe829243399d82eddf3c76204f770e9943f91`) | 0.26.2 |

Both are `main` at origin. **Witnessed** (`jj log -r main@origin`).

Locks 1161 `F6db8dProtosDrift` and 1162 `F6db8dDatomCodecDrift` were taken after
`Observe.Locks` showed no f6db8d lock on either path, and both were released on
completion. No lock was held on ethos-zero at either moment, and it was not
touched.

## D1 and D2 — the contracts now come from the pinned generator

Both repositories pinned ethos-zero `daf0072…` (6.1.2) for generation. Both now
pin `da58504926dabe4680bb7863d812846b0f845d86` (8.0.0), and every committed
contract is that generator's byte-exact output:

| repository | contract | was |
|---|---|---|
| protos | `generated-contract/protos.rs` | 6.1.2 output: no `#[rustfmt::skip]`, no `Clone, Debug, PartialEq` derives |
| protos | `generated-contract/protos-kinds.rs` | **the output of no declaration at all** — `Serial`, `Classifying`, `Conceivable`, `crate::Glyph`, names from an older design, against a declaration stating `BoundedProtosizable`, `Protosizable`, `Textualizable`, `Canonicalizable` |
| datom-codec | `generated-contract/datom-codec.rs`, `…-kinds.rs` | 6.1.2 output, same two differences |

Nothing broke: in neither repository is a committed contract compiled — each is
evidence beside its declaration, and `cargo build`, `cargo test`, `clippy` and
`doc` are unchanged by the regeneration. **Witnessed** by grep over `src/`,
`crates/`, `Cargo.toml` and `flake.nix` for `generated-contract`, which appears
only in `flake.nix`.

The gate: protos gained `checks.generated-kinds-contract`, the same three-line
`checks/generated-contract.sh` its sibling check already used, pointed at
`protos-kinds.ethos`. datom-codec already carried both checks; they now compare
against the repinned generator.

Seen failing once, each: a `// drift` line appended to
`protos/generated-contract/protos-kinds.rs` failed
`checks.x86_64-linux.generated-kinds-contract` with
`cmp: EOF … after byte 476, line 19`, and the same line appended to
`datom-codec/generated-contract/datom-codec.rs` failed its
`generated-contract` check with `cmp: EOF … after byte 1337, line 46`. Both
files were restored. **Witnessed.**

Note on the generator, not on this work: 8.0.0 emits `#[rustfmt::skip]` on most
items but not on four consecutive ones in `protos.rs` (`Enclosed_Data` through
`Protos`). The contract is committed exactly as emitted, so the check holds; the
inconsistency is ethos-zero's and is left where it lives.

## D5 — six stack traversals became one machine and one statement of structure

protos had six hand-written stack walks over `Protos`, each with its own step
enum: `Drop` (`src/dropping.rs`), `Clone`, `PartialEq`, `Debug`
(`src/traversing.rs`), printing and canonicalization (`src/core.rs`).

They are now two shapes, each stated once:

- `src/rendering.rs` — one `Step` type, one iterative driver, two renditions
  (`Printed`, `Shown`) and two sinks (`Written`, which writes into any
  `fmt::Write`; `Measured`, which counts bytes and records each node's extent).
  `Textualizable`, `Canonicalizable` and `Debug` are three callers of it.
  Canonicalization no longer restates the canonical layout rules: it renders
  `Printed` into `Measured` and settles the recorded extents back onto the tree
  in the order the rendering opened the nodes.
- `src/traversing.rs` — one `Structuring` kind saying what a node holds: its
  `aspect` (everything but the children, compared by a derived `PartialEq` on a
  small borrowing enum), its `children` and `children_mut`, its `skeleton`, and
  the inverse pair `adopt` and `shed`. `Clone`, `PartialEq` and `Drop` are three
  callers of it; `src/dropping.rs` is gone.

The depth guarantee is unchanged — every one of them is still an explicit stack,
and `tests/deep.rs` (100 000 deep, 50 000 wide, 10 000 constrained heads) is
green, as is `tests/scale.rs`'s bounded memory probe for `clone-deep` and
`canonicalize-deep`.

Two deliberate breakages confirmed the tests carry the two orderings the
refactor had to get right (both restored immediately):

- swapping the settle order of a head's constraints and body failed
  `canonicalization_assigns_utf8_extents_without_reading`;
- swapping the child order of a constrained head failed
  `a_deep_tree_of_constrained_heads_clones_into_the_same_tree`.

**Witnessed**, both.

One incidental fix: `char::encode_utf8` tripped protos's own
`no-forbidden-vocabulary` check (it contains "encode"). The sink took a
`take_glyph` capability instead, which is also allocation-free where the old
code was.

## D6 — the unreachable refusal is gone

datom-codec's `Positioning::position` raised `ErrorKind::Arity` when asked past
the end, but `DatomPositioning::positions(arity)` validates the exact count
before any position is read and `Positions` is constructible only through it. The
refusal, its `Error` construction and the `path` field that existed only to fill
it are removed; the capability now takes the position `positions` promised. The
`Arity` variant itself stays — `positions` still raises it, and
`tests/composition.rs` still holds it to `expected: 3` against every wrong count.

## Line counts

Rust lines of tracked source, before → after:

| | source | tests |
|---|---|---|
| protos `src/` | 1 083 → **1 042** (−41) | 1 286, unchanged |
| datom-codec `src/` + `crates/` | 1 767 → **1 758** (−9) | 1 256, unchanged |

Net **−50** source lines. The line delta understates the change: six step enums
and six drivers became one of each, and the canonical layout rules, which were
written out in three places, are written in one.

## Left standing

- datom-codec still pins protos at `e8701521` (0.30.0), not tonight's 0.30.1.
  Deliberate: protos 0.30.1 changes no public API, and repinning it here would
  force every consumer the migration subflow is currently repinning to move with
  it or hold two incompatible `protos` crates. The repin belongs with that
  subflow's sweep.
- protos 0.30.1 is therefore gated by its own suite only, not by a consumer's.
- D3, D4 and the ARITY Vision question are untouched, as briefed.

## Sources

- `/home/li/primary/flows/f6db8d/reports/substrate-review.md` — the defects
  acted on; its §4.1, §4.2 and §5 are the authority for what D1, D2, D5 and D6
  are. Read whole.
- `/git/github.com/LiGoldragon/protos` and `/git/github.com/LiGoldragon/datom-codec`
  — `src/`, `crates/`, `tests/`, `flake.nix`, `checks/`, the `.ethos`
  declarations and the committed contracts, read and edited; every claim above
  about them is this flow's own witness.
- `/git/github.com/LiGoldragon/ethos-zero` at `main` — read only, to confirm
  `da58504` is version 8.0.0 and is pushed to origin.
  `nix build github:LiGoldragon/ethos-zero/da58504…` →
  `/nix/store/3hy1j4sfdps580rrzrqvq1dhzi412w2z-ethos-zero-8.0.0`, run over all
  four declarations to produce the committed contracts.
- `orchestrate 'Observe.Locks'` before taking locks 1161 and 1162, and the
  `Released` replies for both.
- `nix flake check -L --builders ''` in each repository: `all checks passed!`
  in both, after the edits and before the commits.
