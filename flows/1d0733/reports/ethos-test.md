# ethos-test

Repository: https://github.com/LiGoldragon/ethos-test (public).
Pushed revision: e21e686b821e12daae08094a60df5e679c8e0b0c (main).
ethos-zero pinned by flake.lock at 07714b0171802787bea1eefe4caa2d826d9c4030
(main check). The held set's candidate tree pinned by flake.lock as input
`ethos-zero-candidate` at a3f6068ecef547fd2a1e884677d8164d3456792c
(candidate check).
Written to psyche-skills vision/ethos.md at 850fd27, the ruled items of
flows/d5df1d/reports/ethos-solution.md, and d5df1d's rulings on the
statement map (relayed by the coordinator).

Witness: `nix flake check -L --keep-going --refresh github:LiGoldragon/ethos-test/e21e686`
ran on Prometheus (`hostname` returned `prometheus`), exit 0,
"all checks passed!". The local tree passed evaluation
(`--no-build --option allow-import-from-derivation false`), then a full
`nix flake check` on Prometheus from a copy of it. The outputs of the
`report` and `candidate` checks are the source of the counts below.

## How the set's tree is pinned

All on the ethos-zero GitHub repository, under non-main branches; main
untouched:

- `candidate/held-set-datom-codec` 3e86f81: datom-codec 4dff16b plus
  item12-on-item5-datom-codec.patch. Its tree equals Prometheus
  `/tmp/datom-codec-item12b` 296b256 (tree 81cf9f9).
- `candidate/held-set-protos` aa97df7: protos 15b41da plus
  item12-on-item5-protos.patch.
- `candidate/held-set-bare` a3f6068: ethos-zero 07714b0, then
  a6f3826 (item12-on-item5-ethos-zero.patch), c4a7a78
  (item6-on-set-ethos-zero.patch; tree equals Prometheus `/tmp/ez-i6`
  77fc650, tree 746430a), then a3f6068, which only moves the pins: Cargo.toml
  and Cargo.lock datom-codec from `file:///tmp/datom-codec-item12b` 296b256
  to `https://github.com/LiGoldragon/ethos-zero` at 3e86f81 (cargo finds the
  package in that commit's tree), and the flake inputs `protos` and
  `datom-codec` to `github:LiGoldragon/ethos-zero/aa97df7` and `/3e86f81`.
  `nix flake check --keep-going github:LiGoldragon/ethos-zero/a3f6068` on
  Prometheus: exit 0, "all checks passed!".

ethos-test takes it as input `ethos-zero-candidate`
(`github:LiGoldragon/ethos-zero/candidate/held-set-bare`, locked at a3f6068),
and `harness-candidate/` holds the harness crate with datom-codec at 3e86f81
(protos stays 15b41da: the set's protos patch touches only protos.ethos).
Each scenario's derivation carries a `candidate` derivation, the same drive
against that pair under its `candidateTarget`; `checks.candidate` gathers them.

## Counts

Main check (07714b0):

- Pass: 26 scenarios (25 checks and the Flow fixture).
- Expected-failing: 5.
- Differs: 10 rows of STATEMENTS.md.
- No observable: 21 (20 vision rows and ethos-solution item 8).
- Unruled, no target: 19 (the Represented ethos form added).

Candidate check (a3f6068):

- Pass: 31 (the 26, and the 5 ruled targets promoted: items 1, 2 and 6).
- Expected-failing: 0.
- Differs, no observable, unruled: as the main check (10, 21, 19); these
  rows carry no target in either check.

Also lint (the style gate) and report. When the set lands, the two checks
become one (STATEMENTS.md, "Two pinned checks").

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

Expected-failing (target `ruled`; `pass` in the candidate check):

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
