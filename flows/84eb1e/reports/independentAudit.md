# Independent audit of the Ethos Zero candidate

This is an independent review of the candidate named by the delegated task.  The reviewed Ethos Zero revision is `main` at `341c5c57e45d` (working tree clean); the declared dependencies are Protos `0.26` at `2d999f173334` and datom-codec `0.21` at `41a3c073d5c5`.  I treated source observations, the earlier reports, and fresh executions as separate evidence.

The candidate is not ready for closure.  The parser and situated faults are substantially improved, and the substrate Decimal behavior is fixed, but accepted/publicly constructible values still reach noncompiling Rust and generation panics.  Those are concrete F2/F3/F5/F9 boundary defects, rather than optional extensions.

## Fresh verification

The existing focused gate was run once with the required bounded environment:

```text
ulimit -v 8388608
timeout 900s env CARGO_BUILD_JOBS=1 RAYON_NUM_THREADS=1 cargo test --locked
```

It passed: 75 tests (50 Ethos, 15 generated, 7 CLI, 3 freshness), with zero unit or doc-test failures.  No Nix check was run; that final check remains for the main flow.

The four original F1 inputs all returned typed faults with no CLI panic: a `Self` declaration is `Name.Self`, a raw identifier is `Name.r#type`, 27 constraints are `Arity.{26 27}`, and an empty constraint is `Empty`.  The four original F4 fault probes also returned exact source slices `Bogus`; their paths use the corrected body index `1`, including qualified head arguments and associated bounds.

For F2 controls, fresh generation followed by bounded standalone `rustc --edition=2021 --crate-type lib` compiled decimal equality, sourced decimal, decimal in `Vector`, prelude `Box`, prelude `Result`, direct `Self` recursion through `Box`, and empty/unit cases.  This independently confirms that the old DecimalEq failure is gone after the substrate rewrite.  Two accepted cases did not compile:

* `nested-collision.ethos` generated an enum `XA` and an authored struct `XA`; `rustc` reported E0428 and conflicting implementation errors.
* `alias-self-generic.ethos` generated the recursive alias `pub type B = A<B>;`; `rustc` reported E0391.

The current CLI was exercised against 48 malformed and supported scratch inputs under a 1 GiB/15 second per-input bound; none panicked.  That does not establish that every generated output compiles, because the nested collision above was found by a separate Rust compiler pass.

## Findings by original obligation

### F1 — malformed input handling

The original four parser failures are now typed and situated as described above.  Source inspection shows a conception depth limit of 128 and parser checks for declaration names, constraint arity, and empty constraints.  The F1 obligation is substantially met for those exact probes.  This result does not make the public concept API safe: `File` remains publicly constructible and can bypass the parser checks (see F2 and F9).

### F2 — accepted declarations must generate compiling Rust

The decimal and standard-container regressions are fixed in fresh compilation.  Nested synthetic names remain unchecked: the generator forms a nested name from the enclosing identity and variant name, but no emitted-name collision check precedes generation.  The independent `nested-collision` compile failure is therefore a current defect.

The generated Rust uses fully qualified standard containers, so local declarations named `Box` and `Result` did not capture them in the fresh controls.  Direct `Self` recursion is boxed and compiled in the supported parsed case.  The generic alias case remains accepted but emits the Rust recursive-alias cycle above; checking detects alias cycles without substituting applied generic arguments, which is a concrete gap in generic-cycle handling.

### F3 — layer and ascent behavior

The current source directly projects `File` to a situated Protos form and provides `File: protos::Protosizable` and `File: protos::Textualizable`; `protos::Delineation` directly conceives `File`.  Fresh generated consumer fixtures use the rewritten datom/protos bounds, and no old DecimalEq failure was reproduced.  This supports the substrate rewrite claims for the exercised path.

The public `Canonical` wrapper itself has no direct `protos::Protosizable` implementation; actualization reparses its `text` as `str`.  If the original layer table requires every named layer wrapper to carry that bound, this remains unproved and should be recorded as an ontology/vision gap.  More materially, direct public ascent is only infallible for representationally validated fields; it does not validate that the resulting Rust is compilable.

### F4 — situated fault paths

The four fresh exact probes produced the literal slice `Bogus` and corrected paths: type argument `[0 1 1 0 1 0 0]`, kind argument `[0 1 1 0 0 0]`, second kind argument `[0 1 1 0 0 1]`, and associated bound `[0 1 1 0 1 1 0 0]`.  Their extents selected only the bad identifier.  The old body-zero/remapping defect was not reproduced.

### F5 — identity, references, and cycles

Fresh parser/checker cases refuse duplicate members, local arity errors, repeated ambiguous generic constraints, alias cycles, and superkind cycles; an unreferenced overlapping constraint is retained.  Intrinsic explicit arity is checked.  The applied generic alias cycle remains the exception documented under F2: the cycle walk follows an alias body but does not substitute its arguments, allowing an accepted declaration whose Rust is recursively aliased.

Ethos identity retains the name plus constraints, while Rust emission derives an identifier from the name alone.  Thus same-name kinds can remain distinct in Ethos resolution (bare references become ambiguous) while still targeting the same Rust identifier if both declarations are emitted.  The candidate deliberately does not invent mangling; this identity-to-emitted-name collision policy is still a real audit/vision gap requiring an explicit closure decision.

### F6 — recursive generated data

The existing generated test constructs a 10,000-level nested value and, with `IncorporationBudget = 256`, receives typed `BudgetExhausted`.  The Ethos parser test also refuses a 2,000-level nested source with a typed depth fault.  These are meaningful bounded-recursion tests.

The budget is caller-supplied and the public type permits larger values; there is no universal hard maximum for a programmatic caller that chooses an extreme budget.  The evidence establishes bounded refusal for the tested budget, not an unconditional stack-safety guarantee for arbitrary budgets.

### F7 — flat resource scaling

The current flat alias input with 1,000 aliases returned immediately with a typed `Depth` fault at path `[0 1 1]` and extent `{9 9797}` under a 1 GiB/60 second bound.  This is an effective bound for that alias chain.  The source declaration cap of 512 is checked only in `Types::check`; 513 kinds were accepted and compiled, and imports, associations, Signal, and Sema declarations have no corresponding flat cap.  If “flat declaration cap 512” is intended globally, that is an unclosed resource-limit defect; if it is intentionally a type-only cap, the candidate report should say so precisely.

### F8 — identity naming and Types shape

The concept model distinguishes same-name identities by constraints, while emitted Rust names remain bare identifiers as described under F5.  No safe Rust-name disambiguation was found.  The Types documentation says there are three sections (imports, declarations, associations), and the current parser/emitter requires and emits all three.  The literal example in the original prose has only two sections; current handling is to reject the omitted association section with an arity fault rather than infer `[]`.  This is a documentation/vision mismatch, not evidence that the implementation silently accepts both forms.

### F9 — emitted names, CLI, and final gates

Lowercase associated constants are refused, grouped qualified imports such as `std:clone:[ Clonable.Clone ]` are accepted, and generated qualified standard names are emitted without `use` capture.  `Name` accepts `Self` specially, rejects raw `r#` names and Rust keywords, and accepts Unicode identifiers such as `café`; `Source` accepts `Self`, `self`, `super`, `crate`, and raw path segments.  Rust path syntax alone does not make module-level `Self` valid: a parsed `Types` input with source `Self` generated `Self::Text`, which a bounded standalone `rustc` invocation rejected with E0220/E0223.

The public `Name` and `Source` tuple/representation fields are private and validated through `TryFrom`, but public declaration fields permit constructing checked-out-of-band `File` values.  Two bounded programmatic probes demonstrated remaining panic paths:

* A public `File` containing `Name::try_from("Self")` as a type declaration/reference reached `Generating::generate` and panicked in `syn::parse2` because emitted `Self` was invalid as a declaration identifier.
* A public identity with 27 valid constraints reached `Lettering` and panicked at `Ident::new` when the parameter index became 26 (`"["` is not an identifier).

The generator also contains infallible `Ident::new` and `syn::parse_str`/`syn::parse2(...).expect(...)` boundaries.  Therefore the direct-ascent claim is true for structural Protos projection but not a total guarantee for every publicly constructible value or conversion/derive bypass.

## Assessment for the final gate

The candidate has credible fresh coverage for the original malformed-input cases, F4 situated paths, decimal substrate behavior, qualified standard containers, and finite budget/depth refusals.  It should not be approved as complete while the nested synthetic-name collision and applied generic alias cycle still produce accepted noncompiling Rust, and while public construction still reaches generation panics.  The `Source::try_from("Self")` acceptance and the scope of the 512 declaration limit need explicit decisions.  These findings do not require expanding into Nexus architecture.

## Sources

- Candidate repository at reviewed `main` revision `341c5c57e45d`: `/git/github.com/LiGoldragon/ethos-zero`.
- Candidate implementation: `src/lib.rs`, `src/conception.rs`, `src/actualization.rs`, `src/checking.rs`, `src/generation.rs`, `src/protosization.rs`, and `src/main.rs`.
- Candidate tests: `tests/ethos.rs`, `tests/generated.rs`, `tests/cli.rs`, and `tests/freshness.rs`.
- Original audit: `/home/li/primary/flows/1a6ca4/reports/auditEthosZeroAstra.md`.
- Substrate rewrite report: `/home/li/primary/flows/da223f/reports/rewrite.md`.
- Candidate rewrite report: `/home/li/primary/flows/84eb1e/reports/rewrite.md`.
- Authority and behavior sources read: `/home/li/primary/Vision/ethos.md`, `/home/li/primary/Vision/protos.md`, `/home/li/primary/Vision/datom.md`, `/home/li/primary/Intent/mandatoryTraits.md`, `/home/li/primary/Intent/protosParsing.md`, `/home/li/primary/Intent/data.md`, and `/home/li/primary/flows/84eb1e/vision/` plus its flow log.
- Fresh probe corpus and bounded outputs: `/tmp/ethos-zero-astra-EfNPnY/inputs/` and `/tmp/ethos-zero-astra-EfNPnY/inputs/current-out/`.
