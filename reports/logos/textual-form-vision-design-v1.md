> SUPERSEDED (2026-07-17) by `textual-form-vision-design-v2.md`, which seats the
> psyche's four rulings answering this document's open joints: the tree/storage
> question closes as immaterial and decode becomes ordered first-match expectation
> enums with named transitional types (corrects §3, resolves DECISION 1); the
> TextualRust syn/prettyplease bypass of §6 is REJECTED and replaced by real per-type
> Rust textual-form data (resolves DECISION 2); §5.1's "NOTA is the base every language
> specializes" is CORRECTED to the proto-language framing (resolves DECISION 3); and
> component Input/Output objects with standard Version/Help variants are added. Read v2
> as the authority; this v1 remains the prior step.

# TextualForm / EncodedForm — the founding-vision design, seated and reconciled (v1)

Design-authority document. Session `LanguageEngine`, lane `TextualFormVisionDesign`,
Fresh, generalist, Opus 4.8 (1M), 2026-07-17. Read-only on every engine repo; this
file plus the small settled naming edits and tracker registrations are the lane's
only writes. The psyche does not read reports — the chat return is his surface; this
file is the agent pickup point.

## 0. Status, authority, and what this supersedes

Today the psyche restated a **founding vision** that the built system partially lost.
His words are the source of truth for this pass. This document seats that vision as
design authority and reconciles it against the delivered engine and the prior
authority `up-close-design-v1.md`.

**Authority lineage.** `up-close-design-v1.md` remains the reconciled code-level
design of the four-crate family and the logos→Rust lowering. This document **is the
new authority for the TextualForm / EncodedForm abstraction and the two side-data
organs** (the nametree and the structuretree). It **supersedes by reference** the
parts of `up-close-design-v1.md` that this reshapes:

```
[ (up-close-§6.1  the `TextualForm` trait  RESEATED here §2 — the trait now reads/writes
     the nametree and structuretree explicitly; the two organs are named)
  (up-close-§6.2  TextualRust as foreign-raw bypass  RECONCILED here §6 — trees-over-a-raw-layer,
     syn/prettyplease demoted to Rust's RAW LAYER under a structuretree)
  (up-close-§4.1/§4.3  AddressedStructuralTable  KEPT as the structuretree's flat STORAGE and
     addressing index; the tree the psyche named is the traversal view over it §3)
  keeps  up-close everything else (the crate split, the evaluator, the sequence algebra,
     the conformance triad, the phase order) unchanged ]
```

Identity authority is unchanged: `schema-unit-lineage-design-v2.md` (the two laws).

**Provenance markers.** **[psyche verbatim]** = his exact words today; **[ruling]** =
a settled psyche decision (today or a prior bead); **[observed — cite]** = a code fact
at `file:line` from the `SyntaxSideDataReview` map or a sibling report; **[reconciled]**
= this document's design move; **[DECISION n]** = a tension I cannot resolve from the
verbatim words and existing rulings, collected in §9 for the manager (never asked of
the psyche directly).

## 1. The founding vision, verbatim

The complete source-of-truth statement, recorded faithfully and never silently
resolved where it leaves something open:

- **[psyche verbatim]** "I had a great vision for a shared abstraction around
  textualform and encodedform (use to be called true/core)"
- **[psyche verbatim]** "The vision had associated data-tree (which we thought
  belongs in the textualform) to drive most of the structural encoding/decoding of
  the text."
- **[psyche verbatim]** "a nametree and a structuretree"
- **[psyche verbatim]** "textualform trait writes and reads the name and structure
  trees"
- **[psyche verbatim]** "this drives all textual en/decoding, including rust"
- **[psyche verbatim]** "actually, the vision even allowed multiple textualforms per
  encodedform; logos -> logos or logos -> rust"
- **[psyche verbatim]** "even nota can take this architecture; it would be the
  basic/most-universal example."

Adjacent rulings settled today, treated as fixed constraints:

- **[ruling]** The two ways to see a language are named **TextualForm** and
  **EncodedForm** (supersedes the hedge on `primary-56d1.37`; `EncodedForm` names the
  *view*, not the types — `Core*` type prefixes stay per `.25`).
- **[ruling]** Nomos gets a structural table so **plain raw NOTA decodes into macros
  first**, with the dollar-sigil / double-angle template spelling coming later as a
  **second form** ("we can do that").
- **[ruling]** NOTA is the textual carrier for everything we author; foreign formats
  (JSON/YAML/TOML) exist only as **boundary exports** for systems we did not write.
- **[ruling]** The old-stack byte-comparison is retired; the bar is **working
  programs**.

Two laws are inviolable in every option below (`schema-unit-lineage-design-v2.md` §1):
**rename touches one row and no value**, and **side-data never enters identity**.

## 2. The trait contract — TextualForm reads and writes the two organs

**[psyche verbatim]** "textualform trait writes and reads the name and structure
trees" and "this drives all textual en/decoding."

A **TextualForm** is one textual mouth of an **EncodedForm** (a stringless Core
value family). It owns nothing about meaning; it owns the two-way bridge between text
and Core, and it drives that bridge entirely from two side-data organs:

- the **nametree** — the identifier space (delivered flat as `NameTable`), which the
  form **reads** on encode (resolve identifier → spelling) and **writes** on decode
  (intern spelling → identifier);
- the **structuretree** — the type-directed structural shapes (delivered flat as
  `AddressedStructuralTable`), which the form **reads** to drive every structural
  encode/decode, and which is **assembled/written** when a language is given a mouth
  (§5).

```rust
/// One textual rendering of an EncodedForm. Every textual encode/decode in the
/// family is driven by the two organs — no bespoke per-form parsing/printing code
/// beyond the raw layer and the leaf codecs the structuretree names.
pub trait TextualForm {
    /// The stringless Core value family this form is a mouth of (the EncodedForm).
    type Encoded;

    /// The raw layer: NOTA-family forms share the Recognizer; a foreign form
    /// (Rust) supplies its own reader/printer. The raw layer NEVER classifies
    /// meaning — it only discovers/serialises glyph structure (§6).
    fn raw_layer(&self) -> &RawLayer;

    /// The structuretree this form owns — the type-directed structural shapes
    /// (delivered `AddressedStructuralTable`), READ to drive decode/encode.
    fn structuretree(&self) -> &StructureTree;

    /// text + expected type at the boundary  →  Core value.
    /// WRITES the nametree (interning); READS the structuretree.
    fn decode(&self, expected: ScopedCoreTypeId, text: &str, names: &mut NameTree)
        -> Result<Self::Encoded, DecodeError>;

    /// Core value  →  canonical text.
    /// READS the nametree (resolving); READS the structuretree.
    fn encode(&self, core: &Self::Encoded, names: &NameTree) -> Result<String, EncodeError>;
}
```

**[reconciled] The nametree is a shared organ; the structuretree is owned per form.**
The psyche named "a nametree and a structuretree" as a pair, and the trait reads and
writes both. But the two are not symmetric in ownership, and the difference is forced
by a ruling, not chosen:

- The **structuretree belongs in the TextualForm** — **[psyche verbatim]** "associated
  data-tree (which we thought belongs in the textualform)." Each form owns its own
  structuretree; the schema form's shapes are not the Rust form's shapes.
- The **nametree crosses layers.** The delivered hand-off passes Core values plus the
  continuous `NameTable` and never the structural table
  [observed — `core-nomos/src/engine.rs` `Lowering { items, names }`]. So the nametree
  is a **shared organ the form reads and writes but does not own**; the form's decode
  interns into it and its encode resolves from it. This is recorded intentionally in
  §7 (help/layer-handoff), so a future reader does not read the asymmetry as a bug.

**Reconciling the organs with what exists — honestly.** The delivered organs are flat
keyed maps, not literal trees:

- `NameTable` — flat, continuous (`extend_from` preserves schema indices into logos),
  hash-excluded, one-row rename [observed — `name-table`; `content_hash` drops `names`,
  `signal-sema-storage/src/lib.rs:280-309`].
- `AddressedStructuralTable` — flat, keyed by `ScopedCoreTypeId`, hash-excluded, its own
  co-versioned content identity [observed — `structural-codec/src/table.rs:66-129`].

The psyche said **trees** where the code has **flat keyed maps**. That is a genuine
open design question, not a loose word — see **[DECISION 1]** (§9). The recommendation
seated below is that the flat maps stay as *storage* and the *tree* he named is the
traversal the trait walks; **the two inviolable laws hold in every option**, so the
question is one of representation, not of behavior.

## 3. The two organs as trees — storage versus traversal

**[reconciled — recommended reading, DECISION 1]** The tree the psyche named is
**already present** in the delivered data; it is the *traversal shape*, not a second
storage shape.

- **The structuretree is a tree by construction.** A `StructuralForm` is recursive —
  `StructuralElement::{ Product, Application, Delimited(SequenceForm), Delegate, … }`
  [observed — `structural-codec/src/form.rs`]. A `Delegate(ScopedCoreTypeId)` edge
  points at another entry, so the closure of forms reachable by `Delegate` from a root
  type **is** a tree/DAG of structural shapes. The flat `AddressedStructuralTable`
  keyed by `ScopedCoreTypeId` is the **addressing index** into that tree — the array
  that lets the walk resolve a `Delegate` edge in O(1). "Structuretree" = the
  Delegate-closure of `StructuralForm`s rooted at a type; the flat table is how it is
  stored and entered, never a competitor to it.

- **The nametree is flat storage under a scope-structured view.** Names are genuinely
  flat and continuous, and must stay so: a flat continuous `NameTable` makes **rename =
  one row, value unchanged** trivially true, and identity-exclusion is a property of
  the Core value, not of the table's shape. The "tree" over names is the scope
  structure (universe → type → field) that the *structuretree already carries* through
  its `ScopedCoreTypeId` keys and field references. So the nametree-as-tree is a
  **view materialised on demand** from the structuretree's type graph, not a second
  store. This keeps the flat table's two-law guarantees intact and spends no new
  storage complexity.

**Why this dissolves the special case (design-quality gate).** If we made the organs
literal tree stores, rename and identity-exclusion would each need a fresh proof
against the tree shape, and we would carry two representations (the flat index the
evaluator needs for O(1) `Delegate` resolution, and the tree). Reading the tree as the
traversal over one flat store means there is exactly one representation, the two laws
are proved once, and "tree" and "table" are the same object seen two ways — the normal
case, with no side path.

```
;; the structuretree of the schema example, rooted at Struct, as a TRAVERSAL over the
;; flat AddressedStructuralTable (next-gen grammar; Delegate edges resolved by the index):
Struct
  └ Application( PascalCase-atom , Brace.Repeat(Delegate → Field) )
                                                    │
                                     Field ─────────┘   (two ConstructorCodecs)
                                       ├ TypeOnly : PascalCase-atom
                                       └ Named    : camelCase-atom . PascalCase-atom
```

## 4. Cardinality — one EncodedForm, many TextualForms

**[psyche verbatim]** "the vision even allowed multiple textualforms per encodedform;
logos -> logos or logos -> rust."

One EncodedForm is viewed through a **family** of TextualForms, each a full
`TextualForm` (its own structuretree + raw layer, sharing the nametree). The worked
example is `CoreLogos`:

```
                         EncodedForm = CoreLogos            (stringless Rust-as-data algebra)
                        /            |             \
             TextualLogos      TextualRust     TextualZig…    (sibling TextualForms, one family)
             (logos text)      (Rust text)     (future)
                 |                  |
           Recognizer raw      syn/prettyplease raw           (§6: each is trees-over-a-raw-layer)
```

- **TextualLogos** and **TextualRust** are **siblings over one EncodedForm** — the
  psyche's "logos -> logos or logos -> rust." Both are structuretree-driven; they
  differ only in which structuretree they own and which raw layer sits beneath the
  leaves. TextualLogos does not exist today and TextualRust bypasses the structuretree
  today [observed — review §4, §5]; §6 reconciles both.
- A **third emission language** is a third TextualForm — data plus custom leaves, the
  kernel unchanged (`up-close-§6.3`).

**Foreign-format boundary exports are projections off the EncodedForm, outside the
family.** **[ruling]** NOTA is the carrier for everything we author; JSON/YAML/TOML
exist only as boundary exports for systems we did not write. A JSON export is **not a
TextualForm**: it does not round-trip through the nametree/structuretree discipline
and is not required to be a two-way mouth. It is a one-directional (or lossy)
**projection of the EncodedForm** for a foreign consumer, housed outside the family:

```
   EncodedForm = CoreX ──[ TextualForm family: NOTA-carrier mouths, two-way ]── TextualX, TextualRust, …
                    └────[ boundary projections, OUTSIDE the family, one-way ]── JsonExport, YamlExport, …
```

No such export exists in code today [observed — review §5: no serde/json/yaml/toml
anywhere], and none is required by the PoC; this seats where one would live if a
foreign system ever needs it.

## 5. NOTA as the base instance, and the give-a-language-a-mouth operation

### 5.1 NOTA is the basic, most-universal pair

**[psyche verbatim]** "even nota can take this architecture; it would be the
basic/most-universal example."

The base pair is **raw NOTA text ↔ encoded positional records**: the most universal
TextualForm/EncodedForm pair, with the **empty (identity) structuretree**. Raw NOTA
text decodes to positional records (NOTA's own `Block`/record data) with a
pass-through structuretree — no type-directed shapes, only the raw layer's positional
discovery. Every richer language **specializes** this base by *adding structuretree
entries* that map its named Core types onto those positional shapes, plus a richer
EncodedForm; the base is the structuretree-empty degenerate case
[reconciled — this reading of "specializes" is a lean; see **[DECISION 3]**].

```
[ (base    TextualForm = raw NOTA text   EncodedForm = positional records   structuretree = ∅ (identity))
  (schema  + structuretree { Struct, Field, Newtype … over CoreSchema })
  (nomos   + structuretree { MacroDefinition, InputSignature, Escape … over CoreNomos })
  (logos   + structuretree { CoreItem kinds over CoreLogos }, and a sibling TextualRust) ]
```

This is why "even nota can take this architecture": NOTA is the family member whose
structuretree is empty, so the machinery is exercised at its simplest and every other
language is the same machinery with a non-empty structuretree.

### 5.2 Give-a-language-a-mouth: the general operation

Giving a language a mouth is the general operation of **assembling a TextualForm's
structuretree over an EncodedForm**. It already exists, concretely, at the schema
layer: `core-schema/src/document.rs:184-208` assembles `entries` and calls
`AddressedStructuralTable::seal(revision, payload)` [observed — review §Deliverable 3].
Under the trait, that assembly is the reusable act — *"build the structuretree that
maps each Core type of this EncodedForm to its structural form, seal it, hand the
sealed tree to a `TextualForm`."* Schema is the first instance; the operation is not
schema-specific.

### 5.3 The Nomos instantiation — the first new instance (implementation slice, not built here)

**[ruling]** Nomos gets a structural table so **plain raw NOTA decodes into macros
first**; the `$` / `<<>>` template spelling comes later as a **second form**.

The first new mouth is a **raw-NOTA door into CoreNomos**: assemble a structuretree
over `CoreNomos` (`MacroDefinition { name, kind, input, template }` and its parts
[observed — `core-nomos/src/definition.rs:13`]) so that plain raw NOTA text decodes
into a real macro value. The **candidate witness is the newtype-wiring macro**
(`WireNewtype`), authored in Rust today [observed — `core-nomos/tests/pipeline.rs:522-548`:
`InputSignature { name.Name, type.Type }`, `MacroKind::Structural(Newtype)`, a
`ResultTemplate::Item(Newtype{…})` of `Escape::Realize`/`Escape::Invoke`]. The door
must decode raw NOTA into a `MacroDefinition` **equal to the Rust-built `WireNewtype`**.

The escapes are the crux of "plain NOTA first, `$` later": the base door spells an
escape as an **ordinary positional named record**, not a sigil. `Escape::Realize(type)`
is written `Realize.type`; the richer second form later spells the same thing `$type`.
Both decode to the identical `CoreNomos` value — a clean instance of one EncodedForm
(CoreNomos) with two TextualForms (plain-NOTA base, `$`/`<<>>` richer sibling).

**Next-gen grammar, plain-NOTA door** (glued-dot binding, `{}` struct, `()` payload,
`[]` vector — the next-gen rules the `NotaGrammarUnification` lane is settling):

```
WireNewtype.(
  Structural.Newtype
  { name.Name type.Type }
  Item.Newtype.{ visibility.Public wrapped.Realize.type } )
```

Decodes (structuretree over CoreNomos, expected type `MacroDefinition` at the boundary)
to a value equal to the Rust-built `WireNewtype`. `Realize.type` is the plain-NOTA
carrier of the escape; the later `$`-form spells the same field `$type`.

**Hard dependency — do not implement yet.** The `NotaGrammarUnification` lane is
actively rewriting the NOTA substrate. The Nomos door must be **cut into the unified
grammar**, not the legacy one (two live grammars still coexist — legacy space-and-`*`
vs next-gen glued-dot [observed — review §1]). This slice **blocks on**
`NotaGrammarUnification` landing; every example above is written in next-gen grammar
so it lands directly on the unified substrate. Registered as a tracker item (§8).

## 6. Rust reconciled — trees over a raw layer, syn/prettyplease demoted

**[psyche verbatim]** "this drives all textual en/decoding, including rust."

Today TextualRust is the one form that **bypasses the structuretree**: it is
`syn`-on-decode / `prettyplease`-on-encode with no `AddressedStructuralTable` reference
[observed — review §5; `up-close-§6.2` designed it as a deliberate foreign-raw bypass].
That bypass is exactly the special case the vision says must not exist.

**[reconciled] Every TextualForm is trees-over-a-raw-layer, Rust included.** The
uniform shape is: a **structuretree** drives the type-directed structure (which
construct, which shape, in what order), sitting **over a raw layer** that handles only
tokens/formatting at the leaves. For the NOTA family the raw layer is the shared
`Recognizer` (NOTA's raw reader — the **universal** raw layer). For Rust the raw layer
is **syn (decode) / prettyplease (encode)** — demoted from "the whole codec" to "the
leaf tokenizer/formatter beneath a structuretree." The structuretree maps `CoreLogos`'s
item kinds to Rust structural forms whose leaves are largely `LeafCodec::Foreign`
(syn/prettyplease-backed).

```
   TextualRust  =  structuretree (CoreItem kinds → Rust structural forms)     ← NEW: was absent
                     over
                   raw layer = syn (read tokens) / prettyplease (write tokens) ← KEPT: demoted to raw
```

**What this changes about the current deliberate bypass.** Today the CoreLogos→Rust
mapping lives in hand-written Rust match arms (`textual-rust/src/project.rs`, `read.rs`,
`codec.rs`). Under the vision that item-level mapping becomes **structuretree data**,
identical in kind to schema's — so help-printing (§7) and the family's uniformity apply
to Rust, and TextualRust stops being "the one with no table."

**What it costs — stated plainly.** TextualRust is byte-exact against real schema-rust
goldens today [observed — review §5; `textual-rust/tests/fixtures/PROVENANCE.md`;
153 items in `pipeline.rs`]. Re-seating a working, byte-exact path as
structuretree-driven is real work against something that already runs. Two facts bound
the cost:

- The bar is now **working programs**, not byte-exactness against the old stack
  **[ruling]** — so the re-seat is not required to preserve golden bytes as sacred,
  which relaxes the risk.
- Rust's grammar is vast; a *full* structuretree for all of Rust would re-implement what
  syn already does. The recommendation is a **shallow structuretree**: it names the
  item-level structure (the ~7 `CoreItem` kinds and their child slots) uniformly, and
  leaves everything below the item boundary to `Foreign(syn/prettyplease)` leaves. syn
  still does the heavy lifting; the structuretree earns uniformity and help without
  re-grammaring Rust. Pace and depth are **[DECISION 2]** (§9).

## 7. Help as a structuretree projection; the layer-handoff boundary recorded

### 7.1 Help printing is a projection of the structuretree

**[observed — review §Deliverable 3]** The structuretree **already holds every accepted
form**: `ConstructorCodec.decode_forms` is the set of disjoint accepted shapes per Core
constructor. **Nothing renders them** — help exists only as a legacy renderer over the
old source model (`schema-language/src/source.rs:3865-4028`); the new engine projects no
help.

**[reconciled]** Help/usage text is a **projection of the structuretree**, not a
separate authored artifact and not a port of the legacy renderer. A generic
`StructuralForm → usage-text` walk in `structural-codec` turns each constructor's
`decode_forms` into the shapes a human may write. It lives generically (the forms are
shared vocabulary), so **every** TextualForm — schema, Nomos, logos, and (after §6)
Rust — gets help for free from the same walk. This makes the structuretree earn a
second use beyond decode/encode, and it is the natural home because the tree already
*is* the enumeration of accepted shapes. Registered as a tracker item (§8).

### 7.2 The layer-handoff boundary is intentional

**[psyche verbatim]** "associated data-tree (which we thought belongs in the
textualform)." **[ruling / deliverable framing]** layers exchange only Core values plus
names.

The schema→Nomos→logos hand-off passes **Core values + the continuous nametree only**,
and **never the structuretree** [observed — `core-nomos/src/engine.rs` `Lowering { items,
names }`]. This is **intentional and correct**, recorded here so a future reader does not
read the structuretree's absence at the boundary as a bug:

- The structuretree is a **text-view** organ; it **belongs in the TextualForm** and does
  not propagate. Propagating it would re-introduce a text dependence into the layer
  hand-off that the identity law forbids ("Core never depends on text").
- The nametree **does** cross (continuous `extend_from`), because names are shared
  substance the next layer legitimately consumes. This is the asymmetry named in §2:
  the form **reads/writes the shared nametree** and **owns its structuretree**.

So each layer, when it needs a mouth, **assembles its own structuretree** (§5.2) over
the Core values it received; it does not inherit the previous layer's tree. Only schema
has a structuretree today [observed — review §Deliverable 3]; Nomos (§5.3) and logos are
the honest gaps, sequenced in §8.

## 8. Implementation slices (tracker items — registered, not implemented here)

Each slice below is registered under the epic `primary-56d1` so nothing in this design
lives only in prose. None is implemented in this pass (design-authority only).

1. **TextualForm trait seated over the two organs** — introduce the `TextualForm` trait
   (§2) reading/writing the nametree and structuretree, with `TextualSchema` re-expressed
   through it as the reference instance. Acceptance: schema round-trips through the trait
   with no behavior change; the two organs are the only drivers.
2. **Nomos raw-NOTA door (first new mouth)** — assemble a structuretree over `CoreNomos`
   so plain next-gen NOTA decodes `WireNewtype` into a `MacroDefinition` equal to the
   Rust-built value (§5.3). **Blocks on `NotaGrammarUnification`** (cut into the unified
   grammar). Acceptance: decode(next-gen NOTA) == Rust-built `WireNewtype`.
3. **TextualNomos `$`/`<<>>` second form** — the richer sibling TextualForm over the same
   `CoreNomos`, spelling escapes as `$name`/`<<name>>`; decodes to the same values as
   slice 2. Depends on slice 2. Acceptance: `$`-form and plain-NOTA form decode equal.
4. **TextualLogos** — the logos-text sibling over `CoreLogos` (does not exist today);
   structuretree over `CoreItem` kinds, Recognizer raw layer. Acceptance: logos text
   round-trips a `CoreLogos` value.
5. **TextualRust re-seated as trees-over-a-raw-layer** — shallow structuretree over
   `CoreItem`, syn/prettyplease demoted to the raw layer (§6). Gated by **[DECISION 2]**.
   Acceptance: Rust still emits working programs through the structuretree.
6. **Help as a structuretree projection** — generic `StructuralForm → usage-text` in
   `structural-codec` (§7.1); every TextualForm gets help from it. Acceptance: schema
   help renders from `AddressedStructuralTable` with no legacy renderer.
7. **Record the layer-handoff boundary as intentional** — the structuretree is text-side
   and does not cross layers; only Core + nametree do (§7.2). Documentation/decision
   record, ties to review Decision item 2.

## 9. Decision items for the manager (options + recommendation; not asked of the psyche directly)

**[DECISION 1] Tree versus flat keyed map for the two organs.** *Tension:* the psyche
said "a nametree and a structuretree" (trees); the delivered organs are flat keyed maps
(`NameTable`; `AddressedStructuralTable` keyed by `ScopedCoreTypeId`). His word is not
assumed loose. *Options:* (a) **keep the flat maps as storage; treat the tree as the
traversal view** the trait walks — structuretree = the `Delegate`-closure of
`StructuralForm`s over the flat index; nametree = a scope-structured view materialised
from the structuretree's type graph over the flat continuous `NameTable` (§3);
(b) **restructure storage into literal trees** — a scoped/hierarchical nametree and a
hierarchical structuretree registry; (c) **hybrid** — literal tree for the structuretree
registry, flat for names. *Recommendation:* **(a).** It carries one representation, not
two; the two inviolable laws (rename = one row, side-data excluded from identity) are
proved once against the flat store and never re-proved against a tree; and the tree the
psyche named genuinely exists as the recursive-form + `Delegate`-edge traversal, so (a)
honors his word without duplicating state. (b) spends storage complexity and re-opens
both law proofs for no behavioral gain; (c) is (a) with an unnecessary second shape for
the registry. All three preserve the two laws.

**[DECISION 2] Pace and depth of re-seating TextualRust as trees-over-a-raw-layer.**
*Tension:* the vision says the structuretree drives "all textual en/decoding, including
rust," but TextualRust already works and is byte-exact via a deliberate syn/prettyplease
bypass; the bar is now working programs. *Options:* (a) **re-seat now, shallow** — a
structuretree naming only the item-level `CoreItem` structure, all sub-item leaves
`Foreign(syn/prettyplease)`; (b) **re-seat now, deep** — a full Rust structuretree
(re-implements much of syn); (c) **defer** — keep the bypass until after the PoC port
(`.39`) proves the data path. *Recommendation:* **(a).** It removes the special case
(TextualRust stops being "the one with no table"), gives Rust help and family uniformity,
and keeps syn/prettyplease doing the heavy lifting at the leaves, so cost is a thin
structuretree layer, not a Rust re-grammar. (b) is large and duplicative; (c) leaves the
special case standing, which is precisely what the vision rejects — but (c) is the safe
fallback if slice 5 proves costlier than a shallow tree suggests.

**[DECISION 3] What "every richer language specializes" the NOTA base means precisely.**
*Tension:* "even nota … the basic/most-universal example" and "every richer language
specializes it" are clear in spirit but leave the specialization relation informal.
*Options:* (a) **structuretree-empty base** — NOTA is the family member with the identity
(empty) structuretree over positional records; a richer language = base machinery + a
non-empty structuretree + a richer EncodedForm (§5.1); (b) **subtype/inheritance** — a
richer EncodedForm is formally a subtype of positional records, with the base form
inherited; (c) **independent instances** — each language is its own TextualForm/EncodedForm
pair that merely happens to also be expressible as positional records, with no formal
"specializes" relation. *Recommendation:* **(a).** It is the reading that dissolves the
base into the normal case (one machinery, structuretree ranging from empty to rich) and
matches "even nota can take this architecture" — NOTA is the machinery at its simplest.
This is a **lean**, revisable if the psyche means a stronger formal subtyping (b).

## 10. Naming flip executed (settled mechanics) and tracker changes

- **`primary-56d1.37`** moved from hedged lean to **accepted**: the two ways to see a
  language are **TextualForm** and **EncodedForm**; `EncodedForm` names the *view*, not
  the `Core*` types (`.25`). Today's ruling is the evidence.
- **Doc-scoped naming edits** (settled TextualForm/EncodedForm vocabulary reads
  consistently): `up-close-design-v1.md` (§6 opening, the trait, the add-a-language
  block), `vision-evidence-ledger-v1.md` (L11/L13 rows and the many-forms row),
  `language-family-poc-epic-design-v1.md` (the hypotheses list and the many-form slice).
  Each points to this document as the new authority for the pair.
- **New tracker items** registered under `primary-56d1` for the §8 slices.

## 11. Validation scope

Design-authority only. No engine source, generated artifact, store, deployment, or
Spirit record was changed. Code and status claims are the `SyntaxSideDataReview` map and
sibling-report citations at the revisions that review recorded; ruling claims cite the
psyche's 2026-07-17 chat and the epic bead thread. Nothing here is accepted until the
psyche grades it; the design items in §9 are returned to the manager, never asked of the
psyche directly. This lane's writes are this file, the §10 naming edits, and the §8/§10
tracker registrations.
