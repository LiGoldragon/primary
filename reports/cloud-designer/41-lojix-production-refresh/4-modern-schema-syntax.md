# Modern schema syntax vs lojix's `.schema` files

cloud-designer recon, 2026-06-12. Grounds every claim in a file read or
command run. Scope: the `.schema` source language, the codegen crate that
consumes it, and whether lojix's two schema files need the rewrite the psyche
described.

## Headline

The psyche's framing ("schema syntax has changed; lojix `.schema` probably
need a full rewrite") is **half right**. The syntax DID change materially
between 2026-06-09 and 2026-06-11, but lojix's two `.schema` files
(`schema/nexus.schema`, `schema/sema.schema`) were already ported to the
modern compact surface — they need **at most light touch-ups, not a full
rewrite**. The real, concrete work the psyche is sensing is a **dependency
refresh**: lojix's `Cargo.lock` pins all five upstream codegen/contract crates
behind their current `main@origin` heads, and a bump forces an artifact
regeneration (and a likely red build via `triad-runtime`, tracked in report
38/7).

## The codegen crate and its layering

Two crates, both git build-deps; lojix consumes only the second:

- `schema-next` (`/git/github.com/LiGoldragon/schema-next`) — the schema
  LANGUAGE: NOTA-block reader, position-aware macros, lowering to the semantic
  `Schema` value. Source of truth for the grammar is
  `schema-next/README.md` and `schema-next/ARCHITECTURE.md`. Current head
  `2397d5b2`, last edit 2026-06-11.
- `schema-rust-next` (`/git/github.com/LiGoldragon/schema-rust-next`) — the
  Rust SOURCE EMITTER built on `schema-next`
  (`schema-rust-next/Cargo.toml:8,19`: "Rust source emitter for schema-next
  typed schema data"). Current head `cedb2e06`, last edit 2026-06-11.

lojix depends on `schema-rust-next` as a `[build-dependencies]` entry
(`lojix/Cargo.toml:36`) and drives it in `lojix/build.rs:3` via
`schema_rust_next::build::{DependencySchema, GenerationDriver, GenerationPlan}`.
The older crate name `schema-rust-next` IS the current successor — there is no
newer codegen crate; `schema-rust-next` rides `schema-next` HEAD.

## The modern syntax rules (source: schema-next README + ARCHITECTURE + fixtures)

A `.schema` file is legal NOTA first, then schema-read. Root shape is
**positional** (schema-next/ARCHITECTURE.md:381-389, root.schema:4):

1. optional leading imports map `{ Local crate:module:Type ... }`
2. input root enum body, e.g. `[Record Reindex]`
3. output root enum body, e.g. `[Recorded (Rejected Rejection)]`
4. namespace map `{ TypeName Value ... }`
5. optional trailing relation-declaration vector (NEW, 2026-06-11) — see below

Rules that the modern surface enforces:

- **Braces are key/value maps ONLY, never enum sugar** (ARCHITECTURE.md:396).
  Namespace entries are `Name Value` pairs written directly inside `{ }` — no
  `(Name Body)` wrappers, no doubled-name pairs. Doubled-name and `(Name Body)`
  forms are rejected (ARCHITECTURE.md:413-416).
- **Bare `Name Type` is ALWAYS a distinct newtype — aliases were dropped**
  (schema-next commit `qz6j`, 2026-06-09: "drop aliases entirely; bare Name
  Type is always a distinct newtype"). So `ClusterName String` and
  `ContainerName String` generate `struct ClusterName(String)` newtypes, not
  type aliases. Verified in lojix's own generated output:
  `lojix/src/schema/sema.rs:144` `pub struct ContainerName(String);`.
- **Struct body** = `Name { field Type ... }`. `TypeName *` derives the field
  name from an already-declared type (`GenerationIdentifier *` → field
  `generationIdentifier: GenerationIdentifier`); explicit `field TypeRef` when
  the field name differs (ARCHITECTURE.md:399-401). A one-field body lowers to a
  **newtype**, not a struct (ARCHITECTURE.md:195-198, 252-254).
- **Enum body** = a square-bracket vector of variant-signature objects
  (ARCHITECTURE.md:402-406, nota-design.md:124-131):
  - bare PascalCase `Foo` → unit variant (or resolves to a same-named
    namespace declaration at root positions),
  - `(Foo)` → self-tagged data-carrying variant (added `52ro`, 2026-06-09:
    "(X) self-tag form, equivalent to (X X)"),
  - `(Foo Foo)` → the explicit repeated-variant form, lowers identically to
    `(Foo)` (fixture `lowering/explicit-repeated-variant.schema`),
  - `(Foo PayloadType)` → only when the payload type name differs.
- **Type references at value positions** (ARCHITECTURE.md:432-447, root.schema:19):
  reserved scalar leaves are `String Integer Boolean Path Bytes`
  (`Bytes` added `yp29`, 2026-06-09; fixed-size `(Bytes N)` added 2026-06-10);
  composites are `(Vec T)`, `(Map (K V))`, `(Optional T)`; a bare declared
  PascalCase name is `Plain(Name)`. These nest recursively.
- **Single-colon qualified names** `crate:module:Type` for imports/cross-module
  refs (README:55-58) — mirrors Rust module tree without `::`.
- **Strings are broad bare atoms** in schema text (schema-next commit
  2026-06-10 "adopt broad bare NOTA strings"); schema names emit through a
  `Name` codec (bare unless non-symbol). No quotation marks.
- **NEW, not yet used by lojix (2026-06-11):** recursive *scoped enum* type
  references and *relation declarations* — a recursive enum
  `Domain [(Information [Database]) (Technology [...])]` plus a trailing 5th
  root field of `(Equivalence [...])` relation entries
  (fixture `source-codec/relations.schema`). This is a Spirit/domain-tree
  feature; lojix has no use for it.

## Before / after — does lojix differ?

lojix already uses the modern surface. The forms it uses, all confirmed
current:

- `{ ... }` leading imports map with `Local crate:module:Type` pairs
  (`nexus.schema:26-45`, `sema.schema:16-44`) — current.
- bracket root enums `[NexusWork]` / `[NexusAction]`,
  `[SemaReadInput SemaWriteInput]` — current.
- namespace `Name Value` pairs, derived `*` fields, `(Vec X)`, `(Optional X)`,
  bare-newtype scalars (`ContainerName String`, `CommitSequence Integer`) —
  all current.
- enum-variant payload pairs `(SignalArrived SignalInput)`,
  `(OrdinaryInput OrdinaryInput)` — current (the latter is the explicit
  repeated form; both still lower).

So there is **no stale grammar** in lojix's `.schema`. A representative
slice — these lines need NO change under the modern syntax:

```schema
;; lojix/schema/sema.schema:56-58 — already modern
ContainerTransition { ClusterName * NodeName * container ContainerName state ContainerState }
ContainerName String
ContainerState [Starting Started Stopping Stopped Failed]
```

The only candidate cosmetic touch-ups (NOT required for correctness):

- `(OrdinaryInput OrdinaryInput)` / `(MetaInput MetaInput)`
  (`nexus.schema:49-50`) could collapse to the `52ro` self-tag form
  `(OrdinaryInput)` / `(MetaInput)` for terseness. Equivalent lowering; purely
  stylistic.
- Genuinely-different-payload pairs like `(SignalArrived SignalInput)` MUST
  stay as the two-name form (variant name ≠ payload type name).

There is **one real artifact-level change** that DOES land on a bump, not a
syntax rewrite: `schema-rust-next` HEAD "stop emitting nota bridge methods"
(2026-06-11 21:46, newer than the checked-in artifacts dated 2026-06-11 12:42).
lojix's checked-in `src/schema/{nexus,sema}.rs` still carry the bridge wrappers
(`rg -c 'pub fn to_nota|pub fn from_nota_block'` → `nexus.rs:64`, `sema.rs:60`).
On regeneration against current `schema-rust-next`, those wrappers disappear.
`build.rs:36` runs `.write_or_check("LOJIX_UPDATE_SCHEMA_ARTIFACTS")`, so a bump
without regeneration **fails the freshness check** — the artifacts must be
regenerated and re-checked-in.

## The dependency refresh (the concrete "dependency update")

`lojix/Cargo.lock` pins every upstream behind current `main@origin`
(`rg name=... Cargo.lock` vs `jj log -r main@origin` per repo, 2026-06-12):

| crate | pinned in Cargo.lock | current main@origin |
|---|---|---|
| schema-rust-next | `b252e81e` | `cedb2e06` |
| schema-next | `ccdf5487` | `2397d5b2` |
| nota-next | `af6a2080` | `065fa2ad` |
| signal-lojix | `8f6c498a` | `b31cd980` |
| meta-signal-lojix | `2e69371b` | `317b7fab` |

All five are behind. The `schema-rust-next` gap carries the bridge-method
removal (forces artifact regen, above). The dependency map is in `build.rs`:
lojix imports the ordinary and meta Signal roots from `signal-lojix` and
`meta-signal-lojix` (`build.rs:47-62`, `into_generation_plan`), so those two
contract crates must move in lockstep — a bump there can shift imported wire
types. Report 38/7 (2026-06-10) is the direct predecessor; it is now partly
superseded (it still references the removed `triad-port/` subdir, dropped by
the 2026-06-11 flatten commit) but its core warnings hold: a `triad-runtime`
bump red-builds on the `Actor*`→`Async*` listener rename, and a
`schema-rust-next` bump rewrites the checked-in artifacts.

## Exact rules to follow when touching lojix's `.schema`

1. Do NOT rewrite — the files are already modern. Only refresh deps + regenerate
   artifacts.
2. Refresh `Cargo.lock` to current heads of all five crates above; the contract
   pair (`signal-lojix` / `meta-signal-lojix`) moves with the codegen pair.
3. After the bump, regenerate artifacts:
   `LOJIX_UPDATE_SCHEMA_ARTIFACTS=1 cargo build` so `nexus.rs`/`sema.rs` shed
   the nota bridge methods and re-pass `write_or_check`.
4. If collapsing self-pairs, only collapse where variant name == payload type
   name (`(OrdinaryInput OrdinaryInput)` → `(OrdinaryInput)`); never touch
   different-payload pairs (`(SignalArrived SignalInput)`).
5. Keep braces key/value-only, scalars bare (`Name Type`), `*` for derived
   fields, `(Vec/Optional/Map ...)` for composites. No `(Name Body)` namespace
   wrappers, no doubled-name pairs.
6. Watch the `triad-runtime` bump separately (report 38/7): the `Actor*`→
   `Async*` listener rename breaks `daemon.rs` at compile time — that is an
   operator code change, not a schema change.

## Sources

- `/git/github.com/LiGoldragon/schema-next/README.md`,
  `schema-next/ARCHITECTURE.md` (grammar source of truth)
- `/git/github.com/LiGoldragon/schema-next/schemas/{root,core}.schema`
- fixtures: `schema-next/tests/fixtures/lowering/{self-tagged,explicit-repeated}-variant.schema`,
  `.../source-codec/{relations,reference-fields,namespace-enum-bare-variants,root-inline-payloads}.schema`,
  `.../design/same-name-payload-variant.schema`
- `/git/github.com/LiGoldragon/lojix/schema/{nexus,sema}.schema`,
  `lojix/build.rs`, `lojix/Cargo.toml`, `lojix/Cargo.lock`,
  `lojix/src/schema/{nexus,sema}.rs`
- reference modern schemas:
  `/git/github.com/LiGoldragon/signal-lojix/schema/lib.schema`,
  `/git/github.com/LiGoldragon/spirit/schema/sema.schema`
- predecessor: `reports/cloud-designer/38-lojix-production-readiness/7-engine-dependency-freshness.md`
- commit history via `jj log` in schema-next / schema-rust-next (syntax-change
  timeline 2026-06-09..06-11)
