# 412 — Review of `/system-designer/42` (the `/167` horizon intent-divergence audit)

*Kind: Review (audit-of-an-audit) · Topics: schema, horizon, audit, schema-next, schema-rust-next, review · 2026-05-28*

*Per psyche directive 2026-05-28: audit and review
`reports/system-designer/42-horizon-167-intent-divergence-and-fixes.md`. I
verified its claims against the live schema-rust-next emitter
(`src/lib.rs` at main `d5f4201`) and the schema-next engine. Verdict: 42 is
a high-quality, accurate, artifact-grounded audit — I agree with all four
divergences. Below: confirmation per divergence, three sharpenings the
emitter source lets me add, and one staleness note.*

## 1. Verdict — sound, agree with all four

`/42` is a model audit: it reads the actual artifacts (the report, the
`.schema`, the 777-line emitted `lib.rs`), separates "runs honestly" from
"generates the right thing," and gives a clean dependency-ordered fix list
with status. Its four divergences (D1 collections-free caricature, D2
duplicated runtime floor, D3 vestigial signal planes, D4 engines emitted
not driven) are each real and correctly characterised. I confirmed each
against the engine/emitter source; nothing in 42 is wrong. The notes below
ADD to it, they don't correct it.

## 2. Confirmation + sharpening, per divergence

### D1 — collections-free caricature: CONFIRMED, and now closing on two branches
The emitter on main proves it: `RustEmitter`'s `rust_type` /
`parse_expression` / `format_expression` all read `reference.name.as_str()`
(`lib.rs:1036-1058`) — `TypeReference` is still a **bare name**, no
`Vector`/`Map`/`Optional`. So main literally cannot emit a collection-bearing
`ClusterProposal`; `/167`'s 2-node, 1-feature caricature was forced by the
type model, exactly as 42 says.
**Update to 42's status**: 42 lists D1 as "in flight (`/41`)". As of now it
is closing on **two** branches — the system-designer's `collections-horizon`
AND a designer `designer-schema-collections-2026-05-28` (just reported green
on both repos, off main, with the `KeyValueMap`→`KeyValue` rename per record
1045, pushed). D1 is the most-progressed divergence, not merely in-flight.

### D2 — duplicated runtime floor: CONFIRMED, and DEEPER than 42 states
42 says the generic floor is "duplicated per generated module." The emitter
source shows it is worse than duplication on two axes:
1. **The floor is emitter-HARDCODED, not schema-derived at all.** `emit_nota_support`
   (`lib.rs:145-259`), `emit_mail_event_support` (`:646-786`),
   `emit_signal_frame_support` (`:497-535`), `emit_plane_envelope`,
   `emit_upgrade_support` are all `self.line("<literal Rust>")` — roughly
   **600 of the emitter's ~1077 lines are literal Rust strings** for the
   generic floor (`NotaDecodeError`, the plane envelopes, `OriginRoute`, the
   mail nouns, `NexusEngine`/`SemaEngine`, `UpgradeFrom`). None of it comes
   from a schema. So this isn't only "duplicated per module" — the floor is
   not schema-at-heart in the first place; it's emitter boilerplate.
2. **Why it can't currently be schema-derived**: the floor is generic +
   trait-shaped (`NexusMail<Payload>`, `Signal<Root>`, `MessageProcessed<Reply>`,
   `trait NexusEngine`, `trait MessageSentHook`). The schema language emits
   only structs/enums/newtypes — no generics, no traits. So even a shared
   `schema-core` crate (42's D2 fix) would dedupe the *location* but the floor
   would stay **emitter-hardcoded** until the schema language can express
   generic + trait substrate.
**So D2's fix is two-layered**: (a) extract the floor to one shared crate
imported via `/39` cross-crate import (deduplication — 42's fix, correct and
mechanism-proven); (b) eventually make the floor itself schema-declared,
which needs schema-language generics/traits (a gap 42 doesn't name). (a) is
the near-term win; (b) is the deeper schema-at-heart closure.

### D3 — vestigial signal planes: CONFIRMED
The engine requires it: `SchemaEngine::lower_document_with_context`
(`engine.rs:155`) hard-errors unless the document holds exactly 4 root
objects, and `RootEnumMacro` lowers Input/Output as mandatory positions. A
pure types module has no way to omit them. 42's fix (make Input/Output
optional — the types-only-module shape, a `/39`-flagged gap) is the right
one. Accurate.

### D4 — engines emitted not driven: CONFIRMED, softer, and now connectable
42 correctly calls this the softest (gated on the open runtime-shape
decision, record 1050). Two additions:
1. The emitted-but-undriven surface has **grown since `/167`**: main now also
   emits the `schema::Plane` data-carrying enum (`lib.rs:788-809`, record
   1052) and the plane-routed `signal`/`nexus`/`sema` namespace modules
   (`:856-896`, record 1042) — more engine scaffolding, still undriven in
   `/167`.
2. **The "drive it" work already exists in the designer lane**: `/408`
   prototyped a live three trait-ordered engine chain (Signal→Nexus→SEMA) in
   spirit-next, and bead `primary-ijhw` carries the envelope/plane-driven
   version. 42 doesn't connect D4 to `/408`; the connection is: once
   Horizon's runtime shape (1050) is decided, Horizon adopts the `/408`
   chain pattern rather than inventing one. D4's fix is less open than 42
   implies — the chain pattern is prototyped, only Horizon's *adoption* of it
   waits on 1050.

## 3. One staleness note

42 (and `/167`) describe the emitter's runtime model as a snapshot. The
emitter is a **fast-moving target**: between `/167`'s emission and now, main
went `0a6a8cb` (plane-routed namespaces) → `d5f4201` (plane kind tag →
plane enum, record 1052). So `/167`'s "incorporates the latest runtime
model" was true at capture but is already one step behind (it predates the
`schema::Plane` enum). Not a flaw in 42 — but any audit of emitted output
should pin the emitter rev (42 does pin `/167`'s branch commit, good), and
re-reads should expect drift.

## 4. Bottom line

`/42` is accurate and well-sequenced; agree with all four divergences and
its fix order (D1 central + closing, D2/D3 capability gaps, D4 gated on
1050). The value I add: D1 is closing on two branches now (not just `/41`);
D2 is deeper than per-module duplication — the floor is emitter-hardcoded
and not schema-derivable until the schema language gains generics/traits, so
its fix is two-layered; and D4's "drive the engines" pattern already exists
in `/408` + `primary-ijhw`, so Horizon's only open piece there is adopting it
once the runtime shape (1050) is decided. The current engine/emitter reality
that produces these divergences is represented in detail in `/413`.
