# Datom output vision

This flow acquires the living psyche's vision for Datom syntax after witnessing `orchestrate 'Observe.Locks'` render `Observed(Locks(LockSnapshot { locks: Locks([]) }))`.

Remembered: ac1e9ec8 — depth 2. Its direct psyche corrections settle expected-type-driven positional data, omitted struct field/type names, curly quotes for plain strings, parentheses reserved for Meaning, and Datom as Signal's textual edge form; its proposed complete reply syntax was never approved.

Remembered: 01a03d6e, 01a03eda — depth 1. The interface is verb-oriented; `Observe` is the request root, and `Observe.Locks` superseded the earlier `Observe.Locks.Current` proposal.

## Witnessed

- The ordinary client prints `OrchestrateReply` with Rust `Debug` (`println!("{reply:?}")`); the live test asserts that exact debug string.
- Only `[]` is already valid Datom. The surrounding constructor parentheses, Rust type name, field label and colon, and transparent newtype name are not Datom.
- The visible nesting reflects the authored chain `Observed → Observation::Locks → LockSnapshot → locks: Locks → Vec<Lock>` rather than recursive data.

## Open

- Ruled provisionally: the empty observation reply textualizes as `Observed.Locks.[]`; the living called this “good enough for now.”
- Failing-first witness: the focused ordinary-client test expected `Observed.Locks.[]` and received the old Rust Debug rendering.
- Partial realization pushed in ethos-monolith: `7520bbb191be` generates typed Datom reply roots; `b73d535118c2` projects nested single-record enum Heads. No consumer cutover is committed yet.
- Reality returned a design blocker: Ethos enum payloads currently accept only a bare type symbol, so the approved direct `Vector<Lock>` payload is rejected before generation. Rule whether enum payloads accept full type expressions, or whether a transparent named wrapper remains provisionally.
- After that ruling, finish the Signal revision/package bumps, coordinated upgrade, consumer pins, deployment, and proof.
