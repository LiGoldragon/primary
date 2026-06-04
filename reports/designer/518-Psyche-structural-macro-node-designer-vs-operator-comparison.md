---
title: 518 — Structural macro nodes — designer vs operator, compared
role: designer
variant: Psyche
date: 2026-06-05
topics: [nota, schema, structural-macro, macro-node, nota-next, schema-next, comparison, asschema]
description: |
  Honest comparison of the two independent structural-macro-node
  implementations: operator's (landed on main, integrated into schema-next,
  registry-backed trait) vs designer's (feature branch, standalone demo,
  direct typed BlockShape dispatch). Operator's is the stronger base to
  land. But the comparison surfaces a real design tension — even the
  operator's own code carries TWO patterns — and a concrete critique
  (string-dispatch in from_structural_match) that should shape the final design.
---

# 518 — Structural macro nodes — designer vs operator, compared

Two implementations landed independently from the same psyche prompt
(records `ejvc`/`lcwu`). This is the honest comparison.

**Bottom line:** the operator's is the stronger base to build on — it is
integrated into real schema-next source, verified with clippy, and its
`structural_variants()` is a ready derive-macro target. My version is a
cleaner standalone demonstration that, in the comparison, surfaces a real
design tension the operator's own code contains and a concrete critique
worth fixing before this hardens.

## Side by side

| Axis | Operator (`nota-next 35786532`, `schema-next 87991f83`) | Designer (`nota-next structural-macro-nodes`, `c2b4cc72`) |
|---|---|---|
| Where it landed | main, both repos | feature branch, pushed |
| Integration | **Real**: `SourceVariantSignature` parses authored enum-variant sugar, round-trips actual `.schema` text, lowers to Asschema | **None**: standalone `examples/` on an invented type-reference dialect |
| Matching | Reuses `MacroRegistry`/`MacroNodeDefinition`/`Pattern` + captures | Fresh `BlockShape` (PascalAtom / HeadedParenthesis / PascalHeadedParenthesis) on Block predicates |
| Decode | match by structure → `MacroMatch` → `from_structural_match` reads captures, **dispatched on `macro_name()` string** | `from_block` fuses structural match + typed construction in one arm; no captures, no string |
| Encode | `to_structural_nota() -> String` (bespoke) | `Display` (canonical trait domain) |
| Variants as data | `structural_variants() -> Vec<MacroNodeDefinition>` — first-class list | hand-coded `if`-ladder in `from_block` |
| Sequence positions | `from_blocks(&[Block])` already handled | flagged as open; single-block only |
| Verification | `cargo test` + `clippy -D warnings`, both crates | example run + 18 existing tests; no clippy |
| Diagnostics | `UnsupportedMacroNodeStructure { position, expected[], found }` | `NoVariantMatched { node, found }` |

## Where we converged (this is the validation)

Independently, both implementations chose: a trait an enum implements;
**typed decode + encode-back**; **declaration-order** first-match;
**recursion** into nested positions; **bidirectional** round-trip; **keep
Asschema for now** (retire after more positions migrate); and **a derive
macro as the endpoint** (`nota-next-derive`). Two agents reaching the
same shape from the same prompt is strong evidence the design is right.
Both honored the same captures; the operator confirmed `ejvc`/`lcwu`
were canonical and removed their subagent's duplicate record `24ds`.

## Where the operator's is stronger

1. **It is integrated and proven on real schema source.** Authored
   `[Reserved (Record Entry) (Inline { Topic * })]` parses through the
   structural node, round-trips to the same `.schema` surface, and lowers
   to Asschema — including an inline-declaration payload that becomes a
   real exported type. Mine proves the *mechanism* on a toy dialect; the
   operator proves the *claim* (schema sugar is bidirectional NOTA) on
   the actual artifact. This is the bigger result.
2. **`structural_variants() -> Vec<MacroNodeDefinition>` is a real
   derive target.** The per-variant patterns are first-class data a
   derive macro can emit. My hand-coded `from_block` ladder is not.
3. **Sequence positions are handled** (`from_blocks`) — the exact
   extension I left open.
4. **Verified with `clippy -D warnings`.** I ran the example and existing
   tests but not clippy.

## Where mine is cleaner — and what it surfaces

1. **`Display` over a bespoke `to_structural_nota`.** methods.md §"Use
   existing trait domains": the encode is `Display`. Minor, but the
   operator's bespoke method re-invents the canonical trait.
2. **The decisive one — fused typed decode vs. a string bridge.** The
   operator's path is four hops: variant → `MacroNodeDefinition` →
   `MacroMatch` (captures) → `from_structural_match` that **re-dispatches
   on `matched.macro_name()`, a string** (`"unit variant"` /
   `"data variant"`). That is the *string-matching-as-dispatch*
   anti-pattern named in `skills/enum-contact-points.md` and
   `skills/rust/methods.md` §"Don't hide typification in strings" — the
   structural match is computed, then thrown away and recovered from a
   string name. My `from_block` *fuses* the structural match with the
   typed construction in the same arm, so there is no capture map and no
   string round-trip: one hop, typed end to end. Splitting match from
   construction is what *forces* the string bridge; fusing them removes it.

3. **The operator's own code already contains two patterns.** This is the
   most important finding. The formal registry-backed trait is used for
   exactly **one** position (`SourceVariantSignature`). Every *other*
   schema-next position — `SourceDeclarationValue`, struct fields,
   declarations — uses a plain `match block { Atom|Parenthesis => …,
   Brace => …, SquareBracket => … }`, i.e. **my** direct typed dispatch,
   just inlined instead of reified into a `BlockShape`. So the heavyweight
   `Pattern`/`MacroRegistry` path was not the natural reach even for the
   operator; they used the direct typed match everywhere except the one
   showcase node. Two patterns for one concept is exactly what shouldn't
   harden.

## Recommendation — synthesize, don't pick

Land on the operator's base (it's integrated and on main), but resolve
the two-patterns tension toward the **direct typed dispatch**, reified:

- **Make the direct typed `from_block` THE structural macro node** — it's
  what both of us reach for, it's one hop, and it avoids the string
  bridge. The registry/captures path stays only where a position needs
  named multi-capture extraction it can't get from positional slots.
- **Reify the per-variant shape as data** (my `BlockShape`, extended with
  per-slot sub-shapes + sigils) so there is still a first-class list for
  the derive macro to target — but the derive emits *direct typed
  `from_block` arms*, not a registry build plus a `macro_name()` string
  reader.
- **Keep** the operator's `from_blocks` sequence handling, the
  `UnsupportedMacroNodeStructure` diagnostic, and the schema-next
  integration. **Adopt** `Display` for encode.
- **Fix** the `macro_name()` string dispatch: if a matched node must name
  which variant it is, that name is a typed token (an enum), not a
  string — or, preferred, fuse so the question never arises.

## The decision for the psyche

The substantive call is which shape *is* the structural macro node:

- **(1) Registry-backed** (operator's trait): reuses the existing
  `Pattern`/captures machinery, first-class variant list, but a four-hop
  decode with a string bridge, and it's only used for one position even
  in the operator's own code.
- **(2) Direct typed `from_block`** (mine, and the operator's *other*
  positions): one hop, typed end to end, no string — but needs the shape
  reified as data to be a clean derive target.

My recommendation is **(2) with reified shapes**, integrated on the
operator's base. The convergence says the *concept* is settled; this is
the one open seam, and the operator's own code already votes for (2)
everywhere except the showcase.

## Where things live

- Operator: `nota-next 35786532`, `schema-next 87991f83`, report
  `reports/operator/312-...`.
- Designer: `nota-next` branch `structural-macro-nodes` (`c2b4cc72`),
  report 517.
