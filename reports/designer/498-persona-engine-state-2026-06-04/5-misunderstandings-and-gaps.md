---
title: 498.5 - What the psyche may have misunderstood, and what is missing
role: designer
variant: Audit
date: 2026-06-04
topics: [persona-engine, two-spirits, schema-stack, symbol-path, codec, misunderstanding, gaps, vision]
description: |
  Slice 5 of the state-of-the-engine assessment. A skeptic's pass over the
  gap between the psyche's apparent mental model (from recent intent and
  reports) and the actual state of the persona engine. Each potential
  misunderstanding is stated as [apparent assumption] vs [reality] grounded
  in source and record numbers; plus a missing-from-vision list. Honest and
  precise — this is the psyche asking to be corrected.
---

# Slice 5 — misunderstandings and gaps

The psyche asked directly: are there things I might have misunderstood? I
went in as a skeptic, not a problem-inventor. Most of the recent intent is
in good shape and faithfully captured. The corrections below are real
divergences I could ground in source or in the record timestamps — not
manufactured doubt. I rank them by how much they would bite if left
uncorrected.

## The verdict in one paragraph

The largest live divergence is the SymbolPath one: the psyche's own latest
word (record 1586, 08:46:30) reopens the structured form *after* it had
been ratified flat (record 1577, 08:44:41) and *after* report 496
recommended confirming flat as canonical — the report and the latest record
point opposite ways, and report 496 has not yet absorbed 1586. The
two-spirits divergence is real and mostly understood, but two sub-points
are easy to miss: the rename (1588) is half-done (path renamed, package
identity not), and the production feature set the pilot must absorb is
larger and less decided than "port the removal thread" suggests — five of
those designs are themselves blocked on un-made psyche decisions. The
schema-stack maturity framing is mostly honest but two ratified items
(one-engine unification, the token model) are ratified-not-built, and the
dual-engine bug they fix is still on main. The lean/break-freely vs
protect-production pair does NOT conflict — the psyche already reconciled
it in 1579/1589. And a genuinely-missing item: nothing in the vision yet
designs *how* the pilot crosses over to become production, nor an
intermediate where they run the same contract.

## Potential misunderstandings — [assumption] vs [reality]

### M1 — SymbolPath: flat is NOT settled; your own latest record reopens structured

[Apparent assumption] The structured-vs-flat SymbolPath question was
resolved to flat, and report 496 asks you only to *confirm* the flat shape
as canonical (496 §"Decision 3", the brief's framing too).

[Reality] Your records cross. Record 1577 (Decision, dialed to Medium,
**08:44:41**) confirms flat and "clos[es] the structured
component-plane-variant-payload-field record alternative *for now*." But
record 1586 (Decision, Zero, **08:46:30** — two minutes *later*) says
[Psyche wants to try the structured SymbolPath form — a record of
component, plane, variant, payload, field — as the fully qualified symbol
identity, rather than the landed flat vector of names. Prototype it in
actual code to show what it looks like before confirming the canonical
shape] (record 1586). Report 496, written this morning, recommends
confirming flat and "clos[ing] the structured-record alternative" — which
runs against 1586's "prototype the structured form before confirming." The
built code is flat (`schema-next/src/asschema.rs:86`,
`pub struct SymbolPath(Vec<Name>)`); no structured prototype branch exists.
Note 1586 sits at Zero certainty — but Zero here is almost certainly an
artifact of the 08:46:30 recalibration batch (1578/1581/1582/1584/1586 all
landed Zero in the same instant, and report 497 only documents zeroing
1589/1590 as duplicates), not a deliberate retraction of the prototype
ask. **The correction you most need: flat is the *landed* shape, not the
*decided* shape — your last word asked for a structured prototype first.**
This is a one-line decision for you: is 1577 (confirm flat, close
structured) or 1586 (prototype structured before confirming) the standing
order? Designer 492 §B.5 had earlier proposed the five-segment structured
path as canonical, so the structured idea has lineage; it is not a new
whim.

### M2 — The two Spirits are understood as two, but the rename is half-done and the package still says spirit-next

[Apparent assumption] Record 1588 renames spirit-next → spirit and that
rename is essentially a naming cleanup that has happened.

[Reality] The rename is *half* applied. The filesystem checkout is renamed
— `/git/github.com/LiGoldragon/spirit-next` is GONE and the pilot now lives
at `/git/github.com/LiGoldragon/spirit` with the spirit-next commit history
— and `protocols/active-repositories.md:41` already describes it as the
renamed pilot with the stale concept repo retired. But the *package
identity* is still spirit-next: `spirit/Cargo.toml` reads `name =
"spirit-next"`, the library target is `spirit_next`, and the binary is
`spirit-next`. So the rename is path-done, identity-not-done — an
in-progress state, not a finished one. This is operator follow-up, not a
misunderstanding of intent; flagging it so you do not assume the rename is
complete when you next reach for the `spirit` binary (the deployed one is
still the *production* `spirit` CLI from persona-spirit; the pilot binary is
`spirit-next`). Separately, the old stale concept-track `spirit` repo the
record says to delete is already retired from the active map, but
`design-deep-spirit-2026-05-26` — a frozen-since-May-26 *third*
designer-parallel deep Spirit implementation — still exists on disk
(`/git/github.com/LiGoldragon/design-deep-spirit-2026-05-26`, last commit
2026-05-26). It is not the repo 1588 names, but it is a third spirit
codebase that can muddy "which Spirit" — worth an explicit abandon
decision (slice 1 owns the disposition).

### M3 — The pilot must absorb a production feature set that is larger AND less-decided than "port the removal thread"

[Apparent assumption] The schema pilot (now `spirit`) lacks the production
removal-candidates / variant-ladder / privacy thread, and absorbing it is
mostly a porting exercise once you say go.

[Reality] Two corrections. First, the gap is concrete and large: the pilot
schema (`spirit/schema/lib.schema`) has **zero** occurrences of
removal/collect/recorddefault/recency/recordedtime/archivetarget
vocabulary; the production contract (`signal-persona-spirit/spirit.schema`)
has 13. The pilot *does* carry `Privacy` on its `Entry`
(`lib.schema:89`, `Entry { Topics * Kind * Description * Magnitude *
Privacy * }`) — so privacy is NOT entirely absent from the pilot, contrary
to the brief's "NONE of the privacy thread"; but it lacks
CollectRemovalCandidates, RecordDefault, the small-record/summary type, the
recency depth words, the output-target enum, and daemon-stamped time on
records. Second — and this is the part most likely to surprise you — those
production designs are themselves **not field-level decided**. System-designer
59 found all five blocked on psyche decisions you still owe:
CollectRemovalCandidates is Reading-A-vs-B (pure-extract vs fused
archive-then-retract — the deployed code is B, but 1547's "separates ...
from the destruction concern in Remove" reads toward A); the output-target
enum's Stdout/Stderr/Inline membership is open; the small-record field set
(does it carry privacy? which "magnitude"?) is open; RecordDefault's
defaulted-field partition is open; the tier-1 recency shortcut name set and
clock semantics are open
(`reports/system-designer/59-design-to-implementation-audit-2026-06-04/1-spirit-production-triad-gap.md`).
**The correction: the pilot cannot "become production Spirit" by porting,
because the thing it would port is itself a pile of un-made decisions. The
production daemon shipped one reading (B, etc.); the pilot would have to
either inherit those de-facto choices or re-litigate them.** This is the
real weight behind 1588 — renaming spirit-next → spirit does not make it
production; it inherits a feature debt whose top layer is undecided design.

### M4 — Two ratified schema-stack items are ratified-NOT-built, and the bug they fix is still on main

[Apparent assumption] The recently-ratified items (the triad runner
extraction 1574/1581, the RustItem token model 1576/1584, one-engine
lowering 1572/1578) are landed, and the dual-engine bug report 496 named is
the one remaining defect.

[Reality] Per the landed-means-main rule you elevated (record 1568,
VeryHigh), these are *ratified intent*, not *landed code*. The one-engine
unification is not built: `schema-next/src/engine.rs` still carries both
`lower_source` (registry path) and the typed `SchemaSource::lower` path,
and the bug itself — `declarative.rs:1849`, `payload: None` on the registry
path that silently drops the namespace lookup — is still present on main.
The RustItem token model is ratified (1584) but `schema-rust-next` still
builds ~80% of its output through `self.line(format!(...))` with
hand-counted indentation (496 §"Decision 2"). The triad runner is ratified
in *shape* (1581) but not extracted — `spirit`'s daemon still hand-writes
the accept loop. **The correction is a calibration one: the schema stack is
in good shape on the *design* axis (your intent is captured, clean, and
mostly faithfully implemented for the older thread), but the three newest
ratifications are forward-looking operator work, not done. If your mental
model is "ratified = the stack now has this," dial it to "ratified =
operator's next targets."** This is not a criticism of the operator — the
last session froze right after these landed as intent; it is a status
correction so the psyche-report does not overclaim.

### M5 — schema-as-its-own-codec and sugar syntax are emerging, NOT proven

[Apparent assumption] schema-as-its-own-codec (1573) and the shorthand
sugar / bare-name header syntax are implemented and dependable.

[Reality] You already half-caught this yourself: record 1591 says [Do not
assume schema sugar syntax has really been implemented; audit and prove the
sugar syntax before depending on it] (record 1591). Reading the source
confirms the caution is warranted. A one-way *emit* path exists —
`schema-next/src/source.rs` has `to_schema_text()` and `into_source()`, so
typed schema can render back to authored text — but a proven full
round-trip (authored text → typed → identical authored text) that would
make schema genuinely "its own codec" per 1573 is not witnessed. And the
bare-name header resolution, while implemented and consumed by the pilot's
`lib.schema` header, is exactly where the dual-engine bug lives: the
registry lowering path drops the header payload (M4). **The correction:
treat the codec/sugar direction as a ratified destination with a partial,
not-yet-witnessed implementation — which is precisely what 1591 already
tells you. Nothing here contradicts your model; it confirms the skepticism
1591 expressed was the right instinct.**

### M6 — The lean/break-freely and protect-production pair does NOT conflict (a non-finding, stated to reassure)

[Apparent assumption] There might be a quiet conflict between
[value lean ... do not fear breaking things ... breaking freely in
development is what development is for] (record 1579, Maximum) and the
protect-production stance.

[Reality] There is no conflict; you already reconciled it in the records
themselves. 1579 scopes breakage to development explicitly ("Breakage
belongs in development, not production"), and 1589 restates it as [Prefer
lean and correct development architecture over preserving breakage-free
development compatibility; breaking development surfaces is acceptable
while production remains protected] (record 1589). The two-deploy-stack
discipline (production persona-spirit deployed; pilot `spirit` free to
break) is the structural embodiment of exactly that split. I checked this
specifically because the brief flagged it as a candidate tension; it is
not one. Stated here so the psyche-report can affirm the pair is coherent
rather than leave it as an open worry.

### M7 — "most-correct wins" and "schema-as-its-own-codec" do not conflict either

[Apparent assumption] The one-engine "keep the most-correct lowering, even
if larger" direction (1572/1578/1580) might pull against the
codec-round-trip direction (1573).

[Reality] They compose. 1578 names them together in one record: [keep the
single most-correct lowering ... The retained engine should make schema its
own codec — the shorthand source form round-trips through the schema codec]
(record 1578). Most-correct selects *which* of the two current engines
survives; codec-round-trip is a *property* the survivor must have. They are
a sequence, not a tension. Non-finding, stated for completeness.

## Missing from the vision — not designed at all

These are genuine holes: things the whole-engine vision implies but that
have no design, not merely unbuilt designs.

1. **The cutover mechanism itself.** INTENT.md §"Two deploy stacks coexist"
   says production persona-spirit and the pilot run side by side until
   cutover, and 1588 wants the pilot to *become* Spirit. But there is no
   design for *how* the switch happens: no contract-equivalence gate (a
   test that the pilot's wire contract matches production's before cutover),
   no data-migration path for the live redb store from the hand-written
   schema to the schema-emitted one, no rollback story. "Rename
   spirit-next → spirit" is a naming act; the actual production-replacement
   act has no designed steps. This is the single biggest hole.

2. **A shared signal contract the two Spirits provably agree on.** Today
   the production contract (`signal-persona-spirit/spirit.schema`, 8 roots +
   2 injected verbs) and the pilot contract (`spirit/schema/lib.schema`)
   are independently authored and have diverged (the production removal
   thread; the pilot's leaner Entry). Nothing forces them to converge, and
   nothing measures the gap. The vision wants ONE Spirit; the path needs an
   intermediate where both daemons answer the *same* contract.

3. **meta-signal-<component> for the pilot.** The triad is daemon +
   signal-<c> + meta-signal-<c> (the owner-only policy contract). Production
   has the signal contract; I found no `meta-signal-spirit` /
   `meta-signal-persona-spirit` policy contract in the pilot at all, and the
   policy-signal leg of the triad is thin-to-absent across the engine. The
   vision names a three-legged triad; the third leg is largely undesigned.

4. **Help/description namespace (1493) and NOTA config-by-convention
   (1494).** System-designer 59 found both are pure design with no emitter,
   no resolver, no SymbolPath-keyed description store. These are named in
   intent and in designer 492's ratification queue, but no field-level
   shape exists — they block on the psyche picking storage homes and
   humanization rules.

5. **The generated `TraceEventFrame` last-mile.** The only hand-written
   trace code left in the pilot is a 12-line rkyv round-trip impl repeated
   per component (`spirit/src/trace.rs`). The "shrink the per-component
   adapter to zero" intent is named but the mechanism (derive macro vs
   schema-rust-next emission vs blanket impl) is undecided — a small but
   real undesigned slot.

## What this slice did NOT find (honesty about the bar)

I did not find evidence that the psyche thinks the schema stack is
production-ready — the framing across 492/496 is consistently "pilot
proving the path," which is correct. I did not find a misunderstanding in
the engine-trait / trace / SEMA-single-writer story; those are genuinely
ahead of where reports assumed (system-designer 59 §2 documents the pilot
being *ahead* of the brief snapshot on the runtime axis). And I did not
find the lean-vs-production conflict the brief asked me to probe (M6). The
real corrections are M1 (SymbolPath crossed records), M3 (the production
feature set is undecided, not just unported), and M4 (ratified ≠ built) —
in that order of bite.
