# The Golden Bridge — charter for the minimal new language engine

**This document is the sole charter for a fresh Codex session (the ChatGPT-side
agent, gpt-5.6) working in the `/home/li/primary` workspace. Read it whole before
touching anything. It is written to be self-contained: nothing here needs a prior
session's memory, and every fact carries an artifact behind it.**

Authored 2026-07-16 by Claude (Opus 4.8, generalist), session
`LanguageFamilyPrototype`, lane `EngineCharter`. It changes no source; it is the
pickup surface for the engine work tracked as bead **`primary-56d1.34`**
("Minimal new engine end-to-end: all components as real daemons, fully
scaffolded — Codex-owned, many agents many slices"). The psyche does not read
reports; this file is the agent pickup point, so it is written for you, the
implementing agent, not for him.

A note on language, because tonight the psyche ruled that manager/agent talk had
drifted into unexplained invented words: **every coined name in this document is
explained in plain words the first time it appears. A name is never an
explanation.** Carry that same discipline into everything you write back to the
psyche.

## 1. Mission

Tonight (2026-07-16) the psyche settled what he means by "the golden bridge," and
it is not what the agents built. His words, verbatim, are the mission statement.

**What "the golden bridge" means to him** (bead `primary-56d1.27` comment,
2026-07-16 13:03, verbatim):

> "to me the golden bridge was an expression to speak of a minimally implemented,
> but real all-components (daemons) fully scaffolded system"

**The order** (2026-07-16 chat, verbatim):

> "lets get codex to implement it - he can use many agents in many slices - we
> just want the minimally working new engine e2e - create a deep context for him;
> ill start him on a fresh session"

**The standing lean grant** (bead `primary-56d1.27` / epic comment, 2026-07-16
09:39, verbatim):

> "Im also ready for multiple slices going with the agent leans; to get a working
> prototype; leans can be revised afterwards"

**The system-level acceptance relaxation** (epic `primary-56d1` comment,
2026-07-16 13:03, verbatim — the hedge is load-bearing and must be preserved):

> "well, thats asking much. maybe if it gets compiled independantly, with same
> deps, and gives the same lib crate?"

### The mission restated in plain words

Build the minimally working new language engine, end to end, as **real running
daemons** — one long-lived background process per component of the language
system — every component present, each minimally implemented, all wired together
through their message contracts, and demonstrably carrying one real document all
the way from text to generated, independently compiling Rust. "Minimally
implemented" means each daemon does the smallest real version of its job, not a
stub that fakes it. "Fully scaffolded" means no component is missing: the whole
shape of the system stands up, even if thinly.

**Why this needs saying at all.** Tonight the term "golden bridge" was found to
have meant two different things. The agents, reading a phrase of Codex's, built a
**migration proof**: a small test that carries one legacy schema file through the
new pipeline in a single process and checks the output byte-for-byte. That proof
is real and valuable (it is the `golden-bridge` repository, described in §3), but
it is a test harness, not a system. The psyche meant the second thing: the real,
scaffolded, all-daemons system above. **This charter is for his meaning.** The
migration proof stands as completed substrate you will reuse, not as the thing
being asked for.

## 2. Psyche vision and rulings digest

This is the settled ground the engine sits on. Where a psyche statement is
load-bearing it is quoted verbatim; everything else is a plain-language
restatement of a settled or accepted position. Sources are named so you can
re-verify: `reports/logos/up-close-design-v1.md` (the design authority, called
"up-close" below), `reports/logos/vision-evidence-ledger-v1.md` (the evidence
ledger that classifies what is truly ruled versus merely proposed),
`reports/logos/core-first-architecture-v1.md`, the two signal-contract design
reports under `reports/schema/`, and the epic bead `primary-56d1` with its
children.

### 2.1 The stack and its orientation

The language system is a pipeline of five layers. In plain terms:

- **NOTA** — the base textual notation and its reader. NOTA is positional
  (records are read by position, not by labels), delimiter-based, and knows only
  raw shape (atoms, brackets, application) before any meaning is assigned. The
  reader crate is `nota`.
- **schema** — the layer where a person declares types (structs, enums,
  newtypes). A `.schema` document is authored here.
- **Nomos** — the transformation language. "Nomos" is the psyche's name for the
  layer of **macros**: typed data that rewrites one Core representation into
  another (schema declarations into Rust-shaped data). A macro here is data, not
  arbitrary code.
- **Logos** — the layer that models a fixed subset of Rust as exploded,
  fully-desugared, strictly-typed positional **data**. Logos is one-to-one with
  Rust.
- **generated Rust → rustc** — Logos data is projected to Rust source text, which
  the ordinary Rust compiler then compiles.

The orienting slogan, verbatim from the psyche's handover (evidence ledger L0):
**"Rust is our assembly language."** Logos is one-to-one with Rust; the fixed
lowering from Logos to Rust is the small kernel that every dialect ultimately
reduces into. Rust is the target you compile down to, the way assembly is the
target a compiler emits.

### 2.2 Core-first: the substance is the data, text is a bridge

The single most important orientation, verbatim from the handover (evidence
ledger L0, and `core-first-architecture-v1.md` §0):

> the Core aspect — the in-memory and in-database true logical representation — is
> the essential substance; the text is a bridge.

"Core" (capital C) is the name, ruled tonight (see §2.5), for the **canonical,
strictly-typed, binary, stringless data** representation of any layer —
`CoreSchema`, `CoreNomos`, `CoreLogos`. It is stored with `rkyv` (a Rust library
that serializes typed values to a fixed portable binary layout) and is the true
form of the language. Text is a projection of Core for three purposes only:
authoring, letting a language model read and write it, and bootstrap compiling —
until in-daemon Core editing matures enough that text becomes viewing-only.

The end-state the psyche describes, verbatim from his core-first statement
(`core-first-architecture-v1.md` §2.3): **the direct in-schema-daemon and in
nomos/logos daemons editing, snapshotting, and version-controlling** of Core —
each language layer becomes a daemon that edits Core directly (not by
re-parsing its own text), and gets snapshotting and version control from the
storage engine it sits on. This sentence is the seed of the whole target system
(§4): the components are daemons because the psyche wants editing, snapshotting,
and version control to happen inside daemons, on Core, seated on the storage
engine.

### 2.3 Stringless Core via NameTables, and the identity keystone

- **Stringless Core** (ruled, evidence ledger L1, verbatim: "all Core\* have no
  strings, they use the corresponding NameTable"). A Core value carries no text.
  Every human name in it is an integer index. The mapping from index to spelling
  lives in a separate **NameTable** — an append-only table that interns a name and
  hands back a small integer (`Identifier`). The NameTable is a sidecar: never
  embedded in a Core value, never part of a Core value's identity.
- **The identity keystone** (ruled, evidence ledger L2). A Core value's identity
  is a `blake3` content hash (`blake3` is a fast cryptographic hash) taken over
  its canonical stringless binary bytes, under a domain-separated,
  layout-version-tagged context, **with the NameTable excluded from the
  pre-image**. The consequence the psyche wants: **renaming something does not
  move its identity** (the spelling is not in the hash), while a structural edit
  (adding a field, changing a type) does move it. This is the keystone because the
  whole "text is a bridge" claim rests on it — text can evolve without disturbing
  Core identity.

### 2.4 Structural tables and the many-forms Textual family

- A complex Core type is paired with a **structural table** that drives both
  directions of its text conversion — decode (text → Core) and encode (Core →
  canonical text) from one table (ruled in principle, evidence ledger L7,
  verbatim: the table is used for "both encoding and decoding"). The reader never
  guesses what a piece of text means; the **expected type** at each boundary
  selects the table, and the raw layer only discovers shape (ruled, handover
  ruling 5).
- **Textual is a family of forms** (ruled, evidence ledger L11, verbatim):

  > "actually, we extend the textual to have many forms, so corelogos has both the
  > logos and rust textual form data-trees ... this even opens us emitting other
  > languages than rust from logos."

  So one Core is viewed through several **Textual** forms. `CoreLogos` is viewed
  through both a `TextualLogos` form (the Logos surface text) and a `TextualRust`
  form (actual Rust source). Each is a two-way codec. A third target language
  would be a third form. "Textual" simply means "a text rendering of a Core"; it
  replaced an earlier, rejected word "True" (evidence ledger L13, verbatim: "true
  made no sense for any of them. It's just textual").

### 2.5 Terminology and naming rulings

- **`True*` → `Textual*`** (settled, up-close §9 Fork B). There is no `True`
  anywhere; the text-side types are `TextualSchema` / `TextualNomos` /
  `TextualLogos` / `TextualRust`.
- **`StructuralForm`, and `macro` reserved for Nomos** (settled, up-close §9 Fork
  A). The parser-side conversion-pattern data is called a **StructuralForm** (a
  "structural form": data describing what shape of text a Core type expects). The
  word "macro" is kept for Nomos transformations only, so the two ideas do not
  blur. Verbatim: "instead of saying structural macro, we say structural form."
- **Core versus sema — the naming ruling** (settled tonight, bead
  `primary-56d1.25`, 2026-07-16 10:12, verbatim):

  > "a - sema will be more complete and correct than core; we are laying the
  > foundation for it."

  Meaning: **Core** stays the name of the canonical stringless data layer — every
  `Core*` type prefix stays. **sema** names the durable storage/runtime component
  (which is why the storage engine is already named `sema`). His orientation: sema
  is the more complete and correct layer whose foundation this engine is laying.
  **No renames anywhere.** Do not rename `Core*` to `sema*` or vice versa.

### 2.6 Visibility, document kinds, and the central authority

- **Visibility is Schema-authoritative** (ruled tonight, bead `primary-56d1.29`,
  2026-07-16 10:11, verbatim: **"agreed"**). The public/private visibility a
  declaration carries in Schema Core is the source of truth; Nomos must lower it
  faithfully into generated Rust; CoreLogos stores the final visibility
  explicitly. A schema `Private` must not be silently dropped to `Public`.
- **Document kinds, accepted with review-later** (ruled tonight, epic and bead
  `primary-56d1.4` comments, 2026-07-16 09:40, verbatim):

  > "yes - and we can review the design later; easy to work with once it's all
  > up."

  The accepted direction: **four distinct Core document kinds — TypeSchema,
  SignalContract, NexusRuntime, SemaStorage — sharing generic declaration
  records; Signal owns Stream plus the opens/belongs relations; Sema owns
  Family.** In plain terms, a `.schema` file's first line will declare which kind
  of document it is, so the reader never guesses. This is accepted **as a
  direction to review later**, not as a frozen design — treat it as ground you may
  build on, not as settled detail. (See the caution on the over-settled v2 report
  in §7.)
- **The central-authority premise** (ruled tonight, verbatim, recorded in
  `core-signal-contract-handoff-v1.md` §0):

  > "then we cannot have a coordination-free universe; I never believed in such
  > idealist fantasies."

  Meaning: identifier allocation cannot be a free-for-all where every daemon mints
  its own ids independently — that recreates collisions. There is a single logical
  allocation authority. The manager's proposed shape (given to the psyche in chat,
  **ruling still pending**): that authority is **seated in the sema storage/runtime
  component**, and the language daemons are clients that hold **leased blocks of
  ids** — each daemon is granted a range to allocate from, rather than minting
  freely. **Amendment (2026-07-17):** the seat is no longer pending — the psyche
  ruled it (bead `primary-56d1.11`, comment recorded 2026-07-16 23:50), verbatim:
  **"yes, seat it centrally in sema."** That settles allocation-authority
  *placement*: a single logical allocation authority per sema deployment, seated
  centrally in sema, with the language daemons as leasing clients that hold leased
  identifier blocks — exactly the shape proposed above, now ruled rather than
  pending. The broader lineage semantics (the unit of "one schema", split/merge
  identity) advanced on the same bead out of blocked-on-psyche into actionable
  design; the "must not be hardened" caution just below now applies only to that
  remaining lineage detail, not to the seat. **This frame must not be hardened beyond this.** The formal lineage
  ruling — what the unit of "one schema" is, and how identity survives split and
  merge — is **blocked on the psyche** (bead `primary-56d1.11`; his open question,
  verbatim: "so where is the authority? In each corresponding daemon?"). Until he
  rules, every daemon stays on an explicit **fixture universe** (a single fixed
  allocation scope hard-wired for the prototype), exactly as the existing `core-*`
  crates already do. Do not invent split/merge lineage policy.

## 3. What exists today

By tonight the entire transformation kernel is already built, green, and pushed —
this is the substrate you assemble into daemons, not code you write from scratch.
All repositories live under `/home/li/primary/repos/<name>`, are Jujutsu-colocated
Git repos on a `main` bookmark, and depend inward by **pinned Git revision** (never
by local path). The pins below are the current tips verified 2026-07-16; re-read
tips at pickup in case a repo advanced.

### 3.1 The nine transformation crates (all closed and flake-green)

These nine are "the nine-crate next-generation language family" named in
`reports/logos/stack-re-audit-v1.md`. Each is a single-crate repo whose acceptance
witness is `nix flake check` (Nix owns the durable test evidence). Dependencies run
strictly downward, so stringless Core never depends on text.

| Crate (repo) | Pin | What it is |
| --- | --- | --- |
| `content-identity` | `6cc0408` | The dependency leaf (only `rkyv` + `blake3`). Owns the portable-archive bound, `ContentHash<Domain>`, and the domain/layout tags. The identity keystone (§2.3) lives here. |
| `name-table` | `c3237f7` | The stringless identifier space: `Identifier` (a `u32` index), the append-only `NameTable` interner, transactional interning (a failed decode leaves no name allocated), and name-derivation helpers. |
| `raw-discovery` | `a4e8c6d` | The language-agnostic raw structure layer: a `Recognizer` reads text into raw `Block`s (atoms, delimiters, application) and never classifies meaning. Lifted from the `nota` parser. |
| `structural-codec` | `104f924` | The Core-associated, bidirectional, revisioned StructuralForm kernel with the **trusted evaluator that ships in the runtime** (settled, up-close §9 Fork C): tables are data the evaluator executes directly, both decode and encode from one form. |
| `structural-codec-derive` | `348bd89` | The generated-codec side: an attribute macro `#[structural_form(...)]` that emits an optimized concrete codec per type. Conformance tests prove the generated codec and the evaluator agree. |
| `core-schema` | `566544e` | The first real stringless Core schema layer, and the first real Textual form (`TextualSchema`). Owns `CoreSchema`, `CoreDeclaration`, `CoreType`, `CoreReference` (which dispatches on kind/projection, never on a head string), `Visibility`, and the `CoreUniverse` codec bridge. |
| `core-logos` | `17cbd75` | The stringless Core algebra of Logos — Rust-as-data, one-to-one with Rust, entirely text-free (no `syn`, no `quote`). |
| `textual-rust` | `b0ea9fb` | The `TextualRust` form codec: the two-way bridge between actual Rust text and `core-logos`. Reads Rust with `syn` (a Rust parser library) and writes byte-exact Rust with `prettyplease` (a deterministic Rust formatter, the sole formatting authority). |
| `core-nomos` | `88a1ecf` | The stringless Core of Nomos, the macro/transformation language, and the five-language pipeline capstone: a macro is typed data that lowers a `CoreSchema` into a `CoreLogos`. |

Dependency shape (allowed source dependencies, not data-flow direction):
`content-identity` and `raw-discovery` are leaves; `name-table` sits on
`content-identity`; `structural-codec` sits on `raw-discovery` + `name-table`;
`core-schema`/`core-logos`/`core-nomos` sit on `content-identity` + `name-table`
(and the codec crates for their Textual forms). No Core crate depends upward on a
Textual, parser, `syn`, or formatter crate.

### 3.2 The golden-bridge repository — the one-capability migration proof

`golden-bridge` (pin `03929a4`, public at `github.com/LiGoldragon/golden-bridge`)
is the migration proof described in §1 — valuable completed substrate, but a **test
harness, not a system**. Precisely (bead `primary-56d1.30`, done and byte-exact):

- It is **one capability**, in three source files (`src/lib.rs`, `src/error.rs`,
  `src/ingest.rs`) — not literally one file, but one focused job. Its public
  surface is `LegacySchemaIngest`, `Migration`, `Exclusion`, `BridgeError`.
- It **reuses the legacy parser** rather than hand-rolling one: it parses a legacy
  `.schema` with `schema-language`'s own parser, then translates the already-parsed
  model object-to-object into the new stringless `CoreSchema` + `NameTable`,
  carrying no strings across (every legacy name is re-interned).
- Its **byte-exact witness** is `tests/spirit_bridge.rs`: it migrates the real
  `spirit-min.schema` through the whole new vertical
  (`legacy text → ingest → CoreSchema → core-nomos macros → CoreLogos →
  TextualRust → Rust`) and asserts the six in-subset declarations (`Topic`,
  `Description`, `Summary`, `RecordIdentifier`, `Entry`, `Query`) reproduce the
  legacy generated bytes exactly, with four out-of-subset declarations as loud
  typed exclusions. The witness is the full `nix flake check`.

**Amendment (2026-07-17):** The frozen `golden-bridge` witness above remains the
six-in-subset / four-loud-exclusion proof at its pin. The delivered
`language-engine-witness` (§4.3) since carried this same `spirit-min.schema` fixture
through **all ten declarations byte-exact** against the legacy golden — the four
formerly out-of-subset declarations now migrate exactly rather than standing as named
exclusions. Read the six-subset boundary here as golden-bridge's frozen historical
scope, not the live engine's current reach.

This vertical is the **transformation spine your daemons will carry live.** The
engine's job is to make each stage of that spine a running daemon with state seated
on the storage engine and messages flowing between daemons — the same
transformation, but as a scaffolded system rather than a single in-process test.

### 3.3 The schema-language / schema-rust next-gen migration (held on branches)

Two legacy build-time crates were migrated to the next-generation NOTA grammar and
verified green, but are **deliberately held on feature branches, not landed to
main** (bead `primary-oay8`):

- `schema-language` — next-gen branch `language-family-nextgen-schema-language` at
  pin **`41a7b257dddbcaebf151a053c6fd43324a2a8e39`** (commit subject:
  "schema-language: migrate structural decoding to next-gen NOTA"). Its `main` tip
  is `59d59ac`.
- `schema-rust` — next-gen branch `language-family-nextgen-schema-rust` at pin
  **`a92a9d0e2940b4debed74a2f7d06ea44c4360c99`** (commit subject: "schema-rust: pin
  next-gen schema closure"). Its `main` tip is `87de872`.

Both are built on the `nota` **next-gen** branch tip
**`18e2e8d0dba37e9e84045af3608585b51f6e3b36`** (bookmark `next-gen`; nota v0.8.0,
which includes the revised string-rejoin behavior). Useful context: compiling the
un-migrated `schema-rust` main against nota `18e2e8d0` produces exactly 13 compile
errors (10 non-exhaustive-match, 3 method-not-found from new nota enum variants);
the migrated branch resolves all 13 to zero, and the generated-Rust golden corpus
stays byte-identical to `schema-rust @ 87de872`. These branches are held because a
concurrent lane (**`LojixCanonicalMigration`**) is migrating `schema-language` main
toward a *different* nota revision — the canonical v0.7.0 tip
`f8de7a5` — so landing the next-gen branch to main would clobber it; and because
mainline merges are gated on the train's whole-closure order (§6). **Do not land
these to main; consume them by pinned rev if you need them.**

### 3.4 The earlier core-signal-contract handoff — now subordinate to this charter

`reports/schema/core-signal-contract-handoff-v1.md` is a detailed, source-cited
implementation brief for the **signal-contract component** — the daemon-side
representation of a signal contract (its streams and its opens/belongs relations).
**It is now subordinate to this charter and serves as that one component's detailed
spec** (recorded on bead `primary-ezut`, 2026-07-16 13:03). One thing in it is
explicitly **superseded**: its long analysis of "own crate versus fold into
`core-schema`" is resolved — **crate placement becomes a lean inside this engine's
system design, not a standalone open question.** The psyche's own criterion governs
it: a crate exists when it is shared by multiple crates (otherwise it can live
inside an existing one). Read that handoff for the exact stream/relation record
shapes, the identity-domain reasoning, and the byte-exact signal goldens when you
build the signal-contract component; take its component-boundary conclusion as a
revisable lean.

### 3.5 The storage seat

- `sema` (pin `51d7927`) — the durable **storage kernel**: a `redb`-backed,
  `rkyv`-archived, typed-and-version-guarded key/value store. This is the literal
  on-disk seat of durable state.
- `sema-engine` (pin `71508ca`) — the **runtime engine** over that kernel:
  `Engine` composes `sema` and executes typed record-family operations. Its
  versioned, hash-chained commit log is the authoritative source of truth; the
  materialized store is a rebuildable view folded from the log. It is library-only
  (no daemon, no sockets). This is what the psyche means by seating each language
  daemon "on sema-engine" — a daemon mounts its Core state through this engine and
  inherits snapshotting, version control, and log-replay for free
  (`core-first-architecture-v1.md` §2.3).

### 3.6 The message-contract substrate (existing, reused)

The workspace already runs dozens of daemons on a shared component pattern
(§4.1). The shared wire-frame codec is `signal-frame`, and each component has a
`signal-<name>` contract crate. A `signal-schema` contract crate already exists.
`signal-nomos` and `signal-logos` are called for by bead `primary-56d1.4`
("signal-nomos and signal-logos contract crates", still open). Verify current
pins of these at pickup; the evidence ledger's `signal-schema` / `signal-frame`
pins date to 2026-07-15 and may have moved.

## 4. The target system

### 4.1 The ruled component shape (ground this in the `component-architecture` skill)

Every component in this workspace has one fixed shape, and the engine's daemons
must follow it. Load the `component-architecture` and `actor-systems` skills before
building; the essentials:

- A stateful component = **one runtime crate (the daemon) + one thin CLI + one
  public message contract crate named `signal-<component>`** (plus an optional
  owner-policy contract `meta-signal-<component>` only if configuration needs its
  own authority boundary). The daemon owns state, logic, the process, and the CLI.
  The contract crate owns only the wire vocabulary and codecs — no actors, no
  runtime state, no daemon startup.
- Inside the daemon, three runtime planes, and a request flows through them in
  order and returns on the same typed path:
  - **Signal** admits framed requests, checks the caller shape, returns the typed
    reply. ("Signal" = the admission/wire plane; also the name of the contract
    family.)
  - **Nexus** owns async mail, external effects, fanout, and timeouts — it turns a
    request's intent into executable work. ("Nexus" = the coordination plane.)
  - **SEMA** owns durable single-writer state and commits the legal transition.
    (Here "SEMA" is the state plane inside a daemon; it is seated on the
    `sema-engine` storage described in §3.5. Same word, two scopes — the plane and
    the storage engine — because the plane commits into that engine.)
- **Actors mark correctness boundaries** (the `actor-systems` skill). A plane that
  owns state, ordering, IO, or supervision is an actor with a real data-bearing
  type carrying its state between messages — not a zero-sized forwarder. Durable
  state lives behind one single-writer owner; readers consume snapshots or
  subscribed views, they never mutate the store. The runtime here is **Kameo** (an
  actor runtime for Rust); follow the `kameo` skill's lifecycle discipline,
  especially the spawn-in-thread restart trap.
- **Push, not pull** (the `push-not-pull` skill). Where one daemon must learn of
  another's results, design a subscription where the producer pushes events;
  do not poll.
- **Typed storage and typed binary wire, NOTA as human projection** (the
  `rust-storage-and-wire` skill). State lives in typed stores; daemon-to-daemon
  traffic is a typed binary contract; NOTA text is the human-facing projection at
  the edges, never the transport between components.

### 4.2 The minimal component list, derived from the psyche's own words

The psyche named the components himself: the in-**schema**-daemon, and the in-
**nomos**/**logos** daemons, doing editing/snapshotting/version-control, each
seated on the storage engine (§2.2). That yields the minimal engine as four
daemons plus their contracts, all seated on one storage seat:

1. **The schema daemon.** Owns `CoreSchema` state (stringless type declarations +
   its NameTable) for one document, seated on `sema-engine`. It accepts a schema
   document as text, holds it as Core, and can edit / snapshot / version-control it
   as Core. Wraps `core-schema` (and, for legacy text ingestion, the
   `golden-bridge` ingest path). Public contract: `signal-schema` (exists).
2. **The nomos daemon.** Owns `CoreNomos` macro packages. It applies macros to a
   `CoreSchema` to expand it into a `CoreLogos` (the `core-nomos`
   `MacroPackage::apply` step). Public contract: `signal-nomos` (bead
   `primary-56d1.4`).
3. **The logos daemon.** Owns `CoreLogos` state (Rust-as-data). It projects
   `CoreLogos` to generated Rust text through the `TextualRust` form
   (`textual-rust`, i.e. `syn`/`prettyplease`). Public contract: `signal-logos`
   (bead `primary-56d1.4`).
4. **The sema seat.** The durable storage/runtime component the other three sit on,
   and the single logical **id-allocation authority** (§2.6). For the prototype it
   stays fixture-universe: it hands each daemon a fixed allocation scope; it does
   **not** implement split/merge lineage (blocked on `primary-56d1.11`). This may
   be realized as `sema-engine` mounted per-daemon plus a thin allocation-authority
   surface — Codex's structural call, recorded as a lean.

**The ruled component layer** the daemons expose (from the accepted next-slice
direction, bead `primary-56d1.27`): each daemon's signal surface should be able to
**list its slots** (enumerate the documents/types it currently holds) and serve
**hash-addressed fetch** (return a value by its content hash — the §2.3 identity).
Conversions between stages run in two topologies: a **pull** topology (a consumer
asks a producer to convert and return) and a **push** topology (a producer pushes
converted results to subscribers, per push-not-pull). All state seated on the sema
engine. Keep this minimal for the prototype — a real slot-list and a real
hash-fetch on each daemon, one working conversion path between each adjacent pair.

**The signal-contract component** (§3.4) is present in the fuller system as the
daemon-side representation of a signal contract document (the `SignalContract`
document kind). For the *minimal* end-to-end witness it is not on the critical path
— the witness runs the plain `TypeSchema` path (schema → nomos → logos → Rust). If
Codex chooses to include the signal-contract slice in the first prototype (it is a
ready, fully-specified slice), fold it in as a parallel document kind; otherwise
carry it as the next component after the witness is green.

### 4.3 The end-to-end witness (what "working" means concretely)

The minimal demonstrable flow, which is the acceptance object for bead
`primary-56d1.34`:

> A real schema document enters the **schema daemon** as text and comes to rest
> there as `CoreSchema` (stringless Core + NameTable), its state seated on the sema
> engine. The **nomos daemon**, given that `CoreSchema` (fetched across the signal
> contract), applies its macros and produces a `CoreLogos`. The **logos daemon**
> holds that `CoreLogos` as Rust-as-data and emits generated Rust text through
> `TextualRust`. That generated Rust is then **compiled independently, with the
> same dependencies, into an equivalent library.** Throughout, daemon state lives on
> the sema engine and the signal contracts carry the mail between daemons.

Use the `golden-bridge` fixture (`spirit-min.schema`, whose six-declaration subset
is already proven to migrate byte-exact) as the first document through the live
daemons, so the transformation is known-good and only the daemon scaffolding is new.

**Amendment (2026-07-17):** The live witness now proves **all ten declarations** of
this fixture migrate byte-exact end-to-end (`tests/e2e.rs`, "all ten declarations
preserve the free byte-exact witness"), superseding the six-declaration subset noted
above; the byte-exact reach is the full fixture, not a subset.

### 4.4 System-level acceptance (preserve the hedge)

Per the psyche's relaxation tonight (§1, verbatim "maybe if it gets compiled
independantly, with same deps, and gives the same lib crate?"), the **system-level**
acceptance for the minimal engine is:

- the generated code **compiles independently** (as its own crate),
- **with the same dependencies**,
- exposes the **same public surface** (the same lib crate / public API), and
- **behaves the same** under shared tests.

It is **not** byte-for-byte text identity at the system level. Byte-for-byte
identity remains only as the **pipeline-internal witness where it is already free
and passing** — that is, the `golden-bridge` / `textual-rust` per-item byte
comparison, which already holds and costs nothing to keep asserting. Preserve the
psyche's hedge: this relaxation is recorded as a **hedged lean** ("maybe"), not a
settled ruling, and is revisable. Do not treat "same public surface, same behavior"
as licence to let the generated text drift where it need not; keep the free
byte-exact witness green, and claim the relaxed criterion only where byte-identity
genuinely costs more than it is worth.

## 5. Slice decomposition

This is a **suggested** parallel slice graph. Restructuring it is Codex's
prerogative — the psyche explicitly granted "many agents in many slices." The point
is to show what can proceed concurrently, what gates what, and where the existing
crates plug in unchanged. Every existing crate in §3 plugs in **as a pinned library
dependency, unchanged** — no slice edits the nine crates, `golden-bridge`, or
`sema`/`sema-engine` to make a daemon fit; if a shared crate genuinely must change,
that is a separate claim plus manager coordination (§6).

**Foundational (start first, unblocks the daemons):**

- **S0 — the sema seat + fixture-universe id authority.** A thin component that
  mounts `sema-engine` per daemon and hands out fixed allocation scopes. Stays
  fixture-universe; does not implement lineage (gated by `primary-56d1.11`, which
  it must **not** wait on — it proceeds fixture-scoped). Everything else seats on
  this.

**Contracts (parallel, independent — pure wire vocabulary, no runtime):**

- **S1a — `signal-nomos`**, **S1b — `signal-logos`** (bead `primary-56d1.4`),
  confirming/extending **`signal-schema`**. These are the message contracts the
  daemons speak. They can be authored concurrently and in parallel with S0, since a
  contract crate owns only operation/reply types and codecs. Follow the
  `contract-repo` discipline.

**Daemons (parallel once their contract exists and S0 is up):**

- **S2 — schema daemon** on `signal-schema` + `core-schema` (+ `golden-bridge`
  ingest for legacy text).
- **S3 — nomos daemon** on `signal-nomos` + `core-nomos`.
- **S4 — logos daemon** on `signal-logos` + `core-logos` + `textual-rust`.

  Each daemon is one runtime crate + thin CLI, three planes (Signal/Nexus/SEMA),
  Kameo actors, seated on S0. The three can proceed in parallel; they share only
  the contract crates and the seat, both of which are stable interfaces.

**Integration (gates on the daemons):**

- **S5 — the end-to-end witness** (§4.3): a driver that feeds `spirit-min.schema`
  into the schema daemon, walks it through nomos and logos over the live signal
  contracts, captures the emitted Rust, and **compiles it independently** as a
  crate with the same dependencies, asserting the same public surface and the same
  behavior under shared tests (§4.4) — plus the free byte-exact per-item witness.
  This is the acceptance object for `primary-56d1.34`.

**Optional parallel document kind (ready, self-contained):**

- **S6 — the signal-contract component** (§3.4, spec in
  `core-signal-contract-handoff-v1.md`, bead `primary-ezut`). Can be built in
  parallel by an independent agent; it consumes `core-schema` + `structural-codec`
  by pinned rev and does not block the S2–S5 critical path.

Ordering rationale: contracts before their daemons (a daemon imports its contract
types); the seat before daemons (they commit into it); the witness last (it needs
all three daemons live). The nine crates and `golden-bridge` are frozen inputs at
every slice.

**Absorb the pre-existing open scaffolding beads — do not duplicate them.** Several
open children of the epic already name this work; map your slices onto them rather
than filing parallel beads: `primary-56d1.1` (Logos language spec),
`primary-56d1.2` (Nomos macro model and syntax), `primary-56d1.3` (pipeline
component architecture — the natural home for the S2–S4 daemon-shape work),
`primary-56d1.4` (signal-nomos / signal-logos contract crates — the S1 slices), and
`primary-56d1.7` (Nomos and logos component scaffolds — the S3/S4 daemon
scaffolds). Close or re-scope these as your slices land; the engine bead
`primary-56d1.34` is their umbrella.

## 6. Operational law

**Coordination and identity.** Before editing any shared file, register a
Session/Lane and claim the exact paths with Orchestrate; names are PascalCase
alphanumeric (uppercase first letter, then letters/digits only — the daemon
strictly enforces this). Each new repository you create has its own checkout, which
is not a shared-primary path and needs no primary claim for its internal files; if
you work under the shared `repos/` layout, claim the repo path once. **Never claim
`.beads/`** — track work through `bd`. This charter was written under session
`LanguageFamilyPrototype`, lane `EngineCharter`; you register your **own fresh
Codex Session/Lane** (not a generic name), e.g.:

```sh
meta-orchestrate "(Register ((<CodexSession> <CodexLane> ([Generalist] Structural) [minimal new engine end to end]) Fresh))"
```

**Non-overlap with the Claude side.** The Claude-side lanes own the `golden-bridge`
repository and the `reports/logos/` documentation surface — do not edit those. The
`reports/schema/` surface is Codex's documentation surface (this charter is written
into it as your pickup point). Keep engine docs on the `reports/schema/` side.

**The synchronizer train is a separate Codex lane; this engine rides pinned Git
dependencies, never the train.** The "synchronizer train" is the immutable
multi-repository release mechanism that materializes an epic's exact pinned closure;
its gating-defect work (the `train-flow-audit` defects) is Codex's own separate
lane. **This engine work must not depend on, edit, or be blocked on the train.**
Every daemon depends on **pushed commits by exact rev**, not on a train lock. When
this engine is eventually merged to mainlines, that follows the psyche-approved
**train order: producers before consumers, the whole closure green, Spirit last.**
Until then, hold your work on branches and pin by rev (as the schema-language /
schema-rust migration does, §3.3). Note one concurrent Claude-side lane that
touches your neighborhood: **`LojixCanonicalMigration`** is moving `schema-language`
main toward the canonical nota v0.7.0 tip `f8de7a5`, a different revision than your
held next-gen branch — do not land the next-gen branch to `schema-language` main, or
you clobber that lane.

**The lean protocol.** Under the standing grant (§1), every decision the psyche has
not ruled is an **explicit, recorded lean** — chosen, reasoned, and revisable, and
it must **never foreclose a psyche-open item.** Record each lean where the next
agent will find it (the repo's `ARCHITECTURE.md`, a code comment at the decision
site, or a bead comment), stating what it is, why, and what would revise it. Leans
are revisable after a working prototype exists; that is the whole point of the
grant.

**The psyche-pending list — do NOT settle these** (they are his authority, not
yours; stay clear of each):

- **`primary-56d1.11`** — the formal lineage ruling: the unit of "one schema" and
  split/merge identity semantics. His open question: "so where is the authority? In
  each corresponding daemon?" Stay fixture-universe; do not implement lineage.
- **`primary-56d1.31`** — string-versus-text: whether an elided string field
  derives the name "text" (new grammar) or legacy "string". Currently a lean, no
  golden impact yet.
- **`primary-56d1.9` and `primary-56d1.10`** — the non-rejected pile: the next-gen
  syntax slate (macro dotting, escapes, `$` sigil, meta-types, visibility spelling,
  delimiters, `rustfmt.skip` path) and the core-first storage proposals
  (format-upgrade mechanism, co-versioned NameTables). **Explicitly not accepted —
  must be reviewed later, must not decay into silent acceptance.** Design
  compatibly, do not rely on any of these as ruled.
- **`primary-56d1.26`** — pile-disposition procedure: whether to rule the pile now
  or per-slice-gates. Blocked on the psyche.
- **The document-kind design review** — the four kinds are accepted **as a
  direction to review later** (§2.6); the detailed design is explicitly review-later.
  Do not treat the detail as frozen.

(For context, not for you to settle: `primary-56d1.12` is a lost bootstrap question
awaiting the psyche's restatement, and `primary-56d1.13` is the sema.schema
document-kind / stored-record-identity design, blocked behind `.11`/`.12`.)

**Reports hygiene.** The psyche does not read reports; do not grow a pile of stale
design. Where a file already exists for a topic, **append a dated section rather
than spawning a new file.** Keep chat carrying the user-attention items (open
questions, blockers, recommendations) restated in enough substance to answer
without opening the report. Bead `primary-56d1.14` tracks a hygiene sweep of the
`reports/logos/` pile; do not add to the mess.

**Language discipline for any psyche-facing output.** Speak the psyche's own
vocabulary. Explain every agent-coined name — a repository name, a work-item
shorthand, a pattern label — in plain words in place, in any message that leans on
it. A name is never an explanation. When a reply builds on an earlier artifact or
decision, restate in one plain clause what it is. This is the discipline that
prompted this charter's own plain-language rule (§introduction) and is now in the
`management` skill.

## 7. References

**Repositories and current pins (2026-07-16; verify at pickup).** All under
`/home/li/primary/repos/`, `main` bookmark unless noted, depend inward by pinned
rev.

- Nine crates: `content-identity` `6cc0408`, `name-table` `c3237f7`,
  `raw-discovery` `a4e8c6d`, `structural-codec` `104f924`,
  `structural-codec-derive` `348bd89`, `core-schema` `566544e`, `core-logos`
  `17cbd75`, `textual-rust` `b0ea9fb`, `core-nomos` `88a1ecf`.
- `golden-bridge` `03929a4` (public: `github.com/LiGoldragon/golden-bridge`).
- Storage seat: `sema` `51d7927`, `sema-engine` `71508ca`.
- Held next-gen migration branches: `schema-language`
  `41a7b257dddbcaebf151a053c6fd43324a2a8e39` (branch
  `language-family-nextgen-schema-language`, main `59d59ac`); `schema-rust`
  `a92a9d0e2940b4debed74a2f7d06ea44c4360c99` (branch
  `language-family-nextgen-schema-rust`, main `87de872`); both on `nota` next-gen
  `18e2e8d0dba37e9e84045af3608585b51f6e3b36` (bookmark `next-gen`).
- Legacy/adjacent: `schema` `36a79b7` (legacy live stack). Message substrate:
  `signal-frame`, `signal-schema` (verify pins; `signal-nomos`/`signal-logos` to be
  created, bead `primary-56d1.4`).

**Reports authority map.**

- **Design authority:** `reports/logos/up-close-design-v1.md` — the code-level
  reconciliation of the shared-codec family, the Textual many-forms family, and the
  Logos→Rust lowering. This is the design ground.
- **Evidence discipline:** `reports/logos/vision-evidence-ledger-v1.md` — classifies
  every claim as ruled versus proposed; read it before treating anything as
  settled.
- **Core-first architecture:** `reports/logos/core-first-architecture-v1.md` — the
  daemon-resident-editing end-state and the seat-on-sema-engine mechanism.
- **Signal-contract component spec:** `reports/schema/core-signal-contract-handoff-v1.md`
  — the detailed spec for that one component (§3.4), subordinate to this charter.
- **Document kinds:** `reports/schema/document-kinds-signal-contract-design-v1.md`
  (v1) plus the psyche acceptance (§2.6) is ground. **Caution:**
  `reports/schema/document-core-adapter-design-v2.md` **over-settled** v1's open
  questions and its slate/authority framing is **NOT authority** — treat v1 plus the
  acceptance as ground; v2's concrete record shapes may be reused as faithful
  proposals, its framing may not.
- The nine-crate roster is named in `reports/logos/stack-re-audit-v1.md`. The epic
  design context is `reports/logos/language-family-poc-epic-design-v1.md`.

**Beads.** Epic `primary-56d1` (Next-generation NOTA). This engine's bead:
**`primary-56d1.34`** (minimal new engine end-to-end, Codex-owned). Component
slices: `primary-56d1.4` (signal-nomos/signal-logos contracts), `primary-ezut`
(signal-contract component). Held migration: `primary-oay8`. Psyche-pending (do not
settle): `.11`, `.31`, `.9`, `.10`, `.26`, plus `.12`/`.13` for context. Completed
substrate: `.15`/`.16`/`.18` (raw-discovery/content-identity/name-table), `q551`
(structural-codec), `.19`/`.20` (core-schema/structural-codec-derive),
`.21`/`.23` (core-logos/textual-rust), `.24` (core-nomos), `.30` (golden-bridge leg
1), `.22` (dogfood train). Deferred post-PoC: `.17`, `.32`, `.33`.

Every fact in this charter is grounded in one of the artifacts above and was
verified against them on 2026-07-16. Where the psyche's word is still pending (the
lineage ruling and the non-rejected pile), this charter stays clear of it and says
so.
