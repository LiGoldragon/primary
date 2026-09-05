# Ethos Zero rewrite handoff

## Current result

This subflow acquired Orchestrate lock `814` for the complete Ethos Zero write
set and migrated Cargo and the flake inputs to Protos `2d999f173334` (0.26.0)
and datom-codec `41a3c073d5c5` (0.21.0). It did not touch either substrate.

The first migration compile was a deliberate red witness. With an 8 GiB
address-space cap, one Cargo job, and a 900-second timeout, it found 102
errors: generated contracts still implemented removed `Datomic::conceive`,
while the reader still used the former `Head`/body-zero anatomy. That is the
expected F3/F4 and F9 dependency boundary, not a substrate regression.

The library is now green under the same cap (`cargo check --lib --locked`,
0.22 seconds). The concrete changes are:

- canonical conception and ascent now use Protos 0.26 `Symbol`, `Bare`,
  `Qualified`, and headed-body child `1` anatomy;
- `Delineation` publicly implements the shared
  `protos::Conceivable<File>` interaction and returns the original situation;
- `actualization` has the new explicit unit budget shape at the Ethos
  structural layer;
- the generated-fault bootstrap was rewritten to use the new `Datomic`
  incorporation-only contract plus universal `Conceivable<Datom>`;
- the generator now starts emitting the same universal layer instead of the
  removed `Datomic::conceive` method.

## Incomplete obligations

The bootstrap is now complete and landed as Ethos Zero main
`e82dc78b9838`. `src/fault.rs`, `src/contract.rs`, and every fixture product
were regenerated through the rebuilt CLI. The CLI passes a caller-owned
4,096-unit `IncorporationBudget` for untrusted request data.

The following audit items have not received their required durable witnesses:

| Finding | State |
| --- | --- |
| F1 | Self declarations, raw identifiers, more than 26 generated parameters, and empty constraints now receive typed conception/checking faults. |
| F2 | Generated code now implements `Datomic` incorporation plus universal `Conceivable<Datom>`; all committed products compile and round-trip. Additional adversarial Rust-output probes remain advisable. |
| F3 | Shared reader and generated universal layers compile and are freshness-tested. |
| F4 | Protos 0.26 structural types are used; an exhaustive headed path/extent regression remains needed. |
| F5 | Duplicate capabilities, associated members, and explicit/imported Protos intrinsic arity are checked. Generic cycles and repeated constraints remain. |
| F6 | A 10,000-level Tree input with a 256-unit caller budget returns `BudgetExhausted` in a 60-second/8 GiB probe. |
| F7 | Alias graph limits and predictable refusal remain unimplemented. |
| F8 | Still open: ethos identity includes constraints but Rust traits share a name/module namespace; no name-mangling or rejection policy was asserted. |
| F9 | Constant casing, grouped qualified imports, unnamed internal tuples and Nexus scope remain open. |

The living’s recovered statements settle versionless ethos roots and the
mandatory trait surface. They do not settle F8, the omitted Types association
section, or current Nexus scope; no dependent design choice was made here.

## Sources

- Main-flow brief and recovered audit summary.
- `flows/1a6ca4/reports/auditEthosZeroAstra.md` (complete audit read before implementation).
- `flows/da223f/reports/rewrite.md` (complete substrate rewrite report read before implementation).
- `Vision/ethos.md`, `Vision/protos.md`, `Vision/datom.md`,
  `Vision/ethosMonolith.md`, and `Intent/mandatoryTraits.md`.
- Capped migration witnesses in this subflow: Cargo update, red
  `cargo test --locked --no-run`, and green `cargo check --lib --locked`.
