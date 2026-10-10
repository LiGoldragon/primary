# Logos pipeline — component architecture v0

Retired vocabulary (psyche ruling 2026-07-21): "mouth" -> textual interface; "organs" -> the two trees (nametree, structuretree); "spine" -> core invariant / core pathway; "door" -> entry point; "currency" -> value type. Historical text below is unreworded; read it through this table.

The next-generation schema→Rust pipeline, expressed as components, contracts,
runtime planes, and a staged bootstrap. This document is the architecture spine;
the macro-language design (Nomos's own grammar and macro model) is owned by
`reports/logos/nomos-macro-model-v0.md` and is deliberately **not** reproduced
here — this document treats Nomos as a *component* and cites the macro model only
where the component boundary depends on it.

Written 2026-07-13 (session `schema-codex`, lane `pipeline-architecture`).

## How to read this document

Provenance discipline, identical to `design-v0.md` and cited with **no Spirit
intent tags** (a fresh audit found the existing intent tags unresolvable this
session; the design session is cited by date instead):

- **[psyche ruling — cite]** — the psyche's decision, with its `design-v0.md`
  item (or the dated dispatch that carried it). Settled unless retracted.
- **[evidence — cite]** — a worker-verified fact about the current workspace,
  with source.
- **[proposal]** — an agent suggestion where the psyche was **silent**. Not
  accepted; needs a decision. Every proposal is also collected in §11.

Two dated authorities are in play. Most rulings are from the **2026-07-11**
design session, recorded in `design-v0.md`. The three-component spine (§1) was
carried to this lane by the **2026-07-13 dispatch** as the psyche's stated
architecture; where it refines a 2026-07-11 item, both are shown and the
reconciliation is flagged (§1.3, §11-P1).

## 1. Overview — the three-component spine

**[psyche ruling — 2026-07-13 dispatch spine]** The pipeline is three
components plus the existing schema stack as the front boundary:

1. **The schema daemon** — holds `TrueSchema`, addressed by hash. This is the
   existing `schema` stack, already content-addressable (see §1.1).
2. **The Nomos component** — performs the conversion. A request references a
   `TrueSchema` by hash; Nomos performs the schema→logos conversion and sends
   the resulting logos, **serialized**, to the Logos component.
3. **The Logos component** — holds and serves logos (`CoreLogos` + logos
   `NameTable`, rkyv stored form) and owns the text projection.

**[psyche ruling — design-v0 §1]** The end-to-end pipeline these components
realize is `schema dialects → macro expansion → logos → Rust text → rustc`, with
Rust as the runtime backend (the Shen/K-Lambda analogy: logos is the
standardized core, Rust text the lowering target, rustc the host).

```mermaid
flowchart LR
  client([client / schema author])
  schemad["schema daemon<br/>(holds TrueSchema by hash)"]
  nomos["Nomos component<br/>(conversion)"]
  logos["Logos component<br/>(holds + serves logos,<br/>owns text projection)"]
  rust["Rust text → rustc<br/>(runtime backend)"]

  client -- "push: convertToLogos(hash)" --> schemad
  schemad -- "push: chain work to nomos" --> nomos
  logos -- "pull: list schema slots, request conversion" --> nomos
  nomos -- "fetch CoreSchema + NameTable (by hash)" --> schemad
  nomos -- "ship serialized logos" --> logos
  logos -. "project (text / Rust lowering)" .-> rust
```

**[psyche ruling — 2026-07-13, on this report]** The request topology supports
**BOTH flows**, not one:

- **Pull (logos-side driven):** a client "list[s] loaded slots in schema, then
  request[s] conversion from the logos-side" — a caller enumerates the schema
  daemon's loaded slots, then drives conversion from Logos.
- **Push (schema-side chained):** "a `convertToLogos` in schema which pushes the
  work to nomos, in a chain" — the schema daemon exposes a `convertToLogos`
  operation that pushes the conversion work forward to Nomos as a chain (schema →
  nomos → logos).

Both topologies are first-class; the contract spines below (§5) carry the
operations each flow needs.

### 1.1 The schema daemon is the existing content-addressed schema stack

**[evidence — repos/schema/ARCHITECTURE.md]** `schema` is "the schema macro
engine and typed semantic schema data model." Its layout is fully
content-addressable: the hash is computed on the semantic schema-in-Rust value
(`TrueSchema`), never on `.schema` text; `TrueSchema` archives through rkyv
(`to_binary_bytes` / `from_binary_bytes`). `signal-schema` is its current public
contract (`LoadPackage` / `EmitRust` → `PackageLoaded` / `RustEmitted` /
`Rejected`), a schema-derived `WireContract`.

**[proposal]** "The schema daemon holds TrueSchema addressed by hash" is
therefore satisfied by the existing stack; the new construction in this document
is the **Nomos** and **Logos** components plus their contracts. No new schema
daemon is built — but **[psyche ruling — 2026-07-13, on this report]** the schema
daemon's contract gains slot-listing, a hash-addressed fetch that serves
`CoreSchema + schema NameTable`, and a `convertToLogos` push entry point (§5.0,
§5.2a), none of which `signal-schema` exposes today.

### 1.2 Conversions happen outside text — typed objects end to end

**[psyche ruling — 2026-07-13 dispatch spine]** Conversions are typed-object
transformations, never text-to-text. Text appears at exactly two edges:

- **schema text → TrueSchema** at the schema daemon's authoring boundary only
  (existing behavior; the hash is on the typed value, `design-v0 §1.1 evidence`).
- **Logos → text** as a *projection* out of the Logos component (pretty-printed,
  `design-v0 §2`), and the eventual Logos → Rust text lowering (§7).

Everything between — `CoreSchema + NameTable → CoreLogos + NameTable` — is a
typed/serialized transformation carried on the binary wire, never a text stage.
This matches the workspace rule that inter-component transport is binary
protocol frames carrying typed contract messages, with NOTA reserved for
authored data and diagnostics, not as the transport contract.

### 1.3 Reconciliation with design-v0 §3.1 — RESOLVED (P1 confirmed)

**[psyche ruling — 2026-07-13, on this report]** **CONFIRMED.** Nomos is a
**dedicated component**: "schema goes to nomos, nomos goes to logos." The
design-v0 §3.1 tension (which placed Nomos consumption "in the logos daemon")
**resolves latest-wins**: the 2026-07-13 spine governs, and the conversion site
is the dedicated Nomos component, not a plane inside the Logos daemon. History,
for the record: **[psyche ruling — design-v0 §3.1]** had stated Nomos
definitions are *consumed* "in the **logos daemon**, at the schema→logos
conversion site." That earlier placement is superseded. All of §3–§3.1's
*consumption / dispatch / dialect-package* rulings survive unchanged; only their
*host component* moves from Logos to a dedicated Nomos. The three-component count
is settled.

## 2. Components and boundaries

Each stateful component follows the workspace shape: one runtime daemon crate +
thin CLI + a public `signal-<component>` contract crate (owner-policy
`meta-signal-<component>` only if an authority boundary needs it). The canonical
exemplar is the spirit triad (`signal-spirit` public + `meta-signal-spirit`
owner-policy + daemon-local nexus/sema modules), which
`repos/spirit/ARCHITECTURE.md` names as the shape "future component daemon repos
should copy." **[evidence — repos/spirit/ARCHITECTURE.md,
repos/schema/ARCHITECTURE.md]**

| Component | Owns | Public contract | Wire role |
|---|---|---|---|
| schema daemon (existing) | TrueSchema by hash, CoreSchema + schema NameTable | `signal-schema` (+ slot-listing, hash-fetch, `convertToLogos`) | serves CoreSchema+NameTable by hash; pushes convert to Nomos |
| **Nomos** (new) | the conversion; loaded slots (dialects / conversion state) | `signal-nomos` | accepts convert-by-hash; lists+serves slots; ships serialized logos to Logos |
| **Logos** (new) | CoreLogos + logos NameTable (rkyv), text projection, (eventually) Rust lowering | `signal-logos` | receives serialized logos; lists+serves units; drives pull-flow conversion; serves projections |

**[psyche ruling — 2026-07-13 dispatch spine]** The two contracts and what they
expose:

- **`signal-logos`** exposes logos's **main types**, so that Nomos can
  *construct* logos and ship it *serialized* to the Logos component.
- **`signal-nomos`** exposes the **macro objects** that schema needs to
  *recognize macro invocations* (e.g. the `Map` macro object; `design-v0 §3`).

### 2.1 Component-split test (why three, not one)

**[proposal, grounded in the micro-components split test]** The split is
justified by distinct nouns, vocabularies, and state owners:

- schema daemon owns the **schema** vocabulary and TrueSchema identity;
- Nomos owns the **macro / dialect** vocabulary and the conversion function;
- Logos owns the **logos node** vocabulary (CoreLogos/TrueLogos) and its
  NameTable, projection, and stored form.

Each is a separate bounded vocabulary and a separate codec surface — the split
test's positive triggers. **[evidence — design-v0 §1.2, ruling 1]** The psyche's
own "not enough room for another component" hesitation was about proliferating
components; the 2026-07-13 spine resolves it by making Nomos a genuine
first-class component. This is recorded, and P1 asks him to confirm the
three-component count against that earlier hesitation.

## 3. The Nomos component

Nomos is the conversion. This document owns its **component** shape; its macro
language and macro model live in `nomos-macro-model-v0.md`.

### 3.1 What Nomos consumes and produces

**[psyche ruling — design-v0 §2, §3]** Nomos consumes **CoreSchema + schema
NameTable** (not TrueSchema — CoreSchema so CoreLogos re-uses the same
identifier→name allocation) and produces **CoreLogos + logos NameTable** by
extending that allocation. The identifier space is **continuous across schema
and logos**: schema identifiers keep their meaning in logos; logos mints new ones
by extension (`design-v0 §2`).

**[psyche ruling — design-v0 §3]** The conversion logic *is* the macro system:
named macros (table entries, keyed on **minted identity**, never a string) and
structural macros (per-section positional defaults, e.g. the
"particular-struct" default derive sets). An application `X.()` with no
macro-table entry is an **error**; the structural default is specifically the
`X.{}` form. **[psyche ruling — design-v0 §3.1]** A dialect *is* a Nomos macro
package (macro table + structural section rules).

### 3.2 The conversion request references a TrueSchema by hash — both flows

**[psyche ruling — 2026-07-13 dispatch spine]** A request names a `TrueSchema`
by hash. **[psyche ruling — 2026-07-13, on this report]** The topology is
**both** flows (§1, request topology):

- **Pull (logos-side driven):** the caller lists the schema daemon's loaded
  slots, then requests conversion from the Logos side. Logos (or the client via
  Logos) enumerates schema slots and drives the conversion.
- **Push (schema-side chained):** the schema daemon exposes `convertToLogos`,
  which pushes the conversion work forward to Nomos in a chain (schema → nomos →
  logos).

**[psyche ruling — 2026-07-13, on this report, resolves P7 and widens it]**
"exactly. all three should have those types of operations." **All three
components — schema daemon, Nomos, and Logos — expose slot-listing and
hash-addressed fetch on their signal surfaces.** So the CoreSchema + schema
NameTable that the conversion consumes (§3.1) is obtained by a hash-addressed
fetch on the schema daemon's signal surface, which now definitely gains such an
operation (no longer merely proposed — see §5, P7 resolved). Nomos itself also
exposes slot-listing and hash-addressed fetch, and so does Logos.

### 3.3 Does Nomos own durable state? — leaning stateful (P4)

**[psyche ruling — 2026-07-13, on this report — implication]** Nomos exposes
**slot-listing** on its signal surface (§3.2, "all three should have those types
of operations"). **Listing loaded slots implies Nomos holds loaded state** —
which moves the answer toward the **stateful-registry** shape below. Recorded as
an *implication* of the slot-listing ruling, still **pending his explicit word**
on where Nomos definitions are *authored / held at rest* (the still-**[open]**
`design-v0 §8` question). The two candidate shapes, with the lean marked:

- **stateful-registry (leaning — implied by slot-listing)** — Nomos loads and
  holds dialect / logos-conversion slots in a SEMA-owned registry (single-writer)
  it can enumerate; convert requests name a loaded slot; Nomos has a real SEMA
  plane. The slot-listing operation is the direct evidence for this shape.
- **stateless-per-request (now less likely)** — the dialect package travels in
  the convert request (or is fetched by hash), Nomos holds no durable state, no
  SEMA plane. Harder to reconcile with a slot-listing operation.

**[proposal]** Take the stateful-registry shape as the working assumption, but do
not treat it as fully settled until the psyche states the definitions-at-rest
answer (P4, now *leaning*).

## 4. The Logos component

### 4.1 Identity architecture (mirrors the schema)

**[psyche ruling — design-v0 §2]** Logos mirrors the schema identity
architecture:

- **CoreLogos** — a stringless core; identifiers are indices into a logos
  **NameTable**.
- **TrueLogos** — the projected named view over CoreLogos (mirrors TrueSchema
  over CoreSchema).
- **rkyv** — the stored / in-memory form.
- **deserialized text** — the agent-readable projection, pretty-printed.

The logos NameTable **extends** the schema NameTable allocation (§3.1), so a
CoreLogos node addressing a carried-over schema identifier resolves through the
continuous space.

### 4.2 What the Logos component receives and serves

**[psyche ruling — 2026-07-13 dispatch spine]** Logos *receives serialized
logos* from Nomos (the ship step) and *serves* it. `signal-logos` exposes
logos's main types so Nomos can construct and serialize the logos value on the
wire. **[proposal]** The served surfaces are: store/accept a shipped serialized
logos unit; fetch a logos unit by its identity; project a logos unit to
pretty-printed text (`design-v0 §2`); and (eventually, §7) lower it to Rust text.

### 4.3 Storage / stored form

**[psyche ruling — design-v0 §2]** rkyv is the stored / in-memory form of logos.
**[proposal, P5]** *Which* store backs it was not decided. Because logos is a
**derived materialized view** — regenerable by re-running Nomos over a
`TrueSchema` — it is a rebuildable cache, not an authoritative source of truth.
Two shapes:

- **slot store (in-memory)** — mirror `signal-schema`'s `SchemaSlot` model: logos
  units live in an in-memory slot store, rebuilt on demand. Simple; matches the
  "rebuildable materialized store" framing already used for sema-engine
  (`sema-engine/ARCHITECTURE.md`).
- **sema-engine-backed (durable)** — persist logos units through `sema-engine`
  (redb-backed, single-writer, blake3-addressed) like the rest of the fleet's
  durable state, if a durable, content-addressed logos cache is wanted.

**[proposal]** Prefer the slot store until a durable-logos requirement appears;
logos is derivable, so durability buys little beyond a warm cache. Flagged P5.

### 4.4 Text projection and pretty-printing

**[psyche ruling — design-v0 §2, §1.2]** Text is a **projection**, with
pretty-printing; the projection owns the `.`→`::` translation for Rust paths
(`design-v0 §1.2, ruling 7`) and re-sugars on Rust output while logos itself
stays desugared at the dialect boundary (`design-v0 §7.2`). **[evidence —
design-v0 §7.1]** The existing emitter is already token-based
(`proc_macro2::TokenStream` + `quote`, one `prettyplease` pass); the logos→Rust
projection can inherit that token path's parenthesization and hygiene rather than
reinventing them.

## 5. The contracts

Two new `signal-<component>` contract crates (plus an addition to the existing
`signal-schema`), each a schema-derived `WireContract` following `contract-repo`
discipline: operation types, reply types, codecs, round-trip tests; **no** daemon
runtime, actors, tokio, sockets, or state. **[evidence —
repos/signal-schema/ARCHITECTURE.md]** — the existing `signal-schema` is the
pattern to copy.

### 5.0 The shared operation family across all three signal surfaces

**[psyche ruling — 2026-07-13, on this report — P7 resolved and widened]**
"exactly. all three should have those types of operations." Each of the three
signal surfaces — `signal-schema`, `signal-nomos`, `signal-logos` — exposes the
same **two-operation family**:

- **slot-listing** — enumerate the loaded slots/units the daemon holds (the
  schema daemon's loaded schema slots; Nomos's loaded slots; Logos's loaded logos
  units). This is what the *pull* flow (§3.2) calls to discover what is available.
- **hash-addressed fetch** — retrieve a held unit by its hash / identity.

This is no longer a proposal for one daemon; it is a ruling for all three. It
directly resolves former P7 (the schema daemon *does* serve CoreSchema + schema
NameTable by hash — the hash-addressed fetch above) and widens it to Nomos and
Logos. It also grounds §3.3's stateful-registry lean for Nomos (a daemon that can
list its slots holds state).

### 5.1 signal-logos (operation spine)

**[psyche ruling — 2026-07-13 dispatch spine]** `signal-logos` exposes logos's
**main types** so Nomos can construct and ship serialized logos. **[psyche ruling
— 2026-07-13, on this report]** it also carries the §5.0 slot-listing +
hash-fetch family and the *pull*-flow conversion request. **[proposal, P6]** A
stable spine (contract-local verbs, no sema vocabulary on the wire):

- `AcceptLogos` — receive one serialized logos unit shipped by Nomos.
- `ListLogos` — slot-listing: enumerate held logos units (§5.0).
- `FetchLogos` — hash-addressed fetch: retrieve a held logos unit by identity
  (§5.0).
- `RequestConversion` — the **pull** flow: from the Logos side, request
  conversion of a named schema slot (Logos drives the schema→nomos→logos chain
  on the caller's behalf; §3.2).
- `ProjectLogos` — return the pretty-printed text projection of a unit.
- replies: `LogosAccepted` (with stored identity), `LogosListed`, `LogosFetched`,
  `ConversionRequested`, `LogosProjected`, `Rejected` (closed `RejectionReason`,
  no catch-all string).

The logos node types themselves (CoreLogos/TrueLogos) are the contract's **main
types**, exported so Nomos can build a logos value and serialize it into
`AcceptLogos`.

### 5.2 signal-nomos (operation spine)

**[psyche ruling — 2026-07-13 dispatch spine]** `signal-nomos` exposes the
**macro objects** schema needs to recognize macro invocations. **[psyche ruling
— 2026-07-13, on this report]** it also carries the §5.0 slot-listing +
hash-fetch family. **[proposal, P6]** Its exposed surfaces:

- **the macro-object types** (`design-v0 §3`, e.g. the `Map` macro object) —
  imported by the schema side so it can recognize a macro invocation as such;
- **the conversion operation**: `Convert` (names a `TrueSchema` by hash; §3.2),
  replying `Converted` (logos shipped / accepted, referencing the Logos unit
  identity) or `Rejected`;
- **`ListSlots` / `FetchSlot`** — the §5.0 slot-listing + hash-addressed fetch
  over Nomos's loaded slots (the operations that imply Nomos holds loaded state,
  §3.3).

### 5.2a signal-schema addition (P7 resolved)

**[psyche ruling — 2026-07-13, on this report]** The existing `signal-schema`
gains the §5.0 family and the **push** entry point:

- **slot-listing** — enumerate loaded schema slots (drives the *pull* flow's
  discovery step, §3.2).
- **hash-addressed fetch** — serve `CoreSchema + schema NameTable` for a hash
  (what Nomos's conversion consumes, §3.1; former P7, now ruled to exist).
- **`convertToLogos`** — the **push** entry point (§1, §3.2): schema pushes the
  conversion work forward to Nomos in a chain.

**[open — design-v0 §8]** Whether Nomos itself obeys the full NOTA invariants is
presumed-yes-unconfirmed; the no-string-dispatch invariant specifically **is**
confirmed via minted-identity keying (`design-v0 §3`). Every contract keeps macro
and slot lookup keyed on minted identity / hash, never a string.

### 5.3 No owner-policy contracts proposed yet

**[proposal]** Neither component is proposed to need a `meta-signal-*`
owner-policy contract in v0 — there is no configuration or authority boundary
distinct from the public surface yet. Add one only if dialect-package loading
(P4) turns out to need an owner-authority boundary.

## 6. Runtime shape inside each daemon

**[proposal, P2]** The psyche was silent on whether Nomos and Logos are kameo
actor daemons like the rest of the fleet. Proposal: **yes** — copy the spirit
triad shape (`repos/spirit/ARCHITECTURE.md` names it the shape to copy). Each
daemon runs the three planes:

- **Signal** admits framed `signal-<component>` requests, authenticates the
  caller shape, returns the typed reply envelope.
- **Nexus** owns async mail and external effects. In **Nomos** this is the heavy
  plane: fetch CoreSchema+NameTable from the schema daemon (§3.2), run the
  conversion, ship serialized logos to Logos. In **Logos** it handles the
  projection and (eventually) the rustc hand-off (§8).
- **SEMA** owns durable single-writer state and commits legal transitions — the
  loaded-slot registry in Nomos (leaning present, §3.3/P4, since Nomos lists its
  slots), the logos slot/cache writer in Logos (P5).

A root request flows Signal → Nexus → SEMA and returns on the same typed path;
no plane is bypassed by helper calls. The CLI is each daemon's first client,
talking only to its own daemon through its public contract.

**[proposal]** Trace identity is typed and schema-derived: a witness names
component, contract operation, plane, request identity, and terminal outcome —
including, for Nomos, the source `TrueSchema` hash and the shipped logos identity,
so a conversion is traceable end to end.

## 7. Bootstrap staging — explicit phases

**[psyche ruling — 2026-07-13 dispatch spine + design-v0 §3.1, §4]** The
inter-component types are defined in the **current** schema→Rust stack; the
current `schema-rust` pipeline generates their Rust. Eventually logos does the
Rust lowering itself (or via one more component), and *that endpoint replaces
schema-rust emission as THE Rust-generating mechanism*. Presented as phases with
what exists at each:

### Phase 0 — today (exists now)

**[evidence — repos/schema, repos/schema-rust, repos/signal-schema]** The
current schema→Rust stack: `schema` (macro engine, content-addressed TrueSchema),
`schema-rust` (token-based Rust emitter, `prettyplease`), `signal-schema`
(`LoadPackage`/`EmitRust`). **[psyche ruling — design-v0 §4]** The Rust
`schema-rust` currently emits, plus its committed goldens, is the **acceptance
oracle**: any logos that lowers must reproduce that same Rust.

### Phase 1 — define the inter-component contracts on the current stack

**[psyche ruling — 2026-07-13 dispatch spine]** Author `signal-nomos/schema` and
`signal-logos/schema` as `.schema` files, and **extend `signal-schema`** with the
§5.0/§5.2a additions (slot-listing, hash-addressed CoreSchema+NameTable fetch,
`convertToLogos`), letting the **current `schema-rust`** emit all three
`src/schema/*.rs` wire surfaces — exactly as `signal-schema` is generated today.
At this phase the contracts exist and compile; the Nomos/Logos *daemons* do not
yet. The logos node types (CoreLogos/TrueLogos), the Nomos macro-object types,
the shared slot-listing + hash-fetch family, and both operation spines are the
schema-generated output.

### Phase 2 — build the Nomos and Logos daemons above those contracts

**[proposal, grounded in design-v0 §4]** Stand up the two component daemons
(§6). Nomos performs `CoreSchema + NameTable → CoreLogos + NameTable`; Logos
holds/serves logos and **projects to text**. The logos→Rust projection is
validated against `schema-rust`'s existing goldens: the migration is correct when
the macro-produced logos lowers to the Rust the current emitter already produces
(`design-v0 §4`). At this phase **`schema-rust` still emits the production Rust**;
the logos path runs in parallel, gated by the golden oracle.

### Phase 3 — logos becomes THE Rust-generating mechanism (endpoint)

**[psyche ruling — 2026-07-13 dispatch spine]** Logos does the Rust lowering
itself (or via one more component); that endpoint **replaces** `schema-rust`
emission. **[proposal, P3]** Whether the Logos→Rust lowering is a **plane inside
the Logos daemon** or a **separate fourth component** was left as the psyche's
"itself or via one more component" — flagged P3. **[proposal, from design-v0 §3.1
+ §7.2]** At this end state the self-hosting shape holds: a dialect is a Nomos
macro package, and the **Logos→Rust projection is the fixed hosted kernel** (the
Shen/K-Lambda parallel — schema defines its own Nomos macros atop a small fixed
lowering). `schema-rust`'s token-based emission (`design-v0 §7.1`) is the
harvest source for that fixed lowering, then retired.

**Compatibility note.** **[evidence — design-v0 §4]** Because Phase 2 gates on
the existing goldens and Phase 3 only swaps the *producer* of identical Rust, the
public Rust surface is unchanged across the cutover — the goldens are the
byte-verification basis, matching the executed nota-grammar-migration precedent
(`nota-grammar-revision-v0.md §2.5`).

## 8. Diagnostics — rustc errors flowing back (proposal)

**[proposal, P8]** The psyche was silent on how rustc diagnostics flow back.
rustc reports against **generated Rust text**, but the author works in schema /
logos. **[evidence — design-v0 §7.2]** The prior-art brief named a
**source-map** from generated Rust back to the schema/logos origin as a
must-design-early pitfall, alongside defensive parenthesization and name hygiene.
Proposal: the Logos→Rust projection emits a source-map keyed by logos node
identity; a rustc diagnostic's span is looked up to a logos node, and — via the
continuous identifier space (§4.1) — back to its schema identity, so the
diagnostic points at the schema origin. Which component owns this back-translation
(Logos, since it owns the projection, is the natural home) is flagged P8.

## 9. Invariants preserved (carried, all psyche-stated)

**[psyche ruling — design-v0 §6]** The architecture must hold the standing NOTA
invariants: strictly typed positional data (the expected type is known at every
boundary; the parser never classifies); positionality, no named binding; no
aliases; capitalization is semantic; per-kind blocks; one namespace per loaded
whole (duplicate name is an error); generics defined by kind, lowering dispatches
on kind never on a string. The macro table's minted-identity keying (`design-v0
§3`) is how the no-string-dispatch invariant is kept at the component boundary.

## 10. Code map (planned, nothing built yet)

This is report-only; no crates exist. The planned repositories, following the
canonical names:

```text
signal-nomos/     schema/*.schema -> src/schema/*.rs   (Phase 1, schema-rust-emitted)
signal-logos/     schema/*.schema -> src/schema/*.rs   (Phase 1, schema-rust-emitted)
nomos/            daemon + thin CLI, signal/nexus/sema planes   (Phase 2)
logos/            daemon + thin CLI, planes + text projection   (Phase 2)
                  + Logos->Rust lowering                        (Phase 3, P3)
```

## 11. Proposal / decision status

Statuses updated with the 2026-07-13 psyche answers on this report. **P1 and P7
are now resolved; P4 is leaning.** The remainder still await a decision.

- **P1 — three-component count. RESOLVED 2026-07-13.** Confirmed: dedicated Nomos
  component, "schema goes to nomos, nomos goes to logos"; the design-v0 §3.1
  "logos daemon" tension resolves latest-wins (§1.3). No longer open.
- **P7 — hash-addressed fetch of CoreSchema + schema NameTable. RESOLVED and
  WIDENED 2026-07-13.** "all three should have those types of operations": the
  schema daemon, Nomos, and Logos each expose slot-listing and hash-addressed
  fetch on their signal surfaces (§5.0, §5.2a). The schema daemon definitely
  gains the CoreSchema+NameTable hash-fetch (Nomos pulls); the client-pushes
  alternative is dropped.
- **P4 — Nomos durable state. LEANING stateful 2026-07-13.** Nomos exposing
  slot-listing implies it holds loaded state, moving the answer toward the
  stateful-registry shape (§3.3). Marked an *implication* pending the psyche's
  explicit word on where Nomos definitions are *authored / held at rest*
  (`design-v0 §8`).
- **P2 — are Nomos and Logos kameo actor daemons with signal/nexus/sema planes,
  like the rest of the fleet?** Still open. Proposal: yes, copy the spirit triad
  (§6).
- **P3 — is the Logos→Rust lowering a plane inside the Logos daemon or a separate
  fourth component?** Still open. The psyche said "itself or via one more
  component" (§7, Phase 3).
- **P5 — storage engine for the Logos component:** still open. In-memory slot
  store (rebuildable) vs `sema-engine`-backed durable cache; proposal: slot store
  until a durable-logos need appears (§4.3).
- **P6 — the `signal-logos`, `signal-nomos`, and `signal-schema`-addition
  operation spines** (§5.0–§5.2a) — still a proposal for the exact verb set and
  reply vocabulary (the psyche ruled the *operation families* exist; the concrete
  verb names remain agent proposals); confirm or correct.
- **P8 — rustc diagnostic back-flow:** still open. A source-map from generated
  Rust → logos node → schema identity, owned by the Logos component; the psyche
  was silent on the whole diagnostic path (§8).
