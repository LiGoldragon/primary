# Witness report — the protos/datom/ethos estate, 2026-09-13

All jj/git reads were read-only; nothing was edited or committed. Scratch: `/tmp/claude-1001`.

---

## 1. Repository survey

Command: `jj log -n 3` in each repo (`/git/github.com/LiGoldragon/<name>`). Status labels come from each repo's own `AGENTS.md` "Protos estate status" section, added by commit `docs: mark Protos estate status` (2026-08-13).

| repo | bookmark / head | last commit | version | state |
|---|---|---|---|---|
| **protos** | `main` `1febca7836bf` | 2026-09-12 "Give Error, Problem and ReaderBudget a Hash" | 0.31.0 | **alive** — the only character reader/writer |
| **datom-codec** (`datom` is a symlink to it) | `main` `09e2a9d52bf7` | 2026-09-12 "Give the public data types a Hash" | 0.31.0 | **alive** — datomic layer + derive |
| **ethos-zero** | `main` `4bf73cae8d4f` | 2026-09-12 "Write the generated derive list on one line" | 10.0.0 | **alive** — schema reader + Rust generator |
| **orchestrate** | `main` `9070cbb87178` | 2026-09-12 | 0.35.0 | **alive** — 3 crates: nexus, ordinary client, meta client |
| **nexus** | `main` `c495f2acbfff` | 2026-09-12 | 0.5.0 | **alive** — lifecycle ontology; depends on *none* of protos/datom/ethos |
| **signal** | `main` `66e7b1537066` | 2026-09-12 | 7.0.0 | **alive** — framing/exchange; generates from `ethos/signal.ethos` |
| **signal-orchestrate** | `main` `e7221190ed4c` | 2026-09-11 (working copy `6d686a78dc87`, 09-12) | 4.0.0 | **alive** — the ordinary wire contract |
| **signal-ethos-zero** | `main*` `42df8e3c6489` | 2026-09-06 | 0.2.0 | **superseded dialect, still building** — see below |
| **sema** | `main` `4fdc61267fc6` | 2026-08-13 | — | `Stack: correct-new destination / Status: component-associated, adoption unresolved` (`sema/AGENTS.md`). Not depended on by orchestrate (which uses `sema-engine`). |
| **protos-engine** | `main` `7a1bfd191dce` | 2026-08-13 | — | `Stack: incorrect-new / frozen reference / integration-conformance orchestration`. No new code accepted. |
| **ethos-engine** | `main` `3a80a3ec6a16` | 2026-08-13 | — | `incorrect-new / frozen reference / central-storage daemon embryo` |
| **core-ethos** | `main` `818620982ff9` | 2026-08-13 | — | `incorrect-new / frozen reference / in-process Ethos core` |
| **tree-sitter-ethos** | `main` `7440ccfa576a` | 2026-08-13 | — | `incorrect-new / frozen reference / editor grammar` |

**signal-ethos-zero is written in a dead dialect.** `ethos/signal.ethos:1` opens `Interface.{0 2 0}` / `Channel.{EthosZero 1 2}`, uses named fields inside structs (`GenerationRequest.{File.FileLocation}`) and no canonical spacing. Fed to the current generator:

```
$ ethos-zero 'Generate.{ «…/signal-ethos-zero/ethos/signal.ethos» «/tmp/…» }'
GenerationRejected.{ … [] Structural.ProtosError.{ Extent.{ 18 18 } Multiple } }   # exit 1
```

Its own `nix flake check` still passes (its committed `src/generated/signal.rs` predates the current generator). By contrast `signal-orchestrate/ethos/signal.ethos` regenerates **byte-identical** to its committed `src/generated/signal.rs` under ethos-zero 10.0.0 (`diff` empty), even though it pins 8.0.1.

---

## 2. Syntax the reader actually accepts

Authority: `/git/github.com/LiGoldragon/protos/src/core.rs`.

**Types** (all in `src/core.rs`, re-exported at `src/lib.rs:5-8`):

- `Extent { start: usize, end: usize }` — :4-8
- `Separator { Period, Exclamation, Colon }` — :9-14
- `Enclosure { Braced, Bracketed, Angled }` — :15-20
- `Boundary { Guillemets, Parentheses }` — :21-25
- `Symbol(pub String)` — :26-27 (a newtype, not the `Symbol = String` alias the ethos claims)
- `Protos { Headed{extent,head,constraints,separator,body} | Enclosed{extent,enclosure,children} | Opaque{extent,boundary,content} | Bare{extent,text} }` — :28-50. **Carries no `#[derive]` at all**; `Clone`/`PartialEq`/`Eq`/`Drop` are hand-written iteratively in `src/traversing.rs:418,440,452,454`, `Debug` in `src/rendering.rs:248`. There is no `Hash` for `Protos`.
- `Error { extent, problem }` — :51-55; `Problem { Empty, Multiple, Unclosed(char), Unexpected(char), MissingHead, MissingBody, Budget, Depth }` — :56-66 (`char`, not `String`)
- `ReaderBudget { remaining: usize }` — :68-71
- Traits: `ReaderBudgeting` :72, `BoundedProtosizable` :85, `Protosizable{type Output}` :88, `Textualizable` :92, `Canonicalizable{fn canonicalize(&mut self)}` :99-101

**Delimiters** — `src/core.rs:274-282`: `{`→Braced, `[`→Bracketed, `<`→Angled, `«`→Guillemets, `(`→Parentheses; a stray closer is `Problem::Unexpected`. Run terminators are whitespace or any of `{}[]<>«»();` (:366-369). Curly quotes are not in the set, so they are ordinary bare content.

**Heads and separators** — `bare_or_headed`, :360-476. A run is taken as a chain only if every `.`/`!`/`:`-separated segment is non-empty (:379-381), or if it ends in exactly one separator that is followed by an opener (:382-389). Otherwise it stays one `Bare` node (:390-399). A separator with nothing before it is `MissingHead` (:416-418); with whitespace or a closer after it, `MissingBody` (:420-426). Constraints: `<…>` after a head is read as an angled enclosure, and if no separator follows, the reader **rewinds offset and budget** and emits `Bare` (:429-451) — so `Vector<Text>` is bare text, `Vector<Text>.{ … }` is a constrained head.

Consequence, witnessed by the repo's own test `protos/tests/delineation.rs:123-131`:

```rust
fn a_timestamp_is_a_colon_chain() {
    let text = "2026-09-03T17:46:20";
    // head == Symbol("2026-09-03T17"), body claims "46:20"
```

**Strings.** Bare = the run. Guillemets: `src/core.rs:312-358`; a backslash escapes only the boundary's own glyphs and itself, and `\X` for any other X is a literal backslash then X (:321-332). `Boundary::escapes` = `['\\','»']` for guillemets, `['\\','(',')']` for parentheses (:152-158). **Parentheses nest and are read by balance** (:333-338, depth counter), and the writer escapes only the *unbalanced* ones (`Escaping::forced`, :159-182). Escaping is minimal by design (doc comment :137-143).

**Integers / decimals are not a protos concept** — protos has no number. They live at the datomic layer: `datom-codec/src/composition.rs:725-763` (`Scalar for i64`: refuses leading `+`, `-0`, and a leading `0` on a longer run) and `datom-codec/src/decimal.rs` (a `Decimal(f64)` newtype admitting only finite values, :63-75).

**Comments.** `;` to end of line, skipped in `Reader::space`, `src/core.rs:496-508`; `;` also terminates a bare run (:368).

**Meaning / parentheses.** Protos gives `Opaque{boundary: Parentheses}` (:278). datom-codec maps it to a **distinct** `Form::Meaning` (`src/composition.rs:52-59`) with a public `Meaning(pub Opaque)` type (`src/composition.rs:339`).

**Canonical print** — `src/rendering.rs:86-135`. One space inside a non-empty `{}`/`[]` and **never inside `<>`** (:103: `padded = *enclosure != Enclosure::Angled && !children.is_empty()`); nothing around the separator (:127-132); opaque content printed with minimal escaping (:94-96). `Canonicalizable::canonicalize` (:236-247) reruns the same walk against a measuring sink and settles the extents.

Test witness: `nix log` of `protos#checks.x86_64-linux.test` — 49 tests across 5 files, `test result: ok` for each, 0 failed.

---

## 3. Generation: what ethos-zero emits

Generated live from the built tool (`nix build .#default` → ethos-zero 10.0.0).

From `fixtures/orchestrate.ethos` (a `Signal`):

```rust
#[rustfmt::skip]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
pub struct LockRequest { pub lock_name: LockName, pub flow_id: FlowId, … }   // out/orchestrate.rs:14-22
pub type LockId = i64;                                                       // :2-3, aliases carry no derive
```

- **Derive sets** — `src/generation.rs:600-615`. `Carriage::Archived` (Signal only) emits the rkyv line plus the `datom`-gated line; `Carriage::Plain` (Library **and Sema**) emits `#[derive(datom_codec::Datomizable, datom_codec::Composing, Clone, Debug, PartialEq, Eq, Hash)]` unconditionally. `Carrying for File` at :620-627. Documented refusals: never `Copy`, never `Default` (:595-600).
- **Header** — `#![allow(dead_code, non_camel_case_types, non_snake_case)]` at `src/generation.rs:971`.
- **`_Data` naming** — `Nesting::nested_identity`, `src/generation.rs:485-499`: the first level is `<Variant>_Data`; deeper levels prepend ancestry. Witnessed from `fixtures/nested-collision.ethos`: `A_Data_X_Data`, `A_Data`, `B_Data_X_Data`, `B_Data`, `Outer`.
- **Kinds** — `fixtures/capability-kinds.ethos` → `fn summarize(&self) -> String`, `fn push(&mut self, input: String) -> std::result::Result<i64, super::SinkError>`, `fn create() -> Self where Self: Sized`. Complex kind `streamable-kind.ethos` → `pub trait Streamable: super::Fillable { type Item: super::Serializable; const CAPACITY: i64; fn next(&mut self) -> std::option::Option<Self::Item>; }`. Constrained identity `processable-kinds.ethos` → `pub trait Processable<A: std::clone::Clone + std::marker::Send, B: serde::Serialize>`.
- **Associations** — `src/generation.rs:875-910`, emitted exactly as the skill shows: `const _: () = { fn assert_sink_summarizable<T: super::Summarizable>() {} let _ = assert_sink_summarizable::<Sink>; … };`
- **Imports** — no `use` statements; each imported name written fully qualified (`super::SinkError`, `std::vec::Vec`, `std::option::Option`).
- **Sweet form** — `src/canonicalization.rs:14-68`. Pure text surgery: find the first non-comment line, take the leading run, and if it is all ASCII alphabetic and not already followed by `.{`, insert `.{` after it and append `\n}`. It records a `seam` extent and `Resituating::resituate` (:91-98) shifts reader error extents back onto the authored text. A file already in braced form is passed through. `src/actualization.rs:108-126` is the whole descent: canonicalize → protosize → ethosize.

**CLI** — `src/main.rs:150-173`. Exactly one inline datom, no flags; zero args prints the crate's own ethos. Witnessed:

```
$ ethos-zero                       # prints ethos-zero.ethos verbatim
$ ethos-zero 'Generate.{ «…/orchestrate.ethos» «/tmp/claude-1001/out» }'
Generated.[ /tmp/claude-1001/out/orchestrate.rs ]          exit 0
$ ethos-zero 'Generate.{ …/orchestrate.ethos /tmp/claude-1001/out }'   # bare, no guillemets — also accepted
Generated.[ /tmp/claude-1001/out/orchestrate.rs ]          exit 0
$ ethos-zero a b        → Arguments.2                       exit 1
$ ethos-zero 'Nope.{ }' → Malformed.Error.{ Composition [] Variant.{ Query Nope } }   exit 1
```

Orchestrate's clients do the same (`crates/orchestrate/src/main.rs:26-30`: `"accepts exactly one inline Datom query and no flags"`), and Describe prints the wire ethos plus the client ethos (:35-39).

---

## 4. Compilation checks — actually run

`nix flake check -L`, `timeout 900`, one process per repo, outputs in `/tmp/claude-1001/witness/`. **Every one exited 0 with `all checks passed!`**: protos, datom-codec, ethos-zero, orchestrate, nexus, signal, signal-orchestrate, signal-ethos-zero. Each printed `running 0 flake checks` — i.e. every derivation was already in the store for the current source hash, so these are cached-green, not fresh builds. Named test results were then read out of `nix log` on each `checks.x86_64-linux.test` derivation:

| repo | tests | result |
|---|---|---|
| protos | 49 (deep 4, delineation 15, protos 18, textualization 12) | all ok, 0 failed |
| datom-codec | 45 (composition 13, core 32) | all ok, 0 failed |
| ethos-zero | 49 across 6 binaries incl. `the_error_module_is_fresh`, `the_contract_module_is_fresh`, `every_fixture_module_is_fresh` | all ok, 0 failed |
| orchestrate | 43 (unit 10, live-nexus 15, relocation 7, ordinary-lock 4, configuration 3, clients 2×2) | all ok, 0 failed |
| signal-orchestrate | 10 (exchange envelope 8, datom contract 2) | all ok, 0 failed |

**Check inventories** (`nix eval .#checks.x86_64-linux`):
- protos / datom-codec (identical sets): `build clippy doc fmt generated-contract generated-kinds-contract no-forbidden-vocabulary no-production-free-functions no-production-inherent-methods no-zst-behavior test`
- ethos-zero: `build clippy dependency-ethos doc fmt no-free-functions no-inherent-methods test`
- orchestrate: 17 checks including `live-nexus socket-claim relocation carried-store peer-authority stopping datom-free-nexus`
- signal: 15 including `carries-no-engine rkyv-feature-discipline default-features-carry-no-runtime`
- nexus: `clippy fmt test`

**The freshness tests.** Three distinct mechanisms, all comparing generated text to committed text — legitimate, because here the text *is* the product:

1. `ethos-zero/tests/freshness.rs:13-31` — reads the authored `.ethos`, actualizes, generates, `assert_eq!` against the committed `.rs`, message `"{generated} is stale; regenerate from {self}"`. Covers `src/error.rs`, `src/ethos-zero.rs`, and all 17 fixtures.
2. `orchestrate/crates/*/build.rs:1-21` and `signal-orchestrate/build.rs` — the same assertion, at build time, so a stale contract fails the *build*.
3. `protos/checks/generated-contract.sh` and `datom-codec/checks/generated-contract.sh` (byte-identical files) — a Nix `runCommand` that invokes a *pinned* `ethos-zero` on the `.ethos` and `cmp`s against `generated-contract/*.rs`.

I could not verify anything about `sema`, `core-ethos`, `ethos-engine`, `protos-engine` or `tree-sitter-ethos` beyond their status text; I did not run their checks.

---

## 5. Architecture

**Crate boundaries and dependency direction** (Cargo, acyclic):

```
protos  ←  datom-codec (+ datom-codec-derive, path dep)  ←  ethos-zero
                                     ↑                          ↑ (build-dependency)
                                  signal ───────────────── signal-orchestrate
                                                                 ↑
                            nexus ── orchestrate-nexus / orchestrate / orchestrate-meta
```

protos has **no dependencies at all** (`protos/Cargo.toml` has no `[dependencies]` section). `nexus` depends only on rkyv + thiserror — it is outside the protos stack entirely.

**The four-layer descent is implemented as separate passes and is not folded:**
- textual → protosic: `protos/src/core.rs:527-562` (`Protosizable`/`BoundedProtosizable` for `String`/`str`)
- protosic → conceptual (datomic): `datom-codec/src/composition.rs:23-163`, an explicit worklist machine `Former`, never recursive
- conceptual → compositional: `datom-codec/src/core.rs:238-251`, `Composable::compose` / `compose_positions`
- the ascent mirrors it: `Datomizable` → `projection.rs:191-202` (`Protosizable for Datom`) → `Textualizable`
- `Potential::actualize` (`core.rs:444-458`) is the one place the three descents are chained, and it keeps the protos tree so an error can be given its extent (`PotentialExtenting::reader_extent`, :439-443)

ethos-zero adds a **fifth, textual→textual** step ahead of them (sweet → canonical, `canonicalization.rs`), which the protos skill does not name.

**The derive macro** — `datom-codec/crates/datom-codec-derive/src/lib.rs`, two proc-macros, no attributes:
- `#[derive(Composing)]` (:16-121): for an enum, unit variants match `Form::Bare(name)`, one-field variants `body.compose()`, multi-field variants `compose_positions::<(T0,T1,…)>` into a tuple; for a struct, emits both `Compositional` (with `const ARITY` and `from_positions`) and `Composing` (delegating to `compose_positions`). Type parameters get a `T: Composing` where-bound.
- `#[derive(Datomizable)]` (:123-201): struct → `Form::Struct(vec![…child(i)…])`; enum → unit variant `Form::Bare(name)`, otherwise `Form::Variant(Symbol(name), Box::new(payload.datomize(at.child(1))))`.

**The CLI shape** is uniform and matches the skills: one inline datom, no flags, an enum root, an enum response, ethos as the help.

---

## 6. Divergence table

Each row: what the skill says / what the code does / witness.

| # | Skill claim | Code | Witness |
|---|---|---|---|
| 1 | datom: `trait Datomizable { type Output; fn datomize(&self, at: Path) -> Self::Output; }` | No associated type: `fn datomize(&self, at: Path) -> Datom` | `datom-codec/src/core.rs:146-148`. The `Output` form still exists in the version orchestrate is pinned to — `orchestrate/crates/orchestrate/src/main.rs:121-123` writes `T: Datomizable<Output = Datom>`. The skill describes the older shape. |
| 2 | datom: the derive is `datom_codec::Compositional`; `trait Compositional { fn compose(datom, budget) -> Result<Self,Error> }` | The derive is **`Composing`**. `Composing` is the "a datom composes into this" trait; `Compositional` is a *different*, narrower trait: `Compositional: Composing { const ARITY: Integer; fn from_positions(Positions) }` | `datom-codec/src/lib.rs:26`, `src/core.rs:133-142`; derive names at `crates/datom-codec-derive/src/lib.rs:16,123` |
| 3 | datom: `Composable { fn compose<T: Compositional>(…) }` | `fn compose<T: Composing>` plus a second `fn compose_positions<T: Compositional>` | `datom-codec/src/core.rs:126-129` |
| 4 | datom: generated impl calls `datom.positions(2)?` then `positions.position(budget)?` | `positions(arity, budget)`; `position()` takes no budget (it is held inside `Positions`) | `datom-codec/src/core.rs:196-200, 166-178` |
| 5 | datom: "Today a parenthesized text lands as a plain String, with the Meaning type marked in code." | Parentheses land as their **own** `Form::Meaning`, and a public `Meaning(pub Opaque)` type composes only from it | `src/composition.rs:52-59, 334-363`. Skill is behind the code. |
| 6 | datom: `Form::Variant(Symbol, Box<Datom>)` ✔ but the **separator is not carried** | A `Headed` with a non-Period separator never becomes a `Variant`; it is re-textualized into `Form::Bare` | `src/composition.rs:130-133`. Projection always writes `Separator::Period` back (`projection.rs:157`). |
| 7 | datom: "the timestamp has no space and no delimiter, so it is bare" | At the protosic layer it is a **colon chain**, not bare; only the datomic layer repairs it to `Form::Bare` by re-printing | `protos/tests/delineation.rs:123-131`; `datom-codec/src/composition.rs:130-133` |
| 8 | datom: a bare string is "a run with no space and no delimiter glyph" | Also refused: a leading or trailing separator, and two adjacent separators — those fall back to guillemets | `src/composition.rs:167-181`; witnessed by `tests/composition.rs:207-218` (`5::7/128` → `«5::7/128»`, `a..b` → `«a..b»`) |
| 9 | protos: `pub type Symbol` (the ethos says `Symbol.String`) | `pub struct Symbol(pub String)`, a newtype | `protos/src/core.rs:26-27` vs `protos/protos.ethos:6` |
| 10 | protos: `Problem::Unclosed(String)` / `Unexpected(String)` per the generated contract | `Unclosed(char)` / `Unexpected(char)` | `protos/src/core.rs:60-61` vs `generated-contract/protos.rs:74-75` |
| 11 | protos: `trait Canonicalizable { fn canonicalize(&mut self); }` | The real trait has it; the **generated contract** emits `pub trait Canonicalizable {}` — ethos cannot state a unit yield | `protos/src/core.rs:99-101` vs `generated-contract/protos.rs:91`; the `.ethos` admits it in its own comment, `protos-kinds.ethos:3-5` |
| 12 | ethos: "every item carries `#[rustfmt::skip]`" | One skip per *declaration*; a declaration that emits several items (its `_Data` companions) gives the skip to the first only | `src/generation.rs:972` (`#( #[rustfmt::skip] #items )*`); visible in the generated `nested-collision.rs` lines 2/7/11/15/19 and in `ethos-zero/src/ethos-zero.rs:7,13,19,24` |
| 13 | ethos: derives are `Clone, Debug, PartialEq` | Also `Eq, Hash` | `src/generation.rs:605,609` |
| 14 | ethos: "A Signal's types gate them behind a `datom` feature … so the Nexus compiles its contract without datom-codec" | Holds for the derives, **but breaks for the `Decimal` and `Meaning` intrinsics**, which emit `datom_codec::Decimal` / `datom_codec::Meaning` as an ungated field type | `src/generation.rs:62,64`. Witnessed: I generated `fixtures/signal-decimal.ethos` and compiled it in a package with only rkyv: `error[E0433]: cannot find module or crate 'datom_codec' --> src/lib.rs:6:18`. The existing guard `tests/signal_without_datom.rs` only compiles `orchestrate.rs` and `empty-signal.rs`, neither of which uses a Decimal — so this gap is untested. |
| 15 | ethos: a `Sema` root gives "a Nexus … its database types" | Sema is emitted with `Carriage::Plain` — no rkyv derives at all, though sema stores rkyv-archived values | `src/generation.rs:620-627`; witnessed from `fixtures/entry-sema.ethos` |
| 16 | ethos: "an alias bears them through the type it names and carries no derive" | Confirmed ✔ | generated `orchestrate.rs:2-13, 33-34, 61-62` |
| 17 | ethos: "Ethos Zero emits the datom kinds on every struct and enum it generates" ✔ | Confirmed ✔ | as above |
| — | **Not in any skill.** `Meaning`, `Decimal`, `Budget{remaining, reader, depth, maximum_depth}`, `ErrorLayer{Protos,Datom,Composition}`, `ErrorKind{Budget,Structural,Form,Arity,Value,Variant}`, `Potential`/`Actualizing`, `DatomForming`, `Positions`/`Positioning`, `Scalar`, `Variantizing`, `Naming`, `ProtosExtenting`, the 256-node protos depth ceiling and the 4096 forming-depth ceiling, the hand-written iterative `Clone`/`PartialEq`/`Drop` on both `Protos` and `Datom`, and the sweet→canonical *textual* pass with its seam-shifted error extents. | | `datom-codec/src/lib.rs:19-30`; `protos/src/core.rs:231`; `datom-codec/src/composition.rs:9`; `ethos-zero/src/canonicalization.rs` |

**Version skew, which no skill mentions and which the freshness gates hide.** Four different ethos-zero revisions are pinned across the stack:

- `protos/flake.nix:12` → `da585049` (0.…, 2026-09-11)
- `datom-codec/flake.nix:12` → `b232d35e` ("Generate the Composing derive", 2026-09-12)
- `orchestrate/Cargo.toml` → `de3d9928` (8.0.1)
- `signal` + `signal-orchestrate` → `4bf73cae` (10.0.0, main head)

Because of that, both committed `generated-contract/*.rs` files are **stale against ethos-zero main** while their Nix checks still pass. Regenerating with 10.0.0:

```
protos/generated-contract/protos.rs:      12 lines differ
  committed: #[derive(datom_codec::Datomizable, datom_codec::Compositional, Clone, Debug, PartialEq)]
  current:   #[derive(datom_codec::Datomizable, datom_codec::Composing,     Clone, Debug, PartialEq, Eq, Hash)]
datom-codec/generated-contract/datom-codec.rs: 4 lines differ (Eq, Hash missing)
```

`protos.rs` as committed names a derive (`Compositional`) that **no longer exists** in datom-codec. It compiles nowhere, which brings us to:

**The generated contracts are never compiled.** `protos/src/lib.rs:2-4` declares only `core`, `rendering`, `traversing`; `datom-codec/src/lib.rs:12-17` only its six modules. Nothing includes `generated-contract/`. So `protos.ethos` and `datom-codec.ethos` *assert* a public anatomy but nothing proves they describe the real types — and in several places they demonstrably do not (rows 9, 10, 11 above; plus `Datom.{ Path Form }` generating `form: Box<Form>` where the real field is `Form`, and `Budget.{ Integer ReaderBudget Integer Integer }` generating `first_integer/second_integer/third_integer` for `remaining/depth/maximum_depth`). The `datom-codec-kinds.ethos` declaration of `Composable` is outright wrong: it says `compose.{ [ Budget ] [ Result<Self Error> ] }`, which generates `fn compose(&self, Budget) -> Result<Self, Error>` (`generated-contract/datom-codec-kinds.rs:78`), whereas the real trait is `fn compose<T: Composing>(&self, &mut Budget) -> Result<T, Error>`. Ethos has no generics, so the declaration cannot be right; it is currently silently wrong rather than absent.

---

## 7. Ugliness, repetition, compromise

1. **Pointer addresses as map keys.** `datom-codec/src/projection.rs:36,62,70,78,116,128,136` use `datom as *const _ as usize` as `HashMap` keys to memoize node lengths. It is sound only because the tree is immutably borrowed for the duration, and it is silently wrong the moment anything clones or moves a node mid-walk. **Worse, the whole pass is redundant**: `protos::Canonicalizable::canonicalize` (`protos/src/rendering.rs:236-247`) already measures and settles exactly these extents using the real printer. The better shape is for `Projecting::project` to build the tree with zero extents and call `canonicalize()` — one machine instead of two, and the length arithmetic (`+ children.len() + 3`, `+ head.0.len() + 1`, `projection.rs:62-74`) stops being a second, hand-maintained copy of the spacing rules in `rendering.rs:98-134`.

2. **`opaque_length` builds and prints a whole `Protos::Opaque` just to measure it** (`projection.rs:180-189`), then `project_opaque` immediately builds the same node again (:172-179). Two allocations and two escape passes per string leaf. Subsumed by fix 1.

3. **Two ~183-line clients that differ by a noun.** `orchestrate/crates/orchestrate/src/main.rs` and `crates/orchestrate-meta/src/main.rs` differ only in: the contract crate, `ORCHESTRATE_SOCKET` vs `ORCHESTRATE_META_SOCKET`, and one word in three strings. Their `build.rs` files are **byte-identical** (`diff` exit 0); their `client.ethos` files differ in one comment line. Better shape: one client crate generic over the contract type (or one binary taking the socket from its contract), with the two binaries as thin `main`s.

4. **Four grep-based Nix checks copy-pasted across repos.** `no-production-free-functions`, `no-production-inherent-methods`, `no-zst-behavior`, `no-forbidden-vocabulary` appear verbatim in `protos/flake.nix:29-56` and `datom-codec/flake.nix:33-60`, and again as shell files in `ethos-zero/checks/` and `signal-orchestrate/checks/`. The `generated-contract.sh` files in protos and datom-codec are byte-identical. These are style lints, not tests — they match source text and will fire on any edit that changes shape without changing behavior. Better shape: one `rust-build`-hosted lib function the repos call, so the rule lives once.

5. **`no-forbidden-vocabulary` bans `codec` inside a repository named datom-codec** whose Cargo lib is `datom_codec` (`datom-codec/flake.nix:54-55`, `Cargo.toml`). The rule passes only because it scans `src/` and the word survives in the manifest and the crate name. Either the rule or the name is wrong.

6. **`collapse_derives` is string surgery on generated Rust.** `ethos-zero/src/generation.rs:977-1010` re-parses prettyplease's output line by line to rejoin `#[derive(` blocks, because prettyplease and rustfmt disagree and the `fmt` gate would fail. It is honestly documented (:977-982), but it is a third formatter bolted onto two. Better shape: emit the derive list as a single pre-formatted token so no formatter has a choice, or drop prettyplease for a rustfmt invocation.

7. **`#[rustfmt::skip]` is attached to the wrong granularity** (`generation.rs:972`), leaving every `_Data` companion unprotected. One skip per emitted *item*, not per declaration, is the fix.

8. **Hardcoded fixture count.** `ethos-zero/tests/freshness.rs:54` asserts `fixtures.len() == 17`. Adding a fixture and forgetting the number fails the test for the wrong reason; forgetting to commit its generated file is what the test is actually for. The count guard should be "every fixture has a committed generation and every committed generation has a fixture", which is expressible without a magic number.

9. **`Error::datomize` writes `at.child(1)` four times per arm.** `datom-codec/src/core.rs:292-334, 370-382` — each variant repeats `at.child(1)`, `at.child(1).child(0)`, `at.child(1).child(1)`, and `ErrorKind::Structural` nests a `child(1)` inside a callee that already applies one (:299). This is exactly what `Variantizing::named_variant` exists to hide, and it is hand-written where the derive would do it. These impls are hand-written because `Error` is an intrinsic — but the repetition is mechanical and should be a helper, not eleven copies.

10. **`Canonicalizable` means two different things in two crates.** In protos it assigns extents to a built tree (`protos/src/core.rs:99-101`); in ethos-zero it converts sweet text to braced text (`ethos-zero/src/canonicalization.rs:14`). Same word, different act, adjacent crates.

11. **The Nix input graph has a cycle the Cargo graph does not.** `protos/flake.nix` takes `ethos-zero` as an input while `ethos-zero/flake.nix` takes `protos`. It is broken only by revision pinning, which is why three different ethos-zero revisions are live and why the stale generated contracts went unnoticed. Better shape: the contract check belongs in the generator's own `dependency-ethos` check (which already exists, `ethos-zero/flake.nix:66-75`), and the component repos should not hold a reverse input.

12. **`Protos::PartialEq` compares extents.** `traversing.rs:268-274, 440-451` — `Aspect` carries `Extent`, so two structurally identical trees read from differently-indented text are unequal. That is defensible, but it means `==` is not structural equality and every test that builds a tree must get the byte offsets right by hand.

## Sources

Method: direct reading of the working trees under `/git/github.com/LiGoldragon/`, plus executed commands. Every claim above carries its own file:line or command output. No repository was modified; no `jj`/`git` write command was run.

Commands executed (all read-only or scratch-writing):

- `jj log -n 3 --no-graph -T '…'` in each of the 13 named repositories, for bookmark, head and commit date.
- `git log -1 --format='%ci %s' <rev>` in `protos`, `datom-codec`, `ethos-zero` to resolve the pinned revisions `171b21f6`, `627db67f`, `da585049`, `b232d35e`, `de3d9928`, `4bf73cae`.
- `nix flake check -L` (`timeout 900`, detached, one per repo) for protos, datom-codec, ethos-zero, orchestrate, nexus, signal, signal-orchestrate, signal-ethos-zero. Transcripts retained at `/tmp/claude-1001/witness/*-flakecheck.txt`; all `EXIT=0`, all `all checks passed!`.
- `nix eval --raw .#checks.x86_64-linux --apply 'c: builtins.concatStringsSep "\n" (builtins.attrNames c)'` for the check inventories.
- `nix path-info --derivation .#checks.x86_64-linux.test` then `nix log <drv>` for the per-test names and results in protos, datom-codec, ethos-zero, orchestrate, signal-orchestrate.
- `nix build .#default -o /tmp/claude-1001/ez` in ethos-zero (ethos-zero 10.0.0), then direct invocations of `/tmp/claude-1001/ez/bin/ethos-zero` with no arguments, with `Generate.{ … }` over the fixtures and over every `.ethos` in protos, datom-codec, signal-orchestrate and signal-ethos-zero, with two arguments, and with a malformed query.
- `diff` of freshly generated output against each committed `generated-contract/*.rs` and `src/generated/signal.rs`.
- `nix develop -c cargo check --manifest-path /tmp/claude-1001/decimalprobe/Cargo.toml --no-default-features` on a scratch package containing only the generated `signal-decimal.rs` and rkyv, producing the `E0433` cited in divergence row 14.
- `diff` of `orchestrate/crates/orchestrate/{build.rs,client.ethos,src/main.rs}` against their `orchestrate-meta` counterparts.

Primary source files read in full: `protos/src/{core,rendering,traversing}.rs`, `protos/{protos,protos-kinds}.ethos`, `protos/generated-contract/*.rs`, `protos/flake.nix`, `protos/checks/generated-contract.sh`; `datom-codec/src/{core,composition,projection,positional,dropping,decimal,lib}.rs`, `datom-codec/crates/datom-codec-derive/src/lib.rs`, `datom-codec/*.ethos`, `datom-codec/generated-contract/*.rs`, `datom-codec/flake.nix`; `ethos-zero/src/{main,ethos-zero,error,canonicalization,actualization}.rs`, parts of `ethos-zero/src/{lib,generation}.rs`, `ethos-zero/{ethos-zero,error}.ethos`, `ethos-zero/tests/{freshness,signal_without_datom}.rs`, `ethos-zero/checks/*.sh`, `ethos-zero/flake.nix`, `ethos-zero/Cargo.toml`; `orchestrate/Cargo.toml`, `orchestrate/crates/*/Cargo.toml`, `orchestrate/crates/orchestrate/{build.rs,client.ethos,src/main.rs}`; `nexus/src/lib.rs`, `nexus/README.md`; `signal/Cargo.toml`; `signal-orchestrate/{ethos/signal.ethos,src/lib.rs,Cargo.toml}`; `signal-ethos-zero/{ethos/signal.ethos,README.md}`; the `AGENTS.md` estate-status sections of `protos-engine`, `ethos-engine`, `core-ethos`, `sema`, `tree-sitter-ethos`.

Skills consulted as the claims under test: `protos`, `datom`, `ethos` (loaded through the Skill tool), with `subflow`, `vocabulary`, `behavior`, `testing` and `flow-evidence` governing the method.

Not verified: the behavior of `sema`, `core-ethos`, `ethos-engine`, `protos-engine` and `tree-sitter-ethos` beyond their declared estate status — their checks were not run and their sources were not read. The `nix flake check` results are cached-green rather than freshly rebuilt; per the testing skill a build reported green is green, but no derivation was forced to rebuild.
