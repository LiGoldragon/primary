# Ethos audit: versus the vision, and Ethos itself

Subflow of e51411, 2026-09-25. Tool state is ethos-zero 10.0.0 (last commit 4bf73ca, 2026-09-12), built binary `target/debug/ethos-zero` (2026-09-15). Every "probe" below is a scratch `.ethos` file run through that binary. Evidence about usage comes from 56 real `.ethos` files across about 50 repos.

**In short:** the data-schema core (Library/Signal/Sema to Rust, datom derives, Signal-gated datom feature, freshness tests) is built and well tested. The newest ask is absent: whole programs in Ethos, meaning function syntax, implementations and a manifest. Real use has split into three pipelines, and several files have drifted from their Rust without any check noticing. The generator has one correctness bug (it emits duplicate types). Expressiveness stops at i64/String/Vector/Option/Result. Real code works around this constantly.

## Part 1: what the vision asks, and whether it is built

Newest asks come first.

| # | Ask (verbatim, provenance) | Status | Witness |
|---|---|---|---|
| 1 | "develop Ethos to the point where we can just write the whole program directly in Ethos … fleshing out the function syntax … implementations … the manifest … for compiling and finding dependencies" (living, 2026-09-25, flows/e51411/vision/ethos.md) | **Absent** | Kinds give trait *signatures* only. Vision/ethos.md (09-11) still says "the interaction body is hand-written Rust". No body syntax, no manifest. Imports are unchecked Rust paths, and no `.ethos` file can import another (probe: `other_crate:[ Thing ]` emits `other_crate::Thing` blindly). |
| 2 | Nomos (macro layer) and Logos "in series by sending each other signals … from ethos and datom all the way into compiled Rust" (living, 2026-09-24, flows/752e0f/vision/ethosNextGeneration.md) | **Absent** | core-nomos, nomos-engine, logos-engine and core-logos are frozen reference repos from the earlier estate. |
| 3 | Help menu "generated automatically from the ethos … full end-to-end"; Nexus lean, CLI deserializes (2026-09-24, flows/752e0f/vision/helpMenu.md; Vision/ethos.md "point at any object … its Ethos prints") | **Partial** | Only ethos-zero prints its own ethos with no argument (tests/cli.rs `no_argument_prints_the_crates_own_ethos…`). There is no general type-to-ethos reflection and no per-variant help. |
| 4 | "all of the machine-to-machine language … is ethos. You always give an ethos spec" (2026-09-20, flows/b81560/vision/operational-ethosSpecSkillAndTriadBranches.md) | **Partial** | 23 signal-* and 16 meta-signal-* repos are generated and held fresh. But the skills' return types (subflow, operational-final-response, operational-status-presentation) use a `Type` root that ethos-zero refuses (probe: `Conceptual.{ [] Root }`). flow/crates/{signal-flow,meta-signal-flow}/ethos/signal.ethos are never generated and have drifted: the ethos says `Restarted.{ FlowId Integer }` while signal-flow/src/lib.rs:34 has `Restarted { flow_id: String, generation: u64 }`. |
| 5 | Meaning, "a computer language that is purely logographic … defined in Ethos" (Vision/meaning.md, 2026-09-20) | **Partial** | `datom_codec::Meaning(Opaque)` exists (datom-codec src/composition.rs:339). Nothing of the Meaning ontology is in Ethos. |
| 6 | Escaping ethos text inside datom with a balanced, unique delimiter (2026-09-19, flows/b81560/vision/operational-ethosEscapeDelimiter.md) | **Absent, still open** | No delimiter has been chosen. |
| 7 | Typed domain primitives ("not an integer … like volume"); a datom structural editor (2026-09-17, flows/9993b5/vision/) | **Absent** | Not witnessed in any repo. |
| 8 | Ban single-field structs; "a new type … is like `name.string`" (2026-09-08, flows/8e9e77/vision/single-field-structs.md) | **Not enforced** | `Measurement.{ Decimal }` (signal-decimal fixture) and `Result.{ String }` are accepted. |
| 9 | Sema is ethos-authored; "operational editing should yield the migration with the edit" (Vision/sema.md) | **Absent** | The Sema root emits plain structs: no rkyv, no migration, no key or identity notion. |
| 10 | "Any repetition in ethos syntax is an implementation failure" (Vision/ethos.md; psyche 2026-08-01) | **Partial, violated in use** | See Part 2: empty Library sections, forced aliases, and the declaration `DuplicateName.Lock` plus the variant `DuplicateName.Lock` (fixtures/orchestrate.ethos). |
| 11 | Kinds, not generics; identity is name plus constraints (Vision/ethos.md) | **Built** | fixtures/processable-kinds.ethos; tests/generated.rs `constrained_kind_identity_compiles`. |
| 12 | Kinds are qualifier-named | **Not enforced** | Names are unchecked. Probe `a.{ String }` emits `pub struct a`. |
| 13 | Sweet form converted mechanically to canonical; one file is one module; no version in the file | **Built** in ethos-zero | src/canonicalization.rs. **Violated** in the wild: `Interface.{maj min patch}` (pipeline 2), and `Nexus.1`/`Sema.1` (spirit, spirit-ethos). |
| 14 | Generated code is fully qualified and has no `use` | **Partial** | Outer `Option<…>` and `Result<…>` are emitted unqualified (tests/generated/tree-types.rs `Wrapped`; placed-types.rs). |
| 15 | Inline type names carry `_Data` "so it never collides" | **Bug** | Probe `P.[ X.{ String } ] Q.[ X.{ Integer } ] X_Data.String` produces **three `X_Data` items**, which is invalid Rust, and the reply is still `Generated`. The EthosNested allocator covers only nested paths. |
| 16 | A variant named after a defined type carries it | **Built** | This is also a hazard: adding type `Locks` silently turns the unit variant `Sel.[ Locks ]` into `Locks(Locks)` (probe). |
| 17 | Every type bears the datom kinds; aliases carry no derive | **Built** | But the derive is now `Composing` (commit "Generate the Composing derive", 09-12). Vision/ethos.md and the ethos/datom skills still say `Compositional`, so their examples do not compile. |
| 18 | Datom is feature-gated in Signal; the Nexus has no datom-codec | **Built** | tests/signal_without_datom.rs |
| 19 | Signal on the wire is rkyv | **Built, fails on recursion** | signal-aggregator/ARCHITECTURE.md: "`Vec<Self>` and `Box<Self>` both overflow". That contract was forced into index arenas. |
| 20 | "Ethos may generate default implementations for Query and Response" | **Absent** | |
| 21 | Omittable datom fields: "Not yet" (Vision/datom.md) | **Absent** (deferred) | |
| 22 | No tuples in designed code | **Built** in the generator | ethos-zero README still says "`Name.{ T1 T2 }` is a tuple variant". The output is a `_Data` struct, so the README is stale. |

## Part 2: Ethos itself

### Grammar: clarity and consistency

- **Meaning comes from position.** Whether `[ … ]` is an enum, a vector or a section depends only on where it sits. That keeps the syntax terse, but a reader or model must know the section order by heart. `.` is overloaded three ways: as alias/declaration head, as a variant-carries marker, and as the self-receiver in kinds (`summarize.[ String ]`). A variant is a unit variant or a payload variant depending on whether some other declaration exists (row 16), so the same text changes meaning at a distance.
- **The Library form is mostly empty.** All roughly 24 real Library and Interface files leave 3 of their 4 sections as `[]`. `associations` is empty in 100% of them, and no file uses more than 2 sections. That is repetition by the vision's own law. The skills already converged on something else: a `Type` root (a head type plus one definitions bracket). It is the most-written ethos in the estate, and the tool refuses it.
- **Root vocabularies have fragmented.** There are four: Library/Signal/Sema (ethos-zero); `Interface`/`Channel` with versions (core-ethos bootstrap, pipeline 2); `Nexus.1`/`Sema.1` (spirit); and `Type` (skills). tree-sitter-ethos (last commit 08-13) still describes an older grammar with `Map`, `Bytes`, streams, `Optional` and `ScopeOf`. So the editor grammar has regressed away from the language.
- **Naming within ethos-zero is inconsistent.** Its own contract uses `Generation_Error` (a hand-written underscore name, which by the vision's rule should be reserved for derived names), and `Unreadable.{ String String }` (positions that carry no meaning).

### Expressiveness: what real files need but cannot say

These are ranked by how often they bite across the 56 files:

1. **Sized and unsigned integers.** The only integer is `i64`. lojix has 196 hits for hand-written widths. chroma has `KelvinTemperature(u16)` and 5 other hand-written width types. signal-version-handover has `Date{year:u16,…}` while its ethos says `Integer`. Pipeline 2 silently maps `Integer` to `u64` (signal-agent/build.rs:304).
2. **Bytes and fixed arrays.** Seen in clavifaber (crypto), signal-5f4fea `NameDigest([u8;32])`, and a `Signal<T>{bytes:Vec<u8>}` duplicated by hand in 3 meta-signal repos. protos.ethos notes: "Character is not an Ethos intrinsic".
3. **Value constraints.** lojix/src/bootstrap.rs keeps a whole "Validated" shadow type tier (about 15 structs and 6 `From` impls) only to add checks. signal-version-handover validates dates by hand. There is nothing like ASN.1 `INTEGER (0..255)` or Malli `[:int {:min 0}]`.
4. **Docs.** `;` comments are dropped, so doc comments are bolted onto the generated types' consumers (signal-mind, lojix, signal-5f4fea).
5. **Recursion under rkyv** (row 19). ethos-zero boxes recursive positions correctly, but it over-boxes: `Twin.{ Twig Twig }` boxes both fields, and `Twig` boxes `Twin` as well. It also accepts `S.{ Self }`, a struct with no finite value.
6. **Time, maps and ordering.** Timestamps are always hand-written in chrono. horizon.ethos says: "Maps are named vectors because Datom has … not a map primitive". There are no maps by design, which is fine for Datom, but a keyed-vector idiom would help. signal-mind hand-writes `Ord` with a `u8` rank table because declaration order cannot be declared meaningful.
7. **Generic data.** "No generics, only kinds" holds for traits, but data wrappers like `Signal<T>` cannot be expressed, so they get copied by hand.
8. **Defaults and optionals by absence.** meta-signal-aggregator hand-writes a `DefaultingPolicy` trait.

### The field-named-by-type rule

The rule works mechanically: ordinals handle repeats, and lojix's `first_writer_path` through `fifth_writer_path` come out without newtypes. The friction is semantic. The rule pushes authors to declare `LockName.String`, `FlowId.String` and `LockPath.String`, but these are `pub type` aliases, not newtypes. They buy a field name and **no type safety**: `LockName` and `FlowId` are interchangeable in Rust. Authors then wrap by hand anyway. There are about 11 hand-written `X(String)` newtypes (lojix, and 5 in meta-signal-ethos-zero), and clavifaber had to remove one. Choose one of two rules: the alias is a name only, and the docs say so; or `Name.String` emits a transparent newtype. The single-field-struct ruling (row 8) points at the second.

### Generator quality

**Strong:**
- Freshness is rigorous: tests/freshness.rs regenerates both self-files and all 17 fixtures.
- `nix flake check` runs the no-free-functions and no-inherent-methods guards.
- Errors are typed.
- Duplicates, cycles (`A.B B.A` gives `Cycle.A`) and undeclared names are all refused.
- Keywords are escaped (`r#type`).

**Gaps:**
- The row 15 duplicate-type bug.
- Only 9 of 17 fixtures are compiled (tests/generated.rs). composition-types, generic-shadow, alias-format, capability-kinds, multi-types, placed-types, sink-associations and streamable-kind are checked for text only.
- Declaring an intrinsic name is accepted, and later use fails obscurely. Probe: declare `Result`, then use `Result<String Integer>`, and the reply is `Arity.{ 0 2 }`.
- Unqualified `Option`/`Result` (row 14).
- Derives are fixed. Sema gets no rkyv.

### Tooling and errors

- Structural errors carry byte extents (`Extent.{ 24 24 }`).
- Conceptual errors carry only a protos path (`[ 1 1 1 1 0 ]`) and an empty datom Path. There is no line or column, although the README says actualization "situates the error in its source text".
- There is no formatter, no LSP and no `Check` query. Validation happens only through `Generate`.
- tree-sitter is stale.

### Real-use drift: a whole-estate problem

There are three pipelines:
1. ethos-zero, used by about 35 repos. It is clean.
2. core-ethos bootstrap with the `Interface` root. It produces mangled names like `pub struct z2VaBD(u64)` and `field_0`, and needs hand-written `behavior.rs` macro glue. Nine repos use it.
3. `.schema` files through schema-rust (spirit, Persona). The `.ethos` files next to them are orphaned.

Generated contracts that no code uses:
- protos and datom-codec commit generated-contract/*.rs, but src/ never imports them. They have diverged: protos `Extent{start:usize,end:usize}` against the generated `{first_integer:i64,second_integer:i64}`.
- signal-ethos-zero's "generated" file says "Hand-written generation-zero projection".

The ethos is only authoritative where a freshness test binds it. About 40% of real files have no such binding.

### Comparisons, where they shed light

- **Cap'n Proto and Protobuf** both have field ordinals, sized ints, `Data`/`bytes`, `map`, doc comments that pass through into code, and annotations. Ethos is positional with no field numbers, and rkyv archives are positional too. So there is **no schema-evolution story** beyond "version in a manifest". This is the largest gap for Sema migrations (row 9).
- **Datomic schema** is data with per-attribute `:db/doc`, cardinality and uniqueness, and it only ever grows (accretion). Sema needs its key, identity and accretion rules, which the Sema root has no place for yet.
- **Malli** keeps constraints as data inside the schema (`[:and :int [:> 0]]`), and it is a registry you can query at runtime. That is the model for fix 4 and for the self-describing help (row 3). Malli was chosen for the Clojure proof of concept, which is telling.
- **ASN.1** has range and size constraints, and `OPTIONAL`/`DEFAULT` with extension markers. That is proof that constraints and defaults can be terse and still sit in the type.

## Ranked fixes, each sized for one Opus subagent

1. **Design proposal for interaction (impl) syntax and the manifest.** This is the living's newest ask, and nothing exists. The subagent writes a proposal: function-body grammar on protos, interactions that bind a type to a kind with bodies, and a manifest root for crate name, dependencies and ethos-to-ethos imports. It works the proposal through one real crate, orchestrate client.ethos plus its main.rs. Where: a report in the flow, and a scratch branch of ethos-zero with a parse-only prototype. Verified by: the prototype parses the worked example round-trip (sweet, canonical, File, text), and the result is presented to the psyche for a ruling.
2. **Bind the flow crates to ethos-zero.** Generate flow/crates/{signal-flow,meta-signal-flow} from their ethos, with a build.rs freshness assert. Resolve the `Restarted` drift. Where: /home/li/primary/flow. Verified by: `cargo test`, a hand-edit of the ethos that makes the build fail, and a datom round-trip test.
3. **Make rkyv close over recursion.** Emit rkyv 0.8 `omit_bounds` and `serialize_bounds`/`deserialize_bounds` attributes on the boxed recursive positions in the Signal root. Box only the positions that break a cycle. Where: ethos-zero src/generation.rs. Verified by: the tree-types fixture as a Signal archives and restores, and signal-aggregator's arena can then be replaced (a follow-up).
4. **Sized integers and bytes as intrinsics** (this needs a psyche ruling on names). Proposal plus implementation behind the ruling: unsigned and sized integers, `Bytes`, and a fixed `Array`. Update datom-codec to match. Verified by: fixtures compile, datom text round-trips at the width bounds, and chroma or signal-version-handover can drop its hand-written widths.
5. **Fix inline-name collisions.** Allocate unique derived names across the whole file, and refuse an authored name that captures one. Where: ethos-zero checking.rs/generation.rs. Verified by: the row 15 probe as a fixture that is compiled in tests/generated.rs.
6. **Compile every fixture and close generator holes.** Add the 8 fixtures that are not compiled to tests/generated.rs. Qualify every `Option`/`Result`. Refuse declared intrinsic names with a named error. Refuse lower-case type names and `S.{ Self }`. Verified by: `cargo test` and `nix flake check`, with a negative test for each refusal.
7. **Source-located errors.** Map a Conceptual error's protos path to the sweet-text line:column in the CLI reply, and add a `Check` query that validates without writing. Where: ethos-zero actualization.rs, main.rs and the ethos-zero.ethos contract. Verified by: CLI tests that assert the line and column for undeclared, duplicate and arity errors.
8. **Rule on the `Type` root and the empty Library sections.** Either implement `Type` (a head type plus a definitions bracket, generating a Library) with trailing empty sections omittable, or rewrite the three skills to parse. Where: the ethos-zero root enum; Curriculum skills. Verified by: every Type block in the skills extracted and generated in a test.
9. **Doc comments and the newtype-versus-alias rule.** Carry the `;` comment that precedes a declaration into `///`. Present the alias-or-newtype choice to the psyche (see Part 2) and implement the ruling. Verified by: fixtures showing the docs, and a compile-fail test showing whether `LockName` and `FlowId` can be interchanged.
10. **Reconnect or retire the dead contracts, and resync the docs.** Either make protos and datom-codec import their generated-contract (fixing the `Extent` width and field divergence) or delete those contracts. Retire or mark the orphaned spirit `.ethos` files. Update the ethos and datom skills (`Composing`, and naming that no longer claims `_Data` never collides), the ethos-zero README (the tuple line) and tree-sitter-ethos. Verified by: `grep` finds no `Compositional` derive in the skills, the protos/datom-codec builds use the contract, and the tree-sitter corpus parses every fixture.

## Sources

- ethos-zero: README.md, ethos-zero.ethos, fixtures/*.ethos, tests/{generated,freshness,cli,signal_without_datom}.rs, tests/generated/*.rs, git log. Binary probes in the subflow scratchpad: shadow, unitcollide, dupfield, badcase, kw, selfsz, cyc, imp, collision, Type root.
- datom-codec: src/composition.rs, crates/datom-codec-derive/src/lib.rs, generated-contract/. protos: protos.ethos, src/core.rs.
- signal-aggregator/ARCHITECTURE.md; signal-agent/build.rs:304; signal-ethos-zero/src/generated/signal.rs; tree-sitter-ethos/README.md.
- /home/li/primary/flow/crates/signal-flow/{ethos/signal.ethos,src/lib.rs}.
- Vision/{ethos,datom,protos,sema,signal,meaning}.md; flows/e51411/vision/ethos.md; flows/e51411/notion/stack.md; flows/752e0f/vision/{ethosNextGeneration,helpMenu}.md; flows/b81560/vision/*; flows/8e9e77/vision/single-field-structs.md; flows/9993b5/vision/*; flows/38de5b/log.md (09-25 witness: Type root does not parse).
- Two read subagents: a vision-ask extraction, and a survey of the 56 real `.ethos` files (lojix, chroma, clavifaber, horizon-rs, signal-5f4fea, signal-version-handover, signal-mind, meta-signal-*). Their claims were spot-checked: flow drift, protos `Extent`, the rkyv note, the u64 mapping, and the hand-written signal-ethos-zero file.
