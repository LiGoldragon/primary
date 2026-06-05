---
title: 533/2 — Deep situation report — Engine + code-pattern forks
role: designer
variant: Psyche
date: 2026-06-05
session: 533-deep-situation-report (sub-agent 2 of N)
topics: [engine, schema-rust-next, schema-next, triad-runtime, structural-macro-node, token-lowering, methods-on-nouns, forks, decision-points]
description: |
  Scan of the schema-derived / triad engine for GENUINE design forks the
  psyche must rule on — distinguished from execution-remaining. Grounds every
  claim in file:line and Spirit record id. Finding: most of the named "open
  debts" from the 532 audit are now SETTLED in direction (de8i, 4np2, vez8,
  xai7, opvx, rpr5 all land the design); the real remaining forks are
  narrower and three of them are genuine psyche calls.
---

# 533/2 — Engine + code-pattern forks

## Method

Read the 532 engine + code reports, then went to the live source under
`/git/github.com/LiGoldragon/` (schema-rust-next, schema-next, nota-next +
derive, triad-runtime) and the live Spirit store. Counted the real string-vs-
token ratio, read the heavy emit methods, checked whether the structural macro
node derive is actually wired in, and read the design records (de8i, 4np2,
xai7, vez8, opvx, rpr5, z6qu, jo1x) in full. The discipline of this report:
**separate "the psyche already decided this; only execution remains" from "two
patterns genuinely compete and intent does not settle it."** Most of the engine
falls in the first bucket. I report the second bucket as forks.

## The honest current state (so forks are legible)

Numbers from live source, `schema-rust-next/src/lib.rs` (4122 lines):

- `ToTokens` impls exist for the core schema nouns: `RustIdentifier`
  (`lib.rs:962`), `RustTypeReferenceTokens` (`:978`), `RustDeclarationTokens`
  (`:1020`), `RustAliasTokens` (`:1063`), `RustNewtypeTokens` (`:1095`),
  `RustStructTokens` (`:1129`), `RustFieldTokens` (`:1170`), `RustEnumTokens`
  (`:1223`), `RustEnumVariantTokens` (`:1254`). 23 `quote!` sites.
- BUT a `RustWriter` god-struct still exists (`lib.rs:1385`, `impl` at `:1496`)
  with **47 `emit_*` methods** and **573 `self.line(...)` string sites** + 96
  `format!`. The token core fails at `syn::parse2` inside the emitter
  (`lib.rs:1592-1594`); the string surface can only fail at the CONSUMER's
  `cargo build`.
- The structural macro node **derive exists** (`nota-next/derive/src/lib.rs:23`,
  `#[proc_macro_derive(StructuralMacroNode, ...)]`) and is real, but
  schema-next uses it for exactly **one** type (`SourceVariantSignature`,
  `schema-next/src/source.rs:878`). The rest of schema-next still dispatches
  through the hand-rolled `MacroRegistry`/`MacroDispatch`/`MacroContext` path
  (`schema-next/src/macros.rs:234`, `lib.rs:19-20`).

So the engine is genuinely mid-migration on TWO arrows at once: the lowering
arrow (string → token, god-struct → methods-on-nouns) and the floor arrow
(hand-rolled macro registry → structural-macro-node derive). Both DIRECTIONS
are recorded; the question is whether anything in the *how* is an open design
choice or pure execution.

## What is SETTLED (execution-remaining — NOT psyche questions)

I want these on the record so the psyche isn't asked to re-decide them:

- **Finish-the-token-lowering direction.** `4np2` (Principle, High) +
  `de8i` (Principle, High) + `schema-rust-next/INTENT.md:40-72` settle it
  fully: every schema noun owns its `ToTokens`; the cross-object logic becomes
  "its own type (a PlaneType) that the per-noun render methods consult, not a
  reason for a god-struct" (de8i, verbatim). The RustWriter god-struct is
  condemned by name in the record. **This is execution**, not a fork — the
  psyche already said where the verbs go.
- **The enum-payload-variant rule** (operator 290 → 319) is NOT a psyche fork.
  It is grounded in still-live records (1269 "no empty wrappers", 1467/1468)
  and the operator's own report says "the emitter needs no new kind for any of
  this" (319:101). Its only open status is *where it's written down* — operator
  319:137 PROPOSES it land as a constraint in
  `schema-rust-next/ARCHITECTURE.md`. That's a designer task, not a psyche
  decision. (Flagged in §"Settled-but-undone" below, not as a fork.)
- **Runner concurrency** (`opvx`, Decision, High): "Future runner concurrency
  mode is a runtime or deployment configuration choice... the public contract
  does not encode how parallel a daemon runs." Decided. Not a fork.
- **The generated runner adapter** (`rpr5`, Decision, High): "the bundled triad
  runner adapter is generated glue only." Decided. The runner loop lives in
  triad-runtime (`runner.rs:147`); components implement five hooks. Not a fork.
- **The deployment gap** (schema-derived spirit 0.1.0 not deployed;
  persona-spirit v0.5.2 still serves). This is a cutover-ordering execution
  item governed by `fe2j` (port lojix before CriomOS), not a design fork.

## FORK A — Does the runtime-support surface migrate as projection-noun
## `ToTokens`, or as exported `quote!` fragments from triad-runtime?

**The fork.** de8i settles that schema *nouns* render themselves and that
*cross-object schema logic* (plane split, projections) becomes a projection
TYPE. But seven of the 47 emit methods emit Rust that is **not a projection of
any schema noun at all** — it is FIXED runtime glue, the same every time,
parameterized only by a handful of type-names:

- `emit_nexus_runner_adapter` (`lib.rs:3058`) emits a literal
  `struct NexusRunnerAdapter` + `impl triad_runtime::RunnerEngines` whose body
  is identical for every component (`lib.rs:3058-3090` is hand-typed Rust
  strings; only `shape.reply_type`, `shape.sema_write_input_type()`, etc. vary).
- `emit_nexus_runner_next_step_projection` (`:3008`),
  `emit_mail_event_support` (`:2466`), `emit_plane_namespaces` (`:2668`),
  `emit_signal_frame_impl` (`:2041`), `emit_route_impl` (`:2017`).

These resist the de8i framing because there is no `RustStruct`/`RustEnum`
schema noun whose `ToTokens` they are. The competing patterns:

- **Option A — projection-noun ToTokens.** Introduce real projection nouns
  (`NexusRunnerShape` already exists, `lib.rs:1430`; give it + siblings a
  `ToTokens` impl). The runtime glue becomes `quote! { struct NexusRunnerAdapter
  ... }` on the projection type. Keeps everything in schema-rust-next, token-
  validated, consistent with de8i's "projections become their own type."
- **Option B — triad-runtime exports the glue as a generic.** The adapter is
  the SAME every time; arguably it should be a generic `impl` /
  `quote!`-fragment **owned by triad-runtime**, with the generator only wiring
  the component's four type-names into a tiny `type` binding. This shrinks the
  emitter and puts the runtime contract where the runtime lives (consistent
  with `triad-runtime/INTENT.md:53-57` "the runner must not hide capability"
  AND with `rpr5` "the adapter is generated glue only" — but rpr5 says
  *generated*, which leans A).
- **Option C — leave it string-templated.** Honest only as a temporary state;
  the audit named this the top engine debt precisely because string glue fails
  at the consumer.

**Why this is a psyche question and not execution:** de8i covers schema-noun
projections; it does NOT pin down code that belongs to NO schema noun. A vs B
is a real architectural boundary call — does the generated component crate own
its runtime adapter (A), or does triad-runtime own it and the component just
parameterizes (B)? That changes what triad-runtime's public surface IS. The
designer lean is A (keeps token-validation + de8i symmetry, matches rpr5's
"generated"), but B is genuinely attractive for the parts that never vary and
the psyche's "name the noun, collapse the duplication" instinct (532's pattern-
of-patterns) could read either way here.

## FORK B — Is schema-next's hand-rolled MacroRegistry retired in favor of
## the StructuralMacroNode derive, or do both coexist by design?

**The fork.** The structural macro node is, per the 532 engine report, "the
conceptual heart of the floor," and `xai7` (Principle, VeryHigh) +
`vez8` (Decision, **Maximum**) say schema IS specialized NOTA built on
structural macro nodes — "a schema file is full NOTA," decoded by the
structural-macro-node codec. The derive that realizes this exists
(`nota-next/derive/src/lib.rs:23`). YET schema-next uses it for exactly one
type (`source.rs:878`) and otherwise still runs the older
`MacroRegistry`/`MacroDispatch` position-aware dispatch
(`schema-next/src/macros.rs:234`, `engine.rs`). Two macro-handling subsystems
live side by side.

The competing readings:

- **Option A — the derive supersedes the registry; the registry is legacy.**
  vez8 is Maximum and says schema deserializes "via the structural macro node
  codec" directly into schema-in-rust. Read literally, the `MacroRegistry`
  path is the pre-structural-macro-node implementation and should be migrated
  out — every schema authoring form (imports, input/output enums, namespace,
  struct fields, enum variants) becomes a `#[derive(StructuralMacroNode)]`
  enum, first-structural-match-wins, no position-handler registry.
- **Option B — they're different layers and both stay.** The `MacroRegistry`
  might be doing position-aware *document-level* orchestration that the
  per-enum derive doesn't replace, with the derive only for leaf variant-
  signature shapes. If so, "schema is built on structural macro nodes" is
  satisfied at the leaf and the registry is the legitimate composition layer.

**Why this is a psyche question:** I cannot tell from the source alone whether
the one-type usage is "migration barely started" (A, a large execution effort
the psyche should greenlight) or "this is the intended division of labor" (B,
in which case vez8's "schema is full NOTA via the macro-node codec" is already
honestly true and no further migration is wanted). The records lean A
(vez8 Maximum, xai7 VeryHigh, both speak of THE codec as the deserialize path),
but the live code looks like B, and the gap between a Maximum record and a
one-type implementation is exactly the kind of thing the psyche should rule on
before someone spends days migrating the registry out — or before someone
declares the migration "done" when it's one type deep. **Designer lean: confirm
A is the target and that the registry is legacy-to-retire, OR correct me that
B is the design.** This is the single biggest "is the Maximum record actually
realized?" gap in the engine.

## FORK C — `jo1x` (role-name-as-trait) vs the generated concrete enum names:
## does the generator emit trait-mediated runtime code now, or later?

**The fork.** `jo1x` (Principle, Medium) says: "When a reusable engine-role
name is instantiated by component-specific variants, the reusable name should
be represented as a trait or interface rather than treated as one component's
concrete enum name. Shared/runtime code should speak through the reusable role
interface." `k4d9` (Clarification, Medium) reinforces it: generated internal
Nexus nouns should not be promoted to the crate root; keep internal vocabulary
separate from wire-facing APIs. But the live emitter still references concrete
names directly — `emit_nexus_runner_adapter` hard-codes `NexusWork`,
`NexusEngine`, `OriginRoute` as concrete identifiers (`lib.rs:3058-3090`), and
the 532 report flags the crate-root barrel (`spirit/src/lib.rs:47-86`) that
k4d9 warns against.

The competing options:

- **Option A — promote jo1x to a binding constraint now**, before the lojix
  port: the generated runtime code speaks through role traits
  (`RunnerEngines`, a `NexusRole` trait) so the SECOND component (lojix) reuses
  the runtime surface without copying spirit's concrete names. The 532 content
  report and operator `l6zw`/`bodd` both worry the first cloud port already
  copied spirit's all-in-one schema; jo1x is the guard against that repeating.
- **Option B — leave jo1x at Medium and let the lojix port surface the real
  trait boundary empirically.** jo1x is only Medium certainty; forcing the
  trait abstraction before a second real consumer exists risks abstracting the
  wrong axis. The port is the forcing function.

**Why this is a psyche question:** jo1x and k4d9 are both Medium — deliberately
not-yet-binding. The psyche should say whether the imminent lojix port is the
moment to *raise* jo1x to a binding generator constraint (A — abstract first,
the port proves it), or whether to *port concretely first and extract the trait
from two real consumers* (B — the workspace's own mockup-first instinct,
records 502-504). This is a genuine "when does an abstraction earn its name"
fork, and it interacts with FORK A (if B there, triad-runtime owns the glue
and jo1x is half-answered already). **Designer lean: genuinely unsure** — the
"name the noun" pattern says A, but Medium certainty + the one-real-consumer
reality says B; the psyche's call on sequencing matters here.

## Settled-but-undone (track as tasks, NOT forks — listed so they aren't lost)

- Land the enum-payload-variant rule as a constraint in
  `schema-rust-next/ARCHITECTURE.md` (operator 319:137 proposed; substance
  settled by record 1269).
- Finish migrating the 47-method RustWriter to noun-`ToTokens` + a `PlaneType`
  projection type (de8i execution; the FORK is only the 7 runtime-glue
  methods in FORK A — the other ~40 are pure execution).
- Resolve the crate-root barrel (`spirit/src/lib.rs:47-86`) per k4d9 — move
  generated Nexus nouns into the plane module. (Becomes a fork only if it
  collides with FORK C's trait decision.)
- Close the schema-upgrade loop (`UpgradeFrom`/`AcceptPrevious` emit but
  nothing implements them; `migration.rs` exists but the loop isn't closed) —
  execution, governed by existing intent.

## The one-line frame

The engine's *directions* are unusually well-settled — de8i, 4np2, vez8
(Maximum), xai7, opvx, rpr5 each close a question the 532 audit had left open.
The three real forks left are all **boundary-and-timing** questions the records
genuinely don't reach: (A) who owns the runtime-glue code — the generated
component crate or triad-runtime; (B) whether the hand-rolled MacroRegistry is
legacy-to-retire or a legitimate layer under the structural-macro-node derive;
(C) whether the lojix port is the moment to make jo1x binding. None is a
"write the code" task; each changes a public boundary or a sequencing
commitment, which is why they need the psyche.
