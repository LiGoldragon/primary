# Datom codec and Protos rewrite

## Result

The retained rewrite is landed on both repository mains. Protos is
`2d999f173334` (0.26.0), and datom-codec is `41a3c073d5c5` (0.21.0), pinned
to that exact Protos revision. Ethos Zero was not edited; both flakes retain
its fixed `dc54e3323ae00dc3f88f4d65c2785e6800c06b74` pin.

Protos owns target-parametric routing and generic total textual ascent.
`Potential<T, C>` delegates once through `C: Route<T>`; `Protoform` routes to
exactly one structural form with unit context. `Textualizable<C>` now follows
infallible `Conceivable<C>` and `C: Protosizable` without reparsing or a
fallible ascent path. Text itself bears the fallible text-layer
`Protosizable` capability, while Protoform and Delineation bear their
structural concept capability.

Datom-codec selects its Datom concept through `Route<Datom>` with unit
context, and selects a corporate `T: Datomic` with an explicit
`IncorporationBudget`. `Datomic` now bears only corporate incorporation; it
requires the real universal `Conceivable<Datom>` and `Textualizable<Datom>`
capabilities. Concrete scalar bearers and generic Vec, Option and Result
bearers implement the foreign universal trait legally. Box uses Protos's
trait-local generic delegation. No blanket foreign `impl<T: Datomic>
Conceivable<Datom> for T` was added.

The budget is caller-owned, validates nonnegative construction, and keeps its
remaining allowance private. Each library-mediated corporate callback spends
one unit before calling the Datomic reader; Sites, Positions and Variants
reborrow the same budget. Structural and concept routes use unit context.

After the first landing, independent external checking found that the public
raw value `Datom::Variant(Some, Word("a.b"))` could serialize as
`Some.a.b` but conception selected a different, nested Variant anatomy. The initial 0.18 repair closed period-root words; the final 0.20 repair also rejects every malformed separator run from the DatomWord domain and projects it as quoted Text. Together they make every admitted raw Datom composition stable through Text and reparsing. `Datom::Word` now carries
the public, validated `DatomWord` domain. A complete word chain whose root
separator is Period is refused at raw construction, while a private lexical
projection materializes such scalar words as the same nested Variant anatomy
that conception produces. This is a structural canonicalization, not an
ascent reparse: Text, Decimal, and the other contextual values keep their
domains, including Decimal `3.25`, `-42.0`, and `0.5`.

## F1–F10 status

| Finding | Status and current witness |
| --- | --- |
| F1 punctuation-bearing Text | Addressed; contextual bare versus quoted Text now preserves every variant payload boundary, with ordinary and property reading witnesses. |
| F2 Problem strings | Addressed; Problem payloads retain comments, whitespace, and structural-looking content through projection and reading. |
| F3 finite decimal | Addressed; finite decimal property test passes. |
| F4 opaque meaning | Addressed; parenthesized meaning retains semicolons and curly closers. |
| F5 universal layers | Addressed in this landing; real external consumer types, scalar, Vec, Option, Result and Box routes compile through `Conceivable<Datom>` / `Textualizable<Datom>`. |
| F6 projected Protoform/Situation anatomy and raw concept inverse | Addressed. Period-root words canonically become nested Variants; malformed separator runs are outside DatomWord and canonically become quoted Text. The final 3,905-candidate corpus verifies all admitted values through two Variant heads, printed Text, reparsing, and situation equality. |
| F7 deep Clone/Eq/Debug and corporate budget | Addressed in the stated library scope: iterative clone, equality and debug pass the retained 20,000-depth and 100,000-scale witnesses. The caller-owned budget spends before every library-mediated corporate callback; two units for `[ 1 2 ]` faults at path `[1]` on `2`, while three units succeeds. It does not bound arbitrary user recursion or all large budgets. |
| F8 exhausted Positions | Addressed; empty and over-read positions now produce a situated exhaustion fault without advancing the cursor. |
| F9 ethos contract | Addressed for the declaration and executable freshness obligation: 0.26/0.21 declare actual owned String yields and layer associations, explicitly omit char and borrowed forms the grammar cannot express, and import validated `DatomWord` rather than falsely aliasing it to `protos::Word`. Fixed-generator regeneration and both final remote freshness checks pass. The generator's obsolete downstream implementation template is an ethos-zero follow-up, outside this required freshness relationship. |
| F10 named parser state | Addressed in retained parser anatomy; no new designed tuple was added. |

## Gates and limits

Every local Cargo command used `ulimit -v 4194304`, `timeout 180s`, and one
build job. Protos `cargo fmt --check`, clippy with warnings denied, and the
full test suite passed: 30 ordinary tests and six scale modes through 100,000
nodes. Datom-codec 0.21 `cargo fmt --check`, clippy with warnings denied,
docs with warnings denied, and the full test suite passed: 47 ordinary tests
and five
scale modes through 100,000 nodes.

The required temporary local-path integration copy passed datom-codec's full
Cargo suite before either real manifest was changed. The final real datom
pin then passed the same capped Cargo test suite.

Each final Nix invocation used the 4 GiB address-space cap and `max-jobs 0`,
so work was delegated only to
`ssh-ng://nix-ssh@prometheus.goldragon.criome`. The first 180-second client
attempts established the remote derivations but did not retain terminal
evidence. Their recovered final completion used a bounded 900-second client
timeout against the exact pushed, clean heads. Protos evaluated its nine
checks and exited zero with `all checks passed!`. The later 0.26/0.21 F9
declaration repair required and received new final checks for both sources:
Protos evaluated its 10 checks and datom-codec evaluated all 16, including
their regenerated-contract freshness checks; both exited zero with `all checks
passed!`. Nix reported that
datom-codec intentionally omits incompatible aarch64-darwin, aarch64-linux
and x86_64-darwin systems from this flake check.

## Old claims and fresh evidence

The source audit at `flows/1a6ca4/reports/auditDatomCodecAstra.md` describes
the pre-rewrite contracts and its then-current evidence. The initial report's
raw-Datom inverse claim was incomplete; the later external `Some.a.b` witness
and the subsequent 0.20 composition correction above supersede it. This report only
claims the fresh bounded Cargo evidence above, the precise compiler shape of
the new universal-layer API, the explicit budget regression, the new raw
concept inverse regressions, and the observed remote Nix outcomes. It does
not treat generated old-Datomic boilerplate, arbitrary consumer recursion,
arbitrary budgets, or Rust 1.85 as verified.

An isolated temporary crate, with the same 4 GiB cap, one build job, and a
180-second timeout, showed that the fixed generator's old downstream
implementation template still calls removed `Datomic::conceive` methods. That
is a stronger downstream-compilation check than F9's required executable
declared/generated freshness relationship, so it is recorded as an
ethos-zero follow-up rather than a failed crate gate. The in-scope declaration
repair imports the validated `DatomWord` wrapper, eliminating the former false
`DatomWord = protos::Word` generated alias while the two final freshness checks
prove the committed products were generated by the fixed pin.

## Final-head closure

The final raw inverse witness was independently rerun by primary_preflight on
Protos 0.26 `2d999f173334` and datom-codec 0.21 `41a3c073d5c5`: 3,905
candidate words, 246 admitted, and 738 standalone, one-head, and two-head
cases passed raw Datom equality and projected Protoform/Situation equality
through printed Text and fresh reparsing. Unstable runs project as quoted Text;
valid colon/exclamation chains and finite Decimal controls pass. Both final
remote flake checks then exited zero with `all checks passed!` under the 4 GiB,
900-second remote-only limits.

## Sources

- Supplied rewrite brief; `Vision/protos.md`, `Vision/datom.md`, `Vision/ethos.md`, `Intent/mandatoryTraits.md`, and `Intent/protosParsing.md`.
- `flows/1a6ca4/reports/auditDatomCodecAstra.md`.
- Protos main `2d999f173334`; datom-codec main `41a3c073d5c5`.
- Capped Cargo and remote Nix commands observed in this flow, thread provenance from the harness environment.
