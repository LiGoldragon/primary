# Stack map: Protos / datom / Ethos Zero / orchestrate

Flow 1a6ca4, read-only subflow. Witnessed 2026-09-05 00:58–01:30 CEST on host ouranos.
Legend: **[ran]** = this subflow ran the command; **[read]** = this subflow read the file; **[relayed: agentX]** = a delegated read agent reported it (its commands named where it gave them); **[inferred]** = this subflow's inference.

## 0. The one fact that reshapes everything else

**The `/git` checkouts of the stack crates are detached at commits behind `origin/main`** [ran: `git branch -a --contains HEAD`, `git rev-list --left-right --count HEAD...origin/main` in each repo]. The ProtoformStack train was merged into `main` on 2026-09-04 (every `ProtoformStack` tip is an ancestor of `main`; `git log origin/main..origin/ProtoformStack` is empty in every repo) and `main` then received a further pin/regenerate round at ~13:00–15:08 on 09-04. The working copies under `/git` were not moved. So "the code as it stands" has two readings:

| repo | checkout HEAD (detached) | crate ver at checkout | origin/main tip | crate ver at main | behind |
|---|---|---|---|---|---|
| protos | 2f605fd 2026-08-29 "State complete Protos declaration contract in Ethos" | 0.14.0 (pre-rewrite) | 4806136 2026-09-04 14:03 "Derive Clone, Debug, PartialEq, Eq on Situated<F>; bump to 0.15.1" | 0.15.1 | 7 |
| datomic (`datom` is a symlink to it) | e4430bf 2026-09-04 13:06 "impl Datomic for Situated<F>; impl_datomic_box!; bump 0.9.0" | 0.9.0 | 4712361 2026-09-04 14:17 "Fix Cargo.lock version for 0.9.1" | 0.9.1 | 2 |
| ethos-zero | 8bcb0b9 2026-09-04 13:18 "Format lib.rs with rustfmt" | 1.2.0 | 0f19896 2026-09-04 14:27 "Pin protos 0.15.1, datomic 0.9.1; fix e2e test; bump 1.3.1" | 1.3.1 | 2 |
| orchestrate | 885f6e3 2026-09-04 15:08 on branch `main` | 0.29.2 | same | 0.29.2 | 0 |
| signal-orchestrate | 6fc8c5b 2026-08-26 | 0.17.0 (+dirty bump to 0.17.1) | f366d6a 2026-09-04 14:40 "Pin protos 0.15.1, datomic 0.9.1, ethos-zero 1.3.1; regenerate; bump 0.20.1" | 0.20.1 | 12 |
| meta-signal-orchestrate | d4dd208 2026-08-26 | 0.11.0 | 3ae11c1 2026-09-04 14:40 "...bump 0.14.1" | 0.14.1 | 12 |
| curriculum-deploy | 50e12d3 2026-09-04 13:53 | 0.5.0 | 2a1c337 2026-09-04 14:49 "...delete generated_ext.rs; bump 0.5.1" | 0.5.1 | 1 |
| claude-answers | e637388 2026-08-29 | 0.3.0 | f5c1547 2026-09-04 14:47 "...bump 0.5.1" | 0.5.1 | 3 |
| lojix | d3c0ac9 2026-09-04 18:10 (= main) | 0.20.3 | same | 0.20.3 | 0 |
| signal-ethos-zero / meta-signal-ethos-zero | ef56ce7 / c5578c9 2026-08-29 (= local main) | 0.2.0 | origin/main is 1 *behind* local main (unpushed local commit "Bind ... to channel identity") | 0.2.0 | -1 |

The anatomy in section 3 was taken at **origin/main** (via `git show origin/main:<path>`, no checkout changed) unless stated; the build state in section 4 was taken at the **checkouts**, because that is what `cargo check` sees. Any rewrite dispatched from this map must first decide which revision it starts from; the main-branch pins below are the live train.

Protos-estate status (the `## Protos estate status` block each repo carries in AGENTS.md/README.md since the 2026-08-13 "docs: mark Protos estate status" commits) [ran: grep across all repos]: protos, datomic, ethos-zero, orchestrate, curriculum-deploy, Curriculum carry **no** estate block (they are the new stack); every `signal-*`/`meta-signal-*` crate and the components (mind, persona, spirit, lojix, claude-answers, …) are marked `Stack: correct-new destination / Status: active component, current checkout legacy-wired`; `dotos`, `core-ethos`, `core-schema`, `signal-ethos`, `ethos-engine`, `structural-codec`, `core-logos`, `core-nomos`, `sema-translator`, `tree-sitter-ethos`, … are `Stack: incorrect-new / Status: frozen reference` ("No new code is accepted here. Do not add Cargo or Nix dependency edges"); `schema`, `schema-rust`, `schema-language` are `Stack: legacy (Schema + NOTA) / legacy production/reference`.

So, from the evidence, **"old Ethos" = `core-ethos` 0.31.0 (+ `core-schema`, a same-content clone; `signal-ethos` 0.3.0 "old Ethos vocabulary"; `ethos-engine` 0.2.0 "central-storage daemon embryo")** and **"old schema" = `schema-rust` 0.17.0 + `schema` 0.3.0 + `schema-language` (the `.schema` → `SchemaSource` → `TrueSchema` → `schema-rust` emission pipeline, README of `schema`)**, with `dotos` 0.10.1 as the old text codec they project through, and `signal-frame` 0.4.0 as the old wire kernel (rkyv frames + dotos projection + `signal_cli!`).

## 1. Repositories

All under `/git/github.com/LiGoldragon/` (skill variable Repository root `/git`). `/git/worktrees/` is empty [ran: ls]. Remotes are `git@github.com:LiGoldragon/<name>.git` [ran: git remote -v].

### 1.1 Core stack (new)

| path | branch | HEAD | Cargo name/ver | dirty | worktrees registered | ProtoformStack branch |
|---|---|---|---|---|---|---|
| /git/github.com/LiGoldragon/protos | detached | 2f605fd 2026-08-29 02:13 | protos 0.14.0 | clean | 1 (self) | local + origin, tip 56c683e (ancestor of main) |
| /git/github.com/LiGoldragon/datomic (`datom` → symlink) | detached | e4430bf 2026-09-04 13:06 | datomic 0.9.0 | clean | 1 | local + origin, tip a27f9b8 (ancestor of main) |
| /git/github.com/LiGoldragon/ethos-zero | detached (from 31c5984) | 8bcb0b9 2026-09-04 13:18 | ethos-zero 1.2.0 | clean | 3: self; `/home/li/wt/github.com/LiGoldragon/ethos-zero/ethos-zero-keepgoing-6329f1` @8bcb0b9 clean; `/tmp/claude-1001/-home-li-primary/6329f1fb-e1d1-423e-92b8-f4f786184fb4/scratchpad/ethos-zero-build` @185f13a | local + origin, tip 185f13a |
| /git/github.com/LiGoldragon/orchestrate | **main** | 885f6e3 2026-09-04 15:08 | orchestrate 0.29.2 | clean | 2: self; `/home/li/wt/github.com/LiGoldragon/orchestrate/orchestrate-keepgoing-6329f1` @1c0dd76 (0.29.0) clean | local + origin, tip 9585484 |
| /git/github.com/LiGoldragon/signal-orchestrate | detached (from 0251c88) | 6fc8c5b 2026-08-26 | signal-orchestrate 0.17.0 → 0.17.1 in dirty Cargo.toml | **4 dirty**: Cargo.lock, Cargo.toml (0.17.1 bump + ethos-monolith build-dep rev), src/generated/signal.rs (+78), tests/generated_contract.rs (+34); mtime 2026-09-04 11:02 | 1 | local + origin, tip b25bbd9 |
| /git/github.com/LiGoldragon/meta-signal-orchestrate | detached | d4dd208 2026-08-26 | meta-signal-orchestrate 0.11.0 | clean | 1 | local + origin, tip 5a99ccb |
| /git/github.com/LiGoldragon/curriculum-deploy | detached (from 8ca4d4a) | 50e12d3 2026-09-04 13:53 | curriculum-deploy 0.5.0 | clean | 2: self; `/home/li/wt/github.com/LiGoldragon/curriculum-deploy/curriculum-deploy-ProtoformStack-6329f1` **on branch ProtoformStack** @f3f2ee3 (0.4.0) clean | local (checked out in that worktree) + origin |
| /git/github.com/LiGoldragon/claude-answers | detached | e637388 2026-08-29 | claude-answers 0.3.0 | clean | 1 | local only, tip d6ae3ef |
| /git/github.com/LiGoldragon/lojix | detached (= main) | d3c0ac9 2026-09-04 18:10 | lojix 0.20.3 | clean | 1 | none (has `realizer-three-stack-status`) |
| /git/github.com/LiGoldragon/signal-ethos-zero | detached (= local main) | ef56ce7 2026-08-29 | 0.2.0 | clean | 1 | none |
| /git/github.com/LiGoldragon/meta-signal-ethos-zero | detached (= local main) | c5578c9 2026-08-29 | 0.2.0 | clean | 1 | none |
| /git/github.com/LiGoldragon/Curriculum | detached | 8a6f2a9 2026-09-04 16:47 | (skills, not a crate) | clean | 1 (a lock 639 names a `Curriculum-DialectSkills-6329f1` dir under /home/li/wt that is **not** a registered worktree any more) | none |

`/home/li/wt/github.com/LiGoldragon/<repo>/*` also holds ~40 **stale directories that are no longer registered worktrees** (`.git` absent; e.g. `protos/protos-ProtoformStack-6329f1`, `datomic/datomic-situated-6329f1`, `ethos-zero/e3-*`, `orchestrate/orchestrate-ProtoformStack-6329f1`, `signal-orchestrate/signal-orchestrate-ProtoformStack-6329f1` mtime 09-04 05:22, `Curriculum/Curriculum-DialectSkills-6329f1` mtime 09-04 12:16, `lojix/*`) [ran: loop over `git -C <dir> log`, `stat`]. They are leftover trees, not live checkouts; only the three worktrees named above (all from flow 6329f1, all clean, last touched 2026-09-04 13:09–13:41) are registered.

Old-stack repos that the consumers still pin (all at `main` = `origin/main`, untouched since 2026-08-13 except signal-frame 08-26) [ran]: dotos d97dd5c 0.10.1; schema-rust 55e3eaa 0.17.0; schema 1654569 0.3.0; core-ethos 8186209 0.31.0; core-schema 8186209 (same content); ethos-engine 3a80a3e 0.2.0; signal-ethos 417ecdb 0.3.0; signal-frame 000d866 0.4.0; signal 9cfacb6 0.1.0 (**21 dirty files**, mtime 2026-07-31); signal-derive 5cc5efb (1 dirty); sema 4fdc612 0.1.1; sema-engine 27e814a 0.15.1; structural-codec c55ac79 0.22.0; tree-sitter-ethos 7440ccf; protos-engine 7a1bfd1 (1 dirty). Components: mind ee4f34f 0.8.0 (**21 dirty files**: a nota→dotos rename across src/, mtime 2026-07-31); psyche 14b9c3e 0.1.0 (no stack deps in Cargo.toml); persona 9469b0a; spirit 008d8ca; meta-signal-upgrade (12 dirty); signal-orchestrator-judge (7 dirty).

`/home/li/primary` itself: a **jj-colocated git repo** (`/home/li/primary/.jj` exists; `jj` at `/home/li/.nix-profile/bin/jj`) [ran]. At 01:10 its git HEAD was detached at af6899ac6 (this flow's own "log the dispatch" commit, made with git) while jj's `main` bookmark and `origin/main` were at 329d59548; the jj op log shows "import git head" at 01:10:23 reconciling it. Sixteen jj workspaces are registered (`jj workspace list`), most pointing at empty change heads under `/home/li/wt/github.com/LiGoldragon/primary/*`, `../primary-worktrees/*`, `../wt-primary-*`.

## 2. Dependency graph

### 2.1 The new train (Cargo.toml at origin/main) [ran: `git show origin/main:Cargo.toml` per repo]

All edges are `git = "https://github.com/LiGoldragon/<repo>"` with an exact `rev`; no path deps, no crates.io publication, no vendoring (cargo fetches from the network / its git cache) [relayed: build agent, witnessed in its `cargo check` output].

```
protos 0.15.1 (48061367)        <- nothing but crates.io (no LiGoldragon deps)
datomic 0.9.1 (4712361c)        <- protos@48061367
ethos-zero 1.3.1 (0f198968)     <- protos@48061367, datomic@4712361c, syn 3 / quote / proc-macro2 ; dev: rkyv 0.8
signal-orchestrate 0.20.1       <- protos@48061367, datomic@4712361c, rkyv 0.8 ; dev: ethos-zero@0f198968 (regeneration test only)
meta-signal-orchestrate 0.14.1  <- same shape as signal-orchestrate
orchestrate 0.29.2 (885f6e3)    <- protos@48061367, datomic@4712361c, ethos-zero@0f198968, signal-orchestrate@f366d6ac, meta-signal-orchestrate@3ae11c13, sema-engine@7158e550 (store), rkyv 0.8, tokio 1, thiserror 2
curriculum-deploy 0.5.1         <- protos@48061367, datomic@4712361c ; dev: ethos-zero@0f198968
claude-answers 0.5.1            <- protos@48061367, datomic@4712361c ; dev: ethos-zero@0f198968
```

`sema-engine` (0.15.1, estate "correct-new destination, legacy-wired") is the one old-lineage edge that survives in orchestrate main: it pulls `signal-frame 0.3.1`, `signal-sema 0.2.0`, `sema 0.1.1` transitively [relayed: build agent, from cargo's resolution output]. That means `orchestrate` main still links `signal-frame` and `dotos` **transitively through its store**, not through its wire.

### 2.2 Who is still on the old stack

Direct Cargo.toml edges at the checkouts (all equal to their `origin/main` for the old-stack repos) [ran: grep over every `/git/github.com/LiGoldragon/*/Cargo.toml`]:

- **On old protos/datomic revs (pre-rewrite, 2026-08-29)**: `lojix` 0.20.3 (protos@bfde3b87, datomic@b670c72d, plus dotos, signal-frame, signal-lojix, meta-signal-lojix, sema-engine, triad-runtime); `signal-ethos-zero` and `meta-signal-ethos-zero` 0.2.0 (protos@bfde3b87, datomic@b670c72d, ethos-zero@f043fc46 dev). `bfde3b87` = protos "Own textual default behavior in Ethos map" 2026-08-29 03:04 (the last 0.14 line), `b670c72d` = datomic "Pin Datomic to map-default Protos revision" 08-29 03:09.
- **On `schema-rust` (old schema)**: harness, introspect, mentci, mentci-egui, mind, persona, spirit, system, terminal, terminal-cell, upgrade, sema-engine, signal-standard, signal-domain, signal-terminal, signal-upgrade, meta-signal-upgrade, signal-spirit, meta-signal-spirit, and every `signal-*`/`meta-signal-*` marked "legacy-wired" (agent, cloud, criome, lojix, mentci, mentci-client, message, mind, mirror, persona, router, listener).
- **On `dotos`**: essentially every component and signal crate (agent, chroma, chronos, clavifaber, criome, horizon-rs, introspect, mentci*, message, mind, mind-judge, mirror, router, schema, schema-language, signal, signal-frame, terminal*, triad-runtime, version-projection, lojix, and all signal-*/meta-signal-* except the four ProtoformStack ones and signal-forge/signal-derive).
- **On `core-ethos` (old Ethos)**: core-nomos, ethos-engine, nomos-engine, schema-rust, sema-engine, sema-translator, signal-standard, signal-router, signal-version-handover, and the legacy-wired signal-*/meta-signal-* pairs for agent, cloud, criome, lojix, mentci, mentci-client, message, mind, mirror, persona, router.
- **On `signal-frame` (old wire)**: everything above plus aggregator, cloud, listener, repository-ledger, sema-storage, spirit-judge, signal-spirit-judge, orchestrator-judge, signal-orchestrator-judge, mind-judge.
- **Consumers of `signal-orchestrate` old line**: `orchestrator-judge`, `signal-orchestrator-judge` (checkout revs; both "legacy-wired"). `mind` depends on `meta-signal-orchestrate` (old rev).
- **Already on datom + ethos-zero (new)**: orchestrate, signal-orchestrate, meta-signal-orchestrate, curriculum-deploy, claude-answers (at main). `psyche` 0.1.0 has no stack dependency at all [ran: grep of its Cargo.toml — only `repository =` matched].

Named in the brief but not found: no crate named `nexus*` exists under /git [ran: ls]; "Dotos" is the `dotos` repo; "datom" is a symlink to `datomic`.

## 3a. Anatomy: protos, datomic, ethos-zero (at origin/main) [ran: `git show origin/main:<file>` + grep/sed; line counts by `wc -l` on the shown blobs]

Each is a **single-file crate**: one `src/lib.rs`, a self-describing `<crate>.ethos` at the repo root, a `flake.nix`, README/ARCHITECTURE/UPGRADES/AGENTS, and one or two integration test files. No build.rs anywhere in the three.

### protos 0.15.1 (origin/main 4806136; checkout is 0.14.0 — a different crate)

Files: `src/lib.rs` 1068, `protos.ethos` 26, `tests/delineation.rs` 573 (37 `#[test]` + a proptest regressions file), `tests/situated.rs` 40 (2 tests), ARCHITECTURE.md 83, UPGRADES.md 83, README.md 52, flake.nix 32. Cargo: edition per rust-toolchain.toml; no LiGoldragon deps (dev: proptest) [read: Cargo.toml at origin/main].

Types (lib.rs:14–296): `pub type Text = String; Integer = i64; Decimal = f64; Boolean = bool; Symbol = Text;` `struct Extent(Integer, Integer)`; `type Path = Vec<Integer>`; `type Situation = BTreeMap<Path, Extent>`; `enum Separator { Period, Exclamation, Colon }` (+ `fn glyph(self) -> char`); `enum Enclosure { Braced, Bracketed, Guillemets, Angled }`; `enum Boundary { CurlyQuotes, Parentheses }`; `enum Head { Bare(Symbol), Qualified(Symbol, Vec<Protoform>) }`; `enum Protoform { Headed(Head, Separator, Box<Protoform>), Enclosed(Enclosure, Vec<Protoform>), Opaque(Boundary, Text), Bare(Symbol), Qualified(Symbol, Vec<Protoform>) }`; `struct Delineation { protoforms: Vec<Protoform>, situation: Situation }`; `struct Fault { extent: Extent, problem: Problem }`; `enum Problem { Unclosed(Enclosure), UnclosedBoundary(Boundary), Unopened, MissingBody, MissingHead, EmptyInput }`; `struct Potential<T, C = ()>(Text, PhantomData<fn() -> (T, C)>)` (From<Text>, From<&str>, `text()`); `struct Situated<F>(pub Option<Extent>, pub F)`.

Kinds (traits, lib.rs:298–343):
- `trait Structural { fn delineate(&self) -> Result<Delineation, Fault>; }` — impl for `Text` and `Potential<()>`
- `trait Printing { fn print(&self) -> Text; }` — impl for `Head`, `Protoform`, `Delineation`
- `trait Protosizable { fn protosize(&self) -> Protoform; }`
- `trait Conceptual<C: Protosizable> { type Fault; fn conceive(&self) -> Result<C, Self::Fault>; }`
- `trait Corporal<C: Protosizable>: Embodied { type Fault; fn incorporate(concept: C) -> Result<Self, Self::Fault>; }`
- `trait Actualizable<T: Embodied> { type Fault; fn actualize(&self) -> Result<T, Self::Fault>; }` — blanket `impl<C, T> Actualizable<T> for Potential<T, C> where C: Protosizable, T: Corporal<C>, Delineation: Conceptual<C>, T::Fault: From<Fault> + From<<Delineation as Conceptual<C>>::Fault> + Pathed { type Fault = Situated<T::Fault>; }` (text → delineate → conceive → incorporate, faults situated by path → extent)
- `trait Pathed { fn path(&self) -> &[Integer]; }`
- `trait Situating { fn situate(&self, path: &[Integer]) -> Option<Extent>; }` — impl for `Delineation`
- `trait Embodied: Sized {}` with blanket `impl<T: Sized> Embodied for T {}`

The delineator (lib.rs:~540–935) is a private recursive-descent reader over chars: `;` line comments, whitespace, the four enclosures, the two boundaries, `Head<sep>body` headed forms, `Name<...>` qualified heads, paths recorded per protoform into `Situation`. The five "dialects" named in the protos skill are not a code concept here; **protos knows no Datom** — the Datom concept type lives in datomic (`impl Conceptual<Datom> for Protoform/Delineation` is in datomic).

`protos.ethos` (whole, origin/main):

```
; protos.ethos — the substrate's own declaration
Library.{0 15 0}
[]
[ Text Integer Decimal Boolean
  Symbol.Text
  Extent.{ Integer Integer }
  Path.Vector<Integer>
  Situation.« Path Extent »
  Separator.[ Period Exclamation Colon ]
  Enclosure.[ Braced Bracketed Guillemets Angled ]
  Boundary.[ CurlyQuotes Parentheses ]
  Protoform.[ Headed.{ Symbol Separator Protoform }
              Enclosed.{ Enclosure Vector<Protoform> }
              Opaque.{ Boundary Text }
              Bare.Symbol ]
  Delineation.{ Vector<Protoform> Situation }
  Fault.{ Extent Problem }
  Problem.[ Unclosed.Enclosure UnclosedBoundary.Boundary Unopened MissingBody MissingHead EmptyInput ] ]
[ Structural.[ delineate.[ Result<Delineation Fault> ] ]
  Printing.[ print.[ Text ] ]
  Protosizable.[ protosize.[ Protoform ] ]
  Conceptual<Protosizable>.{ [] [ Fault ] «» [ conceive.[ Result<Protosizable Fault> ] ] }
  Actualizable<Embodied>.{ [] [ Fault ] «» [ actualize.[ Result<Embodied Fault> ] ] }
  Situating.[ situate.{ [ Path ] [ Option<Extent> ] } ]
  Embodied.[] ]
[ Text.[ Structural ]  Protoform.[ Printing ]  Delineation.[ Printing Situating ] ]
```

Note the drift already visible between the file and the code: the `.ethos` still says `Situation.« Path Extent »` (guillemet map) and lacks `Head`/`Qualified`/`Corporal`/`Pathed`/`Situated`, which the Rust has (0.15.1 added them) — the declaration is behind the crate [inferred by comparing the two blobs].

### datomic 0.9.1 (origin/main 4712361; checkout 0.9.0 differs only by the protos pin) [ran]

Files: `src/lib.rs` 1252, `datomic.ethos` 20, `tests/datomic.rs` 705 (37 `#[test]` + 1 `proptest!` block), ARCHITECTURE.md 50, UPGRADES.md 89, README.md 51, flake.nix 73. Cargo: `protos = { git, rev = "48061367872b" }`; dev: proptest, rust_decimal-free (Decimal is f64).

Re-exports (lib.rs:8) every protos kind and type: `Actualizable, Boolean, Boundary, Corporal, Decimal, Delineation, Embodied, Enclosure, Extent, Integer, Path, Pathed, Potential, Printing, Protoform, Protosizable, Separator, Situated, Situating, Structural, Symbol, Text`.

Types: `enum Datom { Variant(Symbol, Separator, Option<Box<Datom>>), Struct(Vec<Datom>), Vector(Vec<Datom>), Map(Vec<Pair>), Text(Text), Meaning(Text), Bare(Symbol) }`; `struct Pair(Datom, Datom)`; `enum Meaning { Plain(Text) }`; `enum Expected { Variant, Struct, Vector, Map, Text, Meaning, Integer, Decimal, Boolean, Bare }`; `enum Problem { Shape(Expected, Datom), Arity(Integer, Integer), UnknownVariant(Symbol), Separator(Separator), Value(Text), Pairing, DuplicateKey(Datom), OneValue }`; `enum Fault { Structural(protos::Fault), Conceptual(Path, Problem), Corporal(Path, Problem) }` (impl `From<protos::Fault>`, `Pathed`, private `Prepending::prepend`).

Kinds: `pub trait Datomic: Corporal<Datom, Fault = Fault> { fn datomize(&self) -> Datom; }` — **a type is "datomic" when it can be incorporated from a Datom (Corporal, faulting with datomic::Fault) and can datomize itself back**; `pub trait Textualizable { fn textualize(&self) -> Text; }` with blanket `impl<T: Datomic> Textualizable for T` (datomize → protosize → print). Private helper kinds: `Conceiving::conceive_at(&self, path)` for `Protoform`, `VariantChaining`, `BareSafety`, `IntegerParsing`. `impl Protosizable for Datom`; `impl protos::Conceptual<Datom> for Protoform` and `for Delineation` (type Fault = Fault) — so `Potential<T, Datom>::actualize()` works for every `T: Datomic`.

Datomic impls shipped (lib.rs:477–1260): `Integer, Boolean, Decimal, Text, Meaning, Vec<T: Datomic>, BTreeMap<K: Datomic+Ord+Clone, V: Datomic>, Option<T>, Result<T, E>, Expected, Problem, Fault, Separator, Enclosure, Boundary, Extent, protos::Problem, protos::Fault, Datom (identity), Situated<F: Datomic>` (datom `{ Option<Extent> <F> }`), and `macro_rules! impl_datomic_box { ($t:ty) }` (exported) generating `Corporal<Datom>` + `Datomic` for `Box<$t>` — used by ethos-zero's emitter for recursive enums.

`datomic.ethos` (whole, origin/main):

```
; datomic.ethos
Library.{0 9 0}
[ protos:[ Text Integer Decimal Boolean Symbol Separator Protoform Delineation Path Extent Potential Protosizable Conceptual Actualizable Printing Embodied ] ]
[ Datom.[ Variant.{ Symbol Separator Option<Datom> }
          Struct.Vector<Datom>
          Vector.Vector<Datom>
          Map.Vector<Pair>
          Text.Text
          Meaning.Text
          Bare.Symbol ]
  Pair.{ Datom Datom }
  Meaning.[ Plain.Text ]
  Fault.[ Structural.protos:Fault Conceptual.{ Path Problem } Corporal.{ Path Problem } ]
  Situated.{ Option<Extent> Fault }
  Problem.[ Shape.{ Expected Datom } Arity.{ Integer Integer } UnknownVariant.Symbol Separator.Separator Value.Text Pairing DuplicateKey.Datom OneValue ]
  Expected.[ Variant Struct Vector Map Text Meaning Integer Decimal Boolean Bare ] ]
[ Datomic.{ [ Embodied ] [] «» [ incorporate:{ [ Datom ] [ Result<Self Fault> ] } datomize.[ Datom ] ] }
  Textualizable.[ textualize.[ Text ] ] ]
[ Datom.[ Protosizable ] Protoform.[ Conceptual<Datom> ] Potential<Datomic>.[ DatomicActualizable ] Datomic.[ Textualizable ]
  Integer.[ Datomic ] Decimal.[ Datomic ] Boolean.[ Datomic ] Text.[ Datomic ] Meaning.[ Datomic ] Vector<Datomic>.[ Datomic ] Option<Datomic>.[ Datomic ] Result<Datomic Datomic>.[ Datomic ] Map<Datomic Datomic>.[ Datomic ] Situated<Datomic>.[ Datomic ] ]
```

Its four sections are imports `[ protos:[ Text Integer … Embodied ] ]`, the types above, the kinds `Datomic.{ [ Embodied ] [] «» [ incorporate:{ [ Datom ] [ Result<Self Fault> ] } datomize.[ Datom ] ] }` and `Textualizable.[ textualize.[ Text ] ]`, and the associations `[ Datom.[ Protosizable ] Protoform.[ Conceptual<Datom> ] Potential<Datomic>.[ DatomicActualizable ] Datomic.[ Textualizable ] Integer.[ Datomic ] … Situated<Datomic>.[ Datomic ] ]`. It declares `Library.{0 9 0}` while Cargo says 0.9.1 [read].

### ethos-zero 1.3.1 (origin/main 0f19896; checkout 1.2.0 lacks the Copy derives and the e2e fix) [ran]

Files: `src/lib.rs` 2149, `src/main.rs` 185 (bin `ethos-zero`, 4 unit tests), `src/generated.rs` 41 KB **one unformatted line, not referenced by any `mod` in lib.rs** — it is the checked-in self-bootstrap artifact that `tests/file_contract.rs::bootstrap_module_is_fresh` regenerates from `ethos-zero.ethos` and compares (`"src/generated.rs is stale: re-run the emitter on ethos-zero.ethos"`); `ethos-zero.ethos` 25; `fixtures/example-library.ethos` 13; `fixtures/orchestrate.ethos` 20; `tests/file_contract.rs` 1156 (51 `#[test]` + proptest generators `arb_type_expression/arb_variant/arb_type_declaration/arb_library`); ARCHITECTURE.md 135, README.md 69, UPGRADES.md 82, flake.nix 68. Cargo: `[lib] name = "ethos_zero"`, `[[bin]] name = "ethos-zero"`; deps protos@48061367, datomic@4712361c, syn 3 (full), quote 1, proc-macro2 1; dev rkyv 0.8.

Concept types (lib.rs:34–172): `struct Version(i64, i64, i64)`; `enum Import { Single{source,name}, Multiple{source,names} }`; `enum TypeExpression { Named(String), Applied{..}, SelfType }`; `enum Variant { Unit, Typed, InlineStruct, InlineEnum }`; `enum TypeDeclaration { Struct, Enum, Alias, Map }`; `enum Receiver { Shared, Mutable, None }`; `struct Capability { name, receiver, inputs: Vec<TypeExpression>, output }`; `struct AssociatedType { name, constraints }`; `struct AssociatedConstant`; `struct KindConstraint`; `enum KindDeclaration { Simple{..}, Complex{ …superkinds, associated types, associated constants, capabilities } }`; `struct Association { type, kinds }`; `struct SectionReference { name, type }`; `struct Library { version, imports, types, kinds, associations }`; `struct Signal { version, imports, requests, replies, types }`; `enum Concept { Library(Library), Signal(Signal) }`; `struct Potential(String)` (From<&str>/String, `text()`); `struct RustLibrary(String)`; `struct Fault { extent: Extent, problem: Problem }`; `enum Problem { Protos, Root, Version, Section, Import, Declaration, TypeExpression, Capability, Kind, Association, Emission }` (Display + std::error::Error).

Kinds: `pub trait Actualizing { fn actualize(&self) -> Result<Concept, Fault>; }` (impl for `Potential`, lib.rs:614 — delineate with protos, then walk the protoforms into `Concept`); `pub trait Emitting { fn emit(&self) -> Result<String, Fault>; }` (impl for `Concept`, lib.rs:1145–1912 — `quote!`-built Rust: type aliases for `X.Text`, tuple structs for `{ … }`, enums for `[ … ]`, `pub trait` for kinds, and for every type an `impl datomic::Corporal<datomic::Datom>` + `impl datomic::Datomic`; recursive enums get `Box` + `impl_datomic_box!`; intrinsic names emit fully qualified (`protos::Text`, `datomic::Datom`); imported names qualify by their import source; unit-only enums derive `Copy`; Library types derive `Clone, Debug, PartialEq, Eq`). For a `Signal` root the emitter additionally emits `struct Version(u16,u16,u16)`, `const SIGNAL_VERSION`, `enum Refusal`, `enum Body`, `struct Frame(Version, Body)` and their datomic impls (lib.rs:1914–2060) — the wire envelope. `impl protos::Conceptual<Concept> for datomic::Datom` and `impl Protosizable for Concept` (lib.rs:211–227) make a Concept round-trip through datom text (`canonical_file_prints_to_itself`, `*_round_trips_through_protosize` tests).

**Generation pipeline** [read: main.rs]: `ethos-zero` with no argument prints the canonical form of its own `ethos-zero.ethos` (`include_str!`); with one datom argument `Generate.{ “<file-path>” “<out-dir>” }` it reads the file, `Potential::from(source).actualize()`, `concept.emit()`, rustfmt's via a piped `rustfmt`, writes `<out-dir>/<file-stem>.rs` for a Library or `<out-dir>/signal.rs` for a Signal, and prints `Generated.[ “<path>” ]`; every failure is a datom `GenerationFailure.{ “…” }` on stderr; flags are refused. Consumers (signal-orchestrate, meta-signal-orchestrate, orchestrate, curriculum-deploy, claude-answers) **commit the emitted file** under `src/generated/` and keep it honest with a `tests/regeneration.rs` (or `client_freshness.rs`) that calls the ethos-zero *library* (`Potential::from(ETHOS_SOURCE).actualize()?.emit()?`) and compares — no build.rs, no OUT_DIR, no network at build time for generation.

`ethos-zero.ethos` (whole, origin/main — the language describing itself):

```
; ethos-zero: the ethos schema language, version zero
Library.{1 1 0}
[]
[ Potential.Text
  Concept.[ Library.Library Signal.Signal ]
  Library.{ Version Vector<Import> Vector<TypeDeclaration> Vector<KindDeclaration> Vector<Association> }
  Signal.{ Version Vector<Import> Vector<SectionReference> Vector<SectionReference> Vector<TypeDeclaration> }
  Version.{ Integer Integer Integer }
  Import.[ Single.{ Text Text } Multiple.{ Text Vector<Text> } ]
  TypeExpression.[ Named.Text Applied.{ Text Vector<TypeExpression> } SelfType ]
  Variant.[ Unit.Text Typed.{ Text TypeExpression } InlineStruct.{ Text Vector<TypeExpression> } InlineEnum.{ Text Vector<Variant> } ]
  TypeDeclaration.[ Struct.{ Text Vector<TypeExpression> } Enum.{ Text Vector<Variant> } Alias.{ Text TypeExpression } Map.{ Text TypeExpression TypeExpression } ]
  Receiver.[ Shared Mutable None ]
  Capability.{ Text Receiver Vector<TypeExpression> TypeExpression }
  AssociatedType.{ Text Vector<Text> }
  AssociatedConstant.{ Text TypeExpression }
  KindConstraint.{ Text Vector<Text> }
  KindDeclaration.[ Simple.{ Text Vector<KindConstraint> Vector<Capability> } Complex.{ Text Vector<KindConstraint> Vector<Text> Vector<AssociatedType> Vector<AssociatedConstant> Vector<Capability> } ]
  Association.{ Text Vector<Text> }
  SectionReference.{ Text TypeExpression }
  Fault.{ Integer Integer Text } ]
[ Actualizing.[ actualize.[ Result<Concept Fault> ] ]
  Emitting.[ emit.[ Result<Text Fault> ] ] ]
[ Potential.[ Actualizing ]
  Concept.[ Emitting ] ]
```

The file format as evidenced by the six `.ethos` files read (protos, datomic, ethos-zero, example-library, signal-orchestrate, meta-signal-orchestrate) [inferred]: a `;` comment head; a root `Library.{ major minor patch }` or `Signal.{ … }` **still carrying a version triple**; then for a Library four bracket sections — imports (`[]`, `[ protos:Text ]`, or `[ protos:[ A B … ] ]`), types, kinds, associations — and for a Signal five — imports, requests, replies, types (the ordering differs from the Library's). Types: `Name` alone (intrinsic), `Name.Type` (alias), `Name.{ A B Vector<C> }` (positional struct), `Name.[ V  W.T  X.{ … }  Y.[ … ] ]` (enum with unit / typed / inline-struct / inline-enum variants), `Name.« K V »` (map — the guillemet map the landed Vision dropped), `Name<Param>` (generic). Kinds: `Kind.[ cap.[ Output ] ]` (shared receiver), `cap!{ [ In ] [ Out ] }` (mutable receiver, `!` separator), `cap:[ Self ]` (static, `:` separator), and the complex form `Kind<P>.{ [ superkinds ] [ associated types ] «constants» [ capabilities ] }`. Associations: `Type.[ Kind Kind ]`. Meanings (comment-like values that survive as data) are `(…)` in datom text and `Meaning` in the type language. The self-description declares `Library.{1 1 0}` while Cargo says 1.3.1 [read] — versions in the files are not maintained.

`fixtures/orchestrate.ethos` (20 lines, a Signal fixture) and `fixtures/example-library.ethos` (13 lines, using `push!{…}`, `drain![…]`, `create:[ Self ]`, `Roles.«Text Integer»`) are the emitter's test inputs; `fixture_signal_generated_rust_compiles_and_round_trips_values` and `fixture_library_meaning_round_trips_in_e2e` write a throwaway cargo project and `cargo check` it (the latter is the test that fails at the 1.2.0 checkout, section 4).

### Old Ethos vs Ethos Zero, from the evidence [read: READMEs and estate blocks]

`core-ethos` README: "owns the strict bootstrap Ethos reader and its purpose-built Interface, Nexus, and Sema semantic forms … five authorities that must never collapse (TextualMetadataSnapshot …)"; `schema-rust` README: "the verified bootstrap generation boundary for Interface and Sema Ethos documents … revalidated and lowered by Core Nomos into Whole Logos. Rust Logos then projects it"; `ethos-engine` estate: "central-storage daemon embryo". That is the old Ethos: a multi-crate authority/lowering pipeline (core-ethos → core-nomos → core-logos → rust-logos, with sema-translator, name-table, content-identity), reading a `.ethos` whose surface was Interface/Nexus/Sema documents, projected through `dotos` text and `signal-frame` wire — all now `incorrect-new / frozen reference`. Ethos Zero is one 2149-line crate: text → protos delineation → datom → `Concept` → `quote!` Rust, self-described by one file, with the datom trait pair (`Corporal`/`Datomic`) as the only generated behaviour.


### Additions relayed from the delegated anatomy agent (Fable, read-demanding; it read both revisions of the three crates) [relayed]

- Build instructions per README: protos, datomic and ethos-zero all say `nix flake check -L` (Crane) as the durable gate and `cargo test` (`--locked` in protos) as the fast witness.
- protos 0.14.0 → 0.15.1 delta (`git diff --stat HEAD origin/main`: 10 files, +1592/−1934): the generic `Text<T>` struct became `pub type Text = String` plus `Potential<T, C>`; `Portion` became `Protoform` with the new `Head` enum; `ContentHash`, the `Symbol` newtype, `Bare/Headed/StructuralEnclosed/OpaqueEnclosed/Enclosed`, `StructuralEnclosure/OpaqueBoundary/DialectBoundary` were removed; the five-variant `Enclosure` split into `Enclosure` (4) + `Boundary` (2); thirteen old traits (Delineatable, Embodiable, Embodied, Textualizable, ShapeDefined, ContentHashable, BareSafe, PortionText, ScalarAnatomy, EnclosedArity, EnclosedAnatomy, DelineatedText, Printing) became the nine listed above; `Situation`/`Situating`/`Situated<F>` are new. `tests/delineation.rs` went from 13 to 37 tests; `tests/situated.rs` (2 tests) is new. Neither revision of protos mentions Datom (grep: zero hits).
- datomic: `src/lib.rs` is byte-identical between the 0.9.0 checkout and 0.9.1 main (only the protos pin and version moved). Its 37 tests are listed by name in the agent's return (scalar/container round trips, six proptests, the `vision_*` struct/enum examples, fault self-description, `box_query_recursive_round_trips`, `situated_fault_*`).
- ethos-zero 1.2.0 → 1.3.1 (+133/−28): private helpers `all_variants_unit()` / `enum_derive()` add `Copy` for unit-only enums; `src/generated.rs` is **empty (0 bytes) at the checkout and populated (41 KB) at main**; public API unchanged. The agent counted 48 test functions in `tests/file_contract.rs` (this subflow's grep counted 51 `#[test]` tokens; the difference is presumably the tokens inside the e2e source strings the tests write — not verified) plus 4 in `main.rs`. Emission internals it named: `emit_tokens` (lib.rs:1153), `type_declaration_tokens` (1201), `datomic_impl_tokens` (1437), `kind_declaration_tokens` (1646), `capability_method_tokens` (1755), `association_assertion_tokens` (1790, compile-time assertions that associated types implement their kinds), `section_enum_tokens` (1814) and `wire_envelope_tokens` (1884) for Signals; readers `read_protoform_as_concept` (638), `read_library` (650), `read_signal` (661).
- Every `.ethos` file in the stack repos (bytes): protos/protos.ethos 4102 (checkout; 26 lines at main), datomic/datomic.ethos 1345, ethos-zero/ethos-zero.ethos 1527, ethos-zero/fixtures/example-library.ethos 427, ethos-zero/fixtures/orchestrate.ethos 671, orchestrate/ethos/client.ethos 242, orchestrate/ethos/meta_client.ethos 252, curriculum-deploy/curriculum-deploy.ethos 1173, claude-answers/claude-answers.ethos 246, signal-orchestrate/ethos/signal.ethos 754, meta-signal-orchestrate/ethos/signal.ethos (this subflow: 17 lines). Generated Rust checked in: ethos-zero `src/generated.rs`; orchestrate `src/generated/{client,meta_client}.rs`; curriculum-deploy `src/generated.rs` (+ `src/generated_ext.rs` at the checkout, deleted at main 2a1c337 per its subject); signal-orchestrate and meta-signal-orchestrate `src/generated/signal.rs`; claude-answers (not listed by the agent; its main commit says "regenerate" — not verified which file).
- Old Ethos, as the agent read it: `core-ethos` lib.rs is a single `pub mod bootstrap` ("Strict bootstrap Ethos reading for the Protos language family"), depending on content-identity, name-table, raw-discovery, structural-codec, rkyv; `ethos-engine` is a kameo actor daemon ("EncodedEthos daemon and thin CLI") over core-ethos, schema-language, signal-ethos, signal-sema-storage, tokio. Ethos Zero replaces the authority-sealed, identity-tracked, two-phase (plan → seal) bootstrap and its daemon with one crate that reads Protos text into a `Concept` and emits Rust.

## 3b. Anatomy: orchestrate, signal-orchestrate, meta-signal-orchestrate

### orchestrate 0.29.2 (checkout = main 885f6e3) [relayed: build agent, read + ran find/wc]

File tree (lines): AGENTS.md 80, ARCHITECTURE.md 165, Cargo.toml 48, CLAUDE.md 49, `ethos/client.ethos` 9, `ethos/meta_client.ethos` 9, flake.nix 122, README.md 134, UPGRADES.md 226, skills.md 14, NON_IDEAL_AGENTS.md 16, `src/lib.rs` 7, `src/main.rs` 25 (bin `orchestrate-nexus`), `src/bin/orchestrate.rs` 102 (bin `orchestrate`), `src/bin/meta_orchestrate.rs` 106 (bin `meta-orchestrate`), `src/bin/orchestrate_upgrade_preflight.rs` 24, `src/defaults.rs` 99, `src/ordinary.rs` 48, `src/store.rs` 509, `src/transport.rs` 313, `src/generated/client.rs` 102, `src/generated/meta_client.rs` 102, `tests/client_freshness.rs` 55, `tests/live_nexus.rs` 461, `tests/ordinary_lock_contract.rs` 203.

Public items: `lib.rs` — mods `defaults, ordinary, store, transport`; re-exports `DefaultConfiguration, LegacyStorePreflight, OrchestrateStore, PreflightsLegacyStore`. `defaults.rs` — `struct DefaultConfiguration { store_path, configuration }` with `from_process() -> Result<Self, DefaultConfigurationError>`, `store_path(&self) -> &Path`, `configuration(&self) -> Configure`; `enum DefaultConfigurationError { StartupArguments, MissingRuntimeDirectory, MissingHomeDirectory, RelativePath }`. `ordinary.rs` — `trait Locks { fn lock(&mut self, LockRequest) -> Result<OrdinaryOutcome, StoreError> }`, `trait Releases { fn release(&mut self, lock_id: i64) -> Result<OrdinaryOutcome, StoreError> }`, `trait Observes { fn observe(&self, ObserveSelection) -> Result<Observation, StoreError> }`, `trait IdentifiesLock { fn lock_id(&self) -> &i64 }`, `enum OrdinaryOutcome { Reply(Reply), Refusal(Refusal) }`. `store.rs` — `struct OrchestrateStore` with `open(store_path, defaults) -> Result<(Self, Configure), StoreError>`, `ordinary(&mut self, request) -> Result<OrdinaryOutcome, StoreError>`, `meta(&mut self, request) -> Result<MetaReply, StoreError>`; `enum StoreError` (12 variants); `struct LegacyStorePreflight`; `trait PreflightsLegacyStore`. `transport.rs` — `async fn run(configure, store) -> Result<(), TransportError>`, `struct TransportRuntime`, `struct OrdinarySignalTransport`, `struct MetaSignalTransport`, `enum TransportError` (7 variants). Generated: `src/generated/client.rs` / `meta_client.rs` (`// @generated by ethos-zero`) each carry `enum ClientFailure { Unreadable, Unreachable, Refused }` with `Corporal`/`Datomic` impls, from the two 9-line `.ethos` files (which import protos, datomic, signal_orchestrate).

Wiring [relayed, read]: requests are `signal_orchestrate::Request { Lock(LockRequest), Release(LockId), Observe(ObserveSelection) }`, replies `Reply { Locked(Lock), LockRejected(LockRejection), Released(Lock), ReleaseRejected(ReleaseRejection), Observed(Observation) }`; nexus sockets `$XDG_RUNTIME_DIR/orchestrate-nexus/orchestrate.sock` and `.../meta-orchestrate.sock`; the CLI reads `ORCHESTRATE_SOCKET` (meta: `ORCHESTRATE_META_SOCKET`); the store is a sema-engine file at `$XDG_STATE_HOME/orchestrate-nexus/orchestrate-nexus.sema` (fallback `~/.local/state/orchestrate-nexus/`). The installed wrapper `/home/li/.nix-profile/bin/orchestrate` is a bash script exporting `ORCHESTRATE_SOCKET="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/orchestrate-nexus/orchestrate.sock"` then exec'ing `/nix/store/pnwkgajkgzlipvg38yyp1xzngc2nkl08-orchestrate-0.27.0/bin/orchestrate` — **the installed client is 0.27.0 while the repo is 0.29.2** [relayed: `which`/`cat`].

Tests: 14 `#[test]` — store.rs 2 (preflight), ordinary_lock_contract.rs 4 (lock/release cycle, duplicate name + path overlap rejection, observation ordering, id monotonicity across restart), live_nexus.rs 6 (zero-arg startup, meta configuration persistence, CLI datom round trip, ethos dump on no-arg, error output format, malformed frame rejection), client_freshness.rs 2 (generated client/meta_client match ethos-zero emission).

### signal-orchestrate (origin/main f366d6a, 0.20.1) [ran: `git show origin/main:…`]

Files: AGENTS.md, ARCHITECTURE.md, CLAUDE.md, Cargo.toml, README.md, UPGRADES.md, `ethos/signal.ethos` (31 lines), flake.nix, `src/codec.rs` (57), `src/generated/mod.rs`, `src/generated/signal.rs` (590), `src/lib.rs`, `tests/contract.rs` (3 tests: `all_datom_roots_round_trip`, `spaced_reason_uses_curly_quotes`, `rkyv_frame_round_trips_with_version_validation`), `tests/regeneration.rs` (1 test `committed_module_matches_ethos_zero_generation`: reads `src/generated/signal.rs`, calls the ethos-zero library `concept.emit()`, rustfmt's, asserts equality). **No build.rs on main** (the checkout's build.rs and its `ethos-monolith` build-dependency are gone: main generates by test, not by build script).

`lib.rs`: `pub mod codec; pub mod generated; pub use codec::*; pub use generated::signal::*; pub const ETHOS_SOURCE: &str = include_str!("../ethos/signal.ethos");`

`codec.rs`: `pub trait SignalFrameCodec: Sized { fn encode_length_prefixed(&self) -> Result<Vec<u8>, FrameCodecError>; fn decode_length_prefixed(bytes: &[u8]) -> Result<Self, FrameCodecError>; }`, `pub enum FrameCodecError { LengthPrefixMissing, LengthMismatch{expected,found}, LengthTooLarge, ArchiveEncode, ArchiveDecode, VersionMismatch{expected: Version, found: Version} }`, `impl SignalFrameCodec for Frame` (checks `self.0 != SIGNAL_VERSION`).

`generated/signal.rs` (`@generated`): `type LockId = protos::Integer; type LockName/FlowId/LockPath/LockReason = protos::Text;` `struct LockRequest(LockName, FlowId, Vec<LockPath>, LockReason)`, `struct Lock(LockId, LockName, FlowId, Vec<LockPath>, LockReason)`, `struct LockOverlap(LockPath, Lock)`, `enum LockRejection { DuplicateName(Lock), PathOverlap(LockOverlap) }`, `enum ReleaseRejection { UnknownLockId }`, `enum ObserveSelection { Locks }`, `enum Observation { Locks(Vec<Lock>) }`, `enum Request { Lock(..), Release(..), Observe(..) }`, `enum Reply { Locked, Released, Observed, LockRejected, ReleaseRejected }`, `struct Version(u16,u16,u16)`, `enum Refusal`, `enum Body`, `struct Frame(Version, Body)`; every type gets `impl datomic::Corporal<datomic::Datom>` and `impl datomic::Datomic`.

The `.ethos` file whole (origin/main `ethos/signal.ethos`):

```
; Orchestrate Lock signal — the ordinary wire contract.
;
; The Lock family: acquire, release, observe coordination locks.
; Every lock carries an integer id, a name, a flow, absolute paths,
; and a reason.

Signal.{ 1 0 0 }

[]

[ Lock.LockRequest  Release.LockId  Observe.ObserveSelection ]

[ Locked.Lock  Released.Lock  Observed.Observation
  LockRejected.LockRejection  ReleaseRejected.ReleaseRejection ]

[ LockId.Integer
  LockName.Text
  FlowId.Text
  LockPath.Text
  LockReason.Text
  LockRequest.{ LockName FlowId Vector<LockPath> LockReason }
  Lock.{ LockId LockName FlowId Vector<LockPath> LockReason }
  LockOverlap.{ LockPath Lock }
  LockRejection.[ DuplicateName.Lock  PathOverlap.LockOverlap ]
  ReleaseRejection.[ UnknownLockId ]
  ObserveSelection.[ Locks ]
  Observation.[ Locks.Vector<Lock> ] ]
```

Shape as evidenced [inferred from the file]: `;` line comments; a root header `Signal.{ major minor patch }` (the version triple); then four bracketed sections in order — imports (`[]` here), requests (`Name.Type`), replies, and the type declarations, where `X.Text`/`X.Integer` are aliases, `X.{ A B Vector<C> }` a positional product, `X.[ V.T  W ]` a sum. This is the shape the 1a6ca4 log already notes the landed Vision has moved past (no version triple, no map, imports first, Corporate/Incorporable).

### meta-signal-orchestrate (origin/main 3ae11c1, 0.14.1) [ran]

Same file set (codec.rs, generated/signal.rs 366 lines, `ethos/signal.ethos` 17 lines, tests/contract.rs 2 tests, tests/regeneration.rs 1 test, no build.rs). Ethos: `Signal.{ 1 0 0 }`, requests `[ Configure.Configure ]`, replies `[ Configured.Configure  ConfigurationRejected.ConfigurationRejection ]`, types `OrdinarySocketPath.Text  MetaSocketPath.Text  Configure.{ OrdinarySocketPath MetaSocketPath }  ConfigurationRefusal.[ InvalidConfiguration ]  ConfigurationRejection.{ Configure ConfigurationRefusal }`. Generated: `type OrdinarySocketPath/MetaSocketPath = protos::Text`, `struct Configure(..)`, `enum ConfigurationRefusal`, `struct ConfigurationRejection(Configure, ConfigurationRefusal)`, `enum Request`, `enum Reply`, `Version`, `Refusal`, `Body`, `Frame`.

### The stale checkouts of the two signal crates [relayed: build agent]

At the `/git` checkouts (6fc8c5b / d4dd208, 2026-08-26) these crates are the **previous generation**: generated by `ethos-monolith` via `build.rs`, `signal-orchestrate` depending on `signal-frame`, `datom@4e13442b`, `protos@3b190f9f`, with a `WireContract` (ContractId 1, WireRevision 5) and `signal_channel!` macro; `meta-signal-orchestrate` on `dotos` + `signal-frame` with a `dotos-text` feature. Nothing running consumes them (orchestrate main pins the new revs), but any agent that `cd`s into `/git/github.com/LiGoldragon/signal-orchestrate` sees this old tree plus 4 uncommitted files from 2026-09-04 11:02.

## 4. Build state (at the `/git` checkouts, `cargo` from PATH, not nix) [relayed: build agent; it ran the commands]

| crate | `cargo check` | `cargo test` |
|---|---|---|
| protos (0.14.0 checkout) | pass, 0.03s | pass: 13 passed (tests/delineation.rs) |
| datomic (0.9.0 checkout) | pass, 0.23s (fetches protos 0.15.0 @56c683ec) | pass: 37 passed, 1 doc-test ignored |
| ethos-zero (1.2.0 checkout) | pass, 2.26s | **1 failed / 47 passed**: `fixture_library_meaning_round_trips_in_e2e` spawns `cargo check` on a generated e2e binary; protos 0.15.0 made `Text` a plain `pub type Text = String`, so the fixture's `Text<Meaning>` and `.embody()` no longer compile (`E0107`, `E0599`). main's 0f19896 "fix e2e test; bump 1.3.1" names exactly this fix [inferred from the commit subject]. |
| orchestrate (main) | pass, 9.32s; resolves protos 0.15.1, datomic 0.9.1, ethos-zero 1.3.1, signal-orchestrate 0.20.1, meta-signal-orchestrate 0.14.1, sema-engine 0.15.1, signal-frame 0.3.1, signal-sema 0.2.0, sema 0.1.1 — all from git | pass: 12 passed (2 client_freshness, 6 live_nexus, 4 ordinary_lock_contract) |

Every repo has a `flake.nix`; the READMEs are Nix-centric but the agent used cargo directly. Not built: the worktrees, the main tips of the three stale crates (they are what orchestrate main fetches and compiles, so `cargo check` in orchestrate is indirect evidence that protos 0.15.1 / datomic 0.9.1 / ethos-zero 1.3.1 compile together).

## 5. Live flows and who holds what

### 5.1 Orchestrate locks [relayed: live-flows agent ran `orchestrate 'Observe.Locks'` at 01:08; reply quoted]

```
Observed.Locks.[ { 639 DialectSkills 6329f1 [ /home/li/wt/github.com/LiGoldragon/Curriculum/Curriculum-DialectSkills-6329f1 ] "draft protos datom ethos skills on Curriculum branch" } { 440 WisprAuthWitness run_wispr_live_witness [ /home/li/wt/github.com/LiGoldragon/listener/listener-wispr-auth-witness ] "[create isolated workspace for one authorized witness]" } { 441 WisprEdgeProxy implement_wispr_edge_proxy [ /home/li/wt/github.com/LiGoldragon/listener/listener-wispr-edge-proxy-01a05588 ] "[implement offline EdgeProxy witness in isolated workspace]" } { 726 WisprRecorderFlowArtifacts acf06f [ /home/li/primary/flows/acf06f/log.md /home/li/primary/flows/acf06f/vision/wisprInteraction.md /home/li/primary/flows/index.md ] "Record remembered flow, microphone feedback vision, and flow index" } ]
```

Only lock 639 (flow 6329f1) touches the stack, and its path is a Curriculum worktree directory that is **no longer a registered git worktree** (stale dir, mtime 2026-09-04 12:16) [ran]. No lock covers protos, datomic, ethos-zero, orchestrate, signal-orchestrate, meta-signal-orchestrate, curriculum-deploy, claude-answers or lojix. Lock 726 (acf06f) holds `/home/li/primary/flows/index.md`.

Two nexus daemons are running [relayed: `ps`, `/proc/*/environ`]: PID 3016866 since 09-04 11:05, cwd `/home/li/primary`, binary from `.../orchestrate-rehearsal-6329f1/result/bin/orchestrate-nexus` (a 6329f1 rehearsal build); and PID 3716515 since 09-04 23:41, the systemd-managed 0.27.0 from the Nix store with `STATE_DIRECTORY=/home/li/.local/state/orchestrate-nexus`. Which one the wrapper's socket reaches was not verified; the lock reply above came through the wrapper.

### 5.2 Processes [relayed: live-flows agent ran `ps`, `readlink /proc/PID/cwd`]

Eleven `claude` processes, all cwd `/home/li/primary` (started 09-02 17:27 remote-control service; 09-03 17:53, 18:48; 09-04 12:21, 17:24, 17:26, 19:29, 21:09; 09-05 00:37, 00:41, 00:52 = this flow). Six `codex` processes, all `--cd /home/li/primary` (app-server since 09-04 13:10; sessions 18:39, 20:23 ×2 resumed, 21:11 resumed, 21:35). A `nix build .#codex` (PID 3756987, from 00:48) runs under session 58a86d. No cargo/rustc processes in the stack repos at survey time.

### 5.3 Sessions modified in the last 6 h [relayed: live-flows agent read `~/.claude/projects/-home-li-primary/*.jsonl` first user messages and trailers]

| session file | flow | first message (gist) | trailer |
|---|---|---|---|
| 1a6ca4f9-… | 1a6ca4 | run through the whole stack again, rewrite datom / Ethos Zero, then orchestrate, then port | session_01182yAjLqfw2fqP76zrtPy5 (this flow) |
| 7fba5fce-… | 7fba5f | markdown-then-subflow web report protocol → skill | session_01JCxf1rJegU2a18XcmSSt9p |
| e996e87c-… | e996e8 | remember 6329f1, resume Protos/Ethos declaration distillation | session_013aB57L3R5esQRFTBCHGjzV |
| 58a86d99-… | 58a86d | update Claude desktop app (CriomOS-home) | session_018igMmqtqWgUeLB39vmaP1s |
| b9a334a4-…, ad19b1ad-…, 6329f1fb-…, 7b4d4ce2-… | b9a334, ad19b1, 6329f1, 7b4d4c | earlier stack-vision flows, files touched within 6 h | — |

Codex: ~50 files under `~/.codex` modified in 6 h; the large rollouts (01a06dee 21:38 26.7 MB, 01a06dd9 21:15 23.8 MB) open with plugin-recommendation prompts; 01a06da9 (20:23, 11 MB) is the Wispr flow. None names a stack repository in its opening message [relayed].

### 5.4 Flows open in `flows/index.md` [ran: tail of each log; index has no date column]

The last twelve index rows are ad19b1, 444e5e, 6329f1, 81c0dc, e996e8, 01a06da9, 7b4d4c, b9a334, 4e296a, 7fba5f, acf06f, 1a6ca4. Last log lines: **e996e8** "Awaiting the living: review of the landed texts (Corporate and the third-section sentence…)" — open, and it is the flow landing the Vision this flow reads; **7fba5f** "Awaiting the ruling; nothing landed in the Curriculum" — open; **b9a334** "Published (…)" — effectively done; **6329f1** "Landed (relayed…): Vision/protos.md replaced…" — its last logged act; its lock 639 and three worktrees remain; **58a86d** (no index row) "Sent the running update subflow the desktop bump…" — live, CriomOS-home only; **acf06f** — open, Wispr (lock 726); **1a6ca4** — this flow.

**Flows that touch the stack repositories right now**: none has a lock or a live edit in `/git/github.com/LiGoldragon/{protos,datomic,ethos-zero,orchestrate,signal-orchestrate,meta-signal-orchestrate,curriculum-deploy,claude-answers,lojix}` [inferred from: no lock paths there; all those trees clean except the 09-04 11:02 signal-orchestrate edits and the pre-08-13 signal/mind edits; no cargo processes]. 6329f1 still **holds** (lock 639) the Curriculum dialect-skills directory and **owns** the three registered worktrees (`ethos-zero-keepgoing-6329f1`, `orchestrate-keepgoing-6329f1`, `curriculum-deploy-ProtoformStack-6329f1`) plus the scratchpad worktree of ethos-zero; whether its session is still active was not established (its session file was touched within 6 h; no claude process could be tied to it by cwd, since all share `/home/li/primary`). e996e8 and 7fba5f write only under `/home/li/primary` (`Vision/`, `flows/`, `vision-raw/`). acf06f holds `flows/index.md` — **any index edit by 1a6ca4 collides with lock 726**.

## 6. The "unknown session" 01JCxf1rJegU2a18XcmSSt9p and commit bd577bde9

Witnessed [ran: `jj op log`, `jj op show 5a6ffd31dc32`, `git log --grep`]:

- `/home/li/primary` is jj-colocated. jj op `5a6ffd31dc32` at 01:05:10.329 ran: `jj commit -m 'Flow 1a6ca4: log the brief and the vision spoken before acting  Co-Authored-By: … Claude-Session: https://claude.ai/code/session_01JCxf1rJegU2a18XcmSSt9p' -- flows/1a6ca4/log.md flows/1a6ca4/vision/{datom,flow,mind,nexus,personaMetaHarness,psyche,thinkingMachineProcedures}.md`. Its result: `+ rvrmvnlm bd577bde (empty) Flow 1a6ca4: …` — jj itself marks the commit empty, because 79 ms earlier (op `327cf4c39363` 01:05:10.249 "import git head") this flow's own git commit 18feab40b had already committed the same files.
- Every other commit carrying trailer `01JCxf1rJegU2a18XcmSSt9p` is a flow 7fba5f commit (03467667e 00:46 "open the flow", a8980dfd4 01:05:22, 329d59548 01:06:38) or a "dirty changes found" commit (d4c577bd8 01:04:35 "Distill datom Map section…", which is e996e8's work). The live-flows agent found the same trailer in `~/.claude/projects/-home-li-primary/7fba5fce-ba77-4302-8360-e470233ae26f.jsonl` and eight of its subagent files, and 7fba5f's log says its subflow "found other flows' dirty snapshots in the tree (the ad19b1/e996e8 distillation, 1a6ca4) and committed them first, named for their flows" [relayed].
- No hooks: `~/.claude/settings.json` has no `hooks` key; `/home/li/primary/.claude/` holds only `agents/` and `skills/`; no crontab; no systemd unit/timer that commits [ran; relayed].

So: **session 01JCxf1rJegU2a18XcmSSt9p is flow 7fba5f's main session** (it has been committing through `jj commit` since 00:46), and bd577bde9 is its CLAUDE.md-mandated "dirty changes found in the tree are committed first, as their own commit" step racing this flow's `git commit` within the same second on the shared working copy. jj's working-copy snapshot is what "staged" the files. Not a hook, cron or companion. It also explains why this repo's git HEAD keeps ending up detached (jj exports move `main`; a plain `git commit` on top leaves HEAD off the bookmark until jj's next "import git head").

The collision hazard for the main flow is therefore general: **every flow in `/home/li/primary` shares one working copy and one jj store**, and any of them (7fba5f, e996e8, acf06f, 58a86d) may commit 1a6ca4's unstaged files under 1a6ca4's name at any moment. Stack repositories under `/git` are separate git repos and do not have this problem, but they do share the `/git` checkouts with 6329f1's leftovers.

## 7. What this map settles for dispatch (this subflow's reading) [inferred]

1. Start any rewrite from `origin/main` of each stack repo, not from the `/git` checkouts: protos at `/git` is the pre-rewrite 0.14.0, the two signal crates are the ethos-monolith generation. A dispatched agent that opens `/git/github.com/LiGoldragon/protos/src/lib.rs` reads the wrong crate. Either move the checkouts to main (that is a git-state change nobody has locked, but 6329f1's worktrees hang off ethos-zero, orchestrate and curriculum-deploy and would be unaffected) or work in fresh worktrees.
2. The train is a chain of exact git revs: protos → datomic → ethos-zero → {signal-orchestrate, meta-signal-orchestrate} → orchestrate, and → {curriculum-deploy, claude-answers}. A datom/ethos-zero rewrite forces a re-pin + regenerate + freshness-test pass in the five consumers, in that order; the regeneration tests are the mechanism that detects staleness.
3. No live flow holds any stack repository. The only stack-adjacent lock is 639 (6329f1, a Curriculum dialect-skills directory that is no longer a worktree). Lock 726 (acf06f) holds `flows/index.md`.
4. The shared `/home/li/primary` working copy is jj-managed and four other sessions commit there; expect "dirty changes found" commits of 1a6ca4 files by 7fba5f/e996e8-style sessions, and detached-HEAD states after plain `git commit`.
5. The installed `orchestrate` client is 0.27.0 (Nix store) against a repo at 0.29.2; two nexus daemons run (a 6329f1 rehearsal build from 09-04 11:05 and the systemd 0.27.0 from 23:41). Which one owns `$XDG_RUNTIME_DIR/orchestrate-nexus/orchestrate.sock` was not verified.
6. `lojix`, `signal-ethos-zero`, `meta-signal-ethos-zero` are the only consumers on the 08-29 protos/datomic line; everything else on the old stack goes through `schema-rust`/`core-ethos`/`dotos`/`signal-frame`, and `mind` carries 21 uncommitted files from 2026-07-31 that any port must reckon with.

## Sources

- Repository state: `git status/branch/log/worktree/rev-list/ls-tree/show` run by this subflow in every `/git/github.com/LiGoldragon/<repo>` named above, 2026-09-05 01:00–01:25 CEST.
- Dependency edges: `grep` over `/git/github.com/LiGoldragon/*/Cargo.toml` (checkouts) and `git show origin/main:Cargo.toml` (stack crates), run by this subflow.
- Estate status: `## Protos estate status` blocks in `AGENTS.md`/`README.md` of every repo, grep'd by this subflow; the block text read from `/git/github.com/LiGoldragon/dotos/AGENTS.md`.
- Core-crate anatomy: `git show origin/main:src/lib.rs`, `:src/main.rs`, `:tests/*`, `:*.ethos`, `:fixtures/*.ethos`, `:Cargo.toml` in protos, datomic, ethos-zero, signal-orchestrate, meta-signal-orchestrate, read by this subflow.
- Orchestrate anatomy, the installed wrapper, and all build/test runs: a delegated read agent (Fable, read-demanding) that ran `find/wc`, `cargo check`, `cargo test` in the four `/git` checkouts and read the files it cites; relayed here.
- Locks, processes, sessions, hooks: a delegated read agent (Fable, read-demanding) that ran `orchestrate 'Observe.Locks'`, `ps`, `/proc/*/cwd`, `find ~/.claude/projects ~/.codex -mmin -360`, grep of session files, and read the settings files; relayed here. This subflow independently read `~/.claude/settings.json` (no `hooks` key) and listed `/home/li/primary/.claude/`.
- The bd577bde9 question: `jj op log`, `jj op show 5a6ffd31dc32`, `jj workspace list`, `git log --grep=<trailer>`, `git reflog` in `/home/li/primary`, run by this subflow.
- Flow state: `/home/li/primary/flows/index.md` and the last line of `flows/{6329f1,e996e8,b9a334,7fba5f,58a86d,1a6ca4}/log.md`, read by this subflow.
