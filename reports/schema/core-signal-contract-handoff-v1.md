# CoreSignalContract — self-contained handoff to Codex

**Status:** cross-agent design pickup. This is a bounded implementation brief for a
fresh Codex (gpt-5.6) session, authored by Claude (Opus 4.8, generalist) in the
`LanguageFamilyPrototype` session, lane `SignalHandoff`, 2026-07-16. It changes no
source. Every legacy and new-stack fact below carries a `repo/path:line` citation
verified this session; every design choice is marked as a lean under the psyche's
standing grant, with reasons and revisability stated. The psyche does not read
reports — this file is the agent pickup surface. Chat carries the placement answer,
the path, the bead id, and evidence gaps.

Codex chose this slice after the psyche's verbatim order "give codex a significant
slice." This handoff answers Codex's placement question and supplies the seven
concrete items Codex requested, so a fresh session needs no other reading.

## 0. Grounding — the psyche rulings this slice stands on (verbatim)

These are the settled decisions and standing grants that authorize and bound the
slice. They are carried verbatim so the handoff is self-contained.

- **Document-kind direction accepted, review-later.** Four Core kinds — TypeSchema /
  SignalContract / NexusRuntime / SemaStorage — share generic declaration records;
  **Signal owns Stream plus opens/belongs; Sema owns Family.** Psyche verbatim:
  *"yes - and we can review the design later; easy to work with once it's all up."*
  This partially answers the six psyche-questions closing
  `document-kinds-signal-contract-design-v1.md` §"Psyche-only questions" (Q1, Q3, Q4
  are now ruled in the affirmative; Q2 header spelling, Q5 relation spelling, Q6
  meta-contract taxonomy remain open and are flagged where they touch this slice).
- **Naming ruled: Core = canonical stringless data layer; sema = durable
  storage/runtime component; zero renames.** Psyche verbatim: *"a - sema will be
  more complete and correct than core; we are laying the foundation for it."* So the
  new crate family stays `core-*`; the storage kind is the `sema` concern.
- **Visibility ruled Schema-authoritative** (the visibility a declaration carries in
  Schema Core is the source of truth; see bead primary-56d1.29, closed as a lean).
- **Standing lean grant.** Psyche verbatim: *"Im also ready for multiple slices going
  with the agent leans; to get a working prototype; leans can be revised
  afterwards."* This authorizes the placement and record-shape leans below without a
  fresh psyche round; they are revisable.
- **Central-authority premise.** Psyche verbatim: *"then we cannot have a
  coordination-free universe; I never believed in such idealist fantasies."* This
  governs the id-allocation universe question (§3): a single logical allocation
  authority, not per-daemon minting. That ruling itself is still pending (bead
  primary-56d1.11); this slice stays fixture-universe until it lands.

**Caution on a superseded source.** `document-core-adapter-design-v2.md` over-settled
v1's open questions and invented `NexusRuntime` as a fourth kind on its own slate
framing. Treat `document-kinds-signal-contract-design-v1.md` **plus the psyche
acceptance above** as ground. v2's *record shapes* (`CoreSignalContractV1`,
`CoreSignalStreamV1`, `CoreSignalRelationV1`, the legacy-disposition table, the
consumer-adapter table) are reused here as concrete proposals because they are
faithful renderings of the legacy source; v2's *slate/authority framing* is not
ground. Codex intends to correct v2 — that correction is Codex's `reports/schema/`
lane and is out of scope for this slice.

## 1. Placement — the answer to Codex's question

**Question (Codex, verbatim):** *"Does CoreSignalContract belong in core-schema or in
its own micro-component?"*

**Answer: its own micro-component.** Working name **`core-signal-contract`** (an
agent lean under the standing grant; full-English, mirroring the `core-schema` /
`core-nomos` / `core-logos` family). This is not the fallback bounded-placement
design Codex offered — the analysis lands firmly, so it is a concrete
recommendation, revisable per the grant.

### 1.1 Why its own component (analysis under the micro-components discipline)

The `micro-components` discipline's **split test** — start a new component on *a
distinct noun, a separate bounded vocabulary, a separate state owner, a new
parser/codec, or a test surface that should run independently* — is met on every
clause:

| Split-test clause | Signal contract | Verdict |
| --- | --- | --- |
| Distinct noun | Stream + opens/belongs is **contract topology** (an admission/ack/event-sum/closure relation), not a generic type declaration | new component |
| Separate bounded vocabulary | `Opens`/`Belongs` closed relation kinds, `Input`/`Output` closed root positions — a vocabulary generic `CoreSchema` deliberately does not carry | new component |
| Separate state owner | its own `SignalContractNameTable` and its own content-identity domain (§3) | new component |
| New codec/validation | relation validation (`Opens`→Input, `Belongs`→Output, event-payload compatibility) that generic schema has no place for | new component |
| Independent test surface | byte-exact signal goldens, Help stream-row fixtures, relation negative witnesses (§5) run on their own | new component |

The accepted document-kind direction states the same shape from the top: **each kind
its own Core record family and own NameTable; kinds depend on core-schema's generic
declaration records without editing them.** Putting streams/relations back into
`core-schema`'s `CoreSchema` would reverse the *deliberately retired* generic
Stream/Family constructs (`document-kinds-signal-contract-design-v1.md` §"Current
six-root general schema"; `schema-language/ARCHITECTURE.md` calls them retired) and
would re-mix contract topology into the stringless type substrate.

The design corpus already reached this conclusion in prose:
`document-kinds-signal-contract-design-v1.md:365` — *"CoreSignalContract and its
NameTable/view belong in a focused signal-contract model or contract-schema
component, not as fields restored in CoreSchema/TrueSchema … source dependencies
should remain one-way: the generic type-schema substrate must not import signal
runtime code."* `document-core-adapter-design-v2.md:18` — *"a generic TypeSchema may
not regain Stream, Family, relation, runtime, or storage authority."*

The **design-quality gate** (special case dissolves into the normal case) confirms
it: a Signal contract *is* a normal document kind that owns extra typed topology, and
generic schema stays the pure declaration substrate. The alternative — a stream/
relation side-path bolted onto `CoreSchema` that every future editor must remember —
is exactly the special case the discipline rejects.

### 1.2 Precedent: this is the established family shape

The new stack is already a set of one-capability `core-*` crates, each an independent
flake-green repo depending inward by pinned git rev: `core-schema` (declarations),
`core-logos` (Rust-as-data), `core-nomos` (macro Core), `textual-rust` (syn/
prettyplease form). `golden-bridge/ARCHITECTURE.md:9-16` states the same
one-way-dependency rationale for keeping the legacy seam out of the clean Core
crates. `core-signal-contract` is the next member: it consumes `core-schema`'s
declaration substrate and `structural-codec`'s universe/codec kernel, and nothing in
those depends back on it.

### 1.3 Owning repository and scaffold expectations

- **Repository:** `core-signal-contract` (new public repo).
- **Owner:** LiGoldragon. Public creation is standing-authorized for Codex
  (`repository-publication` discipline). Create from an empty `main`.
- **Mainline branch:** `main`. Jujutsu-colocated like the sibling repos; push
  `main` to `github.com/LiGoldragon/core-signal-contract`.
- **Scaffold (match `core-schema` / `golden-bridge` exactly):**
  - single-crate repo (`[package]`, not a workspace), `publish = false`, package name
    `core-signal-contract`, lib name `core_signal_contract`.
  - `flake.nix` with the five crane checks the family uses, verbatim names from
    `golden-bridge/flake.nix:33-45`: **`build`, `test`, `doc` (`RUSTDOCFLAGS =
    "-D warnings"`), `fmt`, `clippy` (`--all-targets -- -D warnings`)**. `nix flake
    check` is the acceptance witness (`testing` discipline: Nix owns durable test
    evidence).
  - crate layout per `rust-crate-layout`: `src/` modules (`declaration`-analogue for
    the stream/relation records, `identity`, `textual`, `universe`, `error`), tests
    in `tests/`, vendored fixtures under `tests/fixtures/` with a `PROVENANCE.md`
    (§5).
  - `ARCHITECTURE.md` written per `architecture-editor` / `repo-intent`: one
    capability — *the stringless Core of a signal contract (Stream topology + opens/
    belongs relations) and its Textual form* — 100% backed by the psyche rulings in
    §0.
  - Cargo dependencies by **pinned git rev** (`micro-components` dependency
    discipline; never `path = "../.."`): `content-identity`, `name-table`,
    `raw-discovery`, `structural-codec`, and `core-schema` at the tips in §6.

## 2. Exact Stream and opens/belongs Core records

All records are stringless rkyv archives. Every name-bearing reference is a
`name_table::Identifier` resolved through the contract's own `NameTable`; every type
reference is a `core_schema::CoreReference` (kind/projection dispatch, never a head
string — `core-schema/src/reference.rs`). The declaration substrate is reused from
`core-schema` unchanged (`CoreSchema`, `CoreDeclaration`, `CoreType`, `CoreReference`,
`Visibility`, `core-schema/src/declaration.rs:30-97`).

### 2.1 Legacy ground truth (field-by-field, cited)

The new records preserve the legacy tuple exactly. Legacy source
(`repos/schema`, the four-root model still used by `signal-spirit/schema/signal.schema`):

- **`StreamDeclaration`** — `schema/src/schema.rs:2180-2186`:
  ```
  pub struct StreamDeclaration { name: Name, token: TypeReference,
      opened: TypeReference, event: TypeReference, close: TypeReference }
  ```
  Four type references in fixed order token/opened/event/close.
- **`StreamRelation`** — `schema/src/schema.rs:2156-2159`:
  ```
  pub enum StreamRelation { Opens(Name), Belongs(Name) }   // Name = the stream's name
  ```
  Carried as an *optional relation on an enum variant* in the legacy model; it is the
  variant→stream edge, not a field on the stream.
- **`SourceStreamBody`** (the source/help projection of a stream) —
  `schema/src/source.rs:1807-1813`: `{ token, opened, event, close }` — four
  `SourceReference`, **no name field** (the stream name is the declaration key, not a
  body field). Reconstructed by `signal-spirit/src/help.rs:486-493` from the four
  references in order token/opened/event/close. (`SourceDeclarationValue` carries the
  `Stream`/`Family` variants at `schema/src/source.rs:1652-1659`.)
- **Out of scope for this slice, cited for the boundary:** `FamilyDeclaration`
  (`schema/src/schema.rs:2285-2290`: `name, record: Name, table: TableName, key:
  FamilyKey`), `FamilyKey` (`schema.rs:2261-2266`: `Domain | Identified`),
  `TableName` (`schema.rs:2210`, a storage coordinate). **Family is the Sema kind, not
  Signal.** All `NexusRuntime` detail is unruled and out of scope entirely.

### 2.2 Live legacy contract values (from `signal-spirit/schema/signal.schema`)

The one real contract this slice must reproduce (`signal-spirit/schema/signal.schema`,
verified this session):

- **Input root** (line 44) carries one `opens` variant, exact four-object signature:
  `(SubscribeIntent SubscribeIntent opens IntentEventStream)`.
- **`IntentEvent` enum** (line 165) carries the four `belongs` variants, each an exact
  four-object signature:
  `(IntentRecorded IntentRecorded belongs IntentEventStream)`,
  `(IntentClarified IntentClarified belongs IntentEventStream)`,
  `(IntentSuperseded IntentSuperseded belongs IntentEventStream)`,
  `(IntentRetired IntentRetired belongs IntentEventStream)`.
- **Stream declaration** (line 166), the canonical tuple:
  `IntentEventStream (Stream { token.SubscriptionToken opened.SubscriptionStarted event.IntentEvent close.SubscriptionToken })`.
- Supporting decls: `SubscriptionToken Integer` (l.120), `SubscribeIntent Query`
  (l.77), `SubscriptionStarted IntentSubscription` (l.97),
  `IntentSubscription { SubscriptionToken }` (l.146), `IntentEvent [...]` (l.165).

### 2.3 The proposed stringless Core records (lean; positional NOTA shape)

Named for explanation; each name is an `Identifier`. Documented in the pseudo-NOTA
schema convention (`nota-schema-docs`): `<Type>` placeholders, `[X]` = vector, `?` =
optional, `A | B` = closed variant set.

```
;; ROOT — the loaded whole of one signal contract.
CoreSignalContract {
  declarations:  CoreSchema,              ;; reused from core-schema, unchanged (the stringless
                                          ;; declaration substrate: Vec<CoreDeclaration>)
  input:         CoreRootReference,       ;; the Input root enum's identifier (see note below)
  output:        CoreRootReference,       ;; the Output root enum's identifier
  streams:      [CoreSignalStream],       ;; mandatory block, possibly empty
  relations:    [CoreSignalRelation],     ;; mandatory block, possibly empty
}

CoreSignalStream {
  identifier:  Identifier,                ;; the stream name  (legacy StreamDeclaration.name)
  token:       CoreReference,             ;; legacy .token
  opened:      CoreReference,             ;; legacy .opened
  event:       CoreReference,             ;; legacy .event
  close:       CoreReference,             ;; legacy .close
}

CoreSignalRelation {
  endpoint:  CoreSignalEndpoint,
  relation:  CoreSignalRelationKind,      ;; Opens | Belongs
  stream:    Identifier,                  ;; the target stream's identifier
}

CoreSignalEndpoint {
  root:     CoreRootPosition,             ;; Input | Output   (closed)
  variant:  Identifier,                   ;; the variant that opens/belongs
}

CoreSignalRelationKind ::= Opens | Belongs
CoreRootPosition       ::= Input | Output
```

**Positional NOTA shape** (how a value serializes; `nota-design` — records are
positional, bare atoms for canonical strings). The live `IntentEventStream` value:

```
CoreSignalStream.( IntentEventStream SubscriptionToken SubscriptionStarted IntentEvent SubscriptionToken )
```

and the `SubscribeIntent opens` relation:

```
CoreSignalRelation.( CoreSignalEndpoint.( Input SubscribeIntent ) Opens IntentEventStream )
```

(In the stringless substrate every atom shown is an `Identifier(u32)`; the kebab/
Pascal text is the NameTable projection at the boundary.)

### 2.4 Two implementation decisions this slice must settle (flagged, not guessed)

1. **The root representation.** The *current* `core-schema` `CoreSchema` is
   `Vec<CoreDeclaration>` only — it has **no** Input/Output root concept
   (`core-schema/src/declaration.rs:30-33`). The legacy model expresses roots as two
   named enum declarations. So `CoreSignalContract` must own its `input`/`output`
   root references itself (shown above as `CoreRootReference` = an `Identifier` into
   `declarations`), rather than expecting `core-schema` to grow a roots field. This is
   the cleaner boundary and keeps `core-schema` untouched. **Do not edit `core-schema`
   to add roots** — that would be a shared-crate edit requiring a claim and manager
   coordination (§6, §7).
2. **`Opens`/`Belongs` endpoint spelling** is psyche-open (v1 Q5: explicit
   `Input.SubscribeIntent.Opens.IntentEventStream` vs root-position implied by the
   variant's type). The Core record above keeps `root` explicit (matches the legacy
   variant-carried relation and v2's `CoreSignalEndpointV1`). If the psyche later
   rules root-position implicit, `CoreSignalEndpoint.root` is dropped and derived —
   a NameTable-excluded, Core-layout-versioned change. Proceed with explicit `root`
   as the lean; note the openness in `ARCHITECTURE.md`.

## 3. NameTable and identity laws

### 3.1 Own NameTable as co-versioned sibling

The contract has **one** `SignalContractNameTable` for the loaded whole (roots,
variants, types, streams, imports, relation endpoints — one allocation universe, no
ambiguous collisions). It is the `name_table::NameTable` used exactly as `core-schema`
uses it (`core-schema/src/universe.rs:83`, `textual.rs`). It is a **sidecar**: never
embedded in a Core value, never in a Core hash. Its own identity is co-versioned and
separate (the `name-table` crate owns `NameTable::identity()` per the up-close design
§3).

### 3.2 The identity keystone, applied with a new domain string

Core identity is BLAKE3 over the canonical stringless rkyv bytes under a
**domain-separated, layout-versioned** context, NameTable excluded. The keystone
lives in `content-identity` (`ContentHash`, `HashDomain`, `DomainSeparation`,
`LayoutVersion`). `core-schema` applies it exactly like this
(`core-schema/src/declaration.rs:14-48`):

```
pub struct CoreSchemaDomain;
impl HashDomain for CoreSchemaDomain {
    fn separation() -> DomainSeparation {
        DomainSeparation::Contextual {
            context: "core-schema 2026 stringless core schema layer",
            layout:  LayoutVersion::new(1),
        }
    }
}
// CoreSchema::content_identity() -> ContentHash::of_core(self)
```

**Lean for the signal kind — a NEW domain-separation string, distinct from
core-schema's:**

```
pub struct CoreSignalContractDomain;
impl HashDomain for CoreSignalContractDomain {
    fn separation() -> DomainSeparation {
        DomainSeparation::Contextual {
            context: "core-signal-contract 2026 stringless signal contract layer",
            layout:  LayoutVersion::new(1),
        }
    }
}
// CoreSignalContract::content_identity() -> ContentHash::of_core(self)
```

Distinct domain ⇒ a signal-contract Core value and a type-schema Core value with
coincidentally identical bytes never collide in identity. `layout: LayoutVersion(1)`
is the Core-layout tag; bump it only when the stringless record layout changes (not on
a rename, not on a text-format change).

### 3.3 The conformance laws that must hold

From the accepted kernel (`up-close-design-v1.md` §4.6 "the laws", accepted by the
psyche on recommendation trust; and the compatibility witnesses in
`document-kinds-signal-contract-design-v1.md` §"Required compatibility witnesses"):

- **Round-trip both directions.** `decode ∘ encode = core` (Core preserved);
  `encode ∘ decode = canonical(raw)` (text canonicalized). `CoreSignalContract` +
  its NameTable survive an rkyv round trip.
- **Interning atomicity.** A failed decode alternative leaves the NameTable with **no**
  allocation effects (transactional interning — `name-table` provides it).
- **Rename hash-stability.** Editing only a NameTable spelling does not move any Core
  identity (NameTable excluded from the pre-image, by construction).
- **Structural-edit hash movement.** A change to the stringless record (add/remove a
  stream, change a relation endpoint, reorder variants) *does* move Core identity —
  the dual of the previous law.
- **Cross-revision Core-identity preservation.** An old-table decode re-encoded
  through the current table preserves Core identity where semantic equivalence holds
  (the identity-preserving law).
- **Interpreter ≡ generated codec.** The trusted `structural-codec` runtime evaluator
  and the generated codec agree on Core value, NameTable delta, canonical output, and
  typed error, over every fixture — where structural tables are used. `core-schema`'s
  `CoreUniverse::validate_table` already proves each authored codec's positional
  signature equals the Core field signature; the signal universe must pass the same
  gate (`core-schema/src/universe.rs`; `structural-codec` `PositionalSignature`).
- **Relation validation** (signal-specific, from v2 §"Signal contract"): every
  `StreamId`/endpoint resolves; `Opens` targets an Input variant; `Belongs` targets an
  Output variant; each endpoint appears at most once for its role; a belonging event's
  payload is compatible with the stream's `event` type.

### 3.4 Universe handling stays fixture-universe (pending lineage ruling)

The id-allocation universe stays an explicit **fixture universe** for this slice, as
`core-schema` does today (its `CORE_UNIVERSE`, `ScopedCoreTypeId`). The
schema-unit/split/merge allocation lineage — *which persisted universe carries
NameTables across split and merge* — is **blocked on the psyche** (bead
**primary-56d1.11**, blocked-on-psyche; research lane dispatched 2026-07-16; the
psyche's follow-up "so where is the authority?" is awaiting a ruling toward a single
logical allocation authority seated in the sema storage/runtime component). **Do not
infer that policy in this slice.** Scope every identifier by the fixture-universe
identity and Core layout, exactly as the sibling crates do.

## 4. Legacy field-by-field mapping (preserved / translated / absent)

Following `golden-bridge`'s disposition pattern (typed reasons partitioning migrated
vs excluded — `golden-bridge/src/error.rs:4-49`, `tests/spirit_bridge.rs:91-116`).
Legacy sources: `repos/schema` (constructs) and `signal-spirit/schema/signal.schema`
(the live contract).

| Legacy construct | Source | Disposition | New home |
| --- | --- | --- | --- |
| Input root enum + its variants | `signal.schema:44` | **preserved** | `declarations` (a `CoreDeclaration`) + `CoreSignalContract.input` |
| Output root enum + its variants | `signal.schema:45` | **preserved** | `declarations` + `CoreSignalContract.output` |
| namespace type declarations (`Query`, `IntentSubscription`, `SubscriptionToken`, `IntentEvent`, …) | `signal.schema:77,120,146,165` | **preserved** | `CoreSchema.declarations` (reused core-schema records) |
| `StreamDeclaration {name,token,opened,event,close}` | `schema.rs:2180` | **translated** (stringless) | `CoreSignalStream` (identifier + 4 `CoreReference`) |
| stream/variant display names | `signal.schema` atoms | **translated** | `SignalContractNameTable` entries (never in Core) |
| `StreamRelation::Opens(Name)` on Input variant | `schema.rs:2157`; `signal.schema:44` | **translated** | `CoreSignalRelation{endpoint:{Input,SubscribeIntent}, Opens, IntentEventStream}` |
| `StreamRelation::Belongs(Name)` on 4 event variants | `schema.rs:2158`; `signal.schema:165` | **translated** | 4× `CoreSignalRelation{endpoint:{Output,…}, Belongs, IntentEventStream}` |
| `EnumVariant`-carried relation *as a field on the variant* | legacy mixed model | **absent by design** | relations are a top-level `[CoreSignalRelation]` block; they never extend generic `CoreVariant` |
| `FamilyDeclaration`, `FamilyKey`, `TableName` | `schema.rs:2210,2261,2285` | **absent (out of scope)** | the Sema kind (`SemaStorage`), a separate slice/repo |
| generic `RelationDeclaration` not meaning signal topology | legacy | **absent (retired)** | intentionally retired; no generic compatibility projection |
| monolithic `TrueSchema` archive/API | `signal-spirit/src/help.rs:156-159` (`Vec<TrueSchema>`) | **absent as authority** | replaced by a typed `SignalContractSnapshot` for Help (§5); Core authority is `CoreSignalContract` + NameTable |
| legacy NOTA source spelling / four-object `(… opens …)` | `signal.schema` | **translated (registered decoder input)** | historical decoder → current Core; never body-inferred |

No adapter may synthesize a missing stream, relation, or import from the old
projection (v2 §"Legacy TrueSchema disposition"). Source visibility is
Schema-authoritative (§0) and must be represented, not dropped.

## 5. Acceptance fixtures

The gate: **the generated `signal.rs` must reproduce byte-identically before the new
form becomes canonical.** Any byte difference is reviewed as a real generator change,
not dismissed as formatting (v1 §"schema-rust and generated signal artifacts").

### 5.1 Byte-exact goldens to vendor

Vendor into `tests/fixtures/` with a `PROVENANCE.md` following
`golden-bridge/tests/fixtures/PROVENANCE.md` verbatim pattern — *per file: source
repo path `@ <full-40-char-commit>` plus a pointer to the legacy assertion that pins
the golden bytes*:

- **`signal.schema`** — the legacy contract source. From
  `signal-spirit/schema/signal.schema` at signal-spirit's pinned commit. This is the
  decode input.
- **`signal_generated.rs`** — the Rust the legacy generator emits, the byte-exact
  encode oracle. From `signal-spirit/src/schema/signal.rs` (6150 lines, 166233 bytes,
  header `// @generated by schema-rust` at line 1). The acceptance is per-item
  byte-exact comparison, as `textual-rust`/`golden-bridge` established.

The load-bearing generated surfaces the new pipeline must reproduce (cited in
`signal-spirit/src/schema/signal.rs`):

- **StreamingFrame aliases** (lines 6093-6102):
  `type Frame = signal_frame::StreamingFrame<Input, Output, IntentEvent>;` and the
  `FrameBody`/`Request`/`ReplyEnvelope`/`RequestBuilder` aliases over the same
  `<Input, Output, IntentEvent>` triple.
- **Subscription open/event/close routing:** `IntentEvent::into_subscription_frame`
  (6135-6150); route constants `OUTPUT_SUBSCRIPTION_STARTED = 0x0112…` (5631) and
  `OUTPUT_EVENT = 0x0117…` (5636); the forward route map (5957, 5962) and reverse
  decode (5998-6005); `IntentEvent` enum (1106-1111). Close reuses `SubscriptionToken`
  (frame carries `token: signal_frame::SubscriptionTokenInner`, 6139) — matching the
  schema's `close.SubscriptionToken`; there is no distinct generated close type.

### 5.2 Help canonical stream row

The exact row the Help projection must still produce, verbatim:

```
(Stream { token.SubscriptionToken opened.SubscriptionStarted event.IntentEvent close.SubscriptionToken })
```

Produced legacy-side by `HelpBody::from_stream` (`signal-spirit/src/help.rs:486-493`)
assembling a `SourceStreamBody` from the four references in order token/opened/event/
close. Help currently stores `Vec<TrueSchema>` and looks up `TrueSchema::streams()`
(`help.rs:352-357`) / `families()` (`help.rs:359-364`); targets are derived from the
stored schemas (`entry_named`, `help.rs:227-246`), not a hard-coded list. **The new
form must feed an rkyv `SignalContractSnapshot { CoreSignalContract,
SignalContractNameTable, resolved imports }` and project the same canonical rows** —
replacing the stored `TrueSchema` (this is a public-API/rkyv-archive compatibility
event for `HelpModel`, not a text-only change; v1 §"schema-language" and
§"Risks and boundaries"). `SignalContractSnapshot` is a runtime rkyv struct
consumed daemon-side (`HelpModel`); it is never repository content — the
`core-signal-contract` repository holds only type definitions, codecs, laws, and the
vendored legacy fixture pair, exactly like its sibling `core-*` crates, while Core
values live in memory and in daemons.

### 5.3 Other acceptance witnesses

- **rkyv snapshot round-trips:** `CoreSignalContract` + `SignalContractNameTable`
  survive round trip; the Help `SignalContractSnapshot` round-trips.
- **meta-signal-spirit wire/import compatibility:** `meta-signal-spirit/schema/
  meta-signal.schema` is an **ordinary owner-only contract with NO stream
  declarations** (verified: 62 lines, no `(Stream…)`, no `opens`/`belongs`); it
  imports six `signal-spirit:signal` nouns — `DatabaseMarker`, `Entry`,
  `RecordIdentifier`, `RecordCount`, `RemovalCandidateCollection`,
  `RemovalCandidatesCollection` (lines 1-8). It migrates to the **same
  `SignalContract` kind with empty streams/relations** (accepted direction; v2 §"Source
  basis" — a meta-only kind is not created just because the topology is empty). Its
  import resolution against the signal-spirit contract is an acceptance witness. NB:
  whether an empty-topology contract is `SignalContract` or a distinct kind is v1 Q6,
  still psyche-open; the accepted direction is `SignalContract` with empty sections.
- **Negative witnesses** (relation validation must reject): missing stream; missing
  endpoint; `Opens` on an Output variant; `Belongs` on an Input variant; duplicate
  endpoint role; event payload incompatible with the stream `event` type; unknown
  header `(kind, format-version)` before body decode. None repairable by projection
  fallback.

## 6. Dependencies on the active bridge

### 6.1 What the slice consumes (pinned git rev — never the train)

All flake-green today; pin by exact rev (`micro-components` dependency discipline).
Tips verified this session:

| Crate | Git rev to pin | Role |
| --- | --- | --- |
| `content-identity` | `6cc0408cdb96f174cc8fdf6ca23420038de28450` | `ContentHash`/`HashDomain`/`DomainSeparation`/`LayoutVersion` (identity keystone) |
| `name-table` | `c3237f77c087e6feab49d6cf34971cebc14a11e6` | `Identifier`/`NameTable`/`Name`, transactional interning |
| `raw-discovery` | `a4e8c6df84e6a487ca6fe2f3641f9bafd0b0d8c8` | `Block`/`Recognizer` raw layer |
| `structural-codec` | `104f92454a5ba88b376fa706a9fe38c4a4b65ee0` | `ScopedCoreTypeId`/`PositionalSignature`/evaluator, universe/codec kernel |
| `core-schema` | `566544eda56a52fb1b5185d8c634dd9a9f2a47e0` | reused declaration substrate: `CoreSchema`/`CoreDeclaration`/`CoreType`/`CoreReference`/`Visibility`, the `CoreUniverse` bridge |

(These are the exact revs `golden-bridge` and `core-schema` pin today, so the slice
sits on a proven-green closure. `core-nomos` `88a1ecf55272`, `core-logos`
`17cbd7596df2`, `textual-rust` `b0ea9fb61495` are the downstream lowering crates;
this slice does not depend on them directly — they enter when the contract is lowered
to generated Rust, which is bridge-leg-2 territory, §6.3.)

**Never pin the release train.** The train is an immutable epic materialization; a
component depends on pushed commits, not on a train lock (`release-train-development`;
the train-gate defects are a separate lane, §7).

### 6.2 What the slice must NOT touch

- **`golden-bridge` internals and the legacy vertical crates are Claude's lane.**
  `golden-bridge` houses the legacy↔new seam (`golden-bridge/ARCHITECTURE.md:3-16`):
  legacy `schema-language` source → `LegacySchemaIngest` → `CoreSchema` + `NameTable`
  → `core-nomos` → `core-logos` → `textual-rust` → byte-compare. Do not edit it.
- **Do not edit `core-schema`** (or any shared new-stack crate) to make the signal
  slice fit — e.g. adding an Input/Output roots field (§2.4). Any shared-crate edit
  requires an Orchestrate claim on that path and manager coordination. The contract
  owns its own roots representation instead.
- **Do not touch the legacy repos** (`schema`, `signal-spirit`, `meta-signal-spirit`,
  `spirit`) as part of building the component. They are read-only ground truth here;
  their migration is a later, separately-gated step (v1 §"Migration and release-train
  gates").

### 6.3 The seam where Claude's bridge leg 2 will consume Codex's component

`golden-bridge` leg 1 (bead primary-56d1.30, done) migrates one legacy **type-schema**
fixture end-to-end, byte-exact against legacy generated Rust — for the generic
`schema-language`/`schema-rust` path. **Leg 2 is the signal analogue:** it will ingest
the legacy `signal.schema` and drive `CoreSignalContract` through
`core-nomos`→`core-logos`→`textual-rust`, byte-comparing against `signal_generated.rs`
and reproducing the StreamingFrame aliases, subscription routing, and Help rows of §5.

**The clean seam:** `core-signal-contract` exports the typed **`CoreSignalContract` +
`SignalContractNameTable` (+ its `CoreUniverse`/codec table)** as its public contract.
Leg 2 (Claude's lane, in `golden-bridge` or a sibling) consumes that typed surface by
pinned git rev — it does not reach into the component's internals, and the component
does not depend back on the bridge (the one-way rule,
`golden-bridge/ARCHITECTURE.md:9-16`). Codex builds and proves the component
standalone (its own flake-green goldens); Claude's leg 2 later consumes the pinned
artifact. Coordinate the seam interface (the exact public types leg 2 imports) with
Claude before finalizing the public API, but no shared checkout is shared.

## 7. Explicit non-overlap with Codex's Synchronizer lane

- This slice **never edits `synchronizer`** and **never rides the train**. It is a new
  standalone `core-*` component proven by its own `nix flake check`.
- The **train-gate work — defects 1–4 plus defect 10** (the integration flake
  narHash/`?rev=` fixes and the other gating defects in `train-flow-audit`) — remains
  **Codex's separate lane**. That lane operates on the train materialization and
  `synchronizer`; this slice does not participate in it and must not be blocked on it.
- **Doc-surface split:** `reports/schema/` is **Codex's** documentation surface (this
  handoff is written *into* it as the pickup point, but ongoing schema-design docs —
  including the v2 correction — are Codex's); `reports/logos/` is **Claude's**. Keep
  edits on the right side of that line.
- The two lanes touch only at the §6.3 seam (a pinned typed artifact), never at a
  shared checkout or a shared branch.

## 8. Coordination for the implementing session

The implementing Codex session registers its own Session/Lane before editing (the
`edit-coordination` doctrine; a fresh identity, not a generic name):

```sh
meta-orchestrate "(Register ((<CodexSessionName> <CodexLaneName> ([Generalist] Structural) [core signal contract component]) Fresh))"
```

Then, per resource:

- **New repo `core-signal-contract`** is created fresh (LiGoldragon; public); its own
  checkout is not a shared-primary path, so intra-repo files need no primary claim.
  Claim the repo path once created if working under the shared `repos/` layout:
  `orchestrate "(Claim (<CodexLaneName> [(Path /home/li/primary/repos/core-signal-contract)] [component authoring]))"`.
- **Never claim `.beads/`.** Track work through `bd`.
- **Do not edit shared new-stack crates.** If the seam genuinely requires a
  `core-schema` change, that is a separate claim on `core-schema` **plus manager
  coordination** — return it, do not fold it in silently.
- Closeout per `repository-closeout`: `nix flake check` green, `jj` commit + push
  `main` to the public remote, bead closed, commit trailer with model + thinking
  level (`gpt-5.6; <level>`).

### 8.1 Tracker

- **Epic:** `primary-56d1` (Next-generation NOTA).
- **This slice's work bead:** **`primary-ezut`** — filed this session, child of epic
  `primary-56d1` (title names CoreSignalContract, notes Codex-side ownership and this
  handoff path).
- **Pending psyche blocker referenced (not owned by this slice):**
  `primary-56d1.11` (schema-unit allocation lineage, blocked-on-psyche) — keeps the
  slice at fixture-universe (§3.4).
- **Related open beads for context, not this slice:** `primary-56d1.4`
  (signal-nomos/signal-logos contract crates), `primary-56d1.13`
  (sema.schema/Sema kind), `primary-56d1.30` (golden-bridge leg 1, done).

## 9. Evidence sufficiency

Every legacy and new-stack fact above is cited to `repo/path:line` verified this
session. Two items are marked open by ruling, not by missing evidence:

- **Root representation** (§2.4-1): resolved by the lean (contract owns its roots;
  `core-schema` untouched) — evidence sufficient, decision stated.
- **Endpoint spelling** (§2.4-2, v1 Q5) and **empty-topology contract taxonomy**
  (§5.3, v1 Q6): psyche-open questions, not evidence gaps. The lean proceeds on the
  accepted direction and flags the openness.

No fact in this handoff was guessed. Where the psyche's word is still pending (bead
primary-56d1.11 lineage; v1 Q5/Q6), the slice is bounded to stay clear of it.
