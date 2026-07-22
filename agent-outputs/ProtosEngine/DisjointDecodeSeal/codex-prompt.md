# Codex dispatch — disjoint decode, sealed by proof

## Psyche ruling (2026-07-22)

Defining anything already defined — including builtins — is a typed error.
This makes decode disjointness real: no user type may bear a builtin name, so
the bare declared-type-name form excludes the builtin spellings, every form set
becomes provably disjoint, and the prover runs at seal. Ambiguous decode is
statically impossible; decode never depends on constructor trial order.

## Background (witnessed)

- `validate_disjoint` (protos `structural-codec/src/disjoint.rs`) exists but
  `AddressedStructuralTable::seal` (`structural-codec/src/table.rs`) never calls
  it; it runs only in tests and by call-site convention.
- core-schema's reference grammar (`src/document.rs`, `ReferenceConstructor`)
  relies on ordered first-match decode: builtin keyword constructors (`Integer
  String Boolean Bytes Vector Optional ScopeOf`) are tried before the bare-name
  fallback, which matches any PascalCase atom and therefore overlaps every
  keyword. The prover as written would reject this grammar (it marks
  Literal-vs-NameAtom conservatively unprovable, `disjoint.rs:78-81`).
- core-schema universe construction already performs duplicate detection
  (landed at core-schema main `3baedd030633`).

Work from current public mains of `protos` and `core-schema` (separate repos).
The local `repos/protos` checkout may lag the landed rev `a95f89aa31fd`; verify
before starting.

## Work items

1. **Builtins are prior definitions** (core-schema): extend the existing
   duplicate detection so builtin spellings count as already defined. Declaring
   a type named `Integer` (or any builtin) is a typed error — a structural
   error value, never a string.
2. **The bare-name form excludes the lexicon** (protos structural-codec): give
   the name-atom form an exclusion over a committed lexicon (the builtin
   spellings), and teach the prover the corresponding Literal-vs-NameAtom
   separation so the disjointness is provable instead of conservatively
   unprovable. The exclusion is truthful because of item 1.
3. **Prover wired into seal** (protos structural-codec): `seal` runs
   `validate_disjoint`; sealing an ambiguous table is a typed error. Rework the
   core-schema document grammar so every form set seals green under the proof;
   constructor authoring order must carry no decode semantics afterward.
4. **Rename** `ReferenceConstructor::Plain` → `Declared` across code, tests,
   and docs. The psyche rejected the old name; `Declared` is the
   manager-proposed replacement — if a genuinely better name emerges, raise it
   at review rather than minting a third silently.

## Constraints

- The form vocabulary is rkyv-archived and content-hashed: shape changes bump
  the layout under the migration law. Byte-exactness is explicitly not a goal
  ("working programs is what we want"); witness hashes move with the layout.
  Never preserve a hash by mis-tagging or shimming.
- No field names anywhere in the family. Positional records only.
- Typed failures only; no failure collapses into a string.
- Plain-language vocabulary (deltas 41–42): no mouth/organ/spine/door/currency
  terms. Where a touched file still carries retired vocabulary, clean it in the
  touched region.
- Version control per the jj skill: inline messages, no editors, no raw git
  outside documented escape hatches.
- Nix checks green and reproducible: build / test / doc / fmt / clippy.
  Truthful denominators in any reported counts.

## Acceptance

- Every seal site runs the prover; no production or test path constructs a
  sealed table without the disjointness proof.
- A test witnesses: declaring a type with a builtin name is the typed
  redefinition error.
- A test witnesses: `Integer` at reference position decodes as the builtin,
  and permuting constructor authoring order changes nothing.
- core-schema's full grammar seals green under the prover; all existing
  round-trip tests pass against the new layout.
