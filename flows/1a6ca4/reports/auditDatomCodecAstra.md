# Datom-codec and protos: independent Astra audit

**Verdict: datom-codec 0.14.0 is not yet solid enough for general consumer adoption.** The ordinary examples and durable gates pass, and the core tree machinery has improved substantially. However, ordinary supported types still lose data or emit text they cannot read back. The universal kind contracts also remain incomplete. This verdict is this audit subflow's inference from the observations below, not a statement attributed to the living.

## Scope, provenance and method

FLOW_ID: `1a6ca4`. FLOW_DIRECTORY: `/home/li/primary/flows/1a6ca4`. THREAD_ID, obtained from the running harness's `CODEX_THREAD_ID`: `01a0718a-ce5d-7de1-86ff-22296a9257ce`. Audit date: 2026-09-05. No subflows dispatched.

Path variables used throughout this report:

| Variable | Value / origin |
|---|---|
| Primary | `/home/li/primary`, supplied workspace |
| Repository root | `/git`, from `SKILL_VARIABLES.md` |
| D | `Repository root/github.com/LiGoldragon/datom-codec` |
| P | `Repository root/github.com/LiGoldragon/protos` |
| Scratch | `/tmp/audit-datom-astra-01a0718a`, this audit's temporary work |

The requested checkouts were clean and at the requested main heads: D **0.14.0**, `cd43574d8ef61e4c18d768310f67079bf58b0835`; P **0.19.0**, `205408679738d92d1182fe7c6f5c0eeb278ce318`. D pins that exact P revision. All 22 Rust source files and all eight Rust test files, including `tests/common/mod.rs`, were read whole: **4,710 lines**. Both READMEs, all four ethos files, manifests, lock files, flake definitions, ignore files and toolchain files were also read. The inventory is in Sources.

Order: loaded instructions and variables; acquired distilled Intent/Vision and raw records; searched the living's transcript; read sources/tests; ran gates and independent probes; recorded independent findings in `Scratch/independent-findings.txt`; only then opened `FLOW_DIRECTORY/reports/auditProtosDatomic2.md` for regression comparison. The transcript helper automatically included preceding main-flow status snippets; their conclusions were not used as evidence. No earlier audit report seeded the findings.

The only requested workspace write is this report. Scratch contains the probe crate, scripts and run outputs. Repository content hashes taken before and after the runs matched; no library source, tests, manifests or lock files were edited. No commits or pushes were made, as explicitly instructed.

“Observed” below means code read or execution witnessed by this thread. Interpretations, severity and desired fixes are this thread's judgments. Historical report results are attributed as historical claims unless re-witnessed here. An audit cannot establish absence of every possible defect; the probes below delimit the claims made.

## Acquired authority

These quotations preserve the authority rather than replacing it with a new distillation.

**Spirit**, the supplied spirit skill: “Seek disconfirming evidence. Do not seed audits with suspected conclusions.” Also: “Backward compatibility is never a design variable.”

**Intent**, `Primary/Intent/mandatoryTraits.md:5`: “Every method call in our Rust code lives under a trait, because traits are the comprehension surface”. `Primary/Intent/protosParsing.md:3`: “only the current context gives shapes their meaning”; lines 8–10: “text lands in typed values, and typed values project back into the same text.” `Intent/data.md` places types, kinds and implementations on the same data plane; no audited mechanism requires an exception to that intent.

**Vision**, `Primary/Vision/datom.md:61`: “Schema-driven and positional: the reader walks the expected type, writing is the exact reverse projection”. `Vision/protos.md:56`: “Potential and actualize go universally, layer to layer”. `Vision/ethos.md:14`: “Behavior falls under traits, which creates an ontology in code.”

**Raw vision**, main-flow transcript `1a6ca4f9-e0fa-4f2c-bd6f-a40651590354`, physical line 6: “rewrite it better and more anatomically and directly, where the logic is clear through the ontology of the trait system.” The same words are carried at `flows/1a6ca4/vision/datom.md:7`. The library rename is the living's ruling at transcript line 796, carried in that raw record at line 15; it is not an audit-invented name.

Other decisive raw statements acquired:

- `flows/ad19b1/vision/archive-protos.md:9`: “ok lets drop that delimiter and concept entirely from protos and its dialects.”
- `flows/04db2fd2/vision/archive-delimiters.md:11`: “it's content-opaque, so all characters it contains are ignored, until the closing unbalanced closing parenthesis.”
- `flows/6329f1/vision/archive-protos.md:16`: “both the text and the concept are protosizable”; “the protoform are conceivable” appears with the corporate side in the same statement. Lines 24 and 32 explicitly describe incorporate on text and a potential Protoform yielding a Protoform.
- `flows/995a164e/vision/layerMatching.md:18`: “I just mean the trait implementations, right? That is the only thing that is involved in obtaining that data.”
- `flows/aa4c7747/vision/archive-tuples.md:7`: “no tuple in the code we design”; exceptions are dependency contact points.

Current Vision governs over the supplied stale map, Library/Signal-root, version-triple, Corporal, Embodied and MissingBody descriptions. Full Meaning annotation semantics and the exact symbol-qualification rule are explicitly open; this audit does not invent them.

## Compliance by statement

C = compliant in the inspected implementation and named witnesses; NC = concrete non-compliance; partial = both; open = not determined or outside this library's present duty. F numbers refer to ranked findings below.

| Vision / intent statement | Status | Code and execution witness |
|---|---|---|
| Datom Name; Repository and migration | C for these repos | `D/Cargo.toml:2`, `D/src/lib.rs:20`; requested rename and revision present. Whole-estate migration and future Nexus are outside scope. |
| Datom Nature: pure typed data; generation belongs to Ethos | C for responsibility | `D/src/anatomy.rs:7`, `D/src/site.rs:224`, `P/src/actualization.rs:58`; no Rust-generation engine in D. “Most advanced” is an aspiration, not a measurable gate. |
| Datom interface shape: data-bearing variant chains; empty observation | C for library support | `D/src/containers.rs:69`, `D/tests/vision.rs:96`, `:104`, `:109`; `Observed.Locks.[]`, `Success`, Lock/Release passed. No CLI is owed by this library. |
| Datom De/serialization: expected type and exact reverse projection | Partial / NC | `D/src/site.rs:63`, `:157` enforce shape/arity; typed examples pass. F1, F2 and F3 disprove the universal reverse guarantee. |
| Datom relation to Ethos: common structural substrate | C for boundary | `D/src/conception.rs:79` receives Protoform; character reader/writer are `P/src/delineation.rs:315` and `P/src/textualization.rs:166`. Scalar lexical validation in D interprets data, not structural delimiters. |
| Datom syntax: braces, brackets, variant head, bare unit variant, no Datom root | C on covered shapes | `D/src/anatomy.rs:7`, `D/src/site.rs:90`, `D/tests/vision.rs:15`; all 14 typed vision tests pass. |
| Datom syntax: Text is contextual; punctuation may be bare | Partial / NC | `D/src/site.rs:109`, `:121`, `D/src/containers.rs:14`; standalone text works, payload composition fails F1. |
| Datom syntax: curly-quoted strings opaque | C inside the representable Text domain | `P/src/opaque.rs:17`; quoted delimiters/comments pass. U+201D exclusion is a consequential policy, discussed separately. |
| Datom syntax: canonical ASCII integer, no plus/leading zero | C | `D/src/worded.rs:31`, `D/tests/reading.rs:79`; bounds and invalid lexemes tested. The additional `-0` refusal is recorded below. |
| Datom syntax: one semicolon comment, canonical brace/bracket spacing | C | `P/src/delineation.rs:153`, `P/src/textualization.rs:16`, `P/tests/delineation.rs:254`, `P/tests/textualization.rs:37`. |
| Datom Map; Protos Structure: maps/guillemets dropped | C | `P/src/anatomy.rs:65`, `D/src/anatomy.rs:7`; three structural enclosures, no map variant/implementation. Guillemets now classify as ordinary content; removed delimiters need not be rejected glyphs. |
| Datom Meaning: separate from Text; provisional plain payload; balanced parentheses | Partial / NC | `D/src/anatomy.rs:22`, `D/src/containers.rs:39`; Text/Meaning separation and balanced escaping pass. F4 violates opacity. Future annotations are deferred as ruled. |
| Protos What it is / knows: anatomy without dialect interpretation | C | `P/src/anatomy.rs:79`, `:89`; Head, enclosure and boundary are structural; meaning is assigned in D. |
| Protos Structure: recursive headed/enclosed/opaque/bare forms; mixed separators and angle constraints | C for parsing | `P/src/delineation.rs:162`, `:262`, `P/tests/delineation.rs:67`, `:166`, `:188`; chained and qualified cases pass. F6 concerns projected structure. |
| Protos Delineation / Direction: extents beside objects, found inbound/computed outbound | Partial / NC | `P/src/anatomy.rs:37`, `P/src/textualization.rs:149`, `D/tests/situated.rs:37`; inbound paths and core writer situations pass. F6 exposes divergent projected anatomy. |
| Protos Layers: middle-layer capabilities borne from both directions | NC | `P/src/kinds.rs:49`, `D/src/kinds.rs:11`; compile witnesses in F5. Same-named Datomic methods do not satisfy the protos kinds. |
| Protos Layers: Potential at every layer; incorporate chains from text | NC | `P/src/actualization.rs:49`, `D/src/site.rs:225`; only the complete corporate descent is implemented. F5. |
| Protos Layers: Sized, Corporate terminology; no extra layer | C | `D/src/kinds.rs:11`, `P/src/lib.rs:8`; no Embodied/Corporal kind or extra delineated-text layer. |
| Protos Multi-pass | C for separation | Character survey → concept → corporate in `P/src/actualization.rs:58`; corporate → concept → structural writer in `D/src/kinds.rs:17`, `D/src/protosization.rs:125`. No ascent reparse. |
| Protos Canonical print | C on exercised forms; one wording tension | `P/src/textualization.rs:16`, `:30`; braces/brackets spaced, quotes content-preserving, balanced parentheses preserved. Angles remain tight, matching Vision's examples despite its broadly worded spacing sentence. |
| Ethos Kind / Naming; mandatory trait ontology | Partial | All authored production functions are in trait implementations; state-bearing Reader, Writer, Walk, Build, Site are explicit. `P/src/glyph.rs:111` walks enums via capabilities. Public layer ontology still fails F5; whether all private `-ing` names meet qualifier naming is open. |
| Ethos Identity | C in representable declarations inspected | `D/datom-codec-kinds.ethos:9` uses Datomic constraints; `P/protos-kinds.ethos:13` uses Sized. Superkinds, associated types/constants and capabilities are separated. Rust's named generic parameters are its required representation. |
| Ethos Declaration / Generation: faithful schema and resulting Rust | Partial / NC | Separate Types/Kinds, no file versions, imports first and four-section complex kinds are present. F9 records concrete schema/runtime drift and the missing generation witness. Full generator behavior is outside this audit. |
| Ethos no designed tuples | NC | `P/src/delineation.rs:227` creates the custom `(opened, children, qualifying)` tuple. F10. Dependency tuples such as `split_once` results are allowed contact points. |
| Testing: bounded meaningful witnesses, durable Nix gates | C for execution; incomplete coverage | Both flakes expose cargo tests; scale children carry caps/timeouts. New failed behavioral probes establish holes. Source grep guards are static checks, not behavioral proof. |

## Ranked non-compliances and solidity findings

High means an existing supported use can lose a value, fail its promised round trip, or abort a consumer process. Moderate means a public contract, architectural requirement or meaningful extension surface is incomplete. IDs are stable evidence identifiers; ordering below is by severity. Fixes state the wanted outcome, not an implementation recipe.

### F2 — High: a legitimately parsed problem can silently lose data when written

**Observed:** `Potential::<Problem>::from("Value.“a;b”").actualize()` yields `Problem::Value("a;b")`. Its text is `Value.a;b`. Reading that yields `Problem::Value("a")`, silently discarding the suffix as a comment. An empty payload writes `Value.` and cannot be read. Whitespace and structural payloads also fail. This is reachable by reading legitimate datom; it does not require fabricating malformed internal values.

**Code:** `D/src/faults.rs:122` reads UnknownVariant/Value payloads through Text; `:140` and `:141` write their unrestricted String contents as `Datom::Word`. `P/src/delineation.rs:153` correctly applies the comment rule. `D/src/anatomy.rs:83` and `:85` admit unrestricted String values. Witness: `Scratch/probe/tests/contract.rs`, `parsed_problem_preserves_its_content` failed with `Ok(Value("a"))` versus `Ok(Value("a;b"))`; `Scratch/roundtrips-0.log` has the wider cases.

**Inference / requirement:** this violates exact reverse projection (`Vision/datom.md:61`) and makes faults themselves unreliable data. The written/read paths assign different representations to the same payload. **Fix wanted:** every representable problem/fault payload preserves all its text on ascent and descent; content cannot turn into comments, siblings or structural syntax. The representable domain must be consistent in both directions.

### F1 — High: ordinary text fails when carried directly by a variant

**Observed:** `Some(Text::try_from(".").unwrap())` writes `Some..`, then reads as `UnknownVariant("Some..")`. The same happens with `.a`, `a.`, `a..b`, `:` and nested Option/Result payloads. All those strings round-trip standalone. An exhaustive small alphabet test covered **5,220** strings of length 0–3: **0** standalone Text failures, **192** Option<Text> failures. Controls `Ada`, `name:first`, `a.b`, quoted whitespace, empty Text and quoted comments pass in the same nesting positions.

**Code:** `D/src/containers.rs:14`, `:30`, `:82`, `:100` compose a variant with a bare text word; `P/src/delineation.rs:180` through `:210` treats the entire maximal run as a single bare word whenever a separator segment is empty. `D/src/site.rs:90` then has no variant boundary to recover. Witnesses: `optional_punctuation_preserves_legal_text` fails; `Scratch/exhaustive-text-0.log`; `Scratch/roundtrips-0.log`.

**Inference / requirement:** the schema-driven positional promise and bare-text rule (`Vision/datom.md:61`, `:105`) do not compose across a head/body boundary. This affects normal Option and Result consumers, not merely arbitrary hand-built Protoforms. **Fix wanted:** supported Text values retain their exact contents in every declared payload position; composition with variant heads preserves the boundary and honors the ruled contextual bare-text syntax.

### F3 — High: the Datomic Decimal type contains values with no readable output

**Observed:** `f64::INFINITY.textualize()` is `inf.0`; negative infinity becomes `-inf.0`; NaN becomes `NaN.0`. All are refused by the same Decimal reader. The reader itself rejects nonfinite values. Finite values passed the durable property test, five explicit bitwise edge controls, and **9,993** additional deterministic finite bit-pattern round trips, including subnormal values and signed zero.

**Code:** `P/src/anatomy.rs:9` aliases Decimal to unrestricted `f64`; `D/src/worded.rs:47` accepts only finite decimal text, `:60` writes every f64, and `:234` implements Datomic for that whole type. `D/tests/reading.rs:243` deliberately excludes nonfinite values. Witness: `every_inhabitant_of_the_datomic_decimal_has_readable_text` failed; `Scratch/roundtrips-0.log`, `Scratch/survey.log`.

**Inference / requirement:** “a corporate value is already whole” and infallible valid ascent (`Vision/protos.md:29`) are not guaranteed by the type. This is not a demand to admit infinity into finite decimal notation. **Fix wanted:** the Datomic decimal's actual inhabitant set matches its representable domain; no value admitted as a complete Datomic Decimal produces text its reader rejects.

### F7 — High for recursive/untrusted consumers: depth safety does not cover all exposed operations

**Observed:** bounded debug probes successfully parsed 20,000 nested brackets, then aborted with stack overflow when comparing two resulting Delineations or formatting one with Debug. At 100,000 brackets, optimized **Debug still aborted**; optimized equality passed. A normal recursive consumer enum `End | Next(Box<Self>)`, implemented using the public Variant/Carrying and Box paths, passed at depth 100 but aborted during incorporation at 20,000 in debug and **100,000 in release** (500,003 input bytes). Its release textualization at 100,000 passed; this audit does not claim that path failed. The probe intentionally forgets successful recursive values so consumer-owned Drop cannot confound the descent observation.

**Code:** recursive derives at `P/src/anatomy.rs:38`, `:47`, `:80`, `:90`, `:104`; analogous Datom derives at `D/src/anatomy.rs:6`. The recursive callback path is `D/src/site.rs:181` → `T::incorporate`, through `D/src/containers.rs:108`. `D/README.md:91` claims incorporation recurses only as far as the corporate type nests; a recursive type has no finite nesting limit. Scratch's consumer implementation is at `probe/src/main.rs:13`.

**Distinction:** the library's structural reader, conception, structural writer and iterative destructors passed their 100,000-node tests. The recursive consumer callback is authored in the probe, not hidden recursion newly discovered in the protos reader. Exposed derived traits themselves provide the separate library-only abort witness.

**Inference / requirement:** a consumer that logs accepted structure or reads a recursively defined contract cannot infer safety from the core scale gate. This contradicts an unrestricted “every walk” claim and weakens fallible descent. **Fix wanted:** a stated, enforceable depth/resource contract encompassing accepted trees, public diagnostic/comparison operations and supported recursive corporate types; admitted work either completes safely or returns a truthful refusal, with limits explicit to consumers. Do not label an otherwise closed enclosure “Unclosed” to represent a resource refusal.

### F4 — Moderate: Meaning's opaque context inherits the curly-string restriction

**Observed:** `(a “b” c)` faults `Stray(CurlyQuotes)` at byte extent 7–10. `(a ” b)` also faults. `(a “ b)` succeeds. Balanced parentheses and escaped unbalanced parentheses work. The reader is distinguishing an outer-context glyph in a context whose stated delimiter is parentheses.

**Code:** `P/src/opaque.rs:40` saves the curly quote closer as `stray`; `:65` faults on it. `P/src/text.rs:10` excludes U+201D from Text, which is also Meaning's payload (`D/src/anatomy.rs:26`). `P/tests/delineation.rs:365` asserts this refusal; the Meaning property test at `P/tests/textualization.rs:198` excludes the counterexample character. Witness: `parenthesized_context_carries_a_closing_quote` failed.

**Inference / requirement:** this conflicts with `Intent/protosParsing.md:3`, `Vision/protos.md:44`, `Vision/datom.md:178` and the raw opacity statement cited above. **Fix wanted:** parenthesized content obeys its own balance/escape rules and can carry the other delimiters, including U+201D. A plain-string representability choice must not silently redefine Meaning.

### F5 — Moderate, central vision failure: the public kinds do not embody the layer table

**Observed compile failures:** `i64: Textualizable`; `i64: Conceivable<Datom>`; `Text: Protosizable` as an actual generic bound; `protos::Potential::<Protoform>::actualize`; `datom_codec::Potential::<Datom>::actualize`; `String: Incorporable<i64>`. The compile probe reports E0277/E0599. Corporate `Potential::<i64>` succeeds in ordinary tests, so this is not a broken Cargo environment. A Text method call can reach `str::protosize` through Deref; that does not make Text bear Protosizable.

**Code:** `D/src/kinds.rs:11` adds unrelated `Datomic::conceive` and `Datomic::textualize` methods. `P/src/kinds.rs:49` defines Conceivable only as a situated fallible direction, while `D/src/conception.rs:193` and `:212` implement it on structural bearers. `P/src/actualization.rs:49` unconditionally requires the complete text → concept → corporate chain. Only Datom bears the provided generic Incorporable (`D/src/site.rs:225`). `P/src/delineation.rs:346` and `:361` implement Protosizable for str/String. Witness: `Scratch/probe/examples/layer_contracts.rs`, `Scratch/layer-contracts.log`.

**Inference / requirement:** the table at `Vision/protos.md:56` and `:68` is stronger than matching method names. Generic consumers cannot express that table against these types; the layer-specific Potential is also absent. **Fix wanted:** the ruled capabilities are actual kinds borne at the stated layers in both directions; Potential actualizes to its declared layer, and the upper-layer incorporation chain is usable. Intermediate projection preserves its infallible direction contract.

### F6 — Moderate: projected Protoform and Situation disagree with the text's delineation

**Observed:** `3.25f64.conceive().protosize()` yields `Bare(Symbol("3.25"))`, extent 0–4, **no children**. Reading `3.25` yields `Headed(Symbol("3"), Period, Bare(Symbol("25")))` with children at 0–1 and 2–4. Both render the same text but expose different structural anatomy and paths. This uses an ordinary Decimal, not an invalid custom Word.

**Code:** `D/src/protosization.rs:62` puts an arbitrary word in a Symbol; `:118` situates that constructed form. `P/src/textualization.rs:132` writes Symbol verbatim and records a leaf. `P/src/anatomy.rs:14` documents Symbol as separator-free but aliases it to String. Witness: `protosization_yields_the_structure_and_situation_of_its_text` failed in `Scratch/protosization-contract.log`.

Publicly constructible malformed Symbols also print empty text, multiple siblings or comments (`Scratch/proto-values-0.log`). The ordinary Decimal case establishes that merely documenting a caller precondition would not close the current library behavior.

**Inference / requirement:** the structural survey promised by `Vision/protos.md:48` and computed extents at `:31` must describe the output actually read by protos. **Fix wanted:** projecting any supported value produces the same structural anatomy and child situations as delineating its emitted text; Symbol's invariant and bare text's distinct role are represented consistently.

### F8 — Moderate extension-surface defect: reading beyond Positions panics

**Observed:** `"[]"` → concept → `Site.elements()` succeeds; `Positional::<i64>::position(&mut positions)` immediately panics at `site.rs:162`, exit 101. There is no documented panic precondition on that Result-returning method. `position` increments its index before indexing, so catching the panic leaves the cursor past the end, and `remaining` can underflow (`:177`). The latter consequence is code-derived, not separately run.

**Code:** `D/src/site.rs:157`; public contract `D/src/kinds.rs:67`. Witness: `Scratch/positions-0.log`. Built-in Vec checks remaining before reading; fixed-arity generated-style readers check arity. Thus this is an API misuse/extension hazard, not a claim that current built-in Vec accepts input that triggers this panic.

**Fix wanted:** exhaustion has a defined, recoverable public behavior and leaves cursor state coherent; consumers can rely on the stated reader contract.

### F9 — Moderate vision debt: the ethos self-descriptions are not faithful contracts of this Rust

**Observed:** `P/protos-kinds.ethos:6` declares Glyphing's yield as Text, while `P/src/kinds.rs:8` returns `char`. The declared Textualizable/Texted yields at ethos lines 10 and 18 are Text; Rust yields `String` / `&str` at `kinds.rs:30`, `:96`. These are materially different since Text is now a validated type. `P/protos.ethos:6` declares Symbol as Text, while Rust aliases String (`anatomy.rs:15`). `D/datom-codec.ethos:11` declares problem string payloads as Text, while Rust uses unrestricted String (`D/src/anatomy.rs:83`). The source-derived failure F2 shows that difference matters.

The two Types files explicitly omit generic types/borrowed handles because the declaration language lacks a form (`P/protos.ethos:2`, `D/datom-codec.ethos:2`). That explicit omission is an honest limitation. However, even included kinds lack full bearer associations: Glyphing, Delimiting, Serial and Classifying implementations in `P/src/glyph.rs:20`, `:30`, `:68`, `:180` are not listed in the Types associations at `P/protos.ethos:20`. The generated-Rust/freshness relationship is not checked by either flake or test suite. No ethos generator was run in this audit, so this is not a claim that a particular current generator rejects these files.

**Inference / requirement:** the named schema is an approximation, whereas `Vision/ethos.md:19`, `:29` and its Associations section require an inspectable declaration and resulting Rust relationship. **Fix wanted:** self-descriptions accurately identify the public types, capabilities and associations that exist, with unsupported representations explicit and an executable witness of the declared/generated contract. Do not label handwritten-shaped fixtures (`D/tests/common/mod.rs:1`) a generation witness.

### F10 — Low severity, definite vision mismatch: a custom tuple hides a state transfer

**Observed:** `P/src/delineation.rs:227` extracts `(opened, children, qualifying)` from its own Frame, with the same custom tuple constructed at `:233`. This tuple is designed by the parser; no external API requires it. Standard-library tuples consumed by `split_once` or iteration are different, permitted contact points.

**Requirement:** `Vision/ethos.md:169` and `flows/aa4c7747/vision/archive-tuples.md:7`. **Fix wanted:** this state has the named anatomy required for our own data, rather than an ad hoc tuple.

## Gates and adversarial evidence

All executions that could consume significant resources were bounded. Direct Cargo gates used **3 GiB RLIMIT_AS**, one build job, **240-second timeout** with a five-second kill grace and core dumps disabled; build output went under Scratch. Probe builds/checks used the same memory cap with 120-second timeouts. Standalone adversarial processes used **512 MiB address space**, **8 MiB stack**, **20-second timeout**, two-second kill grace, and core dumps disabled. A SIGABRT in these children is an observed failure of the tested operation, not a harness crash.

Host toolchain observed: cargo **1.96.0**, rustc **1.96.0**, x86_64 Linux. Both repositories declare `rust-version = 1.85` and `rust-toolchain.toml` pins 1.85.0; direct host runs did not use that pin. This audit does not certify the minimum supported Rust version from those runs.

| Gate | P result | D result |
|---|---|---|
| `cargo fmt --check` | pass, 0.05 s | pass, 0.06 s |
| `cargo clippy --locked --all-targets -- -D warnings` | pass, 7.44 s | pass, 7.55 s |
| `RUSTDOCFLAGS='-D warnings' cargo doc --locked --no-deps` | pass, 0.30 s | pass, 0.34 s |
| `cargo test --locked` | pass, 11.59 s | pass, 12.57 s |
| `nix flake check --no-update-lock-file --option max-jobs 0 --option builders ''` | pass, 2.33 s | pass, 9.11 s |

The Nix client had the same memory/time bounds. Disabling builders and setting max-jobs to zero prevented uncapped daemon builds: both logs say **“running 0 flake checks... all checks passed!”** after evaluating the nine check derivations. These are cached Nix successes, not nine newly executed builds. By the testing skill, successful infrastructure results stand; they are not represented here as fresh local executions. The D flake explicitly reports that non-host systems were omitted. Direct Cargo tests were freshly executed. `doc --no-deps` checks both audited crates' own documentation independently; cached Nix doc checks provide the repository's durable doc gate.

P passed **28 ordinary tests**, plus six scale modes at 1,000, 10,000 and 100,000 nodes. D passed **39 ordinary tests**, plus five scale modes at those sizes. Each scale child also has its own roughly 2 GB cap and 120-second timeout (`P/tests/scale.rs:84`, `D/tests/scale.rs:75`). At 100,000, observed P peaks ranged **22,560–35,916 kB** and D peaks **29,076–52,724 kB**. Those cases provide good evidence that the formerly quadratic core situation representation is now linear over the tested sizes; they do not prove arbitrary consumer operations safe.

Additional observations:

| Probe | Observation |
|---|---|
| Five initial behavioral contract assertions | Four failed as expected from the vision contracts (F1–F4); finite-decimal control passed. These were seen failing, not merely proposed. |
| Structural projection assertion | Failed (F6): same text, different Protoform/Situation. |
| Layer-contract compilation | Seven diagnostic errors across six requested uses; concrete missing bounds, not a tool failure. |
| Text enumeration, 17-glyph alphabet, lengths 0–3 | 5,220 values; 192 failures only after Option composition. |
| Deterministic structural survey | 50,000 candidate strings; 3,678 accepted; every accepted structure remained structurally equal after canonical print/read. Invalid-input errors were allowed. |
| Deterministic decimal survey | 9,993 finite f64 values round-tripped bitwise. |
| Depth controls / adversaries | Small cases passed; failure and successful counterexamples are separated in F7. |
| Empty Positions | Result-returning read panicked, exit 101. |

The five intended-contract assertion failures establish behavior that needs changing. Exit zero from the general survey/probe driver merely means it finished reporting observations; its printed `equal=false` cases are failures of the library round-trip contract.

Reproduction lives in `Scratch/gates.py`, `Scratch/run-probes.py`, and `Scratch/probe/`. The deliberately non-compiling example is `examples/layer_contracts.rs`; select that example explicitly when reproducing it, rather than confusing its expected failure with the passing library gate. Raw outputs named in findings remain in Scratch. These are temporary audit witnesses; durable regression tests still need to be added to the library's existing Nix-exposed test surface as fixes land.

## Decisions the living would want to see

These are choices visible in the audited code. **Their historical authorship and approval are unknown unless explicitly named below.** “On a flow's authority” must not be inferred as a proven fact about the author's intention merely from missing provenance. No implementation rewrite report was consulted for this section.

| Visible choice | Authority / assessment and reason to surface it |
|---|---|
| Library named datom-codec | Living-ruled, main transcript line 796; compliant. Distinct from the still-correct kind name Datomic. |
| Text excludes every U+201D at construction | `P/src/text.rs:10`; explicit typed refusal now, preferable to emitting broken quoted text. No living approval of this representable-domain restriction was found in the acquired material. It prevents ordinary prose with closing curly quotes, and its extension into Meaning causes F4. The plain-string syntax currently has no stated escape for its own closer: this needs an explicit design resolution, not an invented escaping rule from the auditor. |
| Symbol is unrestricted String; syntax-bearing Word projects to Symbol | `P/src/anatomy.rs:15`, `D/src/protosization.rs:62`. Exact symbol qualification is open, so a particular allowed-character grammar is not imposed here. Nonetheless the implemented invariant already contradicts its documented separator-free role and produces F6. |
| Runs with empty separator segments become one bare word; adjacency becomes siblings | `P/src/delineation.rs:180`, tests `P/tests/delineation.rs:128`, `:147`. Legal bare punctuation is supported at root, a defensible reading of current datom syntax. F1 shows the choice does not compose; `a.{ 1 }.b` and `a<b>c` sibling semantics remain a visible convention without a ruling found here. MissingBody/MissingHead are not demanded back by this audit. |
| Non-dot chains collapse to one Word | `D/src/conception.rs:93`. Useful for contextual colon/exclamation strings; their interior situation children are discarded during conception. A concept leaf's lack of those children is distinguishable from F6, which promises an actual Protoform survey on ascent. |
| Decimal is binary64; finite, mandatory dot, no exponent; signed integer `-0` refused | `P/src/anatomy.rs:6`, `:9`, `D/src/worded.rs:34`, `:50`. Point-mandatory finite decimal behavior is in the supplied skill, but a full numeric policy is absent from current distilled Datom Vision. Binary64 rounding/underflow and fixed i64 width are consequential representation choices; the finite domain is not enforced on values (F3). `-0` refusal is an additional normalization choice, not ranked as a proven vision contradiction. |
| Situation is a parallel tree; head child 0, body child 1; absent part yields NOWHERE | `P/src/anatomy.rs:37`, `P/src/kinds.rs:76`, `P/src/situation.rs:7`. The parallel tree is a strong match to separate extents and the observed linear memory. Returning extent 0–0 for a missing child avoids panics but can hide a caller's mismatched Situation/structure; whether that fallback is the intended public contract is open. |
| No depth limit; safety claimed from iterative core walks | Core safety is well supported by the measured scale cases, but recursive corporate callbacks and exposed derives remain outside it (F7). Consumers need that boundary made explicit before treating any accepted text as safe to process. |
| Datomic duplicates universal capability names | `D/src/kinds.rs:11`. It makes simple calls ergonomic but defeats the declared generic ontology (F5). Same spelling is not the same kind. |
| Generic/borrowed ethos declarations omitted; glyphs rendered as Text | Explicit comments in both Types files disclose a bootstrap limitation. Approximating already expressible contracts is separate debt (F9); downstream readers should not mistake these files for exact generated signatures. |
| Private kinds named with `-ing`; a state-bearing Reader/Writer drives the walk | Unlike earlier ZST wrappers, the nouns now carry actual text, offsets, frames, paths or output. The ontology is inspectable. The naming preference needs the living's judgment; I do not declare every participial qualifier invalid. The remaining custom tuple is definite F10. |

Audit decisions, authorized by the brief: kept both repositories untouched; used the main-flow-reserved unique report path; ran cached-only Nix to prevent uncapped daemon builds; kept the minimum-Rust-version and cross-platform claims open; did not reopen Meaning's postponed annotation design. These choices preserve a concrete audit without taking implementation policy decisions away from the living.

## Regression comparison, read after independent findings

The previous report audited **P 0.18.0 / datomic 0.12.0**, not these commits. Its fourteen numbered remaining items are historical claims. Current status below comes from this thread's source reads and executions, not from a rewrite's assertion of closure.

| Previous item(s) | Current evidence / status |
|---|---|
| 1: quadratic situation memory | **Closed in exercised cases.** Parallel Situation nodes, no full path per node; 100,000-scale modes now tens of MB. `P/src/anatomy.rs:37`, `D/src/conception.rs:35`, scale outputs. |
| 2: corporate faults unsituated | **Closed for tested containers.** `D/tests/situated.rs:46`, `:58`, `:98` assert exact paths/extents through actualize, including Person and Struct/Vector/Option/Result/Box/Variant. |
| 3: headed/enclosed/opaque/qualified extents wrong | **Closed in reader/core-writer witnesses.** `P/tests/delineation.rs:90`, `:105`, `:120`, `:188`, `P/tests/textualization.rs:97`, `:163`. F6 is a distinct projected-word discrepancy. |
| 4: ascent reparses, computes wrong spans, can panic on quote | **Reparse removed; core writer computes situations.** `P/src/textualization.rs:149`, `D/src/protosization.rs:118`. F6 prevents declaring every projected situation correct. |
| 5: recursive core conception/textualization/drop/clone | **Core walks/drop fixed in scale witnesses.** No Clone derive on deep Protoform/Datom; qualified children are shed too (`P/src/dropping.rs:11`). Broader depth safety still incomplete, F7. |
| 6: missing universal layer bearers | **Still open**, F5. D's Potential alias makes corporate use convenient, but does not supply all layers. The old Datom identity-incorporation implementation is gone. |
| 7: U+201D restriction only a comment | **Typed construction refusal added** (`P/src/text.rs:8`). The policy's authority is unknown; its application to opaque Meaning is a present violation, F4. |
| 8: balanced Meaning pairs always escaped | **Closed.** `P/src/textualization.rs:35`, `P/tests/textualization.rs:129`, typed Note/Standup witnesses. |
| 9: ZST behavior, variant rosters, closure-fed scalar macro | **Substantially closed.** State-bearing machinery, `Serial` enum traversal, `Worded` default capabilities and plain impls; no production closure-fed macro/free function/inherent impl. This is an actual anatomical improvement. |
| 10: ethos files | **Partly closed.** Four-section complex kinds, separate roots, no versions, missing generic forms explicitly disclosed. Faithfulness remains F9; current generator acceptance not re-tested. |
| 11: missing/deleted vision examples | **Closed.** `D/tests/vision.rs` supplies all named present examples, including Person, exact Scores, Note, Remark, Standup and the nested observation. |
| 12: fabricated datoms, dead Separator fault, false depth Unclosed | **Closed in inspected paths.** `D/src/conception.rs:96` returns Found/Problem faults; dead variant and parser depth limit are gone. Existing malformed delimiter tests pass. |
| 13: adjacency without whitespace | **Explicitly tested convention, ruling still open.** `P/tests/delineation.rs:147`. No basis to call the mere sibling choice a proven non-compliance. |
| 14: ownership restriction, redundant text copying, unused dependency, repeated glyph literals | **Main defects removed.** Delineation can be destructured; actualize borrows stored text; proptest is used; glyph/comment/escape definitions have their homes. This does not imply every allocation is necessary or every source guard is exhaustive. |

Newly witnessed F1/F2 failures are not established as historical regressions: the old report did not test these payload combinations. F4 is a newly witnessed consequence of enforcing the quote restriction. No claim is made about precisely which intervening commit introduced any of them.

## Observations, inferences and unknowns

**Observations:** all ten requested gate invocations returned zero; core scale cases have linear-looking memory; exact ordinary faults and vision examples pass; the independent contract assertions, compilation failures, data loss and bounded stack aborts above occurred. Source comments that claim more than those observations have not been promoted to verified facts.

**Inferences:** the revised module and state anatomy is clearer, and the core memory/situation rewrite deserves to stand. Whole-value correctness still needs work at representation composition, numeric inhabitant boundaries, public kind ownership and the remaining recursive operations. Those are localized, evidenced requirements; this audit does not infer that another indiscriminate rewrite is wanted.

**Unknowns:** the living's preferred resolution for a curly-string closing quote; exact Symbol grammar; blanket versus explicit kind implementations as an implementation choice; `-ing` naming preference; precise numeric semantics beyond existing syntax; resource-budget ownership for recursive consumers; whether the source's ethos approximations have an approved bootstrap exemption. Current ethos-zero behavior, consumers' production input limits, non-Linux tests and Rust 1.85 compatibility were not independently established. No security advisory or exploit outside these isolated process failures is claimed.

The blocking adoption evidence is already present in standard Option<Text>, Problem and Decimal values. Consumers restricted to the passing examples can function today, but **general adoption should wait for those representation failures and the agreed depth/kind contracts to be resolved and witnessed through the durable gates**. Existing green gates alone do not justify the unrestricted “solid” claim.

## Sources

- Supplied brief and complete skill blocks: subflow, spirit, behavior, psyche, psyche-acquisition, datom, protos, ethos, testing. Locally read: `Primary/NON_MANAGEMENT_AGENTS.md`, `Primary/SKILL_VARIABLES.md`, `.agents/skills/{flow-evidence,edit-coordination,vocabulary,correction,transcript-search}/SKILL.md`. The explicit no-edit/no-commit scope overrides generic repository commit instructions.
- `Primary/Vision/{datom,protos,ethos}.md`, their source catalogs, and every file under `Primary/Intent/` (`data.md`, `mandatoryTraits.md`, `protosParsing.md`). All authority references in the matrix are to the versions read during this audit.
- Selected raw records acquired across `Primary/flows/*/vision/` and `vision-raw/`: source-catalog records for early schema/datamigration (01a02a34, 01a035d3, 01a03d6e, 01a03eda, 01a04339); anatomy/meaning/delimiters/kinds (04db2fd2, 06196cc7, 1c282d, 2b34fafa, 2ef42163, 4decf7, 5abf3be8, 62022e8f); current layers/identity/rulings (6329f1, 6863ef19, 995a164e, a5587095, aa4c7747, ad19b1, b675f3d9, e4a40e, e8c4cc61, e996e8); specifically named raw paths and verbatim quotations above carry the deciding statements. Broad search results alone were not treated as acquired content.
- Living transcript: `Primary`'s main-flow Claude transcript, `/home/li/.claude/projects/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354.jsonl`, typed records at physical lines 6 and 796, accessed through `/git/github.com/LiGoldragon/transcript/transcript.py` because `transcript` was absent from PATH. The current audit thread ID above is the harness evidence provenance, not a new flow identity.
- P at `205408679738d92d1182fe7c6f5c0eeb278ce318`: whole `src/{actualization,anatomy,delineation,dropping,glyph,kinds,lib,opaque,run,situation,text,textualization}.rs`; whole `tests/{delineation,scale,textualization}.rs`; `protos.ethos`, `protos-kinds.ethos`, README, Cargo.toml/Cargo.lock, flake.nix/flake.lock, rust-toolchain.toml, .gitignore.
- D at `cd43574d8ef61e4c18d768310f67079bf58b0835`: whole `src/{anatomy,conception,containers,dropping,faults,kinds,lib,protosization,site,worded}.rs`; whole `tests/{reading,scale,situated,vision}.rs` and `tests/common/mod.rs`; datom-codec.ethos, datom-codec-kinds.ethos, README, Cargo.toml/Cargo.lock, flake.nix/flake.lock, rust-toolchain.toml, .gitignore.
- Independent witnesses by this thread: `Scratch/probe/src/main.rs`, `probe/tests/contract.rs`, `probe/examples/{layer_contracts,survey}.rs`, `gates.py`, `run-probes.py`; `gates.jsonl`, `probes.jsonl`, `*-{fmt,clippy,doc,test,nix}.log`, `roundtrips-0.log`, `exhaustive-text-0.log`, `proto-values-0.log`, `positions-0.log`, depth-mode logs including release runs, `contract-tests.log`, `protosization-contract.log`, `layer-contracts.log`, `survey.log`, `before.json`, `after.json`, `independent-findings.txt`. Scratch paths are temporary, not committed deliverables.
- `FLOW_DIRECTORY/reports/auditProtosDatomic2.md`, read only after independent findings; used solely for the regression comparison, with its old executions remaining attributed to that audit.
