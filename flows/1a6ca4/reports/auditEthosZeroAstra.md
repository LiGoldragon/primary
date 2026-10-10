# Audit of ethos-zero 4.0.0

**Verdict: not solid enough to generate consumers’ contracts generally now.** The repository’s gates pass, every fixture generates and compiles, and the ordinary generated contracts round-trip correctly. Nevertheless, small ethos inputs can terminate the CLI with a panic, accepted declarations can generate uncompilable Rust, fault locations can identify the wrong structure, and the public layer kinds do not meet the current vision. Consumer migration should wait for those defects to be closed and witnessed.

Audit by the Astra subflow of `FLOW_ID=1a6ca4`, harness `THREAD_ID=01a0718a-d624-79f2-be51-5af4a53d076c`, on 2026-09-05. No subflows dispatched. No repository source, fixture, test, manifest, or generated module changed; no commits. This requested report is the only artifact written under `FLOW_DIRECTORY`.

Audit bindings: `FLOW_DIRECTORY=/home/li/primary/flows/1a6ca4`; `Repository root=/git` from `SKILL_VARIABLES.md`; audit scratch `/tmp/ethos-zero-astra-EfNPnY`. Unless otherwise qualified, `src/...:line`, `tests/...:line`, and `fixtures/...:line` refer to `github.com/LiGoldragon/ethos-zero` beneath Repository root. `P/` means the sibling protos repository; `D/` means datom-codec; `Vision/`, `Intent/`, and `flows/` refer to primary.

The inspected main revisions were ethos-zero `dc54e332` (4.0.0), protos `205408679738d92d1182fe7c6f5c0eeb278ce318` (0.19.0), and datom-codec `cd43574d8ef61e4c18d768310f67079bf58b0835` (0.14.0). Cargo and flake pins agree. The ethos-zero working copy was empty above the requested commit. Before/after content hashes found no changes or new files in any of these three repositories, excluding VCS metadata and pre-existing build directories.

## Authority and method

The loaded spirit, behavior, psyche, psyche-acquisition, ethos, datom, protos, testing, and subflow skills were applied; flow-evidence was loaded for this report. The current distilled Vision takes precedence over the pasted skills’ older version triples, Library roots, maps, and directional vocabulary.

The written psyche was acquired before the implementation. `Vision/ethos.md`, `Vision/protos.md`, `Vision/datom.md`, `Vision/ethosMonolith.md`, and all three Intent files were read whole. The source indexes and raw corpus were searched; relevant ethos, kinds, capability, generation, layer, tuple, and matching records were read, including the later reversals of earlier wording. Selected expressions, kept verbatim and by level:

- **Spirit**, loaded skill: “Seek disconfirming evidence. Do not seed audits with suspected conclusions.”
- **Intent**, `Intent/mandatoryTraits.md:5`: “Every method call in our Rust code lives under a trait, because traits are the comprehension surface”.
- **Vision**, `flows/1a6ca4/vision/datom.md:7`: “rewrite it better and more anatomically and directly, where the logic is clear through the ontology of the trait system.” The original dictated request was also witnessed in the main thread’s transcript, line 6; it writes “I want Datum and Ethos 0 to be solid.” The raw vision marks its STT corrections.
- **Vision**, `flows/995a164e/vision/layerMatching.md`: “That is the only thing that is involved in obtaining that data. There's no constant. There's not gonna be a constant.” The later passage in that same file permits a possible associated constant on each kind; it does not restore a separate parallel roster.
- **Vision**, `flows/e996e8/vision/archive-ethos.md:9`: “I think I want to drop the version number altogether. datom doesnt have versions.” This was also witnessed in the e996e8 transcript, line 165.
- **Vision**, `flows/aa4c7747/vision/archive-tuples.md:7`: “tuple: no tuple in the code we design: if some parts require it (standard traits, dependencies), then we allow it at that contact point only”.

Every ethos-zero source file, fixture, and test—including every committed generated fixture module—was read whole. Cargo.toml, Cargo.lock, flake.nix, flake.lock, README, both root ethos files, the three check scripts, and .gitignore were read. Dependency source was read where needed to witness the actual pinned kinds, intrinsic interactions, situations, and positional reader; this is not a second whole-repository audit of those dependencies.

All implementation conclusions below are this subflow’s observations or explicitly labeled inferences. The earlier `reports/auditEthosZero.md` was opened only after independent findings and probes had been recorded in the scratch directory. Its claims are used only in the regression comparison. During late transcript acquisition a user-role search also surfaced injected task notifications; those relayed reports are excluded from psyche evidence and from the findings. The unavailable `transcript` executable was replaced with JSON filtering of human messages and source-line provenance; no transcript was read whole as prose.

## Observed gates and execution evidence

| Gate or witness | Observed result |
|---|---|
| `cargo fmt --check` | Exit 0. |
| `cargo clippy --locked --all-targets -- -D warnings` | Exit 0. |
| `RUSTDOCFLAGS=-Dwarnings cargo doc --locked`, also separately with `--no-deps` | Both exit 0, including full dependency documentation. |
| `cargo test --locked` | 67 passed: 7 CLI, 44 ethos, 3 freshness, 13 generated-contract tests. No library or binary unit tests or doc-tests. |
| `nix flake check --no-write-lock-file` | Exit 0. Log says “running 0 flake checks”; repeating with `--all-systems` also exits 0. To resolve what that establishes, all eight named check outputs were explicitly realized with `nix build --no-link`: build, test, fmt, clippy, doc, dependency-ethos, no-free-functions, no-inherent-methods. Exit 0, all eight output paths returned. No fresh builder execution is claimed. |
| All ten fixtures, generated through the CLI into scratch | All returned Generated; every output was byte-identical to its committed module. |
| Fresh outputs compiled in a scratch Cargo consumer using the exact git pins | All ten fixtures compiled, including processable-kinds, which the repository’s generated integration test does not import. No generated-source repair was needed. |
| Scratch round-trips | 16 tests passed: the repository’s 13 behavioral consumer tests pointed at freshly generated output, plus independent exact-value, exact-text, and exact-fault tests. The three new tests were each seen failing under deliberate corruption of scratch output; fresh output was restored and all 16 passed again. |
| CLI replies decoded through freshly generated `Response` | Arguments, Malformed, Unreadable, Faulty, Unwritable, Generated all decoded and textualized byte-for-byte. No-argument help equals the authored ethos and ends with a newline, as witnessed by the CLI gate. |
| Vision Rust examples | All seven Rust blocks match their corresponding generated declarations modulo whitespace, trailing commas, external qualification, and generated additions. Details below. |

Cargo gates were bounded by a 900-second timeout and 8 GiB address-space limit, with two build jobs and target artifacts in scratch. Compilation probes used 120-second/4 GiB bounds; individual CLI probes used 15-second/1 GiB bounds; scale probes used 10-second/512 MiB bounds, with core dumps disabled. Limits are inherited per-process address-space limits, not a claim about an aggregate cgroup. Nix clients were bounded; the check outputs resolved from cache, and no fresh builder execution was observed. No uncontrolled exhaustion was allowed to take down the harness.

The scratch consumer initially used `Option<Extent>` in an auditor-authored assertion; the pinned `Locus.extent: Extent` was read and that harness error corrected before the reported behavioral results. It is not a product finding.

## Compliance by vision statement

| Statement | Assessment and witnessed implementation |
|---|---|
| Ethos specifies types; datom supplies data (`Vision/ethos.md:5`, `Vision/datom.md:12`) | **Compliant on division of labor.** File declarations yield Rust through `Generating` (`src/generation.rs:625`); generated Datomic interactions walk declared positions (`src/datomization.rs:28`). Ethos reads protos structure, not a second datom text parser. |
| Interfaces and behavior form an ontology (`Vision/ethos.md:10`, `Intent/mandatoryTraits.md:5`) | **Substantially improved, partial.** The main types and kinds are explicit in `src/lib.rs:53` and `:372`; conception, checking, generation and ascent are trait interactions on their respective objects. Production free functions are limited to Rust’s `main` (`src/main.rs:136`), and no inherent impl was found in the complete source read. Shared-layer conformance remains deficient, F3. |
| Generated Rust is committed; freshness mechanism open (`Vision/ethos.md:19`) | **Compliant.** `src/fault.rs`, `src/contract.rs`, and all ten `tests/generated/*.rs` are committed generated products. `tests/freshness.rs:31` regenerates the two self-contracts and all fixtures; fresh CLI outputs matched too. |
| Non-repetition (`Vision/ethos.md:25`) | **Partial.** Positional fields and implicit Request/Response/Record remove repeated field names and associations. The extension that reuses constraint names as parameter references is ambiguous when repeated (`src/checking.rs:155`); `Pair<Sized Sized>.{ Sized Sized }` emits both fields as A and leaves B unused, F5. The vision does not settle how repeated equal bounds are referenced. |
| Self-description, CLI now and objects later (`Vision/ethos.md:30`) | **Compliant for this CLI’s ordinary operation; future object-wide mechanism unimplemented.** `src/main.rs:118` prints its authored contract; `:96` decodes its generated Request and `:131` textualizes Response. Panics escape that contract, F1. The library’s entire public declaration ontology is not exposed by the CLI’s operation-only Signal. |
| Ethos eventually authors everything (`Vision/ethos.md:39`) | **Horizon, not an assertion of present completion.** Rust behavior remains hand-authored; the actual bootstrap is demonstrated by self-generated contracts. No evidence here establishes the eventual full language. |
| A kind bears capabilities and emits a trait (`Vision/ethos.md:45`) | **Compliant for demonstrated forms.** `KindDeclaration`, `KindBody`, `Capability`, `Receiver`, `Signature` make the anatomy explicit (`src/lib.rs:202`); emitted traits are at `src/generation.rs:528`. |
| Qualifier names; legacy Rust names tolerated (`Vision/ethos.md:54`) | **Partial/decision.** Canonicalizable, Checkable, Named and Rooted are qualifiers. Generating, Tokening, Emitting and other participles are the flow’s naming choices; their acceptability is not conclusively ruled by the examples. Renamed imported kinds use explicit authored aliases, not a hidden conversion table. Uppercase associated constants are not enforced, F9. |
| Kind identity is name and constraints (`Vision/ethos.md:62`) | **Partial.** The demonstrated Processable identity emits two bounded Rust parameters. Duplicate detection and resolution identify a kind only by Name (`src/checking.rs:81`, `:254`, `:295`); two same-name heads with different constraints are refused, F8. Type-versus-kind checking exists, but imported identities lack metadata, F5. |
| One File, one module; no internal namespace (`Vision/ethos.md:95`) | **Compliant on file shape.** `File` has exactly Types/Kinds/Signal/Sema (`src/lib.rs:63`), with imports first. The CLI writes one stem-named `.rs` file (`src/main.rs:65`). Synthetic inline enum names may collide, F2. |
| Sweet form is mechanically converted before ethos conception (`Vision/ethos.md:95`) | **Compliant on observed inputs.** `src/canonicalization.rs:14` inserts braces after the root and adds a closer on its own line. Both forms, leading comments, root-line comments and trailing comments without a newline pass tests (`tests/ethos.rs:60`). It uses protos delineation to find the seam, then delineates the canonical text; ethos conception only sees the braced form. |
| No version in a file (`Vision/ethos.md:97`) | **Compliant.** All four roots read only their current sections (`src/conception.rs:277`); legacy Library/version input is refused (`tests/ethos.rs:526`). Manifest version 4.0.0 is separate. |
| Specialized Signal and Sema types have implied kinds (`Vision/ethos.md:99`) | **Partial.** Signal produces Request and Response; Sema produces Record (`src/generation.rs:642`, `:663`). They bear Datomic and the blanket Datom Incorporable path. There is no distinct query/response/storage kind assertion. The required domain kinds are not named in this vision; deciding Datomic is sufficient is unsupported. |
| Imports and intrinsics mean the same; foreign names fully qualified (`Vision/ethos.md:116`) | **Partial.** Shown imports emit correctly without `use` statements (`src/generation.rs:103`). Explicit intrinsic imports bypass intrinsic role/arity checks, F5; emitted implementation scaffolding uses capturable prelude names, F2. Qualified Rust source paths are an extra feature and grouped imports do not work for them, F9. |
| Struct, enum, alias and inline payload anatomy (`Vision/ethos.md:131`) | **Compliant for examples and fixtures.** Tuple structs, tuple variants, bare variants, nested enums, aliases and normal recursive forms all compile and round-trip. Struct and enum definitions are at `src/generation.rs:349`, `:401`, `:419`; aliases at `:459`. Some accepted forms fail, F2/F5. Aliases inherit Datomic through their target instead of creating duplicate impls. |
| No unnamed tuple except dependency contact points (`Vision/ethos.md:169`) | **Non-compliant internally.** The crate defines its own trait signatures with `Option<(&Head, Separator, &Protoform)>` (`src/conception.rs:48`) and `Vec<(Name, Path)>` (`src/checking.rs:226`); its own pending walk and kind decomposition also use unnamed tuples (`src/conception.rs:142`, `src/generation.rs:530`). These are internal ontology choices, not a standard trait requiring a tuple. |
| Simple and complex kinds; receivers; input/yield anatomy (`Vision/ethos.md:178`, `:190`, `:209`) | **Compliant on demonstrated shapes.** Three receivers and two signature forms are explicit (`src/conception.rs:592`, `:620`); four complex-kind sections are enforced (`:537`). Yield must hold one type (`:607`). Streamable emits `Self::Item` (`src/generation.rs:136`). Duplicate members and illegal declarations remain accepted, F5. |
| Associations assert a kind; interactions hand-authored (`Vision/ethos.md:232`) | **Compliant for the shown concrete association.** `src/generation.rs:577` emits assertions, not implementation bodies. Fresh Sink output compiles with hand-authored interactions and those capabilities run. The generic extension and implied domain associations remain decisions, F5/F8. |
| Canonical delimiter spacing (`Vision/ethos.md:257`) | **Compliant on accepted fixture and example text.** File textualization builds Protoform and calls the shared writer (`src/protosization.rs:263`). Processable round-trips its printed canonical ethos; angles remain tight while brackets inside them receive canonical spaces. |
| Protos owns universal structure; context gives meaning (`Vision/protos.md:5`, `:16`; `Intent/protosParsing.md:3`) | **Compliant at the character/structure boundary.** Ethos receives Protoform and interprets braces/brackets/heads by the expected declaration (`src/conception.rs:225`, `:462`, `:519`, `:620`). Import symbol splitting for `::` is dialect logic compensating for the pinned substrate’s bare-word representation, not a second whole character reader. |
| Five delimiters; maps/guillemets dropped (`Vision/protos.md:44`, `Vision/datom.md:149`) | **Compliant in the declared ethos grammar.** No map declaration, map intrinsic, guillemet section or old CAPACITY map form exists in the implementation read. Containers map to Vector/Option/Result; associated constants are bracketed declarations. |
| Text/Protoform/Concept/Corporate; kinds named by destination (`Vision/protos.md:56`) | **Non-compliant/partial, F3.** Protosizable and Textualizable are genuinely borne by File, and Actualizable by Potential<File>. Shared Conceivable is replaced by private Conceiving. Canonical does not bear its advertised Protosizable. Ethos has no separately exposed Incorporable corporate transition before generation. Generated values match pinned Datomic but do not bear shared Conceivable or Textualizable. |
| Descent may fault; ascent cannot; situations found/computed (`Vision/protos.md:27`, `:79`) | **Partial, F1/F3/F4/F6.** Passes exist and ordinary faults have extents. File’s Protosizable ascends to text and reparses it (`src/lib.rs:546`), instead of directly yielding the constructed form with computed situation. Public constructors do not enforce the “checked whole” premise used by infallible generation. Panics and misplaced extents refute blanket solidity claims. |
| Datom’s positional, schema-driven reverse projection (`Vision/datom.md:61`) | **Compliant for witnessed generated contracts.** Generated position reads delegate to Sited/Positional/Headed/Carrying, and writing emits matching Struct/Variant/Word concepts (`src/datomization.rs:28`, `:64`). Tuple payload arity and nested fault paths survive; bare variant names and `Observed.Locks.[]` round-trip. Deep recursive incorporation is not robust, F6. |
| Datom CLI is shaped by an input enum and output enum (`Vision/datom.md:39`) | **Compliant for ordinary paths, F1 for escaping panics.** Generated Request/Response are used directly. Exactly one argument is accepted; extra arguments, malformed input, I/O failure and schema failure have typed responses. |
| Datom strings, scalars and Meaning are position-dependent (`Vision/datom.md:85`, `:168`) | **Delegated correctly on witnessed forms.** The generated code has no scalar parser. Independent Text `A:Z`, Integer `-42`, fixture Decimal/Boolean/Meaning and nested containers round-trip through the pinned codec. This audit does not assert every possible scalar or Meaning value works. Full future Meaning annotation structure is explicitly deferred by the vision. |
| Datom migration/nexus, cached translation, future inline data (`Vision/datom.md:26`, `:19`) | **Outside this crate’s present responsibility.** No repository-wide migration or future datom nexus is established here. The library name/pin is datom-codec, as the current raw vision requests. |
| Monolith goes straight to Rust, brings components into production without cutting corners (`Vision/ethosMonolith.md:5`, `:27`) | **Partial.** A working direct generator and self-generated contract exist. Readiness is refuted by the concrete failures below. |
| Monolith itself is a Nexus; readiness witnessed (`Vision/ethosMonolith.md:21`, `:42`) | **Nexus shape absent.** Cargo.toml declares a library and one finite CLI; `src/main.rs:136` handles one invocation. No Nexus service is implemented here. Whether the newly authorized stack bootstrap deliberately postpones that remains a main-flow decision to show the living, not evidence that this clause was satisfied. |

## Ranked non-compliances and fixes wanted

**F1 — High: accepted source can panic; the CLI then emits no Response.**

Observed under the individual CLI bounds:

| Ethos input | Observed result and source |
|---|---|
| `Types [] [ Self.{ Text } ] []` | Exit 101; `src/generation.rs:689` expects a Rust file, but Self is not a declaration identifier. The reader explicitly accepts Self as any Name (`src/conception.rs:185`). |
| `Types [] [ r#type.{ Text } ] []` | Exit 101; `Ident::new` rejects the accepted raw identifier at `src/generation.rs:37`. |
| `Kinds [] [ K<Sized ...>.[ read.[ Text ] ] ]`, with 27 explicit Sized constraints | Exit 101; the 27th generated parameter name is `[` (`src/generation.rs:73`). |
| `Types [] [ Ghost<[]>.{ Text } ] []` | Exit 101; the empty constraint produces invalid generated bounds (`src/generation.rs:175`, `:689`). |

Each produces empty stdout and an unstructured panic on stderr. These observations refute both “the file having been checked whole” (`src/lib.rs:408`) and the unconditional CLI contract claim (`src/main.rs:5`). Name and all declaration structs also have public unchecked fields (`src/lib.rs:53` onward), so a successful parser is not the sole way to obtain a File.

**Wanted:** every accepted file must support its advertised operations; unsupported/invalid source must produce a typed, correctly situated fault, and every CLI outcome must remain in its generated response contract. The checked-value premise must be true at the public boundary. Support for raw identifiers and arbitrary parameter counts should be coherent, not accidental panic cases.

**F2 — High: ordinary valid declarations produce uncompilable Rust.**

Observed Generated followed by a separate Cargo compilation failure:

- `Types [] [ Scores.{ Vector<Decimal> } ] []` and `Types [] [ Score.{ protos:Decimal } ] []`: E0277, `f64: Eq` not satisfied. The direct `Score.{ Decimal }` control compiles. `Deriving` reuses the boxing reachability walk (`src/generation.rs:296`); that walk stops at Vector (`:227`) and ignores a sourced Decimal’s identity. This explains these particular witnessed failures; it is not a proof that these are its only errors.
- `Types [] [ X.[ A.[ V ] ] XA.{ Text } ] []`: duplicate synthetic XA, E0428 and conflicting implementations. Nested identity is concatenated without a collision check (`src/generation.rs:340`); declared-name collection sees only authored top-level identities (`src/checking.rs:244`).
- `Types [] [ Box.{ Integer } Tree.[ Stop Next.Tree ] ] []` and `Types [] [ Result.{ Integer } A.{ Text } ] []`: emitted Box/Result scaffolding binds to declared local types, causing E0107/E0053/E0599. Generated code uses bare Box, Result, Ok and Vec (`src/generation.rs:57`, `:322`; `src/datomization.rs:78`, `:183`). The absence of `use` statements does not make these names immune to capture.
- `Types [] [ A.{ Self } ] []`: E0072, infinite-size recursive A. Self is emitted literally (`src/generation.rs:60`); the boxing walk compares the reference’s name with A, so it does not recognize this self-reference (`:220`).

**Wanted:** valid compositions of supported types must generate compiling Rust; inferred capabilities must reflect actual type capabilities through every supported container and qualification; generated names and implementation machinery must preserve authored identities without collision; recursive self-reference must have a consistent finite Rust representation.

**F3 — High: the shared layer ontology is broken at the reader and corporate ascent.**

The pinned substrate defines `Conceivable<C>` returning `Situated<C>` and `Incorporable<T>` taking a Situation (`P/src/kinds.rs:47`, `:55`). Ethos instead declares private `Conceiving<C>` returning bare C (`src/conception.rs:15`), uses it throughout, and manually recovers fault extents later (`src/actualization.rs:79`). Compile probes fail for `Delineation: protos::Conceivable<File>` and `Canonical: protos::Protosizable`. The latter contradicts the layer table in `src/lib.rs:11`; README also advertises shared Conceivable on the reader.

Generated Record fails bounds for both `protos::Conceivable<Datom>` and `protos::Textualizable`. It implements only `datom_codec::Datomic` (`src/datomization.rs:181`), whose separate `conceive` and `textualize` capabilities do not confer the shared kinds. **This is also the pinned intrinsics’ shape**, not a generator-specific divergence: `D/src/kinds.rs:11` and `D/src/containers.rs:25`, `:69` use the same contract. Conversely, `Datom: protos::Incorporable<Record>` does work through the codec blanket (`D/src/site.rs:225`); the typed round-trips witness it. File genuinely implements shared Protosizable and Textualizable, but its public Protosizable path prints and re-reads the concept (`src/lib.rs:546`) even though the direct form already exists (`src/protosization.rs:60`).

**Inference:** conception/checking/File currently collapse the concept and the corporate validation boundary. There is no separate exposed ethos Incorporable transition from which Rust is yielded, despite the raw statement “Ethos would also have a Corporal layer, which is the layer that would then be used to yield the generated rust” (`flows/62022e8f/vision/archive-layers.md`). A different name on the same unchecked value would not establish that boundary.

**Wanted:** the reader and generated consumers must participate in the actual shared protos kinds, with the promised layer transitions and situation preservation. The pinned codec and generator need one coherent corporate contract. Ascent should project the existing anatomy and compute its situation without a text-read detour. Public documentation must describe kinds the types actually bear.

**F4 — High: fault paths are incompatible with the substrate and extents can point at unrelated text.**

Ethos documents headed body as child 0 (`src/lib.rs:21`), while the pinned shared path convention is head 0/body 1 and qualified arguments below the head (`P/src/kinds.rs:71`). Datom also uses body 1 (`D/src/site.rs:181`). Ethos’s translator only recognizes a headed body and enclosure children (`src/actualization.rs:23`); it cannot descend into head constraints or bare qualified-head arguments. Conception/checking nevertheless number those arguments as though they were ordinary children (`src/conception.rs:394`, `:434`; `src/checking.rs:405`, `:507`).

Observed source slices selected by returned extents:

| Input | Fault | Extent selects |
|---|---|---|
| `Types [] [ A.{ Vector<Bogus> } ] []` | Undeclared.Bogus | `Vector<Bogus>`, not Bogus |
| `Kinds [] [ K<Bogus>.[ read.[ Text ] ] ]` | Undeclared.Bogus | `[ read.[ Text ] ]` |
| `Kinds [] [ K<Sized Bogus>.[ read.[ Text ] ] ]` | Undeclared.Bogus | the entire K declaration |
| `Kinds [] [ K.{ [] [ Item<Bogus> ] [] [] } ]` | Undeclared.Bogus | `Item<Bogus>` |

The simple `Record.{ Text Bogus }` control does identify Bogus correctly. Structural Fault’s Pathed interaction always returns `[]` (`src/lib.rs:424`); structural extent is carried, but there is no nested structural path. Generated datom faults, by contrast, retain both nested path and correct extent in witnessed consumer cases.

**Wanted:** a single shared path meaning for every layer, and every reported fault must identify the actual offending structure in the original source, including head constraints, arguments, and sweet-form offsets. A plausible nonempty path and a nearby extent are insufficient.

**F5 — High: checking admits locally decidable Rust errors and conflates imported intrinsics.**

Observed Generated, then Rust rejection for duplicate capability names, duplicate associated types, duplicate constants (E0428); local type argument-count mismatch (E0107); a self-superkind cycle (E0391); and an alias cycle through a generic alias (E0391). Examples are preserved in `generation-results.json`. `Checkable for KindDeclaration` checks member references but never checks member-name distinctness (`src/checking.rs:638`). Local type/kind resolutions carry no arity (`:488`); alias cycle traversal can follow the alias body without substituting its applied arguments (`:529`).

Explicit import changes intrinsic validation: `Types [] [ A.{ Text<Integer> } ] []` is rejected as Arity, but adding `[ protos:Text ]` returns Generated and Rust then fails. Imported resolution accepts whichever role the position requests and gives no arity (`src/checking.rs:490`). This contradicts the explicit-import/intrinsic equivalence in `Vision/ethos.md:117`.

`Pair<Sized Sized>.{ Sized Sized }` emits `Pair<A: Sized, B: Sized>(A, A)` and fails for unused B. Only a single, unsourced, argument-free constraint can name a parameter, and the first equal name wins (`src/checking.rs:155`). This generic-type extension is not fully specified by the current declaration examples.

**Wanted:** malformed declarations whose defects are known from the file must be rejected as situated ethos faults, including duplicate members, local arity, and cycles. Intrinsic meaning must be stable with or without an explicit import. Constraint references must unambiguously select the intended parameter; unsupported cases must not silently select another one.

**F6 — High for consumers accepting untrusted recursive data: generated incorporation can abort the process.**

Freshly compiled fixture Tree was fed `Maybe.Some.` repeated 10,000 times followed by `Leaf.1`, under 512 MiB/10 seconds. It aborted with stack overflow. An instrumented run printed “before actualize” and never “after actualize”; the failure is in descent, not inferred from a later destructor. Depths 100, 500 and 2,000 completed text → typed value → identical text and drop.

The generated typed arm calls `Carrying::body` (`src/datomization.rs:109`), whose codec implementation calls T::incorporate (`D/src/site.rs:181`); Option and Box recurse similarly (`D/src/containers.rs:69`, `:108`). This is a witnessed composition failure of the generated consumer and pinned codec. It is not evidence that protos delineation itself overflowed, nor a measured universal threshold.

**Wanted:** recursive consumer input must either complete or receive a defined typed refusal within an explicit supported resource envelope; it must not terminate the consuming service. Limits, if part of that envelope, must be a visible contract decision.

**F7 — Medium: flat declaration graphs escape the structural depth guard and become expensive.**

A valid chain of 100 aliases generated in approximately 0.024 seconds; chains of 1,000, 5,000 and 15,000 each hit the 10-second timeout in the debug-built CLI. These are shallow ethos structures, so `DEPTH_LIMIT=128` (`src/conception.rs:133`) does not bound graph traversal. Duplicate scanning is pairwise (`src/checking.rs:295`); per-alias traversal and name resolution repeatedly walk declarations (`:529`, `:572`). **Inference:** the repeated walks explain the strong scaling concern; no asymptotic complexity proof, release-build throughput or eventual completion time is claimed.

**Wanted:** a declared supported scale for real consumer schemas, with predictable completion or a typed resource refusal for both structural nesting and declaration-graph complexity. The current syntactic limit alone is not such a guarantee.

**F8 — Medium, requiring the living’s attention: identity and file examples contain unresolved contract choices.**

The distinct heads K<Clonable> and K<Sendable>, with valid std imports, are rejected as Duplicate.K. The implementation keys kind identity by bare name, while `Vision/ethos.md:67` explicitly says differing constraints make two kinds. Rust also rejects two same-name trait declarations in one module; the wanted mapping cannot be resolved by silently dropping either half of the vision. The report treats the mismatch as observed and its resolution as open.

Both literal Types files at `Vision/ethos.md:103` and `:108` are rejected with Arity.{ 3 2 }. They omit the association section that the document’s prose requires at `:237`. The fixture adds `[]`. **Wanted:** one explicit, self-consistent file contract and examples, and an explicit account of kind identity across ethos and Rust. No silent insertion, reinterpretation, or Rust naming policy is ruled by this audit.

**F9 — Medium/low: subsidiary syntax and ontology mismatches.**

- Associated constant `capacity.Integer` is accepted and emits lowercase `const capacity`; the vision specifies uppercase (`Vision/ethos.md:211`). Wanted: the declared naming rule must be reflected consistently in accepted ethos.
- The README’s Rust-prefix source extension is incomplete: `Types [ std::clone:[ Clonable.Clone ] ] [] []` faults Name.“”; the single-import form in processable-kinds works. Source splitting at `src/conception.rs:325` only handles the bare run up to the colon, not the following grouped body. Wanted: coherent single/grouped imports for every supported source form, with a truthful diagnostic otherwise.
- Internal unnamed tuples conflict with the current tuple rule, as listed in the compliance table. Wanted: internal compound concepts expressed as the domain’s named types; standard-library contact tuples remain the explicitly allowed exception.
- The crate is a finite CLI/library rather than the Nexus in `Vision/ethosMonolith.md:21`. Wanted: either that specified runtime shape or an explicit current bootstrap deferral, visible to the living. This architecture gap is separate from the immediately actionable generator failures.

## Fixture and vision-example accounting

All ten fixtures generated, matched their committed Rust, and compiled unmodified against the pins: capability-kinds, entry-sema, multi-types, orchestrate, placed-types, processable-kinds, record-types, sink-associations, streamable-kind, tree-types. Companions imported from `super` were supplied in the scratch consumer exactly as the fixture contracts require. Sink’s interaction bodies were hand-authored. No serialized values are claimed for a kinds-only file: those outputs are traits; their compilation and callable companions are the relevant witness. Concrete fixture structs/enums/aliases were exercised through datom in the 16 tests.

Every ethos code block in Vision/ethos.md was accounted for:

| Vision location | Generation and Rust comparison |
|---|---|
| Identity, lines 76–88 | Literal ellipses are placeholders and fault, as expected for non-source. Substituting explicit Clone/Send/Serialize imports and an empty capability list generates the shown bounded trait, with public visibility and full foreign paths. The Processable fixture’s extra `process` capability is separately generated and compiled. |
| Sweet and canonical files, lines 101–111 | Both literal files fault for missing third section; the completed three-section file generates the shown Record shape. This is reported as the document tension F8, not hidden by fixture completion. |
| Import section, lines 121–123 | Wrapped in an otherwise empty Types file, generates successfully. There is no Rust item to emit for an unused import. The shown datomic spelling is the older library name; it is left literal in this example probe, not asserted to be a current dependency. |
| Type section, lines 139–149 | The four shown declarations match individually. Generated derives and Datomic impls appear between them; comparing the whole four-line block as one contiguous string would be the wrong oracle. |
| Request variants, lines 158–166 | Placed in Signal with minimal supporting type declarations and a Done response. Generated Request has exactly Lock(LockRequest), Release(LockId), Observe(ObserveSelection). |
| Summarizable, lines 181–187 | Exact trait/signature shape. |
| Fillable, lines 196–206 | Exact receivers, parameter, and yield shapes; imported SinkError becomes `super::SinkError`. |
| Streamable, lines 213–224 | Exact superkind, associated type, constant and `Option<Self::Item>`; companion kinds fully qualified. |
| Association, lines 239–249 | Exact concrete assertions after full qualification; compilation requires and received the hand-authored Sink interactions. |

Generated additions beyond the example snippets are `pub` on the identity example, derive attributes, `#![allow(dead_code)]`, and Datomic interactions. Datomic generation is required by the loaded ethos/datom instructions; the blanket derive and lint policies are implementation decisions, not statements found in these snippets.

## Decisions to show the living

The following are observed implementation choices whose authorization was not established by the inspected vision. Their existence is witnessed; the original author’s private rationale is unknown unless stated below. They are surfaced because they alter the comprehension surface or the language’s usable contract.

1. **Private Conceiving, body-0 paths, and the combined File boundary.** These choices replace shared kinds and situations just where the vision asks for a common ontology. Their effects are F3/F4. Matching the pinned API through another local trait is not evidence of vision compliance.
2. **Only Datomic implied by Signal/Sema.** The generated Request, Response and Record have no differentiated domain kinds. The vision names the intention but does not supply the respective kind definitions. The finite CLI and concrete Sema `{ record positions }` layout similarly settle bootstrap choices that the living may want to inspect.
3. **Constrained types use the kind name as the Rust parameter reference.** `Placed<Sized>` works, but repeated bounds do not select independent parameters. The extension reaches beyond the shown type-declaration grammar; it needs a coherent meaning rather than accidental name lookup.
4. **Bare-name uniqueness for kinds.** It silently selects one side of the identity/Rust tension. The literal wording and the actual duplicate rejection are both recorded in F8.
5. **Generated type identity and capabilities.** Concatenated nested-enum names, automatic boxing of every position that reaches its owner, derives on all declarations, and suppression of dead_code affect public Rust APIs and allowed consumers. Some are reasonable Rust contact choices, but F2 shows why the derive and naming policies matter. Neither a general boxed-owner policy nor an Eq policy is authorized by the displayed Rust snippets.
6. **128 levels of ethos structural nesting.** This is an explicit implementation constant, absent from the vision’s grammar; a shallow alias graph is still unconstrained. No claim is made that this number is intrinsically right or wrong. Its existence and consequences should be visible.
7. **Rust-source qualification and import renaming.** `std::clone:Clonable.Clone` is an authored syntax extension. It lets the Processable example match Rust without a hidden conversion table, but it is not specified in Vision/ethos.md, and grouped qualified-source imports fail. The living should see what syntax has been added on flow authority.
8. **Participial kind names and unnamed internal tuples.** The former remains a naming question; the latter conflicts with the explicit tuple rule. They should not be presented together as already approved ontology.

Audit-only decisions: used `/tmp` for builds, probes and the consumer; supplied explicitly missing contexts for section-only examples while separately running literal files; treated the Types example/prose disagreement as unresolved rather than changing the language; compared prior findings only after forming this audit’s own findings. No design change or repository edit was made to settle any of these questions.

## Regression comparison with the earlier audit

The earlier report audits 2.0.0 at a2e8eafcd45c. Its findings are historical claims; the following status is based on this audit’s current code and runs, not an assumption that each intermediate revision was tested.

| Earlier finding | Current witnessed status |
|---|---|
| Trailing comment consumes inserted closer | Fixed: closer is appended on its own line; regression test passes. |
| Inline structs acquire synthetic wrapper structs; recursive structs/Option fail | Fixed for those examples: direct tuple variants and finite boxed recursion compile and round-trip. Self spelling, collisions and deep data still fail as separately identified. |
| Streamable lacks Self::Item | Fixed; fresh output compiles and a bearer’s `next` runs. |
| Bare names accepted as self-aliases; simple duplicates/undeclared names ignored; empty signal omitted | Fixed for those cases; typed reader faults are tested. Kind member duplicates and generic cycles remain beyond that coverage. |
| Constrained superkinds/associations rejected; intrinsic association unresolved | Parsing and ordinary resolution support the tested current forms; no blanket correctness claim for all generic associations. |
| Faults all empty; generated faults lose indices | Improved substantially: ordinary ethos positions have path/extent and generated datom nested faults are correct. Qualified-head paths/extents remain wrong; ethos’s convention now conflicts with its pinned substrate. |
| Hand-parsed CLI, malformed reply strings, no self-generation | Fixed for ordinary operation: actual generated Request/Response, six reply variants round-trip, two generated self-contracts fresh. Four independently found source classes can still panic outside the contract. |
| 81 free functions and thin trait facades | Replaced by object-specific trait interactions and pass modules. This is a real improvement, distinct from the shared-kind regression. |
| fmt/doc/Nix failures and stale architecture documents | Gates now pass; stale ARCHITECTURE/CLAUDE/UPGRADES files and unused ETHOS_* flake variables are absent. Some new API documentation claims are wrong, F3. |
| Shared Conceivable on reader and generated corporate values existed | **Regression relative to the old report’s recorded API.** Current reader uses private Conceiving; generated corporations implement only Datomic. Current compile probes directly fail the shared bounds. |
| Dependency ethos declarations fail to generate | The current durable dependency-ethos check is green. It checks reading/generation, not equality to the dependency’s entire handwritten Rust API or compilation of every generated dependency declaration; those stronger claims are not made. |

## Inferences and unknowns

The readiness verdict is this subflow’s inference from witnessed failures: a generator that reports success for common unbuildable contracts, panics on small input, and mislocates faults is not a solid foundation for an autonomous consumer migration. Passing fixtures prove a useful functioning subset, and the repaired self-contract is substantial progress; neither establishes the untested general contract.

Unknowns: the living’s intended resolution of same-name/different-constraint identity, omitted Types associations in the literal example, exact Signal/Sema domain kinds, a current authorized Nexus deferral, full constrained-type/association syntax, the intended resource envelope, and the authorial reasons behind private layer kinds. The audit does not invent those answers. Release-build scale and the precise stack-overflow threshold were not measured. No claim of complete input-space coverage or whole-dependency correctness is made.

The practical acceptance condition is observable: supported ethos must generate compiling contracts with the intended ontology; unsupported source must return situated typed faults; generated data paths must preserve shared kinds and fault locations and respect a defined resource envelope. Those conditions are not met at the audited revision.

## Sources

- Authored authority: primary `Vision/ethos.md` whole (259 lines), `Vision/protos.md` whole (91), `Vision/datom.md` whole (212), `Vision/ethosMonolith.md` whole (43); `Intent/data.md`, `Intent/mandatoryTraits.md`, `Intent/protosParsing.md`; loaded skill text and the flow-evidence skill.
- Raw authority read includes `flows/1a6ca4/vision/datom.md`; `flows/995a164e/vision/{rust,kinds,layerMatching,concept,contexts,explodedForm,archive-ethosTypes}.md`; `flows/6329f1/vision/{archive-ethos,archive-protos}.md`; `flows/e996e8/vision/{archive-ethos,archive-protos}.md`; `flows/ad19b1/vision/{archive-ethos,archive-kinds,archive-protos,archive-designPractice}.md`; `flows/e8c4cc61/vision/{archive-ethosFileAnatomy,archive-kinds}.md`; `flows/62022e8f/vision/{archive-ethosTypes,archive-kinds,archive-layers,archive-concept,archive-passes}.md`; `flows/b675f3d9/vision/{archive-kinds,archive-structuralParsing,ethosMonolith}.md`; `flows/aa4c7747/vision/{ethos,archive-ethosMonolith,archive-ethosTraitSyntax,archive-interactions,archive-tuples}.md`; `flows/2b34fafa/vision/{archive-ethosSourceFiles,archive-ethosNamespaces,archive-traitsAsCapabilities}.md`; `flows/5abf3be8/vision/sectionsExistToConferTraits.md`; `flows/1c282d/vision/archive-protosizable.md`; `flows/04db2fd2/vision/{archive-kinds,archive-multiPass,archive-directionAsymmetry}.md`; `flows/4decf7/vision/archive-kinds.md`; `flows/e4a40e/vision/archive-kinds.md`; the source-index-guided legacy records in the scratch acquisition corpus. That corpus indexes additional records; indexing is not claimed as reading all of them whole.
- Transcript provenance: `/home/li/.claude/projects/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354.jsonl:6`; `e996e87c-55f5-4bdb-8915-9feb1bc0d925.jsonl:165` in the same directory; selected typed-message hits retained in scratch. Injected notifications and subflow prompts are excluded as living testimony.
- Code: the audited ethos-zero revision’s eleven source files, four integration-test entry files, ten generated fixture modules, ten ethos fixtures, both root ethos declarations, check scripts and manifests, all read whole. Pinned protos kinds and actualization/situation contract; pinned datom-codec kinds, containers, anatomy, protosization, conception boundary, and relevant site/reader interactions. Exact locations accompany findings.
- Historical comparison only: `FLOW_DIRECTORY/reports/auditEthosZero.md`, opened after independent findings were formed. No other earlier report was intentionally opened for findings.
- Reproducible scratch evidence: `before.json`, `gates.sh`, `gates.txt`, `fmt.log`, `clippy.log`, `doc.log`, `doc-full.log`, `test.log`, `nix.log`, `nix-all.log`, `nix-explicit.log`; `generated/`, `inputs/`, `probe-generated/`; `generation-results.json`, `vision-generation-results.json`, `vision-rust-comparison.json`, `compile-probes.py`, `compile-results.json`, individual `*-compile.log`; `consumer/Cargo.toml`, `consumer/src/`, `consumer/tests/`, `consumer-final-tests.log`, `sensitivity-control.log`; `cli-responses.json`, `cli-roundtrips.log`; `scale-results.json`, `runtime-phases.log`; `independent-findings.txt` and acquisition files. All beneath audit scratch; these are local execution evidence, not committed regression tests.
