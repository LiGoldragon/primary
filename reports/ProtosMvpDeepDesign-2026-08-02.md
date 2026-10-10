# Protos MVP Deep Design — Gaps for Production Components — 2026-08-02

Commissioned by the psyche: "run a deep design and look for any gaps for
MVP protos-based components (with the signal repos obviously adapted, as
well as the in-repo database specification...)". Grounded in two
inventories taken today at the main bookmarks: the four target daemons
(spirit, mind, orchestrate/orchestrator, message/messenger) and the
engine train (core-ethos, core-nomos, core-logos, rust-logos,
nomos-engine, language-engine-witness). Design authored by the manager;
question marks are the psyche's to close.

## 1. MVP definition

A **protos-based component** is a daemon whose specification is authored
in Ethos across the three-file anatomy — `interface.ethos` (wire),
`nexus.ethos` (logic), `sema.ethos` (store) — generating, in its real
build, its message types with Input/Output/Refusal membership and error
machinery, its behavior trait declarations, and its storage record
types. Implementations remain handwritten Rust falling under the
generated traits. Everything deferred stays deferred: operational
editing, evolution engine, ScopeOf realization.

## 2. What the component inventory established

- **All four daemons already generate from authored schema files** in
  `build.rs` (schema-rust `GenerationDriver`), emitting contract types,
  nexus state machines, sema runtimes, and daemon modules checked in
  under `src/schema/`. The Ethos generator's replacement target is
  therefore precise and proven — this pattern, on the new train.
- **`signal-mind` is the outlier**: its contract types are handwritten
  (`signal_channel!` macro); its schema file documents but does not
  generate. It is the one contract crate where Ethos generation is a
  pure addition displacing nothing.
- **Streams are not deferrable.** Spirit (IntentSubscription,
  ObserverTap), mind (four subscription kinds with demand/backpressure),
  and orchestrate (Watch/Unwatch Observation protocol) all carry live
  subscription surfaces. Only message is plain request/response/refusal.
- **The judge is a second wire surface.** Spirit, mind, and orchestrate
  each delegate judgment to an external judge process over its own
  socket (AdmissionJudgePacket/Verdict; KnowledgeJudge; orchestrator
  judge). Mind even has a real Rust trait today — `KnowledgeJudge` with
  `judge()` and `record_applied_decision()` — a ready-made nexus
  fixture. Components therefore have **multiple interface files** (main
  tier, meta tier, judge contract), which the header-typed file model
  supports without any new machinery.
- **Wire stack is uniform**: rkyv 0.8 (little-endian, 32-bit pointers,
  unaligned) everywhere, dotos-text feature-gated as human projection.
  The existing `WireAttributes` Nomos macro already emits exactly this.
- **Sema is daemon-private**: each daemon declares its own record
  families (spirit 3, mind 10, orchestrate 14, message 6 tables) — the
  `sema.ethos` file is per-component, as the psyche named it.
- **Rename sizing**: orchestrate→orchestrator touches roughly 70-80
  files across ~10 repos (signal crates, Nix service modules, consumer
  repos, primary workspace); message→messenger roughly 10-15 files
  across ~8 repos, less if `signal-message` kept its name.

## 3. What the engine inventory established

- **Trait declarations exist nowhere** — not in WholeLogos (which
  carries only Newtype and Enumeration), not even in the legacy item
  algebra (which does carry ImplBlock and Function with full Rust
  projection). `TraitDef` plus method signatures is the largest single
  vocabulary addition, and plain structs must also join WholeLogos.
- **The codec has one clean insertion point**: today's single hardcoded
  root record. Header-imports-body becomes a composite root with a
  two-phase parse; the structural table already dispatches by encoded
  type ID, so header-selects-body-kind is an application of existing
  machinery.
- **File-kind-driven emission has a natural seat**: six enrichment
  generation classes already exist (interface ergonomics, wire codecs,
  envelopes...). A file-kind axis on generation selection extends a
  pattern rather than inventing one. Interface types get wire
  attributes automatically; nexus types stay plain — same declaration
  syntax, emission decided by the file kind.
- **The offline generator binary is the make-or-break gap**:
  nomos-engine is library-plus-daemon only. The language witness's
  `slice_one` test already wires the full chain offline (decode Ethos →
  transform → WholeLogos → emit Rust → compile and run); formalizing
  that wiring as a batch binary callable from `build.rs`/Nix is what
  makes "in production" true.
- **Golden infrastructure exists** (frozen sema goldens, archive
  round-trips, fixture files); the three new file kinds inherit the
  `slice_one` pattern directly.
- **Universal trait home**: the `protos` crate (0.4.0,
  "implementation-free component contracts for the Protos family") is
  architecturally right but no daemon depends on it yet; `signal-frame`
  is universal but is transport infrastructure.

## 4. The file kinds, full candidate shape

The interface body is **four positions** — inputs, outputs, refusals,
shared types. Streams are NOT a section (psyche-corrected: sections are
earned only by universal roles; patterns are Nomos objects). A stream
is a Nomos-object application declared among the types — full vertical
design in `reports/NomosStreamDesign-2026-08-02.md`:

```ethos
Interface.1
[signal-domain.Domain nexus.{Entry Judgment}]
{
  [Record.Entry Observe.Query]
  [Recorded.RecordIdentifier Observed.Entries]
  [GuardianRejection.Reason ReferentRejection.Reason]
  {RecordIdentifier.Integer Entries.Vector.Entry Reason.Text
   Stream.Observer.{ObserverFilter ObserverSubscription ObservationEvent}}
}
```

- The Nomos object comes first — `Stream.Observer.{...}` is a stream
  named Observer, its payload the open-query, receipt, and event
  types; token and close machinery are universal and emitted, never
  authored.
- Imports group by source: `source.{A B}`, sources being sibling files
  of the component (`nexus`, `sema`, `interface`) or other components'
  contract names (`signal-domain`), resolved by the build wiring the
  same way dependency schemas resolve today.

Nexus (mind's real judge, written as it would land):

```ethos
Nexus.1
[interface.{Knowledge KnowledgeJudgeRequest}]
{
  {KnowledgeJudgeDecision.[Accepted Rejected.KnowledgeRejectionReason]}
  {KnowledgeJudge.{judge.{KnowledgeJudgeRequest KnowledgeJudgeDecision}
                   recordAppliedDecision.{KnowledgeJudgeAppliedDecision Unit}}}
}
```

Sema (spirit's actual three families):

```ethos
Sema.1
[interface.Entry signal-domain.Domain]
{
  {StoredRecord.{RecordIdentifier Entry} StoredReferent.{Referent Aliases}}
  [records.{StoredRecord Domain} referents.{StoredReferent Domain}]
}
```

A sema body: record types, then families as `table.{Record Key}`.

## 5. Gap register

**Syntax — psyche ruling needed:**

| # | Gap | Candidate |
| --- | --- | --- |
| G1 | Stream surface (forced by 3 of 4 daemons) | RESEATED: a Nomos object, not a section — `Stream.Observer.{...}`; full vertical in `reports/NomosStreamDesign-2026-08-02.md` |
| G2 | Import spelling and resolution | `source.{A B}` entries; sources are sibling-file or component names, resolved by build wiring |
| G3 | Unit return | Explicit `Unit` in last position (absence of result is information position cannot infer) |
| G4 | Trait/method prose | Optional pipe-text description position; traits-as-documentation suggests yes |
| G5 | Sema family shape | `table.{Record Key}` as in section 4 |

**Engine — work items, no ruling needed:**

| # | Item |
| --- | --- |
| E1 | `TraitDef` + method signatures in WholeLogos and projection; Struct joins WholeLogos |
| E2 | Header-imports-body composite root and kind dispatch in EthosCodec |
| E3 | File-kind emission axis on generation selection (wire attrs for Interface, plain for Nexus) |
| E4 | Refusal error machinery emission (Error/Display/From impls) |
| E5 | Positional membership impls (Input/Output/Refusal/stream event) |
| E6 | Offline generator binary formalizing the `slice_one` wiring, callable from build.rs/Nix |
| E7 | Golden + round-trip fixtures for the three kinds |

**Integration — decisions and sequencing:**

| # | Item |
| --- | --- |
| I1 | Universal traits home: recommend `protos` crate; four Cargo.toml additions |
| I2 | rkyv parity: generated types must match the uniform wire config (WireAttributes already encodes it) |
| I3 | Contract-crate switchover order: signal-mind first (pure addition), then spirit, orchestrator, messenger (each displaces its old schema generation — clean cut per crate, no bridges) |
| I4 | Sema staging: author + witness `sema.ethos` in MVP; flip generation when the new sema path is complete (avoids splitting one runtime across two generators) |
| I5 | Judge and meta tiers: additional interface files per component; second wave after main-tier seating |
| I6 | Renames ride the train end: orchestrator (large), messenger (small); whether signal-* crates rename with their daemons is open |

## 6. Staging proposal

- **Stage 0 — rulings.** Close G1-G5 and the section 7 questions.
- **Stage 1 — fixtures.** Spirit's three files authored for psyche
  review (the see-it moment), mind's nexus judge file alongside since
  its trait already exists in Rust.
- **Stage 2 — engine.** E1-E7 as a codex package; fixtures become
  goldens; witness extends `slice_one` to the three kinds.
- **Stage 3 — first production landing.** `signal-mind` contract crate
  generated from `interface.ethos` — the outlier where nothing is
  displaced. Witness: generated types are API-equivalent to today's
  handwritten enums.
- **Stage 4 — the wave.** Spirit, orchestrator, messenger contract
  crates switch over one at a time; nexus traits land per daemon;
  sema.ethos authored everywhere and flipped per I4. Renames land at
  the end of the train.

## 7. Questions for the psyche

1. **Streams** (G1): SUPERSEDED — the psyche corrected the section
   design to a Nomos object; the open questions now live in
   `reports/NomosStreamDesign-2026-08-02.md` section 7.
2. **First landing** (I3): fixtures spirit-first as ruled, but the
   first *production* switchover in signal-mind where nothing is
   displaced — accept, or insist spirit lands first in production too?
3. **Universal traits home** (I1): `protos` crate as the contracts
   convergence point — confirm or name another home.
4. **Signal crate renames** (I6): do signal-orchestrate and
   signal-message rename with their daemons (signal-orchestrator,
   signal-messenger)? Recommend yes for coherence, staged at train end.
5. **Imports and Unit** (G2, G3): confirm the candidate spellings or
   correct them at fixture review.
