# Meta-Supreme Audit — Report 1: Engine Analysis

Deep analysis of the schema-derived / triad engine end to end, for the
psyche who designed it. Architect register: real mechanism, named files,
named records, honest both ways. The engine is the schema-derived stack —
`nota-next` (0.3.0), `schema-next` (0.1.4), `schema-rust-next` (0.1.13),
`triad-runtime` (0.2.1), and the running pilot `spirit` (0.1.0). Every
claim below is anchored to a `file:line`, a Spirit record id, or a live
command result.

## Method and verification

I read the `ARCHITECTURE.md` / `INTENT.md` of all five repos and the real
source under each `src/`, then ran the suites offline to ground the
"it works" claim rather than assert it:

| Repo | command | result |
|---|---|---|
| `nota-next` | `cargo test --offline` | all green, 0 fail (7 suites; e.g. macro_nodes 9, codec 8, derive 8) |
| `triad-runtime` | `cargo test --offline` | 29 pass / 0 fail (5 suites: argument 6, daemon 2, frame 4, runner 6, trace 11) |
| `schema-next` | `cargo test --offline` | all green, 0 fail (14 suites; largest 22) |
| `schema-rust-next` | `cargo test --offline` | all green, 0 fail (6 suites; largest 32) |
| `spirit` (`runtime_triad`) | `cargo test --offline --test runtime_triad` | 24 pass / 0 fail |

The whole stack is green. I also verified the cited intent against the
LIVE deployed Spirit store with
`spirit "(Observe (Records ((Partial [triad nexus feature-catalog readability]) None Any Recent SummaryOnly)))"`,
which returned `z6qu` (Principle, VeryHigh), `k4d9`, `3d5z` (Constraint,
VeryHigh), `7ca4`, `hyng`, and the rest of the cluster verbatim — these
records are real, not paraphrase.

One structural fact must frame everything else (see §"The deployment
gap"): the deployed `spirit` binary on this machine is the OLD
persona-spirit engine at v0.5.2 (`spirit "(Help)"` → `unknown request
head: Help`; it speaks an `Observation`/`Records` contract that the
schema-derived repo does not emit). The schema-derived `spirit` repo is
v0.1.0 and is NOT the deployed binary. The engine analyzed here is the
designed future stack proven in-tree, not the thing currently serving
intent records.

## (a) The NOTA floor — decode by shape

`nota-next` owns the raw structural floor and nothing above it
(`nota-next/ARCHITECTURE.md:106-110` — "does not know what a schema type,
field, declaration, enum, macro, or import means"). Three properties make
it the right floor.

**Brackets are the only string form; the parser has no quote rule.** A
`Document` is an ordered `Vec<Block>` (`parser.rs:17-20`), and a `Block`
is exactly three things: `Delimited { delimiter, span, root_objects }`,
`PipeText`, or `Atom` (`parser.rs:56-65`). The five delimiters
(`Parenthesis`, `SquareBracket`, `Brace`, `PipeParenthesis`, `PipeBrace`)
carry their own opening/closing text tables (`parser.rs:258-307`). There
is no string-literal token type in the grammar at all — `[text]` is a
delimited block whose contents are text, `[|...|]` is `PipeText`. This is
the structural reason the AGENTS.md "NOTA never emits quotation marks"
override holds: the floor has no place to put a `"`.

**Records are positional.** A `Block` exposes `root_object_at(index)`
(`parser.rs:169-174`) and arity predicates `holds_single_root_object` /
`holds_two_root_objects` (`parser.rs:161-167`). There is no key lookup,
no label map — the type read against the block decides what slot N means.
This is the floor-level enforcement of the AGENTS.md "NOTA records are
positional, not labeled" override.

**The first pass emits a structural witness before any semantics.**
`Document::structure_header()` (`parser.rs:49-53`) produces a
`StructureHeader` of up to 8 `StructureSlot`s, each a (shape-nibble,
child-count-nibble) byte, packed into a single `u64`
(`parser.rs:340-358`, `packed_word` / `from_packed_word`). This is the
"compact first-two-level structure header" from the workspace intent
(`nota-next/INTENT.md:16-18`) made concrete: a higher layer can triage a
document by shape in one machine word before lowering anything. It is a
genuinely elegant primitive and `schema-next` consumes it as a witness
(`schema-next/src/engine.rs`, `MacroContext` records the header).

**The structural macro node is the conceptual heart.** The decisive
design move lives in `nota-next/src/macros.rs`. A macro node is not a text
template and not a global parser registry — it is a TYPE, and that type is
an enum that decodes by shape. The trait `StructuralMacroNode`
(`macros.rs:1267-1308`) says: a consumer enum declares its
`structural_position()` and an ordered `structural_variants()`, then the
codec tries those variants in declaration order and only after a structural
match is selected decodes the captures into domain data. `BlockShape`
(`macros.rs:194`) is the authoring vocabulary (Pascal atom, headed
parenthesis, literal, delimited block) that lowers to the `Pattern`
substrate (`macros.rs:313`). `StructuralVariantSet::validate_no_silent_conflicts`
(`macros.rs:492-506`) rejects a variant set where an earlier general
variant would make a later specific one unreachable — `silently_shadows`
is a real reachability check, not a comment. The whole macro substrate is
itself `rkyv::Archive` + `NotaDecode`/`NotaEncode` (`macros.rs:5-17`,
`30-48`), so the macro shape is schema data, not a string blob — exactly
the property `schema-next/ARCHITECTURE.md:182-206` ("Core Macro Schema")
depends on.

This is the deepest idea on the floor: **a dialect is a typed enum that
knows its own shape, decodes captures, AND re-encodes to the same surface**
(`to_structural_nota`, `macros.rs:1274`). Schema sugar is therefore
SPECIALIZED NOTA, not a one-way lowering language — round-tripping is a
trait obligation, so the schema language can never drift into a write-only
syntax (`nota-next/INTENT.md:81-87`).

## (b) The pipeline NOTA → deserialize → schema-in-Rust (rkyv) → lower → Rust

The conveyor is five clean stages (`schema-next/ARCHITECTURE.md:5-18`):

1. `nota-next::Document` parses source into blocks.
2. `SchemaEngine` records the `StructureHeader` witness.
3. Root-object-count validation.
4. `MacroRegistry` dispatches position-aware macros (imports, input/output
   enums, namespace, struct fields, enum variants) — its structural
   expectations ARE `nota-next` macro-node definitions; schema-next supplies
   only positions and handlers (`schema-next/ARCHITECTURE.md:11-15`).
5. `SchemaSource` lowers into semantic `Schema`.

The target pipeline shape is the load-bearing claim: authored `.schema`
**deserializes into Rust datatypes that fully define the schema**; that
schema-in-Rust value is **rkyv-serializable**; Rust interface code is
**lowered from that typed value** (`schema-next/ARCHITECTURE.md:21-24`).
`SchemaSource` is the typed authored-language value; `Schema` is the
semantic value consumed by emission; both archive through rkyv
(`Schema::to_binary_bytes`/`from_binary_bytes`, `schema.rs`).

**Where it stands today — two migrations, honestly stated.**

*Asschema is gone.* The compatibility endpoint (the `.asschema` text /
binary artifact and the redb-backed schema store) is fully removed from
active source: `grep -rni asschema schema-next/src schema-rust-next/src
spirit/src` returns NOTHING. `schema-next/ARCHITECTURE.md:114-128` states
it directly: "There is intentionally no `Schema::to_nota`, no semantic
`.asschema` artifact owner, and no schema store in this crate." This
migration is COMPLETE and the architecture text matches the code — a
healthy sign.

*Token lowering is genuinely in progress and the boundary is visible.*
The intent (`schema-rust-next/INTENT.md:52-57`) is that generated Rust
syntax is built as `proc_macro2`/`quote` tokens, then pretty-printed to
visible source. The CORE of that is done: type declarations, type
references, structs, and enums lower through `ToTokens` and `quote!`
(`lib.rs:962-1036`, e.g. `TypeReference::Vector` → `quote! { Vec<#inner> }`
at `lib.rs:986-987`), and `emit_type` routes through `emit_item_tokens`,
which `syn::parse2`s the tokens and `prettyplease::unparse`s them
(`lib.rs:1571-1576`, `1602-1607`). Token output is therefore Rust-validated
before it lands.

But the SUPPORT surface is still hand-built Rust-as-strings. There are 46
`emit_*` methods on the `RustWriter` (`grep -c 'fn emit_'` → 46), and the
heavy ones — `emit_signal_frame_impl` (`lib.rs:2020`), `emit_route_impl`,
`emit_object_name_enum` (`lib.rs:2208`), `emit_mail_event_support`
(`lib.rs:2445`), `emit_plane_namespaces` (`lib.rs:2647`), the
`emit_nexus_runner_adapter` (`lib.rs:2853`) — concatenate source with
`self.line(format!("impl {} {{", ...))` and friends. The whole-file count
is 43 token/quote sites vs 93 `format!`/`push_str` sites. So the engine is
mid-stream: **the typed-shape core is tokens; the runtime-support
scaffolding is strings.** The risk this carries is concrete: a string
emitter can produce text that only fails at the CONSUMER's compile step
(spirit's `build.rs` freshness check + cargo build), whereas the token
path fails inside the emitter at `syn::parse2`. This is the single most
material engine debt and it is correctly named as in-progress, not hidden.

## (c) The runtime triad — Signal / Nexus / SEMA

The three planes are not modules-by-convention; they are enforced
boundaries. The absolute statement is intent record `3d5z` (Constraint,
VeryHigh, live in the store): "the SEMA engine owns ALL database and
durable-state code, the Nexus engine owns ALL decision-making, and the
Signal engine owns ALL communication ... NO database boilerplate, NO
decision-making, and NO communication code outside its respective engine."

**Signal — the communication boundary.** In the pilot, `SignalActor::admit`
(`spirit/src/engine.rs:175`) mints the origin route, issues `MessageSent`,
validates `Input`, and produces `SignalAccepted`. Invalid `Input` becomes
`Output::Rejected(SignalRejection)` before any mail is sent or SEMA is
touched (`spirit/ARCHITECTURE.md:340`). The CLI parses one NOTA argument
into generated `Input`, frames it as short-header + rkyv bytes, sends over a
Unix socket, decodes `Output`, prints NOTA (`spirit/ARCHITECTURE.md:116-124`).
The daemon NEVER parses NOTA — `tests/socket_negative.rs` feeds
length-prefixed NOTA and arbitrary bytes through the wire and proves they
are rejected (`spirit/ARCHITECTURE.md:159-164`), and
`tests/dependency_surface.rs` proves the daemon's `--no-default-features`
tree contains no `nota-next` at all (`spirit/ARCHITECTURE.md:28-30`).
Binary in, binary out; NOTA is a text-client privilege.

**Nexus — the decision plane and the FEATURE CATALOG.** This is the
conceptual center. Record `z6qu` (Principle, VeryHigh, 2026-06-05, live):
the Nexus interface — the verbs and objects in the nexus schema — IS the
engine's internal feature interface, and its MAIN reason for existing is
VISIBILITY. Every computation, every filter or condition on results, every
conditional write MUST be a declared Nexus verb+object in the schema, never
inline hidden logic. The pilot honors this literally. The hand-written
`Nexus::step_decide` (`spirit/src/nexus.rs:289-296`) is a pure
`NexusWork → NexusAction` function — match a typed fact, emit a typed
action — and the two pilot features prove the discipline: `State`
classification is NOT a hidden write branch; Nexus emits
`CommandEffect(ClassifyState)` first (`nexus.rs:300-302`), the effect
returns `EffectCompleted(StateClassified)`, and only THEN does it emit
`CommandSemaWrite(Record)` (`nexus.rs:370-374`). Likewise the Observe
slim-output path recurses through a declared `Stash` effect
(`nexus.rs:347-359`) rather than replying with the full record set inline.
Both features are visible in `schema/nexus.schema`; neither hides in Rust.

**SEMA — the durable plane.** `Store` (`spirit/src/store.rs:34-40`) maps
generated SEMA roots onto `sema-engine` identified-table operations: a
`Record` becomes `assert_identified` (sema-engine allocates the numeric
`RecordIdentifier` and advances the durable `CommitSequence`), a `Remove`
becomes `retract_identified` (`spirit/ARCHITECTURE.md:248-256`). The
read half takes `&self` so parallel readers share the store
(`store.rs`, witnessed by a scoped-thread test in `runtime_triad.rs`).
Crash-consistency is real, not claimed: a reopened `.sema` resumes
committed records AND counters, and `StateDigest` is a real
content-addressed blake3 hash over each committed record's
`(identifier, archived bytes)` folded with the commit sequence
(`store.rs:303-314`, `spirit/ARCHITECTURE.md:278-284`) — an empty store
digests to zero. The process-boundary test kills a daemon and reopens the
file with the sequence resumed.

**The engine traits and the runner.** `triad-runtime` owns ONLY generic
mechanics (`triad-runtime/ARCHITECTURE.md:138-141` — "does not emit
schema, define component signal roots, parse NOTA, own component storage
tables, or decide component behavior"). The crown jewel is `Runner::drive`
(`triad-runtime/src/runner.rs:147-184`): a fixed five-outcome trampoline
over `NextStep<Reply, SemaWrite, SemaRead, Effect, Work>`
(`runner.rs:22-28`). `Reply` exits; the other four spend a typed
`ContinuationBudget` (`runner.rs:103-115`, default limit 32) and re-enter.
A final `Reply` is always allowed; exhaustion forces a typed
`budget_exhausted_reply` — recursion can never run away silently. The glue
between this generic loop and the component is GENERATED, not
hand-written: `spirit/src/schema/nexus.rs:766-776` emits
`NexusAction::into_runner_next_step` (the total projection), and
`lib.rs`-generated `NexusEngine::execute` (`spirit/src/schema/nexus.rs:805-818`)
constructs the `Runner`, wraps the engine in a generated
`NexusRunnerAdapter` (`nexus.rs:821-865`), and drives it. The hand-written
`Nexus` (`spirit/src/nexus.rs:208-274`) implements only the five hooks:
`decide`, `apply_sema_write`, `observe_sema_read`, `run_effect`,
`budget_exhausted_reply`. The runner loop itself is never re-written per
component — record `7ca4` ("extract the generic triad runtime runner now")
realized.

**The mail mechanism.** The `&mut Nexus` borrow on `NexusEngine::execute`
IS the single-flight guard (`spirit/ARCHITECTURE.md:203-204`): Rust's
borrow checker prevents two mutable executions on the same Nexus
simultaneously — concurrency control as a type, not a lock discipline.
`MessageSent`/`MessageProcessed<Output>` carry the same `OriginRoute` from
Signal admission through Nexus, SEMA, effects, and back to reply
(`spirit/src/engine.rs:267` `process_with`), and the `MailLedger`
(`engine.rs:53-56`) records sent/processed markers via hooks. The ledger
is honestly flagged in-memory only (`spirit/ARCHITECTURE.md:476-478`):
mail history resets on restart; only SEMA records + commit ledger are
durable.

**The nexus-schema-as-feature-catalog principle.** This is the through-line
that ties the floor to the runtime. Because every feature is a schema verb,
and the schema is the single source the Rust is lowered from, the engine's
COMPLETE internal-feature surface is readable in one `.schema` file — and
`triad-runtime/INTENT.md:53-57` makes the runner refuse to hide capability:
"it must not hide new component capability behind generic runtime code."
The runner drives ALREADY-DECLARED actions; it never invents a verb.

## (d) Where the engine is strong, where it is weak

**Strong.**

- The floor's "decode by shape" via `StructuralMacroNode` with mandatory
  round-trip encoding (`macros.rs:1267-1308`) is a genuinely novel, sound
  primitive — schema sugar is specialized NOTA, not a write-only DSL.
- Plane separation is type-enforced, not convention. The `compile_fail`
  doctest in `spirit/src/lib.rs:15-21` proves a Nexus envelope with the
  same inner payload names CANNOT be applied to the SEMA engine — the
  triad boundary is checked by the compiler.
- The runner's typed continuation budget (`runner.rs:103-115`) makes
  unbounded recursion impossible and testable, with a forced typed reply
  on exhaustion. 32 is a sane default and is itself a typed
  `ContinuationLimit`, not a magic literal.
- Binary/text bifurcation is proven by executable guards
  (`dependency_surface.rs`, `socket_negative.rs`), not asserted. The daemon
  provably links no NOTA decoder.
- `StateDigest` is a real content hash (`store.rs:303-314`), and durability
  is proven at the real process boundary, not in-memory.
- Architecture docs match code (Asschema removal verified by grep returning
  empty) — the rarest and most valuable health signal.

**Weak.**

- *Token-lowering is half-migrated.* 46 `emit_*` string methods still build
  the entire runtime-support surface (signal-frame, route, object-name,
  mail-event, plane, runner adapter) via `self.line(format!(...))`
  (`lib.rs:2020`, `2208`, `2445`, `2647`, `2853`). These can emit invalid
  Rust that only fails at the consumer's compile. This is the top engine
  debt.
- *The deployment gap.* The schema-derived `spirit` (0.1.0) is NOT the
  deployed binary; persona-spirit v0.5.2 still serves intent. The engine is
  proven in-tree but not in production. Until the cutover (record `fe2j`:
  port-first ordering — lojix triad-port BEFORE CriomOS cutover), the new
  engine is a pilot, and the workspace carries a dual stack.
- *Crate-root barrel tension.* `spirit/src/lib.rs:47-86` flat-re-exports
  every generated noun at the crate root. Record `k4d9` (live, Clarification)
  warns this exact thing: generated internal Nexus nouns should live in the
  plane module, not be promoted to a mixed crate-root namespace. The pilot
  currently does the barrel for ergonomics; ARCHITECTURE.md:186-191 flags
  it as a known tension, not a settled design.
- *Schema upgrade is generated-but-empty.* The `UpgradeFrom`/`AcceptPrevious`
  traits emit (`spirit/src/schema/nexus.rs:867-877`) but nothing implements
  them, and no `last-version` package exists yet
  (`spirit/ARCHITECTURE.md:406-409`, `479`). The migration emitter
  (`schema-rust-next/src/migration.rs`) exists but the loop isn't closed.
- *Single-listener, in-memory ledger.* The daemon is one listener over one
  engine behind a mutex (`spirit/ARCHITECTURE.md:99`); multi-listener /
  meta-signal handoff is deferred. Acceptable for a pilot, named honestly.
- *Contract-vs-daemon split unsettled.* Records `l6zw`/`bodd` (live) say a
  contract repo must carry ONLY wire vocabulary, never Nexus/SEMA engine
  surfaces — and the first cloud port wrongly copied spirit's all-in-one
  schema into the contracts. The pilot's single-crate all-in-one shape is
  the bootstrap, not the triad-split end state; whether `schema-rust-next`
  needs redesign for the split is itself under audit (`l6zw`).

## What the engine fundamentally IS — the single deep idea

**The schema is the program, and Rust is its shadow.**

The engine is a machine for making ONE typed schema description the single
source of truth, and projecting everything else — the wire types, the
codecs, the route headers, the engine traits, the runner glue, the feature
catalog — DOWN from it. NOTA is the floor that lets that description be
read by shape rather than by keyword; the structural macro node makes the
schema language specialized-but-round-trippable NOTA rather than a one-way
DSL; `schema-next` turns shape into a typed, rkyv-serializable schema-in-Rust
value; `schema-rust-next` lowers that value to visible Rust source; and the
triad runtime gives that generated Rust a fixed place to run where the only
hand-written thing left is the real algorithm — "match typed input, make
the decision, call the next typed interface, return typed output"
(`triad-runtime/ESSENCE.md:6`).

The nexus-schema-as-feature-catalog principle (`z6qu`) is the moral of the
whole machine: when the schema is upstream of all the code, the schema can
be made the READABLE INVENTORY of everything the engine does — because
anything the engine can do had to be declared there first to exist in the
Rust at all. The engine's deepest purpose is not code generation; it is
making a running daemon's complete behavior surface VISIBLE in one typed
declaration, with the compiler enforcing that nothing escapes the
declaration. Code generation is merely the mechanism by which "what the
schema says" and "what the daemon does" are kept provably identical.
