# Positional struct syntax — migration spec (separator decided)

The separator is locked: **`key.TypeReference`** (dot, name-first). The common
case is bare types; the dot-prefix names the rare slot. This specs the full
schema-next migration so executing it is mechanical — and is honest that it is a
large all-or-nothing change, not a tail-of-turn edit.

## Why it is all-or-nothing

The struct-body reader's walker (`MacroExpansionFields::lower`) decides per
position whether adjacent objects are a `name type` **pair** or single fields.
The positional form wants every object to be its **own** field. But
`Topics Kind` is the *same tokens* whether read as one pair `(name=Topics,
type=Kind)` or two fields `(topics, kind)` — so the walker cannot support the
old and new forms at once. Flipping it to single-object-per-field **breaks every
existing schema simultaneously**, so all schemas must convert in the same change.

Blast radius (schema-next alone): **42 `.schema` files** + ~16 inline schema
strings across ~10 test files. And the **identity tests hash schema content**
(`identity.rs`, ~20 sites) — converting schemas changes the hashes, so the
expected hashes must be recomputed in the same pass. Round-trip/source-codec
tests assert exact encoding, so the encoder must convert in lockstep.

## The mechanism (3 code changes)

1. **Walker → single-object-per-field.** `MacroExpansionFields::lower` stops
   pairing; each object in the brace body is one field. (The single-object
   lowering path already exists and already derives names — `declarative.rs:1903`.)
2. **`.` differentiator in the atom path.** An atom containing `.` (and not a
   number; `:` stays scope) splits on the first `.`: field name = before, type =
   `from_name(after)`. Additive to the atom-lower path.
3. **Encoder → positional.** Struct-declaration emission writes bare types, or
   `name.Type` when the field name differs from the type's derived name.

## The conversion rules (mechanical, per schema)

| Today | Becomes | Why |
|---|---|---|
| `Topics *` | `Topics` | bare type; name derived (`topics`) |
| `reference TypeReference` | `reference.TypeReference` | name ≠ derived → dot-prefix |
| `name Type` where name == derived(Type) | `Type` | drop the redundant name |
| `declaration (Vector Declaration)` | alias `Declarations (Vector Declaration)` then field `Declarations` | composites get a name via aliasing (dimensional principle `639`) — `name.(Vector …)` is not atom-expressible |
| inline `Field { … }` / `Field [ … ]` | hoist to a top-level declaration, reference by name | same aliasing rule for inline structs/enums |

The composite/inline rule is the only non-trivial part: it **restructures**
schemas (adds alias declarations), which is the dimensional principle `639`
applied — every field's type becomes a single name. This is consistent, not a
new decision, but it is why the migration is a restructure, not a find-replace.

## Plan to execute (a dedicated atomic pass)

This should run as one focused green-to-green pass on the schema-next epic branch:

1. Land the 3 mechanism changes (walker, `.` split, encoder).
2. Convert the 4 canonical `schemas/*.schema`, iterate to green on the core
   suites.
3. Convert the ~38 fixtures + inline test strings, suite by suite.
4. Recompute identity hashes; re-green `identity.rs`.
5. Full suite green + clippy, then commit + push.

Because it is all-or-nothing, nothing is committed until the whole suite is
green — there is no safe partial. It is well-suited to a single focused effort
(or a workflow whose success criterion *is* the green suite), and deliberately
not crammed into the end of a turn that already shipped the consolidation and
both derive extensions.

## Status

Everything else decided is implemented, verified, and pushed (epic branches,
named-field + struct-level derive). The positional syntax is fully specified and
ready to execute as the next focused pass — the separator is the last open
decision and it is now made.
