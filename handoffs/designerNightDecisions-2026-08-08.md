# Designer night decisions — for the psyche's morning review

Authority: "keep working through decisions you can make yourself, just
make a note of them to tell me in the morning. im going to bed"
(2026-08-07, ~22:10Z; logged in
psyche/Vision/workingSpiritNewEthosSyntax.md).

Rulings the Designer made overnight, most consequential first. Each is
revertible; say the word and it re-lands differently.

## 1. Nexus/sema type home (decision-sheet item 6)

Ruled: wire/decision *data* types migrate into the `.ethos` files,
making them the complete type source (the encoded form is the code);
runtime machinery — `Work`/`Action` generics, plane envelopes,
`NexusEngine`/`SemaEngine` traits, the daemon skeleton, subscription
plumbing, staged intake — is handwritten in spirit per hqu.14's
"handwritten runtime/role behavior". The boundary: if a type crosses
the wire or is decided upon, it is `.ethos`; if it exists to run the
daemon, it is Rust.

## 2. hqu.26 commit provenance (decision-sheet item 7)

Decided: the two commits (core-ethos 9fb2ba6f, sema-translator
faf1a7b2) stay standing. They are verified compliant with your
approved conditions, all boundary tests pass, and the unified train is
already built on top of them. Formal blessing (or a fresh re-land)
remains yours; nothing tonight forecloses it beyond what was already
built atop them before the question arose.

## 3. Fixture-internal choices treated as blessed with the fixture

Your blessing of the observer fixture is read as carrying its internal
choices: version stays the typed triple `{Major Minor Patch}`;
stream-section entries are element-type only; `Tap`/`Untap` names;
typed `ObservationTapToken.Integer`; `EffectObserved` means effects
become recorded (the `EffectsOnly` filter becomes honest rather than
dying); refusals in the Refusal section. Logged in
psyche/Vision/observerFixtureBlessed.md.

## 4. Observer vocabulary bodies HELD for you (not ruled)

The blessed fixture references five types with no blessed body:
`OperationKind`, `EffectKind`, `ObservationEndReason`,
`DiscardedOperationCount`, `ObserverFilter`. I ruled only the
sequencing: nothing lands overnight. The anatomy question for you in
the morning: are `OperationKind`/`EffectKind` universal signal-domain
vocabulary or per-component contract vocabulary? (Production's
`OperationKind` is spirit's 21 input verbs — component-specific in
substance.) Also wanted: `ObservationEndReason`'s variant set (the
only production-proven end is daemon shutdown) and `ObserverFilter`'s
body (production: `[All OperationsOnly EffectsOnly]`).

## 5. Five-section train advance authorized

The stream section made the Interface body five sections (Input,
Output, Refusal, Stream, Declarations). I authorized the mechanical
train advance: core-ethos published, schema-rust repinned,
signal-domain repinned with domain.schema regenerated to five
sections through the explicit regeneration path, deterministic
freshness verified. Same main-first pattern as the hqu.30
unification.

## 6. Stream name collision: trait takes `Stream`, struct renamed

The protos crate's runtime handle `Stream<Event>` collided with the
universal trait the Stream section confers. Ruled: the trait takes
`Stream` — section→trait symmetry (Input/Output/Refusal/Stream) is
your sections-confer-traits ruling, and the ontology owns the plain
name. The runtime handle is renamed `OpenedStream<Event>` (the stream
an open produced). **`OpenedStream` is my coinage — review it.**
Rename propagated mechanically through `StreamOpen`, `StreamEvent`,
signal-domain.

## 7. Spirit ethos sources rescued and transcribed (pending your review)

`nexus.ethos` and `sema.ethos` rescued from spirit-ethos into
spirit/schema/, re-spelled to blessed syntax, and expanded with the
wire/decision data types from the old `.schema` files per ruling 1.
Every transcribed block is comment-marked as night transcription,
psyche-grasp `unseen`. Sequencing decisions I made: all 12
`NexusEffectCommand` variants kept (the `.schema` source is the
authority; includes `CloseObserverTap`); the commit pushed to main
(additive, no build wiring).

**Held for you — a real meaning conflict:** the transcribed wire
types reference the old per-verb payload types (`Proposal`,
`Clarification`, `Supersession`, `Retirement`, their receipts), which
the current interface's unified `Entry` + `Kind` model may supersede.
Which wire commands survive is yours to rule; nothing is wired into
generation until then. The 3-section organization of the expanded
files is also a tagged assumption.

## 8. Observer stream anatomy — held for you

Spirit's interface has no termination entry for the Observer intent
stream, and its initiation is ambiguous: `Observe.Query` today means
the one-shot query (answered by `Observed.RecordSet`); whether it
double-duties as stream initiation, or the stream gets its own
initiation entry, is your anatomy call — as is naming the missing
termination entry (the tap surface's analog is `Untap`; the intent
stream has nothing). I ruled only that the migration lands with the
Input section untouched and the mapping marked open in place; the
runtime wiring that needs the answer is a later slice.

## 9. Cross-source imports resolve via staged authorization

Spirit's schema imports `signal/domain.[Domain DomainScopes]`, but the
authority couldn't resolve imports across sources. Ruled: the
authority consults its own previously authorized sources (staged
metadata becomes visible to later `authorize` calls, ordering
controlled by the caller). Rejected the alternative — a caller-facing
`admit_external_type` — because a caller asserting facts about another
source re-opens the caller-owned-authority pattern hqu.26 sealed
away. Boundary tests extended to prove imports resolve only via
authorization. Fallback if the plumbing ran deep: land everything
else, document the gap, no stopgap.

## 10. Hand-rolled `Unit.[Value]` deleted in favor of builtin `Unit`

Spirit's interface declared its own `Unit.[Value]` (one-variant enum
carrying nothing — a one-valued type) because the old schema language
had no builtin unit. The new pipeline's builtin `Unit` is isomorphic;
under replacement-kills the workaround dies. `Marker.Unit` and
`Version.Unit` now reference the builtin. **This deletes a
declaration from your authored source — review it.** (Also noted: the
migration corrected `Optional` to the builtin's `Option` spelling.)

## 11. `Integer` builtin mapped to `i64` — [assumption], review

The emitter needed a canonical Rust mapping for the `Integer`
builtin. The old pipeline was inconsistent: spirit used `u64`,
signal-spirit `i64`. Landed as `i64` tagged [assumption], per the
implementer's recommendation (signed default; unsigned wants a
domain-specific type, not the general builtin). Yours to confirm or
overturn. (Other builtin translations landed: `Unit → ()`,
`Boolean → bool`, `Vector → Vec`.)

---

# Morning status — where the night ended

**Landed, all suites green, everything pushed to main:** the Stream
section (5-section Interface) with the `Stream` universal trait and
role-trait generation across the whole train; `/` imports; the
observer golden fixture; signal-spirit AND meta-signal-spirit fully
migrated onto the authority-sealed pipeline (old batch API and old
generated code dead, cross-source imports resolving through staged
authorization); spirit's nexus/sema ethos sources rescued and
transcribed; emitter parity (derives, rkyv surface, Display/Error for
refusals, builtin translations) with all manual bridging killed;
deterministic source-digest freshness holding everywhere.

**Fires the moment you rule:**
- Observer vocabulary bodies (item 4) → signal-domain landing + the
  spirit observer interface.
- Per-verb wire payloads vs `Entry`+`Kind` (item 7) → spirit's
  nexus/sema generation through the pipeline.
- Stream initiation/termination mapping (item 8) → the runtime wiring.
- Then the handwritten daemon runtime (the ruled-handwritten layer) →
  your working spirit on the new ethos syntax.
