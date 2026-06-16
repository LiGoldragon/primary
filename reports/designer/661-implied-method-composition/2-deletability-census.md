# 661/2 — The deletability census (does composition delete meaningful hand-wiring?)

The thesis is only worth the machinery if a *meaningful* fraction of real hand-written methods
are genuinely composition-of-primitives. Two agents censused the live components. The
adversarial pass then independently tried to refute the "meaningful" claim against the same
code and **could not** — this is the one core claim that survived intact.

## The numbers

| Target | Sampled | Composable | Business logic |
|---|---|---|---|
| spirit (Nexus engine, accessors, conversions, store, guardian) | 37 | 15 | 12 |
| triad-runtime + signal-spirit + hand newtypes | 38 | 22 | 18 |

By *raw count* the composable fraction is higher than the sample ratios, because the
newtype/From/Deref/predicate layer **repeats per type and per triad leg**. Concrete, verified:

- `spirit/src/engine.rs:767-861` — **12 consecutive `Deref` impls**, every body `self.payload()`.
- `signal-spirit/src/lib.rs:1035-1231` — **~11 `Deref` + ~3 `Display` + ~10 `PartialEq` +
  `PartialOrd`/`Ord`** (~25 trait impls), every body `self.payload()` or `self.payload() == other`.
- `spirit/src/plane.rs` — **all 8 cross-namespace conversions** are `Self::new(x.payload())`
  or variant-parallel re-wraps.
- `OperationKind::from_input` (`signal-spirit/src/lib.rs:463`) — a **24-arm** name-for-name
  enum-tag projection.
- `From<Action> for NextStep` (`reaction.rs:112`), `CommandSemaWrite::into_sema_write_input`
  (`nexus.rs:240`) — parallel-variant re-wraps.

## The sharp boundary lands where it should

Both censuses confirmed the boundary falls **precisely at the first `guard_*` / `store.*` /
cross-product call**. From there everything is genuine business logic and stays hand-written:
`apply_effect`'s four-way `Result` dispatch, `decide_signal_arrival`'s routing + side effects,
the guardian's retry/socket/parse loop, base36 minting arithmetic, `blake3` digests, store
mutations with archive writes and dedup, the `Query`/`Selection` matchers, the `validate`
family, `Magnitude::rank`/`next`, `Description::keywords`.

The instructive case is `decide_signal_arrival`: ~20 of its arms *are* constructor
compositions, yet the body also calls `self.observer_tap_table.observe_operation(...)` — not a
primitive — so the **whole method is correctly business logic**. The composition is real; the
*choice of which composition* is irreducible policy. That distinction is the whole point.

## The honest caveats (both census agents raised them)

1. **Line-count saved is modest; the win is the repetition tax, not the engine.** The
   composable methods are individually tiny (1-5 lines). The bulk of hand-written *code* is the
   business logic, which is untouched. What composition deletes is a *recurring, copy-pasted*
   tax that re-appears in every component and every triad leg — real and worth it, but "not a
   revolution."

2. **Much of the Deref/payload wall is better deleted at the source.** A large part of the
   composable mass exists only because those newtypes (`engine.rs` `OriginRoute` et al., the
   subscription token, the cross-namespace triplet) are **not yet schema-declared**. Declaring
   them lets the *newtype emitter* emit the standard trait impls (`Display`/`PartialEq`/`Ord`)
   from fixed per-trait templates — the way it already emits `Deref` — which is *cheaper than a
   composition interpreter* for that specific class. Composition's distinctive value is the
   **variant-isomorphism** class (the 24-arm `from_input`, the `plane.rs` re-wraps), which a
   per-trait template cannot express.

3. **Runtime types outside the schema are out of reach.** `triad-runtime`'s
   `frame.rs`/`streaming.rs`/`runner.rs` accessors *look* composable but sit on hand-written
   runtime types. Reaching them means bringing those types under the schema — a scope
   expansion, not a free win.

## Verdict

> *"Not trivial — it deletes the entire conversion/accessor/Deref/predicate layer plus the
> variant-routing matches, which is a real and repetitive chunk of every component — but it
> does NOT touch the engine's decide/handle judgment, the guardian, or the store, which is
> correct and is the point. The win scales with component count."*

The composition model deletes meaningful, recurring hand-wiring and leaves every genuine
decision hand-written. That is exactly the boundary `d3r2`/`5hjv` intend.
