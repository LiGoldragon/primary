# Costume Trait Fingerprint

Research directed by the psyche, design session `2b34fafa`, 2026-08-20.
Evidence-only. Observations, hypotheses, and unknowns kept separate.

---

## 1. The Rejected Instance (verbatim)

From the design-session transcript (`2b34fafa-afcf-43c5-a8d3-385c8ea7f134.jsonl`,
line 525, role=assistant, 2026-08-20T12:03:39Z), the Designer proposed
the following trait sketch immediately before the psyche's correction:

```rust
// -- Traits: the capabilities of textual code --------------------------

/// A manifest resolves a name to a source -- or errors. No fallback (ruled).
trait Resolving {
    fn source(&self, name: &SourceName) -> Result<&Source, ResolveFault>;
}

/// A source yields one of its files by path. `None` file = lib.es (ruled).
trait FileYielding {
    fn file(&self, path: &FilePath) -> Result<File, SourceFault>;
}

/// Ruled pair -- the text realizes, the real textualizes. Never the same type.
trait Realize    { type Real;    type Fault; fn realize(&self) -> Result<Self::Real, Self::Fault>; }
trait Textualize { type Textual;             fn textualize(&self) -> Self::Textual; }

/// An import reference resolves to the types it names, given the manifest.
trait ReferenceResolving {
    fn referents(&self, manifest: &Manifest, own_dir: &FilePath)
        -> Result<Vec<TypeName>, ResolveFault>;
}
```

The psyche's correction (verbatim, from `psyche/Vision/traitsAsCapabilities.md`
2026-08-20, same session):

> "You misunderstood the trait based approach. your trait methods are
> just regular functions pretending to be traits. if the type needs a
> 'name' to resove the import, then it's not resolvable. So we found
> one of the cornerstone of models not understand my vision. Do a
> research in this"

The shortened form logged in `psyche/Vision/importResolution.md` 2026-08-20:

> "if the type needs a 'name' to resove the import, then it's not
> resolvable."

("resove" is the psyche's typing of resolve.)

The transcript ends with a `turn_duration` system event (line 526) and an
`away_summary` (line 527). The psyche's typed correction is captured in the
psyche log, not in the JSONL file directly.

---

## 2. The Fingerprint

### Diagnostic A: the capability subject is in a parameter, not the receiver

**Statement of the diagnostic.** A trait method that must receive the subject
of the capability as a parameter is a free function wearing a trait. The type
holding the capability is not the type that *is* the thing the capability
operates on.

**Evidence from the rejected instance.**

`ReferenceResolving::referents(&self, manifest: &Manifest, own_dir: &FilePath)`:
Self is `ImportReference`. The import reference holds a `source: SourceName`
and the types it pulls. To resolve, it needs `manifest` and `own_dir` handed
in -- the entire infrastructure for performing resolution. Stripping the trait
wrapper yields a free function `referents(r: &ImportReference, manifest:
&Manifest, dir: &FilePath)`. Nothing is lost. The trait adds no capability
to the type; it only moves an argument position.

`Resolving::source(&self, name: &SourceName)`: Self is `Manifest`. The
manifest does not resolve a `name`; it is the lookup table, and the name
is the subject being resolved. Agent interpretation: the psyche's diagnostic
"if the type needs a 'name' to resove the import" most directly describes
this form -- handing `name` into the manifest as a parameter rather than
making the name-carrier (the `ImportReference`) the receiver.

`FileYielding::file(&self, path: &FilePath)`: Self is `Source`. The path is
handed in to select a file. The capability subject (a particular file at a
path) lives in the parameter.

**Conforming cases in protos.**

`Realize::realize(&self)`: No parameters beyond `self`. Self IS the textual
form; it realizes into `Self::Real` without needing any subject handed in.
The capability is wholly carried by the receiver.

`Textualize::textualize(&self)`: Same structure. Self is the real form; it
textualizes itself. No external subject parameter.

**Boundary: legitimate parameters.**

Not every parameter disqualifies a trait. The diagnostic is about the
capability *subject*, not any parameter.

- `Walk::enter(&mut self, shape: Shape, span: Range<usize>)`: `shape` and
  `span` are data about the block being entered -- the event's payload. The
  capability subject is the walker advancing its own state. Conforming: the
  walker is the receiver and the subject.

- `SourceSlicing::source_slice(&self, span: Range<usize>)`: `span` is a
  query parameter that narrows the operation. The source's capability is
  "I can be sliced"; the span selects what slice. The source IS the subject.
  Conforming.

- `RealizeScoping::realize_body<F>(&mut self, dialect: &mut F)`: `dialect`
  is a behavioral callback (closure) directing what to do with each block.
  The scope IS the subject of "realize scoping." The callback is a
  cooperating agent, not the subject. Conforming.

- `RealizeDriving::realize_blocks(&mut self, source: &SourceText)`: `source`
  is the input being processed. The driver's capability is driving
  realization; `source` is the material it drives over. Agent interpretation:
  conforming. Disconfirming consideration: one could argue `source` IS the
  subject (it is what gets realized), which would make this a borderline
  case. The driver does not become the source; it processes it. The
  distinction from `Resolving::source(&self, name)` is that the driver
  *is* the driving apparatus (it holds walker state), whereas a Manifest
  with a name-parameter is just a keyed lookup.

**Honest boundary summary (agent interpretation):** the fingerprint applies
when the parameter is infrastructure the receiver cannot provide -- the
resolver needs the manifest to do anything at all. It does not apply when
the parameter narrows or directs an operation the receiver can already
perform (query ranges, callbacks, event data).

---

### Diagnostic B: one type carrying many single-function traits is probably one trait

**Statement.** From `psyche/Vision/rustComponentArchitecture.md` 2026-08-17:

> "the problem isnt that it only has one implementor, but that many of
> those traits should be one. if one type implements a bunch of single
> function traits (or is that what you meant by one implementor), then
> all those traits are probably only one trait"

**Evidence in protos.** The ontological map (session `e4be1c4a`, captured in
`design/ProtosEngine/ontologicalMap-2026-08-18.md`) found: StructuralWalk
carries five private single-method traits (FrameFinishing, WalkAborting,
FaultFinishing, HistoryResetting, TransitionRecording) plus Walk and
WalkObserving. All five are internal machinery for one type. The map
proposes fusing them into `<<WalkMachinery>>`.

BlockScanner carries three private traits (Scanning, PrefixChecking,
DelimiterScanning), proposed to fuse into `<<BlockScannerMachinery>>`.

**Relation to the costume diagnostic.** This is a sibling failure, not
the same one. A costume trait wraps a free function. Fragmentation wraps
free functions *individually* across many single-function traits on one
type. Both violate the ontology-in-code principle; both produce placeholder
traits. They often co-occur.

---

### Diagnostic C: both directions of a transformation on the same type

**Statement.** From `psyche/Vision/traitsAsCapabilities.md` 2026-08-18:

> "realize isnt implemented by the same type as textualize. if you
> cant find two different types, the implementation is wrong. You
> dont textualize the text, and you dont realize the realized data."

**Evidence in protos.** The ontological map confirmed: datom and ethos
block-level types implemented both a DatomRealizing and DatomTextualizing
locally (or equivalent pairs), on the same type. This is a wrong
implementation by the psyche's ruling.

`design/ProtosEngine/sourceOntology-2026-08-18.md` identified the same
contradiction in the map's proposed `<<BlockRealizing>>` on the real type:

> "Current contradiction: The ontological map's <<BlockRealizing>> places
> `realize_block` on the real type (dialect types implement both realize
> and textualize directions). The ruling explicitly forbids this."

This diagnostic is distinct from A: it is not about where the subject lives
but about direction-pairing on one type. The receiver can be the correct
subject and still violate this rule.

---

## 3. The Register

### Protos public traits (30 currently; 24 proposed in ontological map)

| Trait | Key method signature | Subject location | Diagnostic A status | Notes |
|---|---|---|---|---|
| `Realize` | `fn realize(&self)` | Receiver | Conforming | Psyche-ruled |
| `Textualize` | `fn textualize(&self)` | Receiver | Conforming | Psyche-ruled |
| `ShapeDefined` | `fn select(shape: Shape, head: Option<&Head>) -> Option<Self::Selection>` | Class method | Conforming | Type IS the shape-defined thing; params are discriminators |
| `Walk` | `fn enter(&mut self, shape: Shape, span: Range<usize>)` | Receiver (walker state) | Conforming | shape/span are event data |
| `WalkObserving` | `fn observation(&self)` | Receiver | Conforming | |
| `CursorObserving` | `fn cursor(&self)` | Receiver | Conforming | |
| `RealizeDriving` | `fn realize_blocks(&mut self, source: &SourceText)` | Receiver (driver) | Conforming (borderline) | source is material being driven; see boundary discussion |
| `TextualizeDriving` | `fn textualize_blocks(&mut self, blocks: &[Block])` | Receiver | Conforming (borderline) | same pattern |
| `RealizeScoping` | `fn realize_body<F>(&mut self, dialect: &mut F)` | Receiver (scope) | Conforming | dialect is a callback |
| `TextualizeScoping` | `fn textualize_block<F>(&mut self, shape, head, dialect)` | Receiver (scope) | Conforming | shape/head are block descriptor; dialect is callback |
| `BlockScanning` | `fn blocks(&self)` | Receiver | Conforming | |
| `Headed` | `fn head(&self)` | Receiver | Conforming | |
| `StringCarrying` | `fn textual_body(&self)` | Receiver | Conforming | |
| `SourceSlicing` | `fn source_slice(&self, span: Range<usize>)` | Receiver | Conforming | span is a query parameter |
| `FrameObserving` | `fn identity(&self); fn shape(&self); fn position(&self); fn span(&self)` | Receiver | Conforming | |
| `IdentityObserving` | `fn ordinal(&self)` | Receiver | Conforming | |
| `ParentObserving` | `fn frame(&self); fn position(&self)` | Receiver | Conforming | |
| `TransitionObserving` | 5 accessors, all `(&self)` | Receiver | Conforming | |
| `ObservationViewing` | 5 accessors, all `(&self)` | Receiver | Conforming | |

Private traits in protos (all implemented by StructuralWalk or BlockScanner):

| Trait | Status | Diagnostic |
|---|---|---|
| `FrameFinishing`, `WalkAborting`, `FaultFinishing`, `HistoryResetting`, `TransitionRecording` (on StructuralWalk) | Proposed to fuse into `<<WalkMachinery>>` | Diagnostic B: fragmentation |
| `Scanning`, `PrefixChecking`, `DelimiterScanning` (on BlockScanner) | Proposed to fuse into `<<BlockScannerMachinery>>` | Diagnostic B: fragmentation |
| `BlockRendering` (on Block, private) | Proposed to vanish | Diagnostic B |
| `ShapeHeading` (on Shape, private) | Proposed to vanish | Diagnostic B (exists only because of Shape/head redundancy) |
| `DriverFailing` | Stays | Conforming |

### Rejected proposal traits (from 2b34fafa transcript)

| Trait | Key method signature | Subject location | Diagnostic |
|---|---|---|---|
| `Resolving` | `fn source(&self, name: &SourceName)` | Parameter (`name`) | A: name is the subject being resolved; Manifest is a lookup table |
| `FileYielding` | `fn file(&self, path: &FilePath)` | Parameter (`path`) | A: the particular file is the subject; Source is its container |
| `ReferenceResolving` | `fn referents(&self, manifest: &Manifest, own_dir: &FilePath)` | Parameter (`manifest` provides all resolution capability) | A + free-function equivalence |

Note: `Realize` and `Textualize` in the proposal are the psyche-ruled pair.
They conform; the Designer correctly reproduced their signatures.

### Design docs (`ontologicalMap-2026-08-18.md`, `sourceOntology-2026-08-18.md`)

Proposed new conforming traits (agent assessment against diagnostic A):

| Proposed trait | Signature (abbreviated) | Assessment |
|---|---|---|
| `<<BlockRealizing>>` | `fn realize_block(&self, scope: &mut RealizeScope)` | Borderline: scope is context. sourceOntology notes this should be on the textual side (Block-in-context), not the real type -- violates Diagnostic C if on real type |
| `<<BlockTextualizing>>` | `fn textualize_in(&self, scope: &mut TextualizeScope)` | Conforming: self IS the real type textualizing into scope |
| `<<ArtifactFreshness>>` | `assert_matches_existing, write_to, pending_path` | Conforming: artifact is the receiver and subject |
| `<<CargoSourcePublishing>>` | `publish, dependency_source_dir, emit_rerun` | Conforming |
| `<<PathDeriving>>` | 6 path join methods | Conforming |
| `ScopedRealizing<Ctx>` (sourceOntology proposal) | `fn realize_scoped(&self, ctx: &mut Ctx)` | Conforming: Block (textual) is the subject; ctx is a context parameter |

Violating trait in design docs:

`<<BlockRealizing>>` on real types (ontologicalMap, section 4A) -- violates
Diagnostic C (both directions on one type). `sourceOntology-2026-08-18.md`
identifies this explicitly as a contradiction and proposes the fix: scoped
realize moves to Block-in-context.

---

## 4. Unknowns and Open Questions

**Unknown: the exact entry point of the psyche's diagnostic.** The correction
names both `Resolving::source` (the "name" wording) and `ReferenceResolving`
(the fuller correction in traitsAsCapabilities.md). The psyche's short form --
"if the type needs a 'name' to resove the import, then it's not resolvable" --
could refer to: (a) `ReferenceResolving` needing the `SourceName` it holds
internally plus the manifest, (b) `Resolving` needing a `name: &SourceName`
parameter, or (c) both. The report presents evidence for both; the boundary
between them is agent interpretation.

**Unknown: the correct shape for import resolution.** The psyche ruled
against the rejected sketch and directed research; no alternative trait
design for resolution has been approved. What a genuinely resolvable
`ImportReference` looks like -- if "resolvable" means capable without
external manifest context -- remains undesigned. A different reading is
that resolution is not a capability on ImportReference at all; it belongs
to a resolution context type that the psyche has not named.

**Unknown: whether `RealizeDriving::realize_blocks` conforms cleanly.**
It takes `source: &SourceText`. The driver IS the driving apparatus; the
source is the material. But if the source is understood as the capability
subject (the thing being realized), the trait has the same shape as
`Resolving::source`. Agent interpretation holds it as conforming because
the driver holds its own state and the source is an input -- not the same
as a lookup table receiving a lookup key. Confidence: moderate.

**Unknown: the scope of "regular functions pretending to be traits."** The
psyche's correction is direct but does not enumerate which of the three
proposed traits triggered it. The most egregious case is
`ReferenceResolving` (the manifest and own_dir hand in all the machinery).
Whether `Resolving` and `FileYielding` are also violating by the psyche's
reading, or whether they are merely placeholder names waiting to be
reconsidered, is not determined by the evidence.

**Unknown: whether `SourceSlicing::source_slice` is truly different from
`FileYielding::file`.** Both take a query parameter. Agent reading: the
difference is that `SourceSlicing` asks the source to slice itself
(the source contains the text), whereas `FileYielding` asks a source
to yield a particular file -- which could be read as the source acting
as a store, not as the capability-bearing entity. Not settled by psyche
words.

**Open: the positive design.** The psyche's ruling establishes what a
costume trait is; the positive form -- what genuine capability traits look
like for import resolution -- remains to be designed and approved.
