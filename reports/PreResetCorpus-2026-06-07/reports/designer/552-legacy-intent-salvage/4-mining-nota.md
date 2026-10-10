---
title: 552 — Legacy intent salvage — mining nota.nota
role: designer
variant: Audit
date: 2026-06-07
topics: [intent, spirit, legacy-nota, nota-design, codec, deletion-readiness]
description: |
  Salvage mining of intent/nota.nota (38 records, the pre-Spirit NOTA-design
  arc). One strong genuinely-at-risk candidate (the codec-complexity-vs-Rust-
  ergonomics principle), one weaker partial-coverage candidate (one-notation-
  one-meaning / audit-for-codec-exceptions). The rest of the file — the entire
  three-case PascalCase rule, branches/leaves vocabulary, curly-brace maps,
  typed map keys, no-tuples, bare paths, Bool-as-enum, Option-wrapping,
  homogeneous lists — is fully preserved in skills/nota-design.md +
  skills/language-design.md and safe to delete.
---

# 552 — Legacy intent salvage — mining nota.nota

## Scope

One file scanned: `intent/nota.nota`, 38 records (the NOTA-language design
arc — mostly the long struct-vs-enum-variant correction series and the
maps/typed-keys/branches-leaves design). 36 records judged already-preserved
or too-specific; 2 surfaced as candidates (1 strong, 1 weaker).

## Salvage candidates

### Candidate 1 — Codec absorbs complexity; Rust types stay natural (the human-authoring boundary)

**Theme:** NOTA codec complexity is the right place to pay; Rust type shapes
must not contort for encode/decode simplicity.

**Kind:** Principle

**Proposed topics:** `[nota codec schema rust ergonomics human-authoring boundary]`

**Proposed description (clarified general idea):**
NOTA is a human-authoring format (cluster data, intent logs, skill files,
configuration, fixtures); inter-component communication inside the system is
pure-binary signal and NOTA never crosses the wire between daemons. Therefore
the NOTA codec must NOT impose constraints on the shape of Rust types in
service of encode/decode simplicity. Encode/decode happens only at the
infrequent human-authoring boundary, so pay the codec-complexity cost once,
inside the codec, and optimise NOTA's grammar + codec for human-readability
and an ergonomic match against natural Rust enum/struct shapes — never force
Rust types to bend toward what is cheapest to serialize.

**Proposed certainty:** High (the legacy record is Maximum, but it was stated
as a forceful in-flight correction of one specific derive split; the general
principle is durable and strongly held, so High is the honest read for the
generalised form).

**Supporting verbatim:** "the current design is totally fucking insane -
making all code contort itself to save a little bit of encode-decode
computation for a format that doesnt even exist insed the system
(inter-component is all pure-binary signal)" (records 22-23).

**Preservation evidence:**
- Spirit `(Observe (Records ((Partial [nota codec ergonomics readability
  authoring]) ...)))` — 47.5KB returned; zero hits for `contort`,
  `codec.*simplic/complex/cost`, `human-author`, `authoring boundary`,
  `encode.decode.*only/once/infrequent`, `optimis.*readab`, or `ergonomic
  match`. The nota records that DO exist (e6ri, pjvv) state the *fact* that
  daemons cannot understand NOTA / NOTA never crosses the wire — but NOT the
  design *consequence* about codec complexity vs Rust type ergonomics.
- `rg -i` across ESSENCE.md / AGENTS.md / INTENT.md / skills/nota-design.md /
  skills/language-design.md / skills/component-triad.md for `human.author |
  never crosses | codec.*simplicity | contort | NOTA never`: the matches in
  component-triad.md (lines 274, 505-514) establish WHERE NOTA lives
  (boundary, not wire) but never draw the codec-design consequence.

**At-risk rationale:** This is the load-bearing *why* behind several decisions
already preserved (mixed-enum support, no-special-case encodings). The
preserved guidance carries the rules but not the principle that justifies
paying codec complexity to keep Rust types natural. On deletion, the next
agent re-encountering a "make the type simpler so the codec is simpler"
tradeoff has nothing telling them which way the workspace has already decided
to lean. The fact (NOTA off the wire) is preserved; the design instinct it
licenses is not.

### Candidate 2 — One notation, one meaning; audit the codec for special-case exceptions (weaker, partial coverage)

**Theme:** NOTA has no syntax exceptions — a notation must never secretly mean
a special container; hunt down and eliminate such codec exceptions.

**Kind:** Principle

**Proposed topics:** `[nota codec syntax delimiters consistency no-exceptions]`

**Proposed description (clarified general idea):**
NOTA has no syntax exceptions: each notation means exactly one thing. A
parenthesized PascalCase form is always a data-carrying enum variant, and a
sequence of those is a vector of enum values — it must never secretly mean a
map or any other special container. When auditing the codec, any place where
one NOTA notation is reused to carry a second meaning (a special-case encoding
to save a delimiter or a derive) is a wrong-shape exception to be eliminated;
give the second meaning its own distinct delimiter/form instead.

**Proposed certainty:** Medium (the legacy records are Maximum, but the
general principle is partially covered by existing skill content — see
preservation note; only the explicit "audit for and eliminate codec
exceptions" framing is at risk, so Medium honestly reflects the residual gap).

**Supporting verbatim:** "that notation means a vector of enums. And it
shouldn't mean anything else. Ever. … Nota doesn't have exceptions." and "I
want you to look for more bullshit exceptions like that. And we have to
fucking eliminate them like the plague." (records 26, 28).

**Preservation evidence:**
- The *specific* instance — the `[(Entry key value)]` map-as-sequence-of-pairs
  encoding — is already fixed and preserved: the curly-brace `{key value …}`
  map form is in skills/nota-design.md lines 343-372 (records 29-30 landed).
- `skills/language-design.md` instinct 18 "Delimiters earn their place"
  (lines 285-326) is the closest preserved content, but it addresses the
  *inverse* question (when to ADD a delimiter) — "cosmetic distinctions" and
  "verb-shaped uses" as reasons to keep a delimiter OUT. It does not state the
  general "one notation = exactly one meaning; never overload a notation to
  secretly mean a container; audit the codec and eliminate such exceptions"
  principle.
- Spirit `(Observe (Records ((Partial [nota syntax notation exceptions
  consistency]) ...)))`: the one near-hit ("with no exceptions: Name@{...} is
  a struct …") is about the at-binder surface, which is itself ABANDONED per
  record `own9` — not the no-codec-exceptions principle.

**At-risk rationale:** A weaker candidate. The specific exception that prompted
it is preserved (curly-brace maps), and the spirit of "keep the grammar small,
delimiters earn their place" is adjacent in instinct 18. What is genuinely at
risk is the active *audit posture* — "go hunt the codec for reused notations
and eliminate them" — which is a recurring maintenance instinct rather than a
one-off. Marginal; flagged for synthesis to judge against Candidate 1's
strength and the psyche's "only a few things" constraint. If trimmed, no harm:
the consequence (curly-brace maps) is already on disk.

## Already preserved / dropped — confirmed safe to delete

The bulk of nota.nota is the canonical source of the NOTA-design skill layer
and is fully manifested. Confirmed preserved (so the file can go):

- **The three-case PascalCase rule** (records 1, 2, 4-14, 24 — the long
  struct-vs-enum-variant correction series): `(VariantName fields…)` =
  data-carrying variant; `(fields…)` no leading PascalCase = struct; bare
  `VariantName` = unit variant. Fully in skills/nota-design.md (Rule 1, "Before
  you sketch", "Grammar facts that catch the recurring mistakes") and
  skills/language-design.md instinct 3-4. Many Spirit records too
  (bracket-swap-enum-vs-struct, enum-vs-struct topics).
- **Positional records, not labeled `(key value)`** (record 1): AGENTS.md hard
  override + nota-design.md step 4. Maximum-certainty founding rule, deep in
  the guidance layer.
- **Drop the superfluous wrapper / variant-question test** (records 2, 4, 5,
  24): nota-design.md Rule 1 + the variant test in "Before you sketch".
- **Homogeneous lists; heterogeneous → record** (records 6, 8): nota-design.md
  "Grammar facts"; language-design.md instinct 13.
- **Bare `Path` typed shape with relaxed alphabet at Path positions**
  (records 3, 33): nota-design.md "Bare `Path`" (lines 374-377). Bare paths
  affirmed as intentional design.
- **Bool-as-enum (`True`/`False` unit variants) and Option-wrapping
  (`(Some inner)` / bare `None`)** (records 15-19, 27): nota-design.md
  "Optional values" (lines 384-391); the True/False UI-of-a-two-member-enum
  framing is the same content.
- **No tuples; tuples are poorly-specified structs (field names are
  information)** (records 31, 32): nota-design.md "No tuples" (lines 379-382);
  language-design.md instinct 13 "No multi-field unnamed structs".
- **Curly-brace maps `{key value …}`, flat stream, no inner pair records;
  PascalCase allowed in key position; keys-with-spaces rejected**
  (records 25, 29, 30): nota-design.md "Map keys" (lines 343-354).
- **Typed map keys — customizable scalar/newtype key (`NodeName`), not raw
  String, not a struct key** (records 34, 35, 36, 37): nota-design.md line 351
  ("a string-like newtype such as `NodeName`"); the must-not-be-a-struct
  constraint is covered by "scalar key type".
- **Branches/leaves vocabulary for typed-record trees** (record 38):
  skills/language-design.md "Branches and leaves — the typed-data-tree
  vocabulary" (lines 327-345) — verbatim landed, exactly as the record
  directed.
- **Restatement = own top-level record; dedup at query time; append-only**
  (record 9): this is the live Spirit model itself (intent-log.md,
  spirit-cli.md, agglomeration/recency topics) — preserved by the deployed
  system.
- **NotaSum/NotaEnum mixed-enum support** (records 21, 22): the specific derive
  split is too-specific AND largely resolved; the durable principle behind it
  is Candidate 1.
- **Brainstorm-in-flight items** (records 18 "forbid bare PascalCase at string
  positions", 20 "unit-variant migration of cluster data files"): too-specific
  / transient-state items, not durable design intent. Dropped.

Verdict: with Candidate 1 (and optionally Candidate 2) lifted into Spirit,
`intent/nota.nota` carries nothing further at risk and is safe to delete.
