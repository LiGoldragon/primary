# Datom output vision

This flow acquires the living psyche's vision for Datom syntax after witnessing `orchestrate 'Observe.Locks'` render `Observed(Locks(LockSnapshot { locks: Locks([]) }))`.

Remembered: ac1e9ec8 — depth 2. Its direct psyche corrections settle expected-type-driven positional data, omitted struct field/type names, curly quotes for plain strings, parentheses reserved for Meaning, and Datom as Signal's textual edge form; its proposed complete reply syntax was never approved.

Remembered: 01a03d6e, 01a03eda — depth 1. The interface is verb-oriented; `Observe` is the request root, and `Observe.Locks` superseded the earlier `Observe.Locks.Current` proposal.

## Witnessed

- The ordinary client prints `OrchestrateReply` with Rust `Debug` (`println!("{reply:?}")`); the live test asserts that exact debug string.
- Only `[]` is already valid Datom. The surrounding constructor parentheses, Rust type name, field label and colon, and transparent newtype name are not Datom.
- The visible nesting reflects the authored chain `Observed → Observation::Locks → LockSnapshot → locks: Locks → Vec<Lock>` rather than recursive data.

## Open

- The reply must acquire a Datom textual contract; its exact nested-enum form is not yet ruled.
- Determine which of `Observation::Locks`, the one-field `LockSnapshot`, and the transparent `Locks` newtype carry enduring meaning and which should disappear from the terminal ontology.
- After the living rules the anatomy, realize and prove the resulting contract.
