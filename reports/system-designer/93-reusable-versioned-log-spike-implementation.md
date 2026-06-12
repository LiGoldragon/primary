# 93 — Reusable version-controlled Sema-state library: the concept-branch spike

A designer concept implementation that makes report 92's central candidate
*runnable*. It is a spike for joint review, not an integration — the
psyche asked for a context report first, then "try an implementation… on
concept branches" while an operator builds a real one on a component's
main, "and then we'll be able to look at this together."

## Where it lives

- **Repo / branch:** `sema-engine`, feature branch
  `reusable-versioned-log-spike`, pushed to origin
  (`git change 92c5634f`, the version-controlled-state spike).
  PR-open link: `github.com/LiGoldragon/sema-engine/pull/new/reusable-versioned-log-spike`.
- **Worktree:** `~/wt/github.com/LiGoldragon/sema-engine/reusable-versioned-log-spike`
  (designer discipline: feature branch in `~/wt`, canonical checkout stays
  on main for the operator).
- **Code:** `src/versioned/` (9 modules, ~1300 lines incl. the demo/tests).
  `blake3` added as a dependency.

## What it implements — Option E from report 92 §4

The reusable core, all behaviour on owning nouns (no free functions
outside `cfg(test)`, typed `VersionedError` enum, no stringly fallback):

- **Identity** (`identity.rs`): `SchemaHash` (the typed decoder selector
  that replaces the catalog's bare `table_name: String`), `EntryDigest`
  (blake3, hash-chain link), `CommitSequence` (the ordered cursor that
  stays *beside* the digest — report 92 §1), `RecordKey`.
- **`ReplayEnvelope`** (`envelope.rs`): the authoritative entry —
  "**typed in motion, erased at rest**." Payload is opaque rkyv bytes +
  a `SchemaHash`; it is a *concrete* type, so it derives rkyv trivially
  and stores directly in a `sema::Table<u64, ReplayEnvelope>`, exactly as
  `sema-engine` stores its own `CommitLogEntry`. Hash-linked via
  `previous_digest`; `verify()` checks both integrity and chain linkage.
- **The genericity seam**: a **sealed `RecordFamily`** trait (one concrete
  rkyv type set per family; `encode`/`decode` required so rkyv bounds land
  on the concrete type) and a per-component **`ComponentRecord` closed
  sum** whose `decode` is a **closed match with no fallback**.
- **`MaterializedView<Record>`** (`view.rs`): the rebuildable view (redb
  demoted to a fold over the log), with the **full 32-byte blake3 state
  digest** the report (§5) demanded as the correctness oracle — not
  spirit's truncated `u64`.
- **Migration** (`migration.rs`): `SchemaTransition` as a first-class
  typed log entry + a component-authored `Reducer` invoked at replay, held
  in a `ReducerSet`.
- **`VersionedLog`** (`log.rs`): the trait whose default methods
  (`commit_assert` / `commit_retract` / `commit_transition` / `rebuild` /
  `next_coordinates`) are the reusable core, with **two backends** for the
  experiment:
  - **`SameFileLog`** — the payload-bearing log as a table in one `sema`
    redb file, written in a single transaction (**Option A**, free
    atomicity).
  - **`FrameFileLog`** — a byte-shippable append-frame file, each frame a
    length-prefixed rkyv archive (**Option C**); backup is a literal byte
    suffix copy.

## What it empirically validates (6 tests, all green)

`cargo test` green; the existing `sema-engine` suite intact
(`dependency_boundary` 8/8, `engine` 22/22, and the rest), no warnings.

1. **`same_file_and_frame_file_rebuild_to_identical_digest`** — the core
   experiment: the *same* multi-family input (two entries + a referent)
   through both backends rebuilds to an **identical state digest** and
   head. The same-file vs separate-file choice is observationally
   transparent at the view boundary — which is what makes "test both" a
   real, decidable experiment rather than a fork.
2. **`schema_transition_migrates_via_reducer`** — a v1→v2 transition
   replayed through the reducer yields a state digest **identical** to a
   world built directly from post-migration v2 records; and replay
   **without** the reducer fails loudly (`MissingReducer`). Migration as a
   typed log entry works end to end.
3. **`unknown_schema_hash_is_rejected_not_fallen_back`** — the knife-edge
   (§6): an unknown schema-hash is a hard `UnknownSchemaHash` error, never
   a silent generic-record decode. The closed sum holds.
4. **`frame_log_ships_as_byte_suffix`** — copying the frame file's bytes
   to a fresh peer reproduces the source exactly: the cheapest backup unit.
5. **`tampered_chain_is_detected_on_rebuild`** — flipping a byte on disk is
   caught at rebuild (digest mismatch / broken link).
6. **`retract_removes_record_in_both_backends`** — retract semantics hold
   on both arms.

### The load-bearing implementation finding

The rkyv-generics quagmire the report worried about (HRTB serializer
bounds resisting `dyn` and cluttering generic sites) **never appears** —
because the stored `ReplayEnvelope` is *concrete* (erased `Vec<u8>`
payload) and each family's `encode`/`decode` is concrete at its impl site.
Genericity lives only in the closed-enum decode step and the one
`MaterializedView<Record>` type parameter. This is the practical reason
Option E is tractable, and a concrete steer for the operator.

## What it deliberately does NOT do (spike boundaries)

Honest limits, so the spike isn't mistaken for the design:

- **No kernel inversion.** The spike is a self-contained `src/versioned/`
  module; it does **not** rewire `sema-engine`'s real `Engine` /
  `CommitLogEntry`, and does not demote the live redb tables. Whether to
  invert the kernel remains the `sema`/`sema-engine` owners' call (report
  92 §7), unchanged.
- **The per-component closed enum is hand-written under `cfg(test)`**,
  standing in for the production derive macro that would emit the
  `Sealed` + `RecordFamily` impls + the closed enum. The sealed trait is
  `pub(crate)` here; production would be `#[doc(hidden)] pub` + a derive.
- **No server mirror, ack policy, or RPO** — the local event-sourcing half
  only. The remote durability contract (the part closest to 29pb's
  "atomic, server-backed") is modelled in the report, not the code.
- **No checkpoint / compaction** — the report's named danger zone (§3
  lesson 3) is untouched; the log is unbounded here.
- **`SameFileLog` stores only the log table** — it demonstrates the single
  redb transaction but not yet "log + materialised view committed in the
  *same* txn," because the view is in-memory in the spike.
- **The demo families are spirit-*shaped*, not spirit's real types** — and
  `mind` / `criome` (report 92 §6's under-grounded consumers) are not
  exercised at all. The genericity claim is only as strong as the most
  awkward real consumer, still unsurveyed.
- **No benchmark / crash harness** — the report's measurement matrix
  (commit latency by fsync count, rebuild time, degraded-mode RPO) is
  *not* run; the spike proves correctness, not the performance trade.

## Hand-off

For the **operator's** parallel main-branch implementation: this branch is
a working reference for the noun set (`RecordFamily`, `ComponentRecord`,
`ReplayEnvelope`, `SchemaHash`, `MaterializedView`, `Reducer`,
`VersionedLog`) and, most usefully, for *how to stay typed-and-generic
without the rkyv-HRTB tax* and *how to hold the closed-sum knife-edge*. It
is a spike to adapt, not a crate to merge: the real work lands against
`sema-engine`'s actual `Engine`/commit-log per the owners' kernel-inversion
decision.

The open decisions are unchanged and remain the owners': kernel inversion,
the library's home layer, the digest function, the ack/RPO policy, and
same-file-vs-separate-file as the *production* choice (the spike shows both
are correct; it does not pick). `blake3` here reuses the criome/spirit
hash choice rather than introducing a third scheme (report 92 §6).

## Correction (system-operator audit 211)

System-operator audit `reports/system-operator/211-Audit-sema-versioned-log-sd-proposal.md`
rightly flags that §"What it empirically validates" overstates the
same-file-vs-separate-file result. The identical-digest test is **only the
first semantic-equivalence witness**, not proof the production backend
choice is "decidable": it does not exercise duplicate-send, expected-head
validation, partial-suffix sync, pruned-head recovery, checkpoint restore,
or crash injection at the fsync boundary. Read every "decidable / decided
by measurement" phrasing in this report as "first equivalence witness; the
production choice still needs the durability tests above." The audit and
the designer response (report 94) also note the operator's mainline is
ahead of this spike on the harder same-transaction invariant (versioned
entry + domain record + metadata log committed in one redb transaction),
which the spike's in-memory view does not demonstrate.
