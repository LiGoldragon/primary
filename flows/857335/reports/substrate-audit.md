# Substrate audit closure

Independent contract review closed the Protos and Datom component audit at:

- Protos `0.28.1`, `d038d20730dc5bfad32119477be3bc8778d5ca5f`
- datom-codec `0.25.1`, `68f0bd5d0d94b69d4bb62fd1f74cd5df22f88375`

This is component closure, not full-stack approval.

## Closed findings

The conversion kinds have a common path and arity model, with associated
`Output` where required by Rust’s common method shape. `Protos::datomize`
therefore takes its explicit `Path`; this is the settled common-method arity,
not a split or an unapproved conversion kind.

Protos nodes retain their extents. The finite reader budget, byte extents,
escaped guillemets and balanced parentheses, and qualified structural heads
are covered. The public tree has an iterative drop path; its prior stale,
uncompiled legacy modules and its leaking deep witnesses are gone.

Datom covers full-text scalar preservation, bare unit variants, generic
containers, and generic enum derivation. The derive bounds handle direct
recursive, mutually recursive, and similarly named wrapper payloads without
self-referential field-bound cycles. Datom owns errors with their raising layer
and path, round-trips them through Datom text, and keeps the retained Protos
reader as the route from a Datom error path to an extent.

Projection, public Protos-to-Datom conversion, and destruction are iterative
or independently bounded. The 100,000-node construction witnesses perform real
destruction, rather than suppressing it with `mem::forget`. There is no known
old invalid public conversion route remaining.

## Evidence and limits

The implementation worker separately witnessed Datom’s 24 local tests and
remote configured-builder `nix flake check -L` passing; Protos’ remote check
also passed. The independent reviewer inspected the latest sources named
below.

Ethos6 fixtures and gates, followed by the producer generated-contract checks
repinned to final Ethos, remain required. This report makes no full-stack or
cutover approval claim.

## Sources

- Independent `/root/contract_review` review of the latest source.
- `datom-codec/crates/datom-codec-derive/src/lib.rs:18-32,75-83,117-130,161-168`
- `datom-codec/tests/core.rs:636-709`
- `datom-codec/src/composition.rs:9-166,713-734`
- `datom-codec/src/projection.rs:1-174`
- `datom-codec/src/dropping.rs`
- `protos/src/dropping.rs:1-51`
- `protos/tests/protos.rs:119-134`
- The user-inlined Vision and Intent, the authority for this realization.

## Recursive-struct correction

After this audit was first recorded, an Ethos-generated fixture exposed a
struct-side derive cycle for `Option<Box<Chain>>`. Datom `0.25.2`,
`cf7d7a7a1f2b43e97ba4c8259f2737054997acbc`, replaces struct field-type where
predicates with generic type-parameter bounds, matching the enum treatment.
Concrete and generic recursive struct round-trips now join the direct,
mutual, and wrapper enum witnesses. The local suite has 25 passing tests and
the configured remote Nix gate passed. Ethos retains the original fixture as
the cross-component witness.

## Canonical extent correction

Protos `0.28.2`, `e18abf0936f23a175ec3c554f994214fabbdf2bd`, adds the explicit
`Canonicalizing::canonicalize(&mut self)` capability. It assigns canonical
UTF-8 byte extents by an iterative structural traversal, without re-parsing or
a reader budget, and leaves parsed source extents intact until called. The
local 16-test suite and configured remote Nix gate passed. Ethos will use this
infallible seam after structural ascent; Datom must still repin this final
Protos revision before its final producer validation.

## Final producer pair and declarations

The final pre-Ethos producer pair is Protos `0.29.0` at
`aac95b0d08a4c7eb7f73c8ea18309f9e2e89315f` and datom-codec `0.25.3` at
`8380c4ca80440c5582bc9fa1cdc1190689caa983`, which pins that Protos revision.
The current declaration heads are Protos
`6845c2b84c1a4af70e628d2a072e2cedacba9912` and Datom
`b7d35ecf20b21a083fc9daaff5d236b23ac249a3`. All four producer declarations
now use `Library` roots and current public anatomy; the retired `Types` and
`Kinds` roots are removed. Final Ethos dependency-ethos and the producer
checks repinned to its landed revision remain pending.

## Declaration grammar limit

`Canonicalizable` is declared as an empty kind in the producer Ethos
manifest. Its real Rust capability, `canonicalize(&mut self)`, returns unit.
The approved Ethos grammar requires exactly one yield type for every declared
capability, while its intrinsic set has no `Unit` type. Consequently the
manifest does not falsely invent a void yield spelling or claim to describe
that capability; it records only the kind. This is a present schema-expression
limit, not a claim that the public Rust interface lacks `canonicalize`.

## Producer declaration scope

The four producer Ethos files now describe the representable conceptual and
conversion surface: structural forms, Datom forms, errors, budgets, and the
conversion kinds Ethos can state. They are not complete Rust reflection.
Borrowed reader handles, operational helper kinds, tuple-wrapper implementation
details, and unit-yield methods remain outside the current grammar. Datom's
public `Meaning` wrapper is included as its one String position, which is the
available conceptual declaration. `Box` is intentionally absent: recursive
Ethos types generate their required Rust boxing and Datom composition treats
`Box<T>` transparently.
