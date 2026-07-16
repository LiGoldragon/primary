# Stack re-audit v1 — the nine-crate next-generation language family

Independent re-audit ledger for the Claude-side NOTA / Schema / Nomos / Logos /
sema Rust stack. Agent pickup surface; lean verdicts, evidence, and graded
defects only. Each section is a dated append.

## 2026-07-16 — full re-audit, session `language-family-re-audit`, lane `rust-stack` (Opus 4.8, rust-auditor)

Scope: verify the corrupted-handover claim inventory against current artifacts.
Method: fresh clones of all nine repos, `nix flake check` at each tip (each flake
runs `build` + `test` + `doc` + `fmt` + `clippy`; the golden suites are the `test`
check), plus file:line code inspection. Clones were throwaway; no crate was
mutated. Citations are crate-relative paths.

### Scope 1 — Repos and revisions: VERIFIED (two pins recovered from corruption)

All nine repos are single-commit repos; every `nix flake check` is green at the
current `main` tip. No crate has advanced since the handover.

| crate | current main tip | handover pin | outcome |
|---|---|---|---|
| content-identity | `6cc0408cdb96f174cc8fdf6ca23420038de28450` | 6cc0408cdb96 | tip == pin, reachable, flake green |
| name-table | `c3237f77c087e6feab49d6cf34971cebc14a11e6` | `c34e8c6df` (INVALID) | pin garbled — recovered true tip; flake green |
| raw-discovery | `a4e8c6df84e6a487ca6fe2f3641f9bafd0b0d8c8` | lost to corruption | recovered true tip; flake green |
| structural-codec | `104f92454a5ba88b376fa706a9fe38c4a4b65ee0` | 104f9245 | tip == pin, reachable, flake green |
| core-schema | `33e5be2769b87920b773c7707c1ceb2c97cd42e8` | 33e5be2769b8 | tip == pin, reachable, flake green |
| structural-codec-derive | `348bd89fafefbc13c87b9c5315f7349de38250c6` | 348bd89f | tip == pin, reachable, flake green |
| core-logos | `10e24ebb3bd7e5ecaa749c1362908f2270080b7d` | 10e24ebb3bd7 | tip == pin, reachable, flake green |
| textual-rust | `92174ceb4a6be76ac5f378475839872169bb1a7b` | 92174ceb4a6b | tip == pin, reachable, flake green |
| core-nomos | `f11bc3bd98ef6a6284461ba895f9f2b2d07040f3` | f11bc3bd98ef | tip == pin, reachable, flake green |

Recoveries: name-table handover pin `c34e8c6df` is not a valid git object; true
tip is `c3237f77c087…`. raw-discovery pin was unrecoverable from the corrupted
text; true tip is `a4e8c6df84e6…`. The garbled `c34e8c6df` shares the `e8c6df`
run with raw-discovery's real hash — likely a transmission cross-contamination.

### Scope 2 — Capstone pipeline: VERIFIED (one hygiene drift)

core-nomos `tests/pipeline.rs` (12 tests) + `src/engine.rs`.
- Pipeline chain schema TEXT → CoreSchema → Nomos macros → CoreLogos → TextualRust
  → Rust is real and chained: `pipeline.rs:165` decode, `:171`
  `package.apply` → `engine.rs:43` `MacroPackage::apply` → `lower_schema`/
  `lower_declaration` (`engine.rs:86,94`) emitting `core_logos::CoreItem`, `:176`
  `RustSource::project_item`, `:177` byte-exact `assert_eq!`. VERIFIED.
- Exactly 6 `GOLDEN_*` constants asserted byte-exact (`pipeline.rs:27,33,40,50,60,75`;
  asserts `:177,:219,:250,:268`). Two further `SAMPLE_*` byte-exact assertions are
  explicitly labelled illustrative samples, correctly not counted. VERIFIED.
- Loud failures all tested and enforced: `NomosError::UnknownMacro`
  (`engine.rs:342-343`, test `unknown_named_invocation_errors_loudly`),
  `RecursionCycle` (`engine.rs:337-339`, test `recursive_cycle_is_rejected`),
  `NoStructuralDefault` (`engine.rs:96-99`, test `missing_structural_default_errors_loudly`).
  Typed `thiserror`, no silent fallback. VERIFIED.
- DEFECT (hygiene) — "6 **real on-disk** goldens" is imprecise: the 6 goldens are
  inline `const &str` transcriptions (`pipeline.rs:27-86`), not on-disk files, and
  no `include_str!`/fs read binds them to source. The crate documents this
  (`pipeline.rs:5-8`: "transcribed verbatim from textual-rust's provenance
  fixtures … copied from schema-rust @ 87de872"). The real on-disk goldens live in
  textual-rust and are proven there (Scope 3); core-nomos isolates Nomos lowering
  as the only new variable. Functional byte-pin holds. Grade hygiene, not gating
  (a downstream drift or transcription slip in core-nomos would not be caught here
  — the only residual risk).

### Scope 3 — textual-rust counts: VERIFIED (two clarifications)

`tests/goldens_roundtrip.rs` computes counts at runtime via `Coverage::survey`;
the `test` flake check ran green.
- 153 in-subset items byte-exact: VERIFIED (28+33+33+59 across the 4 goldens;
  README decomposition 38 newtype + 30 struct + 48 enum + 37 alias = 153). Two-way
  = decode and encode both run and reproduce the golden bytes
  (`goldens_roundtrip.rs:49,61,76`). Clarification: the reverse value-identity law
  (Core → text → Core == identity, stable hash) is proven on 2 hand-built fixtures
  (`core_roundtrip.rs:55-61`), not on all 153.
- 273 = impl/trait excluded frontier: VERIFIED as scoped (254 impl + 19 trait).
  Clarification: the full out-of-subset frontier the survey reports is 304
  (adds ~14 modules + smaller edges); 273 is the impl/trait subset of it.
- 10,779 lines / 8 files: VERIFIED as the UPSTREAM `schema-rust @ 87de872`
  generated corpus (confirmed: exactly 8 `*_generated.rs`, 10,779 total lines).
  textual-rust copied a 4-file / 4,951-line byte-exact proving subset
  (`standard_newtype_impls_generated.rs` 871, `collections_generated.rs` 1105,
  `spirit_generated.rs` 1023, `runner_generated.rs` 1952). Both figures are
  correct for their referents; no defect.

### Scope 4 — Stringless Core: VERIFIED (one mislocated-claim hygiene note)

- Core* carry no strings: VERIFIED. Every name is `name_table::Identifier(u32)`
  (`name-table/src/identifier.rs:24`); zero `String`/`&str` fields across all
  core-logos Core types (`item.rs`, `structure.rs`, `newtype.rs`, `enumeration.rs`,
  `field.rs:15`, `path.rs`, `type_reference.rs`, `visibility.rs`, `alias.rs`,
  `attribute.rs`, `generics.rs`). The lone `String` in the family is name-table's
  `Name(String)` interning store (`name.rs:27`).
- NameTable delegation: VERIFIED (`core-logos/Cargo.toml` depends on name-table;
  resolution threaded through `NameResolver`, `path.rs:17-25`).
- Transactional interning atomicity: VERIFIED. Speculative `NameTransaction` +
  `try_intern` rollback (`transaction.rs:24-89`, `table.rs:116-131`); named tests
  `a_dropped_transaction_leaves_the_table_byte_identical`,
  `try_intern_rolls_back_a_failed_alternative` (`tests/transaction.rs`), reinforced
  cross-crate by `structural-codec/tests/laws.rs:89` `law_three_interning_atomicity`.
- HYGIENE — "cycle rejection" is mislocated in the claim: name-table interning is
  a flat string→u32 map with no graph, no cycle code, no cycle test (grep clean).
  Cycle rejection genuinely exists but as a delegation/recursion property elsewhere:
  `structural-codec` `DelegationCycle` (`src/error.rs:47-48`, `evaluator.rs:116`,
  test `evaluator_behavior.rs:120`) and core-nomos `RecursionCycle`. Guarantee
  present; claim mis-scoped. Not gating.

### Scope 5 — Identity keystone: VERIFIED

- Hash over rkyv bytes: `content-identity/src/hash.rs:56-76` (`of_core` over
  `to_archive_bytes`), `portable.rs:41-44`, blake3 `hasher.rs`.
- NameTable excluded: by construction — Core rkyv bytes physically contain only
  `Identifier(u32)`; documented `hash.rs:62-66`, `core-logos/src/domain.rs`.
- Layout-version-tagged + domain-separated: `core-logos/src/domain.rs:14-17`
  (context `"core-logos 2026 stringless core algebra of logos"`, `LayoutVersion(1)`),
  folded `content-identity/src/domain.rs:65-78`.
- Rename hash-stable / structural + visibility edits move it: named tests
  `a_rename_leaves_core_identity_unchanged`, `a_structural_edit_moves_core_identity`,
  `a_visibility_edit_moves_core_identity` (`core-logos/tests/content_hash.rs:29,50,72`).
- Structural table = external sidecar keyed by `ScopedCoreTypeId`, excluded from
  Core value identity: `structural-codec/src/table.rs:1-5,73`; structural proof —
  `core-logos` has NO dependency on structural-codec; law
  `law_four_identity_preserving_across_revisions` (`laws.rs:129`) shows two tables
  of distinct identity decode to the same Core value with equal content identity.

### Scope 6 — Structural-codec kernel: VERIFIED (one hygiene note; payload recovered)

- ConstructorCodec per constructor, positional signature: VERIFIED type
  (`codec.rs:16-26`: `decode_forms: Vec<StructuralForm>` disjoint, single
  `encode_form`, `signature: PositionalSignature`), gathered one-per-constructor in
  `StructuralEntry` (`codec.rs:51-55`). HYGIENE — the "signature MUST equal the Core
  field signature" invariant is by-construction in the derive
  (`structural-codec-derive/src/generate.rs:456-488`) only; the evaluator never
  reads `signature` at runtime, so it is currently descriptive metadata with no
  independent check. Not gating.
- Product/Repeat sequence algebra: VERIFIED (`form.rs:24-25` `StructuralForm::Product`,
  `form.rs:78-88` `SequenceForm::{Product,Repeat}`, evaluator honours both).
- Table-identity payload (RECOVERED — handover was garbled here): identity =
  `ContentHash::of_core(&TableIdentityPayload)` (`table.rs:65-74,98-108`) under
  domain `"structural-codec 2026 addressed structural table"` + `LayoutVersion(1)`,
  over exactly: (1) `core_universe: CoreUniverseId`, (2) `core_layout_identity`,
  (3) `raw_profile_identity`, (4) `committed_lexicon: Vec<u8>` (glyph bytes),
  (5) `leaf_codec_contracts: Vec<LeafCodecContractId>`, (6) `entries:
  BTreeMap<ScopedCoreTypeId, StructuralEntry>` (the constructor codec data). The
  table's own `identity` and its `revision` are NOT in the pre-image (hash stored
  outside; a bare revision bump does not move it). Matches the handover's
  universe/layout/raw-profile/committed-lexicon/leaf-codec list plus the entries map.
- ScopedCoreTypeId under CoreUniverseId: VERIFIED (`ids.rs:22,53-66`);
  `FIXTURE_UNIVERSE = CoreUniverseId::new(0)` placeholder pending the schema-unit
  ruling (`ids.rs:34-35`, primary-56d1.11).
- Authoring structs normalize to kernel before hash/eval: VERIFIED
  (`authoring.rs:12-73` `AuthoringForm::normalize`; fixture normalizes then seals,
  `fixture.rs:137-153`; evaluator has no authoring case; test `normalization.rs:9-42`).
- Conformance laws — all four hold: (i) round-trip both directions
  `law_one_round_trip_core`, `law_two_round_trip_canonical`; (ii) interning
  atomicity `law_three_interning_atomicity`; (iii) cross-revision Core-identity
  preservation `law_four_identity_preserving_across_revisions` (`tests/laws.rs`);
  (iv) interpreter == generated codec — VERIFIED via the derive's fixtures sub-crate:
  `structural-codec-derive/fixtures/tests/conformance.rs`
  `law_five_the_generated_codecs_match_the_evaluator` runs the real
  derive-generated `GeneratedCodec` through structural-codec's `ConformanceHarness`
  against the trusted evaluator (agreement on value, NameTable delta, canonical
  output, and typed-error decision, across valid + malformed inputs), plus
  `malformed_inputs_are_rejected_by_both_paths`. `fixtures` is a workspace member
  (root `Cargo.toml:2`); the flake's `cargoTest --workspace` ran and passed it.
- Runtime evaluator with generated fast path: VERIFIED. Evaluator ships
  (`evaluator.rs:63-417`, both directions); the generated fast path is the
  derive-emitted per-type `GeneratedCodec` (`generate.rs`), proven equivalent to the
  interpreter by law 5. Note: there is no runtime auto-dispatcher choosing
  generated-vs-interpreter — selection is at the type/compile level (generated code
  used when the derived type is in hand; the evaluator handles runtime-loaded
  tables). This matches the design intent; not drift.

### Scope 7 — Logos–Rust bridge: VERIFIED

- Names always present in CoreLogos, elision is projection-only:
  `core-logos/src/field.rs:13-17` (`name: Identifier`, never optional),
  `item.rs:33-40`; projection always resolves and emits (`textual-rust/src/project.rs:96-108,308-317`).
- Visibility + both derive groups stored, not computed at projection:
  `core-logos/src/visibility.rs:11-17`, `attribute.rs:12-24`; projection reads the
  stored variants/vector (`project.rs:83-94,153-169`).
- prettyplease sole formatting authority: only formatter is `prettyplease::unparse`
  (`project.rs:459`, `codec.rs:52`); no rustfmt run, no hand-emitted layout. Module
  assembly (`project.rs:466-478`) joins per-item prettyplease output — assembly, not
  token formatting; per-item byte-exactness is the acceptance unit.
- Decode leans on syn: `read.rs` — every `ReadRust` impl is on a `syn::` node; no
  hand-rolled parser. `Cargo.toml` `syn = "2" (full,parsing,printing,extra-traits)`.
- Two-way subset boundary principled: the four item kinds are the subset; every
  out-of-subset construct is a typed loud `Error::UnsupportedItem`/`…` (`read.rs:61-110`),
  documented on both sides (`core-logos/src/item.rs:19-21`). Reader never guesses or
  silently skips.

### Scope 8 — Design drift

- StructuralForm enum-vs-struct (primary-56d1.14): CONFIRMED, grade hygiene. The
  design authority declares `pub struct StructuralForm { elements: Vec<StructuralElement> }`
  with a separate `enum StructuralElement`
  (`reports/logos/up-close-design-v1.md:296-298,303-311`); the code declares
  `pub enum StructuralForm` carrying those seven variants and has no
  `StructuralElement` type (`structural-codec/src/form.rs:23-48`) — the wrapper's
  Vec-of-elements role is carried by `SequenceForm` and `ConstructorCodec.decode_forms`.
  Naming + one-level-nesting drift; the code is internally consistent (its own
  header cites "settled terminology, design §4.1") and arguably cleaner (the
  special-case wrapper dissolves into the sequence algebra). Doc-vs-code
  reconciliation only; already tracked, blocked on up-close review.
- CoreItem 7-vs-4: doc §6.2 lists seven kinds (adds TraitDefinition/ImplBlock/
  FreeMethod, `up-close-design-v1.md:889-892`); code has four
  (`core-logos/src/item.rs:23-28`). Intentional, self-documented narrowing (the
  enforced two-way subset). Grade informational; the doc enum is an aspirational
  superset.

### Verdict roll-up

Every technical claim in the corrupted handover is substantiated by current code
and green flake checks. No slice-three-gating or merge-gating defect was found in
the rust stack.

- Defects (all hygiene): Scope 2 "on-disk goldens" phrasing (inline transcriptions);
  Scope 4 "cycle rejection" mislocated onto interning; Scope 6 `ConstructorCodec.signature`
  inert at runtime; Scope 8 StructuralForm enum-vs-struct (tracked .14).
- Informational clarifications: Scope 3 frontier 273 (impl/trait) vs 304 (full),
  10,779/8 is the upstream schema-rust corpus vs the 4-file/4,951-line in-repo
  subset, value-identity reverse proven on 2 fixtures not all 153; Scope 6 no
  runtime generated/interpreter selector (by design); Scope 8 CoreItem 7-vs-4.
- Two corruption recoveries: name-table tip `c3237f77c087…` (handover `c34e8c6df`
  invalid), raw-discovery tip `a4e8c6df84e6…` (pin lost).

Audit note: an initial subagent pass reported Scope 6 law (iv) as an untested
merge-gating defect on the belief that the derive fixtures crate was absent; direct
inspection refuted this — the fixtures workspace member exists and its law-5
conformance test runs green under the flake. Recorded so the correction is
spot-checkable.
