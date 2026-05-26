# 350 — Schema feature drift retraction

*Designer-lane subagent dispatch 2026-05-26. Retracts the
`EffectTable` / `FanOutTargets` / `StorageDescriptor` "Features"
surface from the workspace design surface (skills, INTENT, reports).
Per psyche 2026-05-26 (intent records 713, 714, 715, Maximum).*

## What's retracted (records 713-715)

Three psyche statements, captured 2026-05-26:

- **Record 713** — Schema defines data types ONLY. Effects, fan-out
  targets, and effect tables are runtime dispatch / logic — not data.
  They have no place in `.schema` files.
- **Record 714** — The NOTA schema namespace is a **key-value map of
  user-defined types**, not a flat sequence of declarations plus a
  separate Features section. Enums declare inline as
  `EnumName (Variant1 Variant2 …)`; structs as
  `StructName [FieldType1 FieldType2 …]` (positional fields).
  Universal Unknown injection by macro stays — behind-the-scenes,
  not user-authored.
- **Record 715** — The "Features" section in authored schema files
  is wrong. Schemas have types — that IS the user surface. Composer
  machinery for storage descriptors etc. may live as hidden
  mechanism; the AUTHORED schema file does not carry a Features
  section.

The /343 + /345 + /346 design arc + POCs (/103, /104, /105, /106,
/107) introduced authored `EffectTable` / `FanOutTargets` /
`StorageDescriptor` as schema "Features". That whole authored-feature
framing is drift. This sweep retracts it from the design surface.

## Canonical reference (the one example to learn from)

The right shape for an authored schema is
`/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema`.
Key landmarks:

- **Imports** section: `{ … }` map (key-to-source-spec).
- **Operations** section: `[ … ]` list of operation declarations.
- Two empty `[]` placeholders (extended-header slots).
- **Namespace** section: `{ … }` **map of user-defined types**.
  This is the heart of the authored shape — where the drift was
  pulling away from.
- **Channel-outputs** section: `[ … ]` with `(Reply …)`,
  `(Event …)`, `(Observable …)` declarations.
- **NO Features section** anywhere.

Concrete namespace-map excerpt (lines 18-74 of `spirit.schema`):

```nota
{
  Topic [String]                                        ;; newtype struct
  Topics [(Vec Topic)]                                  ;; newtype wrapping a Vec
  Entry [Topics Kind Description Certainty]             ;; struct with positional fields
  Kind (Decision Principle Correction Clarification Constraint)
                                                        ;; closed enum, unit variants
  Observation (State (Records RecordQuery) Topics Questions)
                                                        ;; enum with mixed unit + data-carrying variants
  ;; …
}
```

Enums declare inline with variants in parens. Variants may themselves
be enums in nested parens. Structs use positional fields in brackets.
The namespace is one NOTA map; one section; no Features sibling.

## Files edited

| File | What changed |
|---|---|
| `skills/schema-driven-actors.md` | **Deleted.** The file leaned heavily on `EffectTable` / `FanOutTargets` / `StorageDescriptor` as authored discipline. The non-drift content (actor schema = ACTION + RESPONSE + universal Unknown; structure-is-schema; rkyv-one-format; reading-actor + auto-tap; auto-migration; NEXT vocabulary) is already canonical in `repos/persona-spirit/INTENT.md`. The skill was redundant once the drift came out. |
| `skills/skills.nota` | Removed the `schema-driven-actors` entry. |
| `INTENT.md` (§"The schema-driven stack") | Removed the "plus an authored EffectTable + FanOutTargets" framing on the actor declaration; added the namespace-as-key-value-map clarification with a pointer to `signal-persona-spirit/spirit.schema`. Reframed the POC inventory: dropped "three new Feature variants (EffectTable / FanOutTargets / StorageDescriptor)"; added a note that the POC schemas still carry the drifted shape and a separate operator pass will re-shape them. |
| `reports/designer/341-schema-crystallizes-architecture-2026-05-25.md` | Amended the existing STATUS-BANNER: §2.6 (effect-table) and §2.7 (fan-out execution) join the §2.5 retraction; the "three new Feature variants" framing is drift; pointers to canonical schema shape added. |
| `reports/designer-assistant/105-implementation-showcase-2026-05-25.md` | Retraction banner at the top: the closed-dispatcher property the C4 tests prove survives; the EFFECT TABLE as an authored feature does not. |
| `reports/designer-assistant/106-schema-driven-poc-from-v0.3-main-2026-05-26.md` | Retraction banner: runtime / dispatcher / migration / dual-emission behavior proven by tests is still useful; the AUTHORED `.schema` shape the POC carries is drift and is queued for a separate re-shaping pass. |
| `reports/designer-assistant/107-signal-frame-self-hosting-bootstrap-2026-05-26.md` | Retraction banner: the five reply-outcome enum declarations are fine as pure enum declarations; any Features-section scaffolding the bootstrap touched is the drifted surface. |

## Reports flagged with retraction banners

- `reports/designer/341-schema-crystallizes-architecture-2026-05-25.md` (STATUS-BANNER amended)
- `reports/designer-assistant/105-implementation-showcase-2026-05-25.md` (banner added at top)
- `reports/designer-assistant/106-schema-driven-poc-from-v0.3-main-2026-05-26.md` (banner added at top)
- `reports/designer-assistant/107-signal-frame-self-hosting-bootstrap-2026-05-26.md` (banner added at top)

## Per-repo INTENT — light review

Reviewed `schema/INTENT.md`, `persona-spirit/INTENT.md`, and
`signal-persona-spirit/INTENT.md` in the canonical `/git/...`
checkouts. None of the three mentions `EffectTable`,
`FanOutTargets`, `StorageDescriptor`, or "three new Feature
variants" as authored schema features. No edits needed there.
The `signal-frame` repo has no `INTENT.md` to review.

`persona-spirit/INTENT.md` §"Every actor has a schema" + §"Structure
is schema; logic is Rust" already carry the actor-schema discipline
(ACTION + RESPONSE + universal Unknown) cleanly — which is part of
why the workspace-level `skills/schema-driven-actors.md` skill could
be retracted outright.

## Open follow-on (separate retraction passes)

- **Schema crate `Feature` enum variants in code.** The
  `EffectTable`, `FanOutTargets`, `StorageDescriptor` variants and
  their recognizers / shape-parser entry points / streaming-decoder
  paths live on POC feature branches in
  `~/wt/.../schema/designer-schema-*-2026-05-2{5,6}/`. Rolling those
  back is operator work — separate slice.
- **POC `.schema` files** carrying authored Features sections in
  `~/wt/.../persona-spirit/designer-schema-poc-from-v0.3-main-2026-05-26/`
  and the sibling worktrees. These need re-shaping to the canonical
  namespace-map-only form. Operator slice, or a new designer pass
  that prepares the re-shape blueprint first.
- **Composer machinery.** The
  `signal-frame/schema-rust/src/lib.rs::{authored_effect_items,
  storage_descriptor_items}` emissions may stay as **hidden** composer
  mechanism if the dispatch tables / table-descriptors are still
  useful behind the scenes; what they cannot do is consume an
  authored Features section. The recipe for that mechanism (compose
  dispatch tables from inferred relationships across the namespace
  map, or accept them through some non-schema substrate) is a
  separate designer pass.
- **`finalize_universal_unknowns` post-pass.** Keeps — universal
  Unknown injection is behind-the-scenes macro work, not a
  user-authored feature.

## References

- Spirit records 713, 714, 715 (psyche 2026-05-26, Maximum certainty)
- Canonical authored schema: `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema`
- `skills/nota-schema-docs.md` — the documenting-pseudo-NOTA convention
- `INTENT.md` §"The schema-driven stack" (this sweep updated it)
- `repos/persona-spirit/INTENT.md` §"Every actor has a schema" + §"Structure is schema; logic is Rust"
