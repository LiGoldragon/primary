# Representing Meaning with Structure — research synthesis, 2026-08-11

Research directed by the psyche during the Datom syntax round
("Research the field of representing meaning with structure",
2026-08-11T19:17+02:00, structuredStringType.md). Subagent web
research, Designer-condensed. Information layer — this document
instructs nothing; the psyche rules the structured string's shape.

Target constraints (ruled): strictly typed, schema-positional, no
self-describing tags in data, decode direct to typed Rust structs;
the structured string is parenthesized, arbitrary depth, "a graph of
sorts".

## 1. The field's central lesson

The founding thesis of descriptive markup (OHCO: text as an Ordered
Hierarchy of Content Objects, DeRose et al. 1990; SGML/XML/TEI
instantiate it) failed on real text: metrical lines, dialogue turns,
and sentences cross each other, and a single tree cannot hold
crossing structures. The authors retreated from strict hierarchy in
1993; TEI's four workarounds (milestones, standoff pointers,
fragment-and-link, parallel documents) all smuggle a second
hierarchy into the first one's metadata. Every modern successor
decouples the text sequence from the structure(s) over it:

- Standoff / W3C Web Annotation: base text untouched; annotations
  are external objects addressing it (offsets/anchors). Unlimited
  overlap; adds an addressing indirection.
- GODDAG: a DAG — character data may have multiple parents;
  overlap is simply multiple parentage.
- LMNL: named ranges over a sequence of atoms; ranges overlap
  freely; annotation values recursively contain ranges.
- TAG/TAGML: a property hypergraph separating containment (which
  text a markup covers) from dominance (markup hierarchy) — the two
  relations XML collapses into parent-child.

Trees keep the tooling and the simple recursive decode; every
graph-shaped alternative buys overlap at the cost of richer
traversal or compilation back to a tree.

## 2. Document ASTs

- Pandoc AST / mdast: recursive trees, type carried inline at every
  node (self-describing at the value level).
- ProseMirror: block tree, but inline content is a flat sequence
  with marks (emphasis, link) as labels on ranges; valid types live
  in an external Schema, not the document.
- Portable Text: flattest — blocks are a flat array; spans are a
  flat array; simple decorators are keys on spans; complex
  annotations live in a block-level markDefs array referenced by
  key. No annotation nesting at all.

Thread: models wanting inline overlap either accept nesting and its
collisions, or flatten inline content and push annotation data
sideways. Schema-external typing (ProseMirror, Portable Text)
matches Datom's positional decode; inline-typed trees (Pandoc) do
not.

## 3. Linguistic meaning representation

- RST: discourse coherence as a binary labeled tree over clause
  units — nuclearity plus rhetorical relation (elaboration,
  contrast, cause…). Organizational meaning across a text.
- AMR: sentence meaning as a rooted labeled DAG in PENMAN
  notation — nested parentheses, concept instances, role edges;
  reentrancy by variable reuse (second mention is a bare variable,
  resolved by reference). Already parenthesized, already a DAG.
- DRS (discourse representation): nested boxes of referents and
  conditions; quantifier scope and cross-sentence anaphora;
  parenthesizable but heavy machinery.
- IGT and ToBI/prosody tiers: aligned parallel sequences (matrix
  shape); standoff labels over token spans.

## 4. Emphasis is semantic, not presentational

"I never SAID he stole the money" — moving the stress changes the
proposition. Rooth's Alternative Semantics: a focused constituent
denotes its value plus a set of alternatives, constraining the whole
sentence's interpretation. Contrastive/narrow/broad focus are
distinct semantic operations. An annotated string marking emphasis
carries meaning, not decoration — the psyche's premise is the
field's own distinction.

## 5. Evidence on structure and LLM performance

- Format sensitivity is real: up to 40% swing across prompt formats
  on GPT-3.5-class models; shrinks with scale (arxiv:2411.10541).
- XML tags pay only past ~500 tokens; +31% token overhead, no gain
  on short prompts (2026 benchmark).
- Forcing structured *output* degrades reasoning (arxiv:2604.25359).
- Chain-of-thought: the strongest structure-helps evidence (GSM8K
  33%→80%, PaLM 540B; structure mattered more than example
  correctness).
- Inline importance labels on prompt segments improve accuracy
  (PSAO, arxiv:2605.14561) — closest existing thing to the
  structured string.
- AMR augmentation is task-gated: helps long-context summarization,
  hurts short-context QA; gains model-size-gated.
- No dedicated "rich text for LLMs" paradigm exists — practitioner
  folklore (XML tags, Markdown) without a formal representation.
  The territory is open.

## 6. Three shapes compatible with the constraints

1. **Recursive positional tree (S-expression style).** Position is
   type per schema; nesting is depth. Simplest decode, native to
   parens. Cannot represent overlapping annotations without
   fragmentation or back-references.
2. **AMR-style DAG, PENMAN-like.** Native parens, arbitrary depth,
   reentrancy by variable back-reference. Tension: back-references
   are an in-band naming mechanism — a mild self-description.
3. **Flat spans with positional mark references (Portable-Text
   style).** Base text as spans; marks in a separate positionally
   typed structure; overlap native, no nesting collisions. Tension:
   span-boundary bookkeeping and one indirection layer in the
   decode.

The deciding question is whether overlapping annotations are in the
type's ambition (emphasis crossing a quotation boundary) or strict
nesting suffices. Tree suffices for nesting; overlap forces shape 2
or 3 — which is where "a graph of sorts" points.
