# Invariants Proposal 4, land: dry run

Build host: `hostname` returned `prometheus` for every cargo and nix run. The work is in the scratch copy `/tmp/ethos-zero-inv4` on Prometheus, which has no remote. Nothing was pushed, and nothing in Primary was committed.

Base: the scratch HEAD has tree 26223cd, the same tree as ethos-zero b2fa8b0 (compared with a fresh clone). `item12-final-ethos-zero.patch` is applied on top. The flake reaches protos through `--override-input protos path:/tmp/protos-item12b`, which is 15b41da plus `item12-final-protos.patch`. The datom-codec Cargo pin is the set's scratch `/tmp/datom-codec-item12b` (296b25, which is 4dff16b plus `item12-final-datom-codec.patch`). `fork-invariants-4.patch` is the diff from the set to this build.

## The layout built

The rule, from d5df1d through the coordinator: a form breaks onto lines when it holds variants (a period-headed bracket, an enum, one variant per line), more than two positions, or a form that itself breaks. A bracket of plain leaves stays on one line.

The build implements it as follows:

- A brace or bracket enclosure breaks on its own when either holds:
  - it is the bracketed body of a period head;
  - it has more than two elements and is a brace, or it has more than two elements and holds at least one element that is not a leaf. A leaf is any element that is not a headed node and not a non-empty brace or bracket.
- An enclosure also breaks when any form it holds breaks on its own, at any depth. This follows enclosure children and headed bodies, but not angles.
- In a broken form, the opener ends its line. Each element starts on its own line, indented two columns beyond the line that opened the form. The closer ends the last element's line, which is the placement in the spec's Voice block.
- The root head and the sections stay at column 0. Angle arguments stay tight.

The layout is built in ethos-zero src/printing.rs. Datom keeps the protos print.

**These three break behaviours are the design's own, pending the living's ruling on Proposal 4 of the invariants book, since the width rule is his:**

1. **A form holding variants breaks, one variant per line.** Example: `Rank.[` followed by `Primary`, `Secondary` and `Tertiary`, each on its own line.
2. **A form of more than two positions breaks.**
   - `Rejected.{ String Location Generation_Error }` breaks.
   - `Start.{ Voice Capsule }` stays on one line.
   - `Conceptual.{ Vector<Integer> ethos_zero:Problem }` stays on one line.
   - `[ LIMIT.Integer ]` stays on one line.
3. **A form holding a broken form breaks.**
   - The section around `Voice.{ Aspect.[ .. ] Topic.String }` breaks, and so does `Voice` itself.
   - `[ flow:[ FlowId Voice Event ] ]` stays on one line, because nothing in it breaks.
   - `[ Start.{ Voice Capsule } Record.{ FlowId Event } ]` stays on one line for the same reason.

**Open wording point (this flow's reading).** The coordinator's clause says a broken form "closes on its own line". It also says the spec's Voice prediction should match as written. In that prediction, the closer ends the last element's line (`Field ]`). The two cannot both hold. The build follows the spec's block. Putting each closer on its own line would make every predicted literal miss.

## Checks

- `cargo test`: all pass.
  - lib 21, cli 17, ethos 33, freshness 4, generated 20, signal_without_datom 2.
  - flow_contract 1, with its inner runs 2 and 1.
  - print 10, the set's 9 plus the acceptance test.
- `cargo fmt --check` and `cargo clippy --all-targets -- -D warnings` are clean.
- `nix flake check --keep-going --override-input protos path:/tmp/protos-item12b` printed "running 9 flake checks" and "all checks passed!".
  - The 8 check attributes are build, clippy, dependency-ethos, doc, fmt, no-free-functions, no-inherent-methods and test.
- Regeneration: after the set's regen script ran, every tests/generated/*.rs, src/error.rs and src/ethos-zero.rs is byte-equal to the set. So is every fixtures/*.ethos.
- Reprint stability: I reprinted the six rewritten sources a second time, and their checksums were unchanged. `every_fixture_prints_...` passes over all 20 sources, including the assertion that print of print equals print.

## Spec predictions against observed

All six match.

1. The acceptance test `each_element_starts_on_a_new_indented_line` passes. `Library [] [ Voice.{ Aspect.[ Psyche Mind Field ]` / `Topic.String } ] [] []` prints byte for byte as the spec's block: `Library\n[]\n[\n  Voice.{\n    Aspect.[\n      Psyche\n      Mind\n      Field ]\n    Topic.String } ]\n[]\n[]\n`.
2. Print of print equals print for all 20 sources.
3. The changed goldens are exactly the six print sources:
   - fixtures/print/flow-library, flow-signal, flow-operation and flow-memory (.ethos);
   - ethos-zero.ethos and error.ethos, which keep their leading `;` comment lines.
4. The tests/print.rs literals changed in the five tests the spec names. `leaves_stay_on_one_line_and_angles_stay_tight` holds the same expected text as before the patch.
5. Every fixtures/*.ethos and every generated module is byte-equal.
6. protos and datom-codec are untouched, so the datom print is unchanged. This holds by construction; I did not rebuild those repositories.

Observed where the spec makes no prediction:

- Sections with at most two unbroken forms stay on one line, for example `[ Launch.{ Voice Brief.String } Report.{ FlowId Event } ]`.
- Import sections also stay on one line: `[ datom_codec:[ Error ] ethos_zero:[ Problem Location ] ]`.

## Files touched (9; +366 / -84 over the set)

All are in ethos-zero:

- src/printing.rs: the layout.
- src/lib.rs: the `Printable` doc line.
- tests/print.rs.
- ethos-zero.ethos and error.ethos.
- fixtures/print/flow-library, flow-memory, flow-operation and flow-signal (.ethos).

The printer declares no trait. It uses two private hand-written types, `Piece` and `Role`, and closures inside `impl Printable for Protos`. protos's `Grouping`, `Layered` and glyph traits are `pub(crate)`. Their element grouping and tight-angle rule are therefore copied into ethos-zero.

Provenance receipt: unavailable.
