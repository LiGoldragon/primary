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
