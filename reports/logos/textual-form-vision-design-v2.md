# TextualForm / EncodedForm — founding-vision design, revision 2 (four rulings seated)

Design-authority document. Session `LanguageEngine`, lane `TextualFormVisionV2`,
Fresh (Recovery-inherited the live lane of the same task), generalist, Opus 4.8
(1M), 2026-07-17. Read-only on every engine repo; this file, the v1 supersession
stamp, and the tracker slice edits are the lane's only writes. The psyche does not
read reports — the chat return is his surface; this file is the agent pickup point.

## 0. What this revision is, and its authority lineage

`textual-form-vision-design-v1.md` (pushed today, commit `1e3339e23397`) seated the
TextualForm / EncodedForm trait vision, the two organs (nametree, structuretree),
and created epic slices `primary-56d1.40`–`.45`. The psyche has now answered the
three open joints v1 returned and added major new vision content. **This v2 is the
new authority for the TextualForm / EncodedForm abstraction.** It supersedes v1
section-by-section where marked below and keeps v1 readable as the prior step.

```
[ (v1-§2/§3   the trait + the two organs         KEPT, sharpened here §2; the tree question CLOSES §3)
  (v1-§5.1    NOTA-as-base-with-empty-tree        CORRECTED here §6 — the universal thing is the proto-language, not NOTA)
  (v1-§6      TextualRust = syn/prettyplease-as-raw-layer   REPLACED here §5 — the bypass is REJECTED; real per-type data)
  (v1-§7.1    Help = structuretree projection      RE-SCOPED here §4 — Help is a variant answerer, not a standalone printer)
  (v1-§9      DECISION 1/2/3                        RESOLVED by the psyche; superseded by the rulings here)
  keeps  v1 everything else (cardinality §4, the give-a-language-a-mouth operation, the layer-handoff boundary) ]
```

Upstream authority unchanged: `up-close-design-v1.md` (code-level four-crate
family), `schema-unit-lineage-design-v2.md` (the two identity laws). Identity laws
remain inviolable in every design move here: **rename touches one row and no value**;
**side-data never enters identity**.

**Provenance markers.** **[psyche verbatim]** = his exact words today; **[ruling]** =
a settled psyche decision seated as design; **[manager proposal]** = a framing the
manager floated in chat, seated here for validation, explicitly *not* psyche words;
**[reconciled]** = this document's design move; **[DECISION n]** = a tension not
resolvable from the verbatim words, collected in §8 for the manager (never asked of
the psyche directly).

## 1. Ruling 1 — what "tree" means; ordered expectation enums; transitional types

**[psyche verbatim]** "What I mean when I say a tree is just, it doesn't matter if
it's a vector... we would have these different enums of different kinds of structure
expectations based on different aspects of what that block can look like. There's an
order, right, because the first match is going to have to take precedence."

**[psyche verbatim]** "we have types that are not really fully resolved yet... they're
transitional types. So like this is, let's say this block is potentially X, Y, or Z.
So it's a potential such and such, and whatever name is most capable of representing
all of the different things that can be in that block is the right name. So there's
different levels of abstraction... there's what the thing turns out to be when it's
actually read all the way, and then there's what these blocks contain as an abstraction."

### 1.1 The storage question is immaterial and closes

v1's DECISION 1 asked flat keyed map versus literal tree for the organs. **[ruling]**
The word "tree" carries no storage commitment — "it doesn't matter if it's a vector."
So the question of whether the structuretree/nametree are stored flat
(`AddressedStructuralTable`, `NameTable`) or as literal tree nodes is **immaterial and
closes**. "Tree" names the *structure of expectations*, not a storage layout. The
delivered flat keyed maps stay as storage with no change and no apology; the two
identity laws stay proved once against them. v1 DECISION 1 is answered: representation
is free, and the flat maps are fine.

### 1.2 Decode is ordered expectation enums with first-match precedence

**[ruling]** The decode semantics are **ordered enums of structure expectations**,
one set of expectations per aspect of what a block can look like, and **the first
match takes precedence**. A block is decoded by walking its expectation enum in
declared order; the first expectation that matches wins. Order is load-bearing design
data, not an accident of iteration — it is authored per aspect.

This is the shape the reader's structuretree drives: for a given expected type at a
given block, the structuretree yields an *ordered* list of structure expectations
(the enum), and decode is first-match over that list.

### 1.3 The reader's type system has named transitional / abstraction-level types

**[ruling]** The reader is not a two-state machine (raw text → fully-resolved type).
It carries **named transitional types at multiple abstraction levels**. A block that
is "potentially X, Y, or Z" *has a type now* — a transitional type — and its name is
**whatever name is most capable of representing all of X, Y, and Z**. There are two
poles the design must name distinctly:

- **the fully-read type** — what the block "turns out to be when it's actually read
  all the way" (the leaf, resolution complete);
- **the abstraction type** — "what these blocks contain as an abstraction" before full
  resolution (the transitional node, named by maximal representational capability).

Design move **[reconciled]**: the reader carries a lattice of types from most-abstract
(maximally-capable transitional names) down to fully-read leaves. Each block is typed
at the highest abstraction level its resolution has reached; first-match ordered
expectations (§1.2) drive the block down the lattice toward its leaf. The naming rule
for a transitional type is fixed by the psyche: **maximal capability to represent the
block's possibilities.** (This is the same discipline `up-close`/`naming` already
apply to type names, now made explicit for partially-resolved reads.)

### 1.4 Reconciliation: first-match precedence versus delivered disjointness discipline

The delivered `structural-codec` enforces `validate_disjoint`: it **rejects** a form
set that is not *provably* disjoint [observed — `structural-codec` conformance law;
`ConstructorCodec.decode_forms` is the set of accepted shapes per constructor]. Ordered
first-match (§1.2) is a *different* resolution rule: it lets overlap exist and lets
declared order decide.

**[reconciled] The two regimes coexist, and the boundary between them is explicit:**

- **Where forms are provably disjoint, order is irrelevant** — at most one expectation
  can match, so first-match and disjoint-match give the identical result. The strong
  static guarantee (ambiguous decode is *impossible*) holds, unchanged, for these sets.
- **Where overlap is by design** — the transitional/abstraction-level case, where a
  block is deliberately "potentially X, Y, or Z" and more than one expectation can
  match — **declared order decides** by first-match. Disjointness is neither provable
  nor wanted here; order is the intended resolution mechanism.

So the honest statement is: *prove disjointness where provable; let declared order
decide where overlap is intended.* Both are first-class. `validate_disjoint` stays as
the checker for the sets that claim disjointness; ordered-overlap sets are a distinct,
explicitly-ordered kind that opt out of the disjointness claim and into order.

**A safety property changes here — surfaced, not decided.** Today the engine's hard
guarantee is *static*: a non-disjoint form set is **rejected at seal time**, so an
ambiguous decode can never reach runtime. Admitting ordered-overlap sets weakens that
specific guarantee: for those sets, decode is no longer *provably unambiguous* — it is
only *deterministic under the declared order*. That is a real change in a delivered
safety property (from "ambiguity is statically impossible" to "ambiguity is resolved
deterministically by author-declared order"). Per the dispatch instruction, I do not
decide it silently — see **[DECISION 1]** (§8): whether to admit ordered-overlap form
sets at all, and if so how to gate them (e.g. require the order to be explicit and
authored, forbid silent overlap in sets that *could* be made disjoint, and keep
`validate_disjoint` mandatory everywhere overlap is not deliberately declared).

## 2. The trait and organs, carried forward and sharpened

v1 §2–§3 stand: a **TextualForm** is one textual mouth of an **EncodedForm** (a
stringless Core value family); it owns the two-way text↔Core bridge and drives it from
the **nametree** (shared `NameTable`, written on decode / read on encode) and the
**structuretree** (owned per form, driving structural encode/decode). The trait shape
in v1 §2 is unchanged. What §1 sharpens: the structuretree yields *ordered expectation
enums*, and decode is first-match over them, producing values whose reader-side types
range over the transitional/abstraction lattice.

**[ruling — Ruling 2, the structuretree's primary identity]** **[psyche verbatim]**
"the language itself is encoded/decoded to/from encodedform using it; it becomes a
data-driven enc/decoder." The structuretree's **primary identity** is seated here: it
**is the data-driven encoder/decoder** through which each language passes to and from
its EncodedForm. It is not "side data that also enables help"; it is the enc/decoder
itself, expressed as data. Help and Version (§4) are **secondary projections** of the
very same data — never the point of it. This corrects any framing (including the
manager's, which the psyche explicitly corrected) that treats the structuretree as a
help/printer artifact first.

## 3. Ruling 2 — component Input/Output objects and the standard variants

**[psyche verbatim]** "the input field in a schema file, which was meant to represent
all of the types of things that a component can receive as an input, as a query... and
then output is all the different types of things that can come out of that component.
And that's why the idea with Sema was the same thing as a database. What are the types
of queries that we can send to that database, and what are the types of answers that
this database can give us? And Nexus was the same thing... my vision was that when we
add more advanced functionality... it would get a corresponding one or more input and
output type objects. And which at the first root level are usually a bunch of enums,
data carrying enums, one of which should by standard be version, and one of which
should be help on like our standard components."

### 3.1 Seated design

- **[ruling]** Every component has **root Input and Output type objects**. Input = all
  the query/request types the component can receive; Output = all the answer types it
  can return. This is the schema-file `input`/`output` field the psyche described, and
  it is the same query/answer duality he intends for Sema (as a database) and Nexus.
- **[ruling]** At the first root level these are **data-carrying enums**. As advanced
  functionality is added, a feature gets **one or more corresponding Input/Output type
  objects** — the surface grows by adding variants/objects, not by bespoke side APIs.
- **[ruling]** **By standard, two variants exist on our standard components: `Version`
  and `Help`.** Every standard component answers these.

### 3.2 Where the reusable logic lives (manager proposal — seated for validation)

**[manager proposal — validate, not psyche words]** The split:

- **Per-component root `Input`/`Output` enums live in each component's own signal
  contract** (`signal-<component>`, the public wire vocabulary per `component-architecture`).
  These are component-specific: a component's queries and answers are its own.
- **The reusable standard-component machinery lives once in the shared signal runtime
  layer** — the standard `Version` and `Help` variants *and the generic logic that
  answers them* — so it is written once and every standard component inherits it rather
  than re-implementing per component. (Concrete home candidate: the shared signal
  contract / runtime layer that `signal-domain` and the Signal plane already establish;
  exact crate placement is an implementation detail for the slice, kept truthful to
  `component-architecture`'s contract-versus-runtime split.)
- **`Help` renders from the component's own schema and structuretree.** This **re-scopes
  v1 slice `.45`**: help is not a standalone printer ported off the legacy renderer; it
  is **the answerer for the standard `Help` variant**, and it produces its text by
  projecting the component's schema + structuretree (§2: Help is a secondary projection
  of the enc/decoder data).
- **`Version` answers from build-stamped version data** — the same mechanical
  build-time stamping already used for provenance (`concat!/env!(CARGO_PKG_VERSION)`,
  cf. the epic's `@generated by logos <version>` ruling), never a hand-maintained string.

### 3.3 Connection to the daemon-port path

**[reconciled]** This is not free-floating: **as daemons port to the new engine
(`primary-56d1.39` Spirit-first, then Orchestrate, etc.), their contracts adopt the
standard Input/Output enums with the standard `Version`/`Help` variants.** The standard
machinery must exist for the ports to adopt it. A new slice (§7) registers the
standard-component interface machinery and sequences it as an enabler on the port path:
the first ported daemon (Spirit) is the first adopter and the first witness that the
standard variants answer correctly through a real component.

## 4. Help and Version as secondary projections (re-scope of v1 §7.1)

v1 §7.1 seated "help = a projection of the structuretree." That reading is kept in
substance but **re-scoped and demoted** per §2 and §3:

- Help is **the answerer for the standard `Help` variant** of a component's Output
  (§3), produced by projecting the component's schema + structuretree. It is not a
  standalone renderer and is not a port of the legacy `schema-language/src/source.rs`
  renderer.
- Help and Version are **secondary projections of the structuretree's primary identity
  as the data-driven enc/decoder** (§2). The structuretree earns them for free because
  it already *is* the enumeration of accepted, ordered shapes — but they are a
  byproduct, never the reason the structuretree exists.

## 5. Ruling 3 — the Rust bypass is rejected; the real thing

**[psyche verbatim]** "I dont care for this bypass; I find it of poor taste and
deceitful when agents do this. I want the real thing, as envisionned."

v1 §6 tried to keep syn/prettyplease as a demoted "raw layer" beneath a shallow
structuretree. **The psyche rejects that bypass.** v2 replaces it.

### 5.1 TextualRust as real per-type textual-form data (redesign of slice `.44`)

**[psyche verbatim]** "on the Rust side, obviously the rules would be quite different,
so it would use its own, like maybe we could create a library for languages a bit more
like Rust that have a certain kind of behavior... right now all of this could just be
embedded in the logos code. We could just have a different separate directory in the
source to keep all of that Rust textual form data. Well, there's going to be data...
this data is per type."

**[psyche verbatim]** "this textual form machinery... becomes usable by Rust or to
create Rust and even read Rust into logos if the Rust qualifies, meaning if it's... a
subset of the syntax that this structure tree and this name tree support."

Seated design:

- **TextualRust is real per-type textual-form data**, not a syn/prettyplease pass-through.
  "this data is per type" — each Core type carries its own Rust textual-form data that
  drives both directions.
- **It lives, for now, in its own separate directory inside the logos source.**
  **[psyche verbatim]** "right now all of this could just be embedded in the logos
  code... a different separate directory in the source to keep all of that Rust textual
  form data." So: no new crate yet; a dedicated directory in the logos source holds the
  per-type Rust textual-form data.
- **It drives both Rust emission and qualified Rust reading into logos.** Emission:
  Core → Rust text through the per-type data. Reading: Rust text → logos, **only if the
  Rust qualifies** — i.e. only if it is a subset of the syntax the structuretree and
  nametree support. Rust outside that subset is not readable, by design; the qualifier
  is a first-class gate, not a best-effort parse.
- **The "library for Rust-like languages" stays future vision**, in the psyche's own
  hedged phrasing ("maybe we could create a library"). It is recorded, not scheduled:
  when several Rust-like languages share this behavior, the embedded logos directory can
  graduate into a shared library. Not now.

This makes TextualRust the real thing: a structuretree/nametree-driven, per-type,
data-defined Rust form that both writes and (for the qualifying subset) reads Rust —
the same machinery as every other TextualForm, no foreign-codec special case.

### 5.2 Doctrine-level norm: bypasses presented as design are unacceptable

**[ruling — seated at doctrine level in this authority]** A convenience bypass
presented as if it were the envisioned design is **unacceptable** — the psyche calls it
"of poor taste and deceitful." The norm for agents on this stack: **when a shortcut
diverges from the envisioned design, surface it as an open decision (a [DECISION] item
returned to the manager), never seat it silently as though it were the design.** v1 §6
seated the demoted-syn bypass as a recommendation rather than flagging the divergence
loudly enough; v2 records this as a standing rule so future passes do not repeat it.
This norm is the design-quality gate (`design-quality`: a special case must dissolve
into the normal case) stated as an ethics-of-agency rule.

## 6. Ruling 4 — the proto-language correction (corrects v1 §5.1)

v1 §5.1 framed NOTA as "the base instance with the empty (identity) structuretree,"
which every richer language specializes. **The psyche corrects this framing.**

**[psyche verbatim]** "(NOTA is the base every language specializes) — that wasnt the
right way to say whan I mean; the basic syntax structure of nota (but actually more
accurately; schema) - how delimiters are used, capitalization and the typed inner
blocks approach to parsing; this is what I mean by the universal aspect, the
proto-language behind all of them. it probably needs a name. it builds on clojure
(syntax; use all the delimiters elegantly) and shen (kernel - encodedform (we add +
nametree + structuretree = real computer language and atomic editing of code + type
safety) and rust (strictness, type-safety enforced by the runtime)."

### 6.1 Seated correction

- The universal thing is **not NOTA-the-instance**. It is the **proto-language**: the
  basic syntax structure — **most accurately schema's structure** — behind every family
  member. Concretely, the universal aspect is **(a) how delimiters are used, (b)
  capitalization, and (c) the typed-inner-blocks approach to parsing.** These three are
  the proto-language; NOTA and schema and logos and Rust-form are all *members* that
  share it.
- v1's "NOTA is the base with the empty structuretree, everything specializes it" is
  **withdrawn** as the framing. NOTA is *a* member (a simple one), not *the* base that
  others subtype. The universal thing sits *behind* all members as their shared
  proto-language, which is most accurately named by schema's structure, not NOTA's.

### 6.2 Lineage, recorded exactly as given

The proto-language's lineage, in the psyche's exact attribution:

- **Clojure** — syntax; "use all the delimiters elegantly."
- **Shen** — the kernel and **EncodedForm**. To Shen's kernel/EncodedForm **we add
  nametree + structuretree**, and the psyche's equation is: EncodedForm + nametree +
  structuretree = **"real computer language and atomic editing of code + type safety."**
- **Rust** — strictness; **type-safety enforced by the runtime.**

### 6.3 The name is OPEN

**[ruling]** The proto-language "probably needs a name" — the psyche states it is
unnamed. This is a **psyche-review item**, tracked (§7). **[manager proposal — unblessed
candidates, NOT leans of the psyche]** the manager floated **Protos** and **Typos** in
chat as candidates only. They are recorded as unblessed candidates for the psyche to
consider, accept, or discard; they are explicitly **not** leans of the psyche and carry
no recommendation weight. See **[DECISION 2]** (§8) — framed as a naming item to route
to the psyche, not an agent decision.

## 7. Tracker changes (slices updated and created)

Grammar dependency re-verified on the tracker: **`primary-56d1.5` (settled-wave grammar
migration) and `.6` (delimiter reshuffle) are CLOSED** — nota main `7d0651a0` is the
unified next-gen grammar; `.41` already depends on the now-closed `.5`, so **the Nomos
door's grammar blocker is cleared.** `.41`'s "cut into the unified grammar the
NotaGrammarUnification lane is producing (two live grammars coexist)" language is stale
and is updated to "cut into the landed unified grammar (nota main `7d0651a0`)."

Slices updated for consistency with the four rulings:

- **`.40`** (TextualForm trait / two organs) — DECISION 1 (tree-vs-flat) is answered:
  storage is immaterial and closes; add the ordered-expectation-enum + first-match
  decode semantics and the transitional/abstraction type lattice (Ruling 1); note the
  structuretree's primary identity as the data-driven enc/decoder (Ruling 2).
- **`.41`** (Nomos raw-NOTA door) — grammar blocker cleared; retarget from "unified
  grammar being produced" to "landed unified grammar `7d0651a0`."
- **`.44`** (TextualRust) — **redesigned**: the syn/prettyplease-as-raw-layer bypass is
  **rejected** (Ruling 3); TextualRust becomes real per-type textual-form data in its
  own directory inside logos source, driving Rust emission and qualified Rust reading;
  library-for-Rust-like-languages recorded as future vision.
- **`.45`** (Help) — **re-scoped**: Help is the answerer for the standard `Help` variant
  (Ruling 2), projecting schema + structuretree; a secondary projection of the
  enc/decoder, not a standalone printer.

Slices created:

- **standard-component interface machinery** — per-component root `Input`/`Output` enums
  in each `signal-<component>` contract; the standard `Version`/`Help` variants and their
  generic answerer in the shared signal runtime layer; `Help` from schema+structuretree,
  `Version` from build-stamped data (Ruling 2 / §3). Sequenced as an enabler on the
  daemon-port path (`.39`): ported daemons adopt the standard variants; Spirit is the
  first adopter/witness.
- **proto-language naming (psyche review)** — the universal proto-language behind the
  family needs a name (Ruling 4 / §6.3); candidates Protos / Typos recorded as unblessed
  (not psyche leans). Blocked-on-psyche.

## 8. Decision items for the manager (options + recommendation; not asked of the psyche directly)

**[DECISION 1] Admitting ordered-overlap form sets weakens a delivered static safety
property.** *Tension:* Ruling 1 makes decode ordered first-match, which *requires*
allowing form sets where more than one expectation can match; the delivered
`validate_disjoint` today **rejects** any non-provably-disjoint set, giving the hard
static guarantee that ambiguous decode is impossible. Admitting ordered-overlap sets
downgrades that guarantee (for those sets) from "ambiguity is statically impossible" to
"ambiguity is deterministically resolved by author-declared order." *Options:* (a)
**admit ordered-overlap sets, gated** — keep `validate_disjoint` mandatory everywhere
overlap is not *deliberately and explicitly* declared; an overlapping set must opt in
with an explicit authored order, and a set that *could* be made disjoint must be
disjoint (order is only for intended, unavoidable overlap such as transitional/
abstraction reads); (b) **admit ordered-overlap sets freely** — order is the universal
rule, `validate_disjoint` becomes advisory; (c) **forbid overlap** — keep strict
disjointness and model transitional types some other way. *Recommendation:* **(a)** — it
honors Ruling 1 (first-match precedence and transitional types are real and needed)
while preserving the strong static guarantee everywhere overlap is not the deliberate
design, so the safety loss is scoped to exactly the case the psyche described and
nowhere else. This is returned because it is a genuine safety-property change, not an
implementation choice — the dispatch instructed me to surface it rather than decide it.

**[DECISION 2] The proto-language's name (route to the psyche).** *Tension:* Ruling 4
states the proto-language "probably needs a name" and leaves it open. *Options:* the
manager's unblessed candidates **Protos** and **Typos**, or a psyche-supplied name, or
"leave unnamed for now." *Recommendation:* **route to the psyche as a naming item** — do
not have an agent pick. Record Protos/Typos as candidates only (explicitly not psyche
leans). The name touches a class of downstream identifiers, so it is worth settling, but
it is a naming judgment that belongs to the psyche, not an agent decision.

**[DECISION 3] Placement of the shared standard-component machinery (validate the
manager proposal).** *Tension:* §3.2 is a manager proposal, not psyche words: per-component
`Input`/`Output` in `signal-<component>`, the standard `Version`/`Help` machinery once in
"the shared signal runtime layer." The exact crate home for the shared machinery is
unstated. *Options:* (a) **shared signal contract crate** (`signal-domain`-adjacent) owns
the standard variant *types*, shared runtime owns the *answerer* — matches
`component-architecture`'s contract-versus-runtime split; (b) **a new dedicated
`signal-standard` (or meta) crate** for both types and answerer; (c) **fold into the
Signal plane** of the runtime library directly. *Recommendation:* **(a)** — it keeps the
contract/runtime boundary `component-architecture` mandates (variant *vocabulary* in a
contract crate, generic *answering logic* in the runtime layer) and avoids a new crate
until a second standard component proves the shape. Returned because the whole §3.2 split
is a manager proposal the psyche has not confirmed; §2's correction shows he *does* correct
manager framings, so this placement should be validated before it is built.

## 9. Validation scope

Design-authority only. No engine source, generated artifact, store, deployment, or
Spirit record was changed. Ruling claims cite the psyche's 2026-07-17 chat (verbatim
passages reproduced above are the source of truth). Tracker facts (`.5`/`.6` closed at
nota `7d0651a0`; `.40`–`.45` state) were re-verified live via `bd` this pass. Nothing
here is accepted until the psyche grades it; the §8 items are returned to the manager,
never asked of the psyche directly. This lane's writes are this file, the v1
supersession stamp, and the §7 tracker edits.
