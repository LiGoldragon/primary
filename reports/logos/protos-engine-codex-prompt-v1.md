# Protos engine — Codex implementer prompt v1 (bootstrap the new engine, 100% in the new syntax)

Authored 2026-07-19, session `ProtosEngine`, lane `CodexBootstrap`, generalist,
Opus 4.8 (1M). This file is the prompt the psyche hands to a Codex agent. It is
self-contained: it restates the syntax law, the Protos vision vocabulary, the
concrete bootstrap task, the conduct, and the joints that remain the psyche's to
rule. It carries only verbatim positive examples verified this pass against the
codec / real repo files (each example is cited); illegal forms are described in
prose, never exemplified. The design authorities behind it are
`reports/logos/textual-form-vision-design-v2.md`,
`reports/logos/stream-construct-design-v1.md`,
`reports/logos/nomos-macro-model-v1.md`, `reports/logos/up-close-design-v1.md`,
and tracker epic `primary-56d1`.

Revision note (2026-07-19, same lane): the psyche ruled on all six previously-open
joints. Those rulings are now seated as settled law in the body (full `Core*` →
`Encoded*` rename §1; one NameTable per component §1; encoded-form contracts in the
signal repos §1; Lineage B is THE generator and Lineage A is deprecated §3.1; the
byte oracle removed, acceptance is working programs §3.3/§3.3a; the
bootstrap-branch workflow and periodic cross-examination §3.3a). Only two joints
remain open (§6): Protos crate topology and the Nomos macro-definition surface.

Everything from `## PROMPT` down is the handoff to the Codex agent.

## PROMPT

You are implementing the bootstrap of the Protos language engine. You work 100%
in the new strict positional syntax and constraints, migrating the engine in
flight. Read this whole prompt before touching anything. You have no local skill
access; the full law you need is restated here.

### 1. What Protos is (vision vocabulary — use these exact terms)

Protos is one end-to-end language engine, built in layers, starting from NOTA.
Most shared logic lives in the Protos library. Speak in these terms, because the
code must reflect the conversation:

- A language has **two views**: a **TextualForm** and an **EncodedForm**.
- The **EncodedForm is the truth.** It is a stringless value family (a Core
  value). Every identity, every hash, every wire message is the EncodedForm.
- The **TextualForm is GENERATED**, not primary. It is an **index of files**:
  a map from a file (or a string) to its content. A TextualForm is produced from
  `EncodedForm + StructureTree + NameTree` (and possibly other trees).
  - The **StructureTree** says, for each thing, how it is re-emitted
    **structurally** — it is the data-driven encoder/decoder, not a side artifact.
  - The **NameTree** says what each thing is **called**, keyed by its
    **encoded identifier** (the stringless index a value carries in place of a
    name). Names are data in the NameTree, never embedded in the EncodedForm.
  - All IDE-like functionality (help, rename, go-to-definition, atomic editing of
    code) is built from these trees. A rename touches one NameTree row and no
    EncodedForm value.
- Say **"encoded form"** and **"encoded identifier"** — not "core value" / "core
  id" — in new code and prose you write, so the code reflects the conversation.
  This is a **full rename, ruled and green-lit** (psyche verbatim: *"full rename
  green light. It was from the start but agents tend to misunderstand my drastic
  engineering approach."*). The concrete `Core*` **types themselves** rename to the
  `Encoded*` / EncodedForm terminology — not only the trait or the view. Take the
  full-strength reading: no partial, view-only, or alias-only rename. Carry the
  rename through the crate and symbol names wherever `Core*` names appear.
- **All conversion to and from a TextualForm goes through one Protos trait.** The
  input side does not start from bare files: it starts from a **manifest of
  files** — an explicit file list that resolves dependencies cargo-crate-style.
  The manifest may be agent-generated ad hoc or checked into version control. It
  is **file-path based** for now; a dedicated source-management component is out
  of scope, so do not build one.
- **Nomos is a pure transformer, entirely in the encoded form.** Schema → logos
  conversion happens through Nomos and never touches text: Nomos knows the schema
  **encoded-form** types and the logos **encoded-form** types and maps one to the
  other. It is **not a store.**
- **One NameTable per component (ruled).** Psyche verbatim: *"yea, one nametable
  for each component. nomos uses the schema nametable to populate the logos
  nametable (and uses its own to read/write from/to its own encodedform)."* Every
  component owns exactly one NameTable for its own EncodedForm. In the schema→logos
  transform, Nomos **consumes the schema NameTable to populate the logos
  NameTable** — adding the new names it introduces that were not present in the
  schema — and Nomos **additionally owns its own NameTable**, which it uses to read
  and write its own EncodedForm. Three tables are in play (schema's, logos's, and
  Nomos's own), each owned by its component; Nomos is the transform that carries
  names from the schema table into the logos table.
- The **encoded-form type definitions are wire contracts, seated in the signal
  repositories (ruled: psyche verbatim "yes").** Talking to a logos daemon means
  talking the logos encoded form. So those type definitions live in the **signal
  repositories**, as another file in the shared contract crates, and they are
  **written in schema itself**.
- Syntax is **strict and simple**. Field names were removed entirely (see §2).
  Anything ambiguous is not worked around — it is **slashed**: simplify the
  architecture and syntax and start over. If you find yourself adding a side path
  to make something fit, stop (see §5).

### 2. The syntax law — total, restated in full

Protos is the shared structure behind the NOTA-family textual surfaces (schema,
NOTA, logos). Its universal aspect is three things: how delimiters are used,
capitalization, and the typed-inner-blocks approach to parsing. Schema expresses
that structure most accurately. Obey every law below and, when you write an
example, quote a real artifact — never spell one from memory.

**2.1 Positional records — the first law, outranking every other rule here.**
Protos records are positional. There are **no field names anywhere in Protos.** A
block's positions are typed by the **expected type at each boundary**: the type
standing at a position fixes the slot count and the meaning of each slot. Field
identity, argument identity, and variant-payload identity come from **expected
type plus position** — a block carries no labels. A construct's sections are
ordered positional slots typed by the expected type at their boundaries, never
labeled heads.

An explicit field name is **completely illegal everywhere** — never authored,
never a candidate, never emitted, not even by a codec. There is **no collision
exception**: two fields of the same type are told apart by position alone, never
by a name. Concretely, the illegal shape is a lowercase atom applied to a type in
a field slot; do not write it, do not propose it, do not present it as valid
Protos. This law bars fabrication, not disclosure: if you encounter a field name
in a real artifact you may quote that artifact exactly and report it as a found
**illegal** form, but you never author, propose, or present a named form as
correct.

The expected type stands at every boundary: file kind, schema field, declaration
slot, generic argument, inner block. The raw layer discovers only atoms,
delimiters, and glued-dot application — it classifies nothing and never guesses
from content. Each inner block is re-read under the type expected at its position
(typed inner blocks), so the same raw shape means different things under
different expected types.

**2.2 Delimiter roles.** Each delimiter carries one role; the glyph set is
`. ( ) [ ] { }`:

- `{ }` — structs (positional field records); a single-element brace is a newtype.
- `[ ]` — vectors (homogeneous, where order or duplicates matter) and enum
  variant lists.
- `( )` — payloads: an application payload (`Head.( … )`), a map written
  `Map.(alpha.1 beta.2)`, or a string whose content forces the bracket.
- `(| … |)` — the literal-preserving multiline string, for content carrying
  delimiters, comment markers, or newlines; the close marker `|)` is escaped in
  the body.

A canonical string is a bare atom (`schema`); a period-joined bare chain reclaims
its dotted text (`a.b`); a string with spaces takes parentheses (`(alpha beta)`);
wrapping an already-canonical bare atom in parentheses is redundant and rejected.

**2.3 Glued-dot application.** A glued period binds a head to the following
payload as one right-associative application: `Topics.Vector.Topic` reads as the
head `Topics` bound to the payload `Vector.Topic`. The dot binds only when glued
on both sides: a space before or after the period, a head with a trailing period
and no payload, and a payload with a leading period and no head each fail to
parse. A period is a structural operator, so an atom never contains one; a dotted
path or a float is an application reconstructed from its segments.

**2.4 Capitalization discipline.** Types, kind heads, and enum variants are
PascalCase (`Topic`, `Stream`, `Vector`, `Decision`); canonical string atoms and
map keys are lowercase bare atoms (`schema`, `alpha`, `beta`). Capitalization is
load-bearing, not decoration: it statically distinguishes a declaration's
PascalCase kind head from lowercase data atoms. A lowercase atom labeling a
positional slot would be a field name, which is illegal everywhere.

**2.5 Positional disambiguation of same-typed fields.** When a struct holds two or
more fields of the same type, position alone assigns each its meaning: the
struct's declared field order fixes which slot is which, and the expected type at
each position carries identity. No name is ever added to separate same-typed
fields — not authored, not codec-emitted. The disambiguation is entirely
positional, the same rule that governs every other slot. (The `PositionalSignature`
machinery in the codec already does this.)

**2.6 Generics and newtypes.** Generics resolve by kind and projection through a
closed table — `Vector`, `Optional`, `ScopeOf`, `Map`, `Bytes` — never by an open
or aliased head string; applications dispatch on kind and projection, not on head
text: `Topics.Vector.Topic`, `Map.(alpha.1 beta.2)`. A single-element braced form
is a newtype carrying just the wrapped type and no field name
(`Summary.{ Description }`, `CommitSequence.{ Integer }`); a multi-field brace is a
struct (`Entry.{ Topics Kind Description Magnitude }`). There is no multi-field
tuple.

**2.7 Verified positive examples (each quoted from a real artifact — copy these
shapes, never invent one).**

Schema declarations, from the `spirit`/`triad` reactive fixtures
(`repos/schema-structural-pipe-retirement/tests/fixtures/big-schemas/*.schema`)
and the `protos-syntax` skill's `spirit-min.schema` set:

```
Topic.String
Topics.Vector.Topic
Summary.{ Description }
Entry.{ Topics Kind Description Magnitude }
Kind.[Decision Principle Correction Clarification Constraint]
```

A newtype and a same-typed-field struct, from the live core-schema round-trip
tests (`repos/core-schema/tests/textual_roundtrip.rs:42` and `:78`), decoded and
re-encoded by the v0.3.0 field-name-ban codec:

```
CommitSequence.{ Integer }
DatabaseMarker.{ CommitSequence StateDigest StateDigest }
```

In `DatabaseMarker`, the two `StateDigest` fields carry **no** names; they are
told apart purely by their positions (second and third slots).

EncodedForm value encodings witnessed by the NOTA grammar tests — struct, enum,
option, vector, map:

```
{(commit sequence) 4}
Idle
Tick.7
Range.{3 9}
None
Some.42
Some.(cache entry)
[alpha beta gamma]
Map.(alpha.1 beta.2)
```

**2.8 Deterministic Rust name derivation (the lowering rule).** The stringless
EncodedForm carries no field names; Rust is a **name-bearing** target, so distinct
Rust identifiers are **manufactured at lowering**, by a pure deterministic rule —
never by reading a stored or authored name. The rule (landed in core-nomos, green):

- A struct field's Rust name is the `snake_case` of its type.
- When a type names more than one field in the same struct, each such field is
  distinguished by prefixing the **ordinal English word of its position among the
  same-typed fields** (`first_`, `second_`, …). The mapping is total over `usize`
  and never falls back to a numeral: `first`, `second`, `third`, `twenty_first`,
  `one_hundredth`, and so on.
- A type naming a single field keeps the bare base name — this is the degenerate
  empty-ordinal case of the one rule, not a separate branch.

It is a pure function of field **position and type**: the same struct always
lowers to the same names, and adding a later field of another type never moves an
earlier field's name. It lives in **Nomos lowering, not in schema**: core-schema
stays untouched at `2e47dec5`; the rule is `Engine::derive_group_names` with the
`SameTypeOrdinal` newtype spelling the ordinal word
(`repos/core-nomos/src/engine.rs`).

Verified emitted Rust — the exact output of the pipeline test
`illustrative_struct_from_schema_text_lowers_and_derives_names`
(`repos/core-nomos/tests/pipeline.rs`), which I ran this pass, from the positional
input `DatabaseMarker.{ CommitSequence StateDigest StateDigest }`:

```rust
#[rustfmt::skip]
#[cfg_attr(
    feature = "nota-text",
    derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode)
)]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct DatabaseMarker {
    pub commit_sequence: CommitSequence,
    pub first_state_digest: StateDigest,
    pub second_state_digest: StateDigest,
}
```

The single `CommitSequence` field keeps its bare `commit_sequence`; the two
`StateDigest` fields become `first_state_digest` / `second_state_digest`. Before
the rule they both derived `state_digest` — invalid Rust; now positionally
distinct.

**2.9 The Nomos macro-definition surface is UNSETTLED — do not exemplify it.** How
a Nomos macro names its input and body and spells substitution (the `$` vs `<< >>`
escape, the input struct shape) is under live psyche design and is not settled. Do
not invent or exemplify its spelling. If you must touch it, name it unsettled and
escalate (§6). This includes the escape sigil.

### 3. The concrete bootstrap task

The psyche's question is answered: **the current Rust-emitting shortcut has
effectively already been re-bootstrapped from the new strict syntax.** Your job is
to carry that from "proven on contract-shaped fixtures" to "the engine rebuilds
its own types." Here is the terrain and the plan.

**3.1 Two lineages — do not conflate them. Lineage B is THE generator; Lineage A
is deprecated, not adapted (ruled).** Psyche verbatim: *"yes, if we dont need it,
all the better. We should get codex to adapt components using it, and he can bugfix
it on a 'bootstrap' branch/worktree used to generate bootstrap code until main
catches up (I guess we should have a cross examination once in a while to make sure
some good ideas dont fall through the crack, or some bad idea isnt forgotten)."*
And on the old syntax intake: *"if we have a generator that works, we dont need to
worry about the old components; we'll deprecate and eventually delete them."*

- **Lineage A (the literal "old" generator) — DEPRECATED, eventual deletion.**
  `repos/schema-language` (semantic decode) plus `repos/schema-rust`
  (`RustEmitter`, `src/lib.rs:62`, entry `emit_file_from_true_schema` at `:84`).
  This is the generator that today emits the real `// @generated by schema-rust`
  files into consumer `src/schema/` directories. It does **not** depend on
  core-schema, and its pre-ban model still resolves same-typed-field collisions by
  an **author-supplied disambiguator stored as name data** — a spelling that is now
  illegal Protos. **Do not rework it.** It is deprecated and slated for deletion:
  do not port the ordinal rule into `schema-language`, do not teach it the new
  syntax, do not fix its now-illegal disambiguator model. It stays only until its
  consumers are moved onto Lineage B, then it is deleted.
- **Lineage B (the new self-hosting pipeline) — THE generator.** `core-schema`
  (v0.3.0, `2e47dec5`, field-name-ban codec) → `core-nomos` (macros + the
  deterministic name rule of §2.8) → `core-logos` → `textual-rust`. It intakes the
  new strict positional syntax, derives names by rule, and emits the Rust that
  builds the engine, with `repos/language-engine-witness` running the delivered
  libraries as OS processes to prove the emitted Rust compiles and behaves. This is
  the generator all components move onto. (It was developed against byte-exact
  goldens of Lineage A's output; per §3.3 and §3.3a, **that byte oracle is now to
  be removed** — working programs are the acceptance, not byte-equality.)

**3.2 What is already done (verify in the artifacts, do not re-derive from
memory).** The deterministic same-typed-field rule is **landed and green** —
core-nomos main carries it (jj commit `4d6e8480`, re-pinned to core-schema
`2e47dec5`; `nix flake check` green). So the generator does **not** hit the
same-typed-field gap; it already crosses it. Nothing in the bootstrap waits on
that rule.

**3.3 What remains — three bounded areas.**

1. **Construct coverage.** Lineage B is proven on contract-shaped types
   (structs, enums, newtypes, derive/attribute vectors — the signal-* contracts).
   The engine's **own** types (in `core-schema/src`, `core-logos/src`,
   `name-table`, `structural-codec`, `textual-rust`) use richer Rust: trait
   definitions, impl blocks, free methods, generics, associated types. The
   `CoreItem` algebra in `core-logos` already names these variants
   (`Newtype, Struct, Enumeration, Alias, TraitDefinition, ImplBlock, FreeMethod`);
   the work is to confirm and complete `textual-rust`'s **emission** coverage for
   them and the schema syntax that **authors** them. Where a construct is not yet
   expressible cleanly, do not bolt on a special case — flag it (§6).
2. **Authoring + manifest.** The engine's own types are currently **hand-written
   Rust with no `@generated` marker** (confirmed: grep for `@generated` over
   `core-schema/src` and `core-logos/src` finds nothing). Author them as **schema
   text in the new positional syntax**, presented as a **manifest of files**
   (§1) — a file-path-based list resolving dependencies cargo-crate-style. The
   **encoded-form type definitions are wire contracts**, so author them in the
   **signal contract crates**, in schema itself.
3. **Self-host proof, and REMOVE the byte oracle.** Drive the manifest through
   core-nomos → textual-rust, rebuild the engine from the emitted Rust, and accept
   on **working programs** (the `language-engine-witness` style: the rebuilt
   libraries run and pass their behavior tests, all-green against a truthful
   denominator). Psyche verbatim: *"I dont care about byte-exactness. get rid of
   that. working programs is what we want."* So **delete the byte-exact golden
   comparison entirely** — it is not preserved as scaffolding, not kept as an
   inner-loop check, not restored anywhere. The Lineage-B pipeline tests that today
   assert byte-equality against schema-rust goldens
   (`repos/core-nomos/tests/pipeline.rs`, `enriched.rs`) are converted to, or
   replaced by, working-program checks; the byte comparison is removed.

**3.3a The bootstrap branch/worktree workflow (ruled working instruction).** Do the
pipeline bugfixing and bootstrap-code generation on a **dedicated `bootstrap`
branch/worktree**, kept separate from `main`, and used to generate the bootstrap
code **until `main` catches up**. Adapt the components that used the old generator
onto Lineage B from that branch. Run a **periodic cross-examination** between the
`bootstrap` branch and `main` — a deliberate checkpoint whose purpose is to make
sure **good ideas do not fall through the cracks and bad ideas are not silently
kept**. Surface the diffs and the decisions at each cross-examination rather than
letting the two lines drift silently. (Obtain an isolated worktree through the
orchestrator's `RequestWorktree` for this branch; do not hand-share a checkout.)

**3.4 Effort shape.** This is **real but bounded rework**, not a small tweak and
not a from-scratch rebuild. The one thing that could have forced a rewrite — the
name-derivation gap for same-typed fields — is **closed**. The residual is
concentrated in `core-nomos` / `core-logos` / `textual-rust` (construct coverage)
plus new schema-authored type sources plus a manifest driver. Sequence it: prove
one engine crate (start with the smallest, e.g. `name-table` or `content-identity`)
self-hosts end to end before authoring the rest.

**3.5 The re-pin cascade context (adjacent, do not silently absorb).** Ten repos
still pin the OLD core-schema `d3cdee9` (v0.1.0): direct in `golden-bridge`,
`signal-sema-storage`, `schema-engine`; transitive in `logos-engine`,
`sema-storage`, `language-engine-witness`, `signal-nomos`, `nomos-engine`,
`signal-logos`, `signal-schema`. The rule that blocked them has landed, so the
cascade is now **unblocked but not executed**. It is a separate lane's work —
touch it only if your task explicitly includes it, and if a dependency pin blocks
your build, report it rather than re-pinning the world.

### 4. Conduct (standing law for this effort)

- **Acceptance = working programs with all-green, truthful denominators.** Every
  test/verification claim must be a real all-green run against the true full set —
  never a green subset presented as the whole. State the exact command and what it
  covered. In this workspace, durable evidence is owned by Nix: flake checks,
  named check derivations, named stateful runners. Bare `cargo test` is inner-loop
  evidence unless the repo says otherwise.
- **No bypasses seated as design.** When a shortcut diverges from the envisioned
  design, surface it as an **open decision**, never seat it silently as though it
  were the design. A convenience bypass presented as the real thing is
  unacceptable (the psyche calls it "of poor taste and deceitful"). A special case
  should **dissolve into the normal case**; if a fix works only by adding a side
  path future readers must remember, keep looking for the shape that makes the
  rule explicit — or, if an accepted constraint truly forces the side path, stop
  and report the forced special case.
- **Never fabricate syntax.** Every example you write must be a verbatim real
  artifact — codec round-trip output or a real repo file. Never spell a form from
  memory, and never present a field-named form as valid. If a real artifact
  contains an illegal form, you may quote it only as a found-illegal artifact.
- **Describe illegal forms in prose, never exemplify them** in any doc or prompt
  you author.
- **Anything ambiguous is reported for simplification, not worked around.** If the
  architecture or syntax does not admit something cleanly, the answer is to
  simplify and start over on that piece — flag it, do not improvise a workaround.
- **Patch source, not installed output.** No `/nix/store` edits, no PATH shims, no
  copied installed source. Closeout is blocked if behavior depends on uncommitted
  runtime edits.
- **Commit and push what you edit**, whole working copy on primary; surface stale
  dependency pins and unmerged producer branches at closeout.

### 5. Design authority boundary

You may investigate and propose major design changes and decide narrow
implementation details **inside an explicitly accepted design**. You may **not**
implement or deploy material changes to authority, security posture, schemas,
generated curriculum, wire/kind topology, compatibility, or deployment policy
without first presenting the concrete delta and receiving explicit psyche
acceptance. Goal-level approval or non-rejection is **not** acceptance. When in
doubt, stop and escalate (§6) rather than broaden scope.

### 6. Joints that are still the PSYCHE's to rule — do NOT settle these silently

Six earlier joints have now been **ruled** and are seated as law above (full
`Core*` → `Encoded*` rename, §1; one NameTable per component with Nomos populating
the logos table, §1; encoded-form contracts in the signal repos, §1; Lineage B is
THE generator and Lineage A is deprecated-not-adapted, §3.1; the byte oracle is
removed and acceptance is working programs, §3.3 / §3.3a; schema-language is
deprecated and not taught the ordinal rule, §3.1). Do not reopen them.

Only these remain genuinely open. Mark them in your work and escalate; do not
resolve them by implementation choice:

1. **Protos crate topology.** Whether the delivered `structural-codec` (trait +
   codec) and `name-table` **fold into one `protos` crate**, or `protos` becomes
   an **umbrella** re-exporting them, or they become a `protos-*` family, is open
   (design-authority `[DECISION 2′]`). This interacts with the full `Core*` →
   `Encoded*` rename (§1): the rename is ruled, but which crate names the renamed
   types land in is part of this open topology. Do not rename or merge crates on
   your own authority — carry the rename inside the existing crate boundaries and
   escalate the topology.
2. **The Nomos macro-definition surface, including the escape sigil.** Unsettled
   (§2.9). Do not exemplify or fix its spelling.

### 7. Return shape expected from you (Codex)

Return: (a) which engine crate you self-hosted first and the exact all-green
command that proves it rebuilds and runs; (b) the construct-coverage gaps you hit
in `textual-rust` / `core-logos` and how you closed or flagged each; (c) the
manifest you authored (paths) and where the encoded-form contracts landed in the
signal crates; (d) every §6 joint you touched, phrased as an open decision for the
psyche, with your recommendation but never a silent resolution; (e) any forced
special case you could not dissolve, reported rather than buried.
