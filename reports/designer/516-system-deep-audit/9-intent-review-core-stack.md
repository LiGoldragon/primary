# Intent Review #9 — Core-Stack INTENT.md

Deep-audit sub-report. Reviews the `INTENT.md` of each of the nine
core-stack repositories: `nota`, `nota-next`, `nota-codec`, `schema`,
`schema-next`, `schema-rust-next`, `triad-runtime`, `spirit`,
`signal-spirit`. For each: does the file exist, what is the repo FOR
(one sentence), what are its load-bearing constraints, and what should
a *curated* INTENT.md keep — the most important and **only** the most
important intent. Every quote below is verbatim from the real file at
the time of audit; no intent text is paraphrased into the repo's mouth.

## Method and what was actually run

This review is reading/analysis. No `cargo` build was needed. Three
commands were run to (a) confirm existence and size of every file and
(b) ground two architectural claims that the prose makes — the
legacy/replacement split, and the live deployed CLI — against reality
rather than against the documents that assert them.

### Run 1 — existence and size, in the repo checkout root

Command, run in `/git/github.com/LiGoldragon/`:

```
for r in nota nota-next nota-codec schema schema-next schema-rust-next triad-runtime spirit signal-spirit; do
  d="/git/github.com/LiGoldragon/$r"
  wc -l "$d/INTENT.md" "$d/ARCHITECTURE.md"
done
```

Verbatim output (line counts):

```
   90 /git/github.com/LiGoldragon/nota/INTENT.md
  127 /git/github.com/LiGoldragon/nota/ARCHITECTURE.md
   79 /git/github.com/LiGoldragon/nota-next/INTENT.md
  110 /git/github.com/LiGoldragon/nota-next/ARCHITECTURE.md
   73 /git/github.com/LiGoldragon/nota-codec/INTENT.md
  202 /git/github.com/LiGoldragon/nota-codec/ARCHITECTURE.md
   37 /git/github.com/LiGoldragon/schema/INTENT.md
  229 /git/github.com/LiGoldragon/schema/ARCHITECTURE.md
  331 /git/github.com/LiGoldragon/schema-next/INTENT.md
  463 /git/github.com/LiGoldragon/schema-next/ARCHITECTURE.md
  286 /git/github.com/LiGoldragon/schema-rust-next/INTENT.md
  306 /git/github.com/LiGoldragon/schema-rust-next/ARCHITECTURE.md
   51 /git/github.com/LiGoldragon/triad-runtime/INTENT.md
  129 /git/github.com/LiGoldragon/triad-runtime/ARCHITECTURE.md
  263 /git/github.com/LiGoldragon/spirit/INTENT.md
  449 /git/github.com/LiGoldragon/spirit/ARCHITECTURE.md
   87 /git/github.com/LiGoldragon/signal-spirit/INTENT.md
   90 /git/github.com/LiGoldragon/signal-spirit/ARCHITECTURE.md
```

**Result: all nine `INTENT.md` exist.** There is no missing-INTENT
gap in the core stack. The audit question therefore shifts from
"which repos lack intent capture" to "which INTENT.md files have
drifted toward exhaustiveness and need distilling."

### Run 2 — grounding the legacy/replacement split

The prose in `nota-next` and `schema-next` claims to *supersede*
`nota`/`schema`. That is a load-bearing claim for the whole review,
so it was checked against the actual files rather than trusted.

Command, run in `/git/github.com/LiGoldragon/`:

```
grep -n -i "predecessor\|replacement\|new NOTA implementation\|new schema implementation\|AssembledSchema\|Asschema" \
  nota/INTENT.md nota-next/INTENT.md schema/INTENT.md schema-next/INTENT.md
```

Verbatim, load-bearing lines from output:

```
nota-next/INTENT.md:3:`nota-next` is the new NOTA implementation for the schema-derived stack.
nota-next/INTENT.md:78:The predecessor surface is the existing `nota` / `nota-codec` family. This
nota-next/INTENT.md:79:repository carries the replacement track on `main`.
schema-next/INTENT.md:3:`schema-next` is the new schema implementation.
schema/INTENT.md:19:6. Lower authored schemas into `AssembledSchema`, the explicit machine
schema-next/INTENT.md:104:*Assembled schema is defined before authored-schema sugar. `Asschema` is the
```

**Result: the split is real and named in the files.** `nota`/`schema`
are the predecessor track and lower into a type literally spelled
`AssembledSchema`; `nota-next`/`schema-next` are the named replacement
track and lower into `Asschema`. The two type names — `AssembledSchema`
vs `Asschema` — are the cleanest single discriminator between old and
new stack. This matters for the audit's recommendations: the legacy
INTENT.md files should not be "improved," they should be marked
superseded.

### Run 3 — grounding the deployed CLI against the pilot

The `spirit` repo INTENT calls itself a *pilot* that proves a daemon
can be built from schema-derived interfaces, explicitly separate from
production. To confirm the deployed binary is a different, older wire
shape (not the pilot), the live CLI was probed.

Commands, run from the home environment:

```
realpath /home/li/.nix-profile/bin/spirit
spirit "(Observe (Query (TopicMatch Partial) [intent] None Zero))"
```

Verbatim output:

```
/nix/store/s6lycvzfi688qhv1814g7iwhv2x9mzdg-spirit-v0.5.1/bin/spirit-v0.5.1
invalid request text: unknown variant `Query` for enum `Observation`
```

**Result.** The deployed CLI is `spirit-v0.5.1`. It parses the NOTA
argument structurally — it recognises `Observe`, knows there is an
`Observation` enum at that position, and rejects `Query` as a variant
of it. The pilot's `INTENT.md` (lines 219-229) describes
`Observe(Query)` with a `Query` payload; the *deployed* `Observation`
enum has no `Query` variant. So the deployed wire shape and the pilot
repo's documented shape are genuinely different surfaces, which is
exactly what the pilot INTENT claims ("intentionally separate from
production `spirit`/`persona-spirit`"). The probe confirms the pilot
is not the deployed binary.

## The stack in one paragraph, then per-repo

Read bottom-up the nine repos form a vertical pipeline plus a shared
runtime crate. NOTA (text/structure layer) → schema (type-name
vocabulary + lowering to assembled schema) → schema-rust-next (Rust
code emission) → the contract crate `signal-spirit` and the daemon
pilot `spirit`, both consuming generated Rust, with `triad-runtime`
supplying shared runtime mechanics across every component. Two of the
nine — `nota` and `schema` — are the predecessor track; the live
direction is `nota-next` / `schema-next` / `schema-rust-next`. The
biggest INTENT.md health problem across the stack is not absence but
**over-capture**: `schema-next` (331 lines), `schema-rust-next` (286),
and `spirit` (263) have grown into near-exhaustive design logs where
the distilled, durable intent is buried under implementation-status
prose that belongs in ARCHITECTURE.md or reports.

## nota

**INTENT.md exists** (90 lines).

**What it is for (one sentence):** `nota` is the spec-only definition
of the NOTA text language — delimiters, the three-case PascalCase
rule, positional records, maps, built-in type spellings — that every
layer above consumes as law.

**Most important constraints (the few that, if violated, break the
repo's purpose):**

- The three-case PascalCase rule. Verbatim: *"PascalCase has exactly
  three meanings in NOTA value positions"* — `(VariantName fields…)`
  data-carrying variant, `(fields…)` struct, bare `VariantName` unit
  variant; *"A bare PascalCase token at an ordinary String schema
  position is a typed error."* This is the single rule the rest of the
  stack's parser and emitter is built to honour.
- Records are positional, never `(key value)`. Verbatim: *"The shape
  used by Lisp / Clojure / JSON is not NOTA."*
- Built-ins obey the same rule: `Bool` is `True`/`False` unit variants
  (no `true`/`false` keywords); `Option<T>` is bare `None` or
  `(Some inner)` — *"there are no exceptions."*
- Tuples are not NOTA — use named-field structs.

**Status note grounding the curation proposal.** The ARCHITECTURE.md
head (Run-1-adjacent read) says verbatim: *"This repo is **spec-only**.
… No Rust code."* and *"Layer 0 of the project."* So `nota` is the
language law, and `nota-codec` is its implementation. But `nota-next`'s
INTENT (line 78) names *"the existing `nota` / `nota-codec` family"* as
**the predecessor surface**. This is a tension: `nota` presents as the
authoritative language spec, yet the replacement track has its own
structural model (recursive pipe forms, `@`-sigil declarations) that
`nota`'s spec does not describe.

**Proposed curated INTENT.md.** Keep the three-case PascalCase rule and
positional-records-not-labeled as the two apex laws — they are the most
quoted rules in the whole workspace (`AGENTS.md` restates both as hard
overrides). Keep the built-in spellings (`Bool`, `Option`) because they
are non-obvious and load-bearing for emitted code. **Add a one-line
supersession banner at the top** stating that the live language model
lives in `nota-next` and that this file is the legacy spec retained as
the canonical statement of the PascalCase/positional laws. **Cut** the
"Macro-pattern integration" section (lines 79-90) — it is report-pointer
prose, not intent, and references designer reports by number, which is
exactly the locator-without-substance shape the workspace forbids.

## nota-next

**INTENT.md exists** (79 lines).

**What it is for (one sentence):** `nota-next` is the live replacement
NOTA implementation that owns the raw structural floor — delimiter
predicates, the first structural-header pass, the shared `NotaDecode`/
`NotaEncode` value codec, and the reusable macro-node mechanism — while
explicitly *not* deciding schema semantics.

**Most important constraints:**

- The layering boundary. Verbatim: *"NOTA is the library that gives
  methods on raw delimiter structures … It does not decide schema
  semantics."* And: *"NOTA owns Rust value codec shapes through shared
  `NotaDecode` and `NotaEncode` traits … Schema owns the type-name
  vocabulary and declaration semantics layered above those value
  shapes."* This is the firewall that justifies the entire repo split.
- The delimiter vocabulary. Verbatim: *"Square brackets are vectors.
  Pipe-square `[|...|]` is the string-safe text form … Pipe-parenthesis
  `(|...|)` and pipe-brace `{|...|}` are recursive delimiter forms."*
- The `@`-sigil declaration interface. Verbatim: *"`Name@{...}` parses
  as a named struct-like declaration, `Name@[...]` parses as a named
  enum-like declaration, and `name@(Reference ...)` parses as a member
  binding … The `@` is a declaration/binding sigil … not a macro-call
  sigil."* This is the single biggest *syntactic* difference from the
  legacy `nota` spec and is why the legacy spec can't simply be reused.
- `known_root` document bodies and `Box<T>` indirection-is-not-syntax.
  Verbatim: *"Rust storage indirection is not a NOTA value shape.
  `Box<T>` decodes and encodes through the contained `T`."*
- Macro nodes are a NOTA-layer mechanism, not schema-owned. Verbatim:
  *"NOTA owns the structural pattern data, named capture extraction,
  registry dispatch … Consumers such as schema-next own the vocabulary
  they register."*

**Proposed curated INTENT.md.** This file is already close to
well-curated — it is 79 lines of mostly-durable layering law. Keep all
five constraints above essentially as-is; they are the contract, not
status. The one tightening: the long parenthetical in the `@`-sigil
paragraph about *"The earlier recursive pipe delimiter support and
`Name@(...)` enum declaration form remain compatibility surfaces"* is
migration bookkeeping — move that compatibility caveat to ARCHITECTURE.md
and leave INTENT stating only the target `@` forms.

## nota-codec

**INTENT.md exists** (73 lines).

**What it is for (one sentence):** `nota-codec` is the
canonical-emission codec for the *legacy* NOTA family whose central
guarantee is that the encoder structurally cannot emit a quotation mark,
making every NOTA value it produces embedding-safe inside any
double-quote host language.

**Most important constraints:**

- The encoder cannot emit a quote. Verbatim: *"The `Encoder`
  STRUCTURALLY cannot emit a quotation mark … `write_string` has
  exactly three branches — bare identifier, `[|...|]` block, `[...]`
  inline — and no fourth quote branch exists."* This is the one rule
  that, if broken, destroys the embedding-safety contract the whole
  workspace leans on (`AGENTS.md` hard override "NOTA-in-anything-with-
  double-quote-strings is escape-free").
- Strict on emit, lenient on accept. Verbatim: *"strict on what we
  emit, lenient on what we accept; the migration always moves toward
  canonical."* The `read_legacy_quote_string` path accepts `"..."` as
  migration input only and is *"authorised for removal"* once emitters
  migrate.
- Embedding-safety is a preserved contract; any future quote-emitting
  toggle *"breaks the embedding contract and is forbidden."*

**Status / drift note.** `nota-codec` is named (with `nota`) as the
predecessor surface by `nota-next` INTENT line 78. Yet the live
replacement `nota-next` re-states the same no-quote-emit law (its
encoder has the same three branches). So the *rule* is current and
load-bearing; the *crate* is legacy. The curated file must keep the
rule and flag the crate's predecessor status, or a reader will conclude
the no-quote guarantee is itself legacy, which it emphatically is not.

**Proposed curated INTENT.md.** Keep the three constraints verbatim —
they are pure durable intent with no status rot. Add the one-line
supersession banner naming `nota-next` as the live codec. **Cut** the
"Macro-pattern integration" section (`is_block_string` predicate
detail) down to a single sentence or move it to ARCHITECTURE.md; it
describes a method, not an intent.

## schema

**INTENT.md exists** (37 lines — the shortest in the stack).

**What it is for (one sentence):** `schema` is the *legacy* typed
substrate for the NOTA schema language — the six-fixed-position
`.schema` file model that lowers into `AssembledSchema` — superseded by
`schema-next`.

**Most important constraints (as the file states them, in its own
priority order):**

- Verbatim #1: *"Represent the NOTA schema language as typed Rust
  data."*
- Verbatim #2: *"Keep the top-level `.schema` file as the six fixed
  positional fields: imports, ordinary header, owner header, sema
  header, namespace, features."* — This six-field model is precisely
  what `schema-next` replaced with the `@`-declaration + import/
  roots/namespace shape, so it is the clearest legacy marker.
- Verbatim #6: lower into *"`AssembledSchema`, the explicit machine
  object"* — note the name, contrast `schema-next`'s `Asschema`.
- Verbatim #8: *"Stay library-shaped until the runtime schema registry/
  triad authority is explicitly settled."*

**Status / drift note.** This file's "Open intent needing later
settlement" block (lines 27-37) asks questions — *"Whether this
repository also owns the eventual `nota-box` crate surface"*, *"Whether
a future schema daemon triad is required"* — that the *replacement*
track (`schema-next` owning the macro engine + assembled model,
`schema-rust-next` owning emission, daemons owning their plane schemas)
has since answered by structure. The open questions are stale: they are
being resolved in different repos. This is the single most drifted
INTENT.md in the stack relative to current reality.

**Proposed curated INTENT.md.** Replace the body with a short
supersession statement: this repo holds the legacy six-position
schema model lowering into `AssembledSchema`; the live schema stack is
`nota-next` + `schema-next` + `schema-rust-next` lowering into
`Asschema`. Keep priority items #1, #2, #4 (positional), and #6 as the
historical record of *what this model was*, framed in past tense.
**Cut the entire "Open intent needing later settlement" block** — every
question in it is either answered elsewhere or moot, and carrying open
questions in a superseded repo's INTENT actively misleads.

## schema-next

**INTENT.md exists** (331 lines — the longest INTENT in the stack).

**What it is for (one sentence):** `schema-next` is the live schema
macro engine and ordered assembled-schema data model — it lowers
authored `.schema` NOTA into `Asschema` (and the persisted `.asschema`
/ rkyv artifacts) and does **not** emit Rust.

**Most important constraints:**

- The repo-split boundary, stated twice. Verbatim: *"This repository
  owns the schema macro engine and the ordered assembled schema data
  model. It does not emit Rust source code."* And up top: *"The
  schema-derived stack uses separate repositories for nota-next,
  schema-next, and schema-rust-next."*
- Assembled schema is live data, not parser state. Verbatim: *"`Asschema`
  is the typed macro-free endpoint … it must read/write legal NOTA
  through the shared NOTA codec and read/write binary rkyv bytes. Rust
  emission consumes that assembled data object, not hidden parser
  state."*
- NOTA-owns-structure / schema-owns-type-names. Verbatim: *"Square
  brackets remain raw NOTA vector structure … they are not the syntax
  for declaring a `Vec` type. Schema type-reference objects include
  `(Vec T)`, `(Map (K V))`, and `(Optional T)`."*
- The authored-surface laws: strict key/value braces; *"declaration
  forms that repeat their own name are removed from the production
  lowering path"*; single-field structs lower to `Newtype` not named
  one-field structs; bare bindings lower to `Alias` not tuple newtypes.
- Visibility-tagged namespace entries. Verbatim: *"`(Public Name Value)`
  or `(Private Name Value)` … Inline PascalCase declarations lower to
  private, module-local declarations."*
- The macro-node target split. Verbatim: *"the target split is:
  nota-next owns structural macro-node dispatch and typed matches/
  captures; schema-next registers the schema vocabulary and lowers
  matches into assembled-schema fragments."*

**Drift assessment — this is the file most in need of distilling.**
Of 331 lines, the genuinely durable intent is the half-dozen
boundary/lowering laws above. The rest is a fine-grained design log:
the multi-paragraph treatment of `Asschema` notation truthfulness,
`SymbolPath` round-tripping, the `core.schema`/`core.asschema`/
`builtin-macros.macro-library` artifact bootstrap, and the
"Current implementation target" bullet list (lines 305-331) are
implementation status and mechanism that belong in ARCHITECTURE.md.
The repo-intent skill's continuous-manifestation discipline wants
INTENT to hold *why/what-must-be-true*, not the current bootstrap
sequence.

**Proposed curated INTENT.md.** Keep the six constraint clusters above
as the curated intent (~60-80 lines). Move the "Current implementation
target" block and the `MacroLibrary`/artifact-bootstrap paragraphs to
ARCHITECTURE.md. Collapse the many near-duplicate paragraphs on
authored-surface sugar (Alias vs Newtype vs Struct, single-field rules,
derived-member `*` shorthand) into one tight section — they currently
say the same thing five times from five angles.

## schema-rust-next

**INTENT.md exists** (286 lines).

**What it is for (one sentence):** `schema-rust-next` is the Rust
emission repository — it consumes macro-free `Asschema` and emits the
schema nouns, plane modules, engine traits, NOTA/rkyv codecs, and the
per-crate generation driver, source-visible under `src/schema/`.

**Most important constraints:**

- Source-visible emission, not `OUT_DIR`. Verbatim: *"Generated Rust
  code is emitted into the consumer crate source tree under
  `src/schema/`, not hidden in `OUT_DIR`. Source-visible generated
  interfaces are reviewable."*
- Methods on data-bearing nouns, never free functions. Verbatim:
  *"runtime engines implement generated Nexus traits with one method
  per reaction variant, and those methods live on data-bearing
  objects, not free helper functions."* (This is the workspace's
  no-free-functions hard override, enforced at the emitter.)
- The plane split: `WireContract` / `NexusRuntime` / `SemaRuntime`
  emission targets, with `ComponentRuntime` as *"the compatibility/
  bootstrap target for unsplit all-in-one schemas."*
- Binary rkyv is universal; NOTA is opt-in. Verbatim: *"Binary `rkyv`
  support is universal; NOTA encode/decode support is an optional
  emitted surface for text-facing clients, not a daemon-default
  surface."* Configured via `NotaSurface::FeatureGated { feature:
  "nota-text" }`.
- Cross-crate imports preserve type ownership. Verbatim: *"A consumer
  schema that imports `crate:module:Type` emits a local Rust alias to
  the dependency crate's generated type instead of re-declaring the
  type locally."*
- The generated component-runner / shared-runner adapter. Verbatim:
  *"generated Rust must project the action enum exhaustively into
  `triad_runtime::NextStep`, emit the data-bearing adapter that
  implements `triad_runtime::RunnerEngines`."*
- Rust emission is data before text. Verbatim: *"The emitter maps
  `Asschema` into a typed `RustModule` object … rendering `RustModule`
  produces `RustCode`."*

**Drift assessment.** Like `schema-next`, this is a near-exhaustive
design log. The trace-emission paragraphs (lines 126-152), the mail-
lifecycle/`OriginRoute`/`MessageIdentifier` paragraphs, and the
`RustEmissionOptions`/`NotaSurface` configuration detail are real intent
but stated at mechanism granularity. The scalar-floor rule (`String`/
`Integer`/`Boolean`/`Path`, *"`Bool` is not a spelling"*) is durable and
should stay.

**Proposed curated INTENT.md.** Keep the seven boundary constraints
above. Compress the trace/mail-lifecycle material to: *"Tracing and
mail lifecycle are schema-defined typed interfaces — typed `TraceEvent`,
`ObjectName`, `OriginRoute`, `MessageIdentifier` generated from the
schema, typed to the client display edge, no stringly trace
vocabularies."* Move `RustEmissionOptions` field-level detail to
ARCHITECTURE.md.

## triad-runtime

**INTENT.md exists** (51 lines).

**What it is for (one sentence):** `triad-runtime` holds the shared,
component-agnostic runtime mechanics — the trace event log + length-
prefixed frame + Unix socket transport, the single-argument
`ComponentCommand`/`ComponentArgument` edge, and the recursive Nexus
`Runner` with its typed continuation budget — that schema-emitted
component surfaces use at run time.

**Most important constraints:**

- The triad-engine readability principle (bracket-quoted as the load-
  bearing statement). Verbatim: *"the system should be readable because
  types name the work, schema names the interface, generated Rust names
  the objects and traits, and handwritten code is mostly the real
  algorithm: match typed input, make the decision, call the next typed
  interface, return typed output."* This is the philosophical anchor of
  the entire schema-derived stack.
- Runtime is separate from emission. Verbatim: *"The runtime crate is
  separate from schema emission. `schema-rust-next` emits component-
  specific nouns and traits; `triad-runtime` provides reusable runtime
  objects."*
- Machines communicate in rkyv; NOTA stays at the edge. Verbatim:
  *"Machines communicate through rkyv archives. `triad-runtime` does not
  own NOTA parsing; text projection stays at CLI and human-facing
  edges."*
- The `Runner` owns the action loop, not component code. Verbatim:
  *"`Runner` owns that loop and the typed continuation budget; generated
  glue projects each component's typed `NexusAction` into the fixed
  `NextStep` shape."*
- Scope discipline. Verbatim: *"Backpressure and deeper runtime-control
  machinery are deferred future runtime work … The current production
  slice is trace substrate plus reusable frame, argument, and runner
  edges."*

**Proposed curated INTENT.md.** This file is well-curated already — 51
lines, almost all durable. Keep all five. The readability principle
should arguably be promoted to the *top* (it currently sits at line 7
under a one-line preamble) because it is the single most important
sentence in the entire core stack and several other INTENT files
implicitly serve it. No cuts needed; this is the model the over-long
files should aim for.

## spirit

**INTENT.md exists** (263 lines).

**What it is for (one sentence):** `spirit` is the pilot daemon proving
a running Spirit-like component can be built entirely from schema-
derived interfaces — three plane schemas (signal/nexus/sema), generated
Rust under `src/schema/`, the binary-only daemon + NOTA-text CLI split,
durable `.sema` storage, and the Signal→Nexus→SEMA→Signal runtime path.

**Most important constraints:**

- It is a *pilot*, separate from production. Verbatim: *"It is
  intentionally separate from production `spirit`/`persona-spirit` so
  operators can iterate without disturbing the deployed intent
  substrate."* **Run 3 confirms this:** the deployed `spirit-v0.5.1`
  has an `Observation` enum with no `Query` variant, while this repo's
  INTENT (line 220) documents `Observe(Query)` — different surfaces, as
  the pilot intends.
- Binary daemon, NOTA-text CLI, enforced as an executable contract.
  Verbatim: *"The daemon build is binary-only and must not depend on
  `nota-next`; the CLI build opts into `nota-text`."* And: *"Tests run
  `cargo tree --edges normal --no-default-features` and assert
  `nota-next` is absent."* — the dependency boundary is a test, not a
  comment.
- The three-plane runtime triad. Verbatim: *"`schema/signal.schema`
  owns `Input`/`Output` for Signal, `schema/nexus.schema` owns
  `NexusWork`/`NexusAction` for Nexus decision flow, and
  `schema/sema.schema` owns `WriteInput`/`WriteOutput` … plus
  `ReadInput`/`ReadOutput`."*
- Nexus is a real object owning the single-flight guard. Verbatim:
  *"The mutable `NexusEngine::execute(&mut self, …)` borrow is the
  single-flight guard. `Engine` is a thin composer of the three centers
  and never calls the store directly."*
- SEMA is durable, named for the plane not the library. Verbatim: *"The
  file extension is `.sema` (not `.redb`) so the name states the
  runtime plane, not the implementation library."* And production-
  candidate handover is tested as a copy of a real `.sema` file.
- No parallel convenience surfaces. Verbatim: *"Old design-convenience
  APIs do not remain beside the working interface (Spirit record 1339)."*
- The daemon's single argument is a binary rkyv `Configuration`, not a
  NOTA string. Verbatim: *"Raw NOTA text sent to the daemon's binary
  socket is invalid data."*

**Drift assessment.** At 263 lines this is the third-longest INTENT and
the most status-laden: many bullets end with present-tense progress
("Durable SEMA storage is now implemented; schema diff/upgrade and the
triad split remain"). The trace-surface bullets (lines 159-204) repeat
material already in `triad-runtime` and `schema-rust-next` INTENT — the
same trace mechanism described a third time from the consumer's seat.

**Proposed curated INTENT.md.** Keep the seven constraints above as the
durable pilot contract. Collapse the ~45 lines of trace-surface detail
into one constraint: *"Optional `testing-trace` builds emit typed
`TraceEvent`/`ObjectName` from live runtime hooks across the real
CLI→daemon→Signal→Nexus→SEMA→Signal path, using `triad-runtime`
transport; the normal packages do not enable it."* Move the
build-freshness/artifact mechanics (lines 53-67) to ARCHITECTURE.md.
Keep the closing status line, but as the *single* status sentence
rather than scattering progress notes through every bullet.

## signal-spirit

**INTENT.md exists** (87 lines).

**What it is for (one sentence):** `signal-spirit` is the ordinary
(non-privileged) signal wire layer for the Spirit component — the
everyday messaging API any peer can call — declared schema-first in
`schema/signal-spirit.schema` with the Rust emitted.

**Most important constraints:**

- Ordinary layer only; privileged ops live elsewhere. Verbatim:
  *"Privileged operations — supervisor start/drain, identity
  registration, bootstrap-policy reload, upgrade handover — do NOT land
  here. Those live in `core-signal-spirit`."*
- Schema-first, inverting the legacy crate. Verbatim: *"the schema IS
  the contract; the Rust is emitted. This contrasts with the legacy
  `signal-persona-spirit` crate, which hand-authored the entire wire
  surface."*
- No Features-section drift. Verbatim: *"schema declares data types
  only. No `EffectTable`, `FanOutTargets`, `StorageDescriptor` as
  authored schema content … forbidden from returning."*
- Positional records (the hard override, restated for the wire).
- Topics are user-creatable strings, not a pre-declared enum. Verbatim:
  *"The schema declares `Topic [String]`; any new topic word a `Record`
  operation uses is registered."*

**Note on the naming triad.** This repo is the `signal-<component>` leg
of the component triad (per `AGENTS.md`: daemon + `signal-<component>` +
`meta-signal-<component>`). Its INTENT correctly scopes itself to the
ordinary signal layer and points privileged ops at `core-signal-spirit`
— note that is `core-signal-`, an older naming than the `meta-signal-`
the current workspace contract uses for the third triad leg. That is a
naming-drift flag, not a content error: the *intent* (ordinary vs
privileged split) is right; the *spelling* of the privileged sibling
predates the meta-signal rename.

**Proposed curated INTENT.md.** This file is already close to curated —
87 lines, mostly verbatim psyche quotes with record citations. Keep all
five constraints. The only tightening: the "Why this repo exists"
section stacks three record quotes (765/767/780) that all say the same
persona-prefix-retirement thing; one quote suffices. Reconcile the
`core-signal-spirit` reference against the current `meta-signal-`
contract — either confirm `core-signal-spirit` is a distinct privileged
crate that still exists, or update the pointer to the meta-signal leg.

## Cross-cutting findings

**No missing-INTENT gap.** All nine core repos have INTENT.md (Run 1).
The audit's energy should go to curation, not creation.

**The real problem is over-capture in three files.** `schema-next`
(331), `schema-rust-next` (286), and `spirit` (263) have grown into
design logs. They violate the repo-intent discipline's separation:
INTENT holds durable *why/what-must-be-true*; ARCHITECTURE holds *how it
is built now*; status belongs in reports. `triad-runtime` (51) and
`signal-spirit` (87) are the models to imitate — short, durable, mostly
verbatim psyche law.

**Two repos are legacy and should say so.** `nota` and `schema` are the
predecessor track (Run 2: `nota-next` line 78 names them predecessors;
`schema` lowers to `AssembledSchema`, the live stack to `Asschema`).
Their INTENT files do not carry a supersession banner, and `schema`'s
INTENT still poses "open questions" that the replacement repos have
answered structurally. A reader landing in `schema/INTENT.md` cold would
not know it is superseded. Each legacy file needs a one-line top banner
naming its live successor.

**The same mechanism is described in three INTENT files.** Trace
transport appears in `triad-runtime` (owner), `schema-rust-next`
(emitter), and `spirit` (consumer). That triple is arguably correct —
each repo states *its* slice — but the prose volume is redundant; the
emitter and consumer files can compress to a one-line pointer at the
owner plus their slice-specific constraint.

**One durable sentence deserves promotion.** The triad-engine
readability principle in `triad-runtime` INTENT (*"types name the work,
schema names the interface, generated Rust names the objects and traits,
and handwritten code is mostly the real algorithm"*) is the thesis of
the entire schema-derived stack. It is buried at line 7 of one repo.
Consider promoting it to the workspace `INTENT.md` / `ESSENCE.md` so the
whole stack visibly serves one stated principle.
