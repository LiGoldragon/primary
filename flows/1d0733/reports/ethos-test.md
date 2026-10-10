# ethos-test

Repository: https://github.com/LiGoldragon/ethos-test (public).
Pushed revision: 3a15f9fa611ab9bb3169a671dca3dc0f7a02c909 (main).
ethos-zero pinned by flake.lock at 07714b0171802787bea1eefe4caa2d826d9c4030.
Written to psyche-skills vision/ethos.md at 850fd27, the ruled items of
flows/d5df1d/reports/ethos-solution.md, and d5df1d's rulings on the
statement map (relayed by the coordinator).

Witness: `nix flake check -L --refresh github:LiGoldragon/ethos-test/3a15f9f`
ran on Prometheus (`hostname` returned `prometheus`), exit 0,
"all checks passed!". The local tree passed the same evaluation
(`--no-build --option allow-import-from-derivation false`) and build first.
The report check's output for that revision is the source of the lists below.

## Counts

- Passing checks: 25, plus the Flow fixture (26 scenarios with target `pass`).
- Expected-failing targets: 5.
- Differs: 10 rows of STATEMENTS.md.
- No observable (not executable): 21 (20 vision rows and ethos-solution item 8).
- Unruled, no target: 18 proposals and forks.
- Also lint (the style gate) and report.

## Targets

Passing:

| check | statement |
|---|---|
| ethos-zero-roots | Roots |
| ethos-zero-file | Declaration: File |
| ethos-zero-imports | Imports |
| ethos-zero-self-description | Self-description |
| ethos-zero-spacing | Spacing |
| ethos-zero-generation | Generation |
| ethos-zero-cargo-trait | Trait |
| ethos-zero-trait-concrete-input | Trait (the generator's reading) |
| ethos-zero-cargo-identity | Identity |
| ethos-zero-cargo-declaration | What a declaration turns into |
| ethos-zero-cargo-inline | Inline types |
| ethos-zero-cargo-inline-collision | Inline types |
| ethos-zero-cargo-variant-defined | A variant named as a defined type carries that type |
| ethos-zero-cargo-variant-inline | A variant may declare its payload inline |
| ethos-zero-cargo-inline-recursive | A variant may declare its payload inline |
| ethos-zero-cargo-derives | Every declared type bears both traits (asserts the code's name, Composing) |
| ethos-zero-cargo-datom-feature | The datom traits are compiled in only where text is spoken (asserts Composing) |
| ethos-zero-cargo-signal | Shapes and placement |
| ethos-zero-cargo-trait-explicit | Traits are explicit; bodies are hand-written |
| ethos-zero-cargo-trait-simple | Trait syntax |
| ethos-zero-cargo-trait-complex | Trait syntax |
| ethos-zero-cargo-associations | Associations |
| ethos-zero-cargo-signal-associations | Associations (implied in Signal) |
| ethos-zero-no-tuple | Associations ("No tuple in the code we design") |
| ethos-zero-inline-import | Choice 3 ruled, d5df1d vision/ethos.md 2026-10-09 (ethos-solution item 3) |
| ethos-zero-flow-example | Flow, a current best example (fixture: generates only) |

Expected-failing (target `ruled`):

| check | statement | miss today |
|---|---|---|
| ethos-zero-cargo-newtype | Newtypes, not type aliases (d4ae97, 2026-10-06; item 1) | the generated Rust holds `pub type FlowId` |
| ethos-zero-cargo-newtype-distinct | the same | rustc accepts a LockName for a FlowId; E0308 expected |
| ethos-zero-cargo-flow-id | the same (item 6) | the generated Rust holds `pub type FlowId` |
| ethos-zero-single-position | A one-position type is called a new type (d4ae97, 2026-10-06; item 2) | `Age.{ Integer }` generates |
| ethos-zero-single-position-inline | the same | `Started.{ String }` generates |

STATEMENTS.md in the repository maps every statement by its vision line
numbers, including the differs, no-observable and unruled rows.

Imports, lines 175-176 against 188, is recorded as "differs: tension within
the vision": `protos:String` emits `protos::String`, which rustc refuses
(E0425, measured); protos exports no `String`. The fork for the living is to
replace 188's example with `protos:Textualizable` shown as
`protos::Textualizable`.

Provenance receipt: unavailable.
