---
title: 88 — production components, and whether Spirit queries filter removal candidates
role: system-designer
variant: Investigation
date: 2026-06-10
---

Two questions, answered from live code (`/git/github.com/LiGoldragon/spirit`
@ `tvqukpntxvsv`, `signal-spirit` schema) and the active-repository map.

## 1. What is actually "in production"

"Production" has two distinct senses in this workspace. Keep them apart.

### Stack A — literally deployed on every node

The horizon / CriomOS deploy stack. These run on real hardware today and
have backward-compat obligations:

| Component | Path | Role |
|---|---|---|
| `horizon-rs` | `/git/.../horizon-rs` | Horizon projection source. |
| `lojix-cli` | `/git/.../lojix-cli` | Monolithic projector → CriomOS flake inputs. Pinned `4c66b8a6`. |
| `CriomOS`, `CriomOS-home`, `CriomOS-lib` | `/git/...` | OS / home / lib layers. |
| `goldragon` | `/git/.../goldragon` | `datom.nota` cluster facts. |

None of these is part of the Persona/Signal/Spirit stack. Production
fixes for *node deployment* go to `main` in those canonical checkouts.

### The Persona/Signal stack — only Spirit is in real use

The restructuring stack has "no production to protect" (AGENTS.md hard
override) — with **one** live exception: **Spirit**. The deployed Spirit
triad runs as a real daemon over a real database (the intent log we write
every session; hence `spirit-migrate-production` exists). So when the
question is "what's production for Spirit," the answer is this triad and
its build/runtime support only:

| Production (Spirit) | Repo | Notes |
|---|---|---|
| `spirit-daemon` + `spirit` CLI | `spirit` | Daemon built `--no-default-features` (NOTA-free); CLI is the only NOTA edge. `default = []`. |
| ordinary contract | `signal-spirit` | Renamed from `signal-persona-spirit`. rkyv-only by default; `nota-text` is an opt-in edge feature. |
| meta contract | `meta-signal-spirit` / in-tree `schema/meta-signal.schema` | Privileged lifecycle/config (`Configure`). |

Production Spirit daemon's runtime dependency closure (from `Cargo.toml`):
`sema-engine`, `signal-frame`, `signal-spirit`, `triad-runtime`.
`schema-next` / `schema-rust-next` are **build-dependencies only** (they
emit `src/schema/*.rs` at build time — they do not link into the daemon).
`nota-next` is `optional` and only pulled when `nota-text` is on, i.e. the
CLI. This is the schema-derived-stack exemplar: every other Persona
component is following its shape, but is **pre-production** (skeleton,
scaffold, or mid-migration) — `mind`, `router`, `message`, `introspect`,
`system`, `harness`, `terminal*`, `criome`, `cloud`, `domain-criome`,
`orchestrate`, `repository-ledger`, and all their `signal-*` /
`meta-signal-*` contracts. Treat them under the no-backward-compat rule.

## 2. Does a Spirit query filter out removal candidates / zero-certainty records?

**No — and the premise has two conflations worth correcting.**

### A normal query filters on three dimensions, and certainty is not one

`signal-spirit` defines the query as:

```
Query { TopicMatch * kind (Optional Kind) privacy_selection PrivacySelection }
```

and `Query::matches` (`spirit/src/engine.rs`, `src/store.rs:687`) is
exactly:

```rust
self.topic_match.matches(&entry.topics)
    && self.kind.as_ref().is_none_or(|kind| &entry.kind == kind)
    && self.privacy_selection.matches(&entry.privacy)
```

Topic, kind, privacy. That's all. The **filtered** paths —
`Observe` / `Count` / `PublicRecords` / `PrivateRecords` /
`SubscribeIntent` — all run through this. **Certainty is never consulted.**
A `Zero`-certainty record comes back from an ordinary query exactly like a
`Maximum` one.

`Lookup` is **not** a filtered path (operator correction): it reads
directly by exact identifier (`store.rs`: `SemaReadInput::Lookup → entry_by_identifier`),
bypassing `Query::matches` entirely. That is correct and must stay — a
`Zero`-certainty (removal-candidate) record stays reachable by exact id for
review/restore even once the default floor hides it from browsing.

(Operator verified against live production spirit `0.4.0`: a 3-field
`Count` works; a 4-field certainty query is rejected. Certainty filtering
is confirmed not live.)

(An `Entry` carries two independent `Magnitude` fields: `privacy`
— which queries *do* filter on — and `magnitude`, which is the
*certainty* and which queries ignore. `ChangeCertainty` only writes
`entry.magnitude`; the certainty value is otherwise read only by
`production_migration` import and an unused `magnitude_weight()`.)

### "Removal candidate" is not a stored mark, and not tied to certainty

There is no persistent "removal candidate" flag in the database. "Removal
candidate" exists only transiently as **the set of records matching a
`RecordQuery` you explicitly hand to the `CollectRemovalCandidates`
operation**, which archives those matches to a separate DB and deletes
them from the live log (`RemovalCandidatesCollected { removal_archive_records,
removed_identifiers, skipped_removal_candidates }`). Candidacy is defined
by *that query* — topic/kind/privacy — run on demand, not by a record's
certainty and not by any standing mark.

### Consequence: the behavior you described doesn't exist today

- Zero certainty does **not** auto-mark a record for removal.
- Removal candidacy is **not** defined by certainty.
- Because `RemovalCandidateCollection` wraps the same `Query` (no
  certainty field), you currently **cannot even express** "collect
  everything at `Zero` certainty" through the contract.
- Ordinary queries do **not** hide low/zero-certainty records.

If the *intent* is "a record dropped to `Zero` certainty becomes a removal
candidate and ordinary queries should stop returning it," that is a
genuine design gap, not current behavior. It would need either a certainty
dimension on `Query` (e.g. a `CertaintySelection` mirroring
`PrivacySelection`, with a default floor that excludes `Zero`), or an
explicit certainty-driven sweep. This is a psyche-intent decision — see §3.

## 3. Intent recorded — a new runtime capability (foreshadowed in the contract)

Psyche decision recorded as Spirit record `oj3i` (the
zero-certainty-is-the-removal-candidate decision): Zero certainty means a
record has no value, so it is the removal-candidate state; the default
Observe query excludes Zero-certainty records; `Query` gains a certainty
selection with a floor defaulting to `Minimum` (excludes Zero); seeing
Zero records requires an explicit certainty selection.

### Correction: no data loss, and the daemon never had this filter

An earlier draft of this report (and my first chat message) said the
certainty filter "regressed / was dropped during the schema-emission
rewrite." **That was wrong, and I corrected it after checking git
history.** The accurate picture, verified by pickaxe:

- `git log -S 'CertaintySelection' -- src/` → **0 commits**.
  `git log -S 'certainty_selection' -- src/` → **0 commits**. The Spirit
  **daemon's** source has *never*, in this repo's history, filtered an
  Observe query by certainty. It was not dropped during emission — it was
  never there in the running daemon.
- `CertaintySelection` exists only in the **`signal-spirit` contract
  crate** — a richer query *design* that the daemon never wired up. That
  crate is now used by the daemon only for `SpiritDaemonConfiguration`
  and as the legacy-record source in `production_migration.rs`. So this
  is a contract-ahead-of-implementation gap, not a lost feature.

| | `signal-spirit` crate (design only, never the live filter) | In-tree emitted `spirit/schema/signal.schema` (**what the daemon runs**) |
|---|---|---|
| Query | `RecordQuery { …, certainty_selection, recorded_time_selection, …, mode }` | `Query { topic_match, kind, privacy_selection }` |
| Certainty filter | spelled (`removal_candidates() = Exact(Zero)`) but unused by the daemon | absent |

**No certainty data was lost.** Certainty lives in `Entry.magnitude`,
which is persisted in `StoredRecord { record_identifier, entry: Entry }`,
written at `Record` time, mutated by `ChangeCertainty`
(`store.rs:432`), and **explicitly preserved** by the production migration
(`production_migration.rs`: `magnitude: Self::magnitude_from(self.entry.certainty)`,
`Zero → Zero` etc.). Every record still carries its certainty; what's
absent is only the *query-time filter* over it.

So "feature parity" between the pre- and post-emission **daemon** holds on
this axis: neither filtered Observe by certainty. The psyche's intent is
therefore a **genuinely new** runtime capability (foreshadowed by the
contract crate's unused design), not a restoration. (`active-repositories.md`
calls `signal-spirit` the "active ordinary wire contract" — per `tb9h`
that is the *correct* target; the daemon violates it by emitting its own
in-tree type copy instead of linking the contract. The doc is right; the
daemon is wrong.)

### Implementation plan — the structural fix comes first (record `tb9h`)

Psyche constraint `tb9h`: **all wire/signal types come from the
`signal-spirit` contract repo** — it is the single source the daemon and
peers link against, per the component-triad. spirit currently violates
this: it emits `Input/Output/Query/Entry/Magnitude` in
`crate::schema::signal`, and hand-written `signal-spirit` (2044 lines, no
`build.rs`) has diverged. `criome` already does it right — it imports
`CriomeRequest/CriomeReply/CriomeFrame` from `signal_criome`.

So the certainty selection does **not** go into the daemon's in-tree
schema. The work is two-staged:

**Stage 1 — converge spirit onto the triad (the real fix `tb9h` names):**

1. Schema-emit the signal contract **in `signal-spirit`** (give it the
   `build.rs` + `schema/` emission flow; it's currently hand-written), so
   the wire types `Input/Output/Query/Entry/Magnitude` are emitted there.
2. Make `spirit` depend on `signal-spirit` for those wire types and
   **delete the in-tree type emission** — the daemon's local
   `schema/signal.schema` keeps only the runtime planes
   (`SignalEngine`/Nexus/Sema/daemon spine) that *consume* the contract,
   matching the criome pattern and component-triad doctrine.

**Stage 2 — add the certainty floor (in the contract, per `oj3i`):**

3. In `signal-spirit`'s emitted contract: add `CertaintySelection [Any
   (ExactCertainty ExactCertainty) (AtMostCertainty AtMostCertainty)
   (AtLeastCertainty AtLeastCertainty)]` + the three `*Certainty Certainty`
   wrappers (parallel to privacy's `Exact/AtMost/AtLeast Privacy`), and
   add `certainty_selection CertaintySelection` to `Query`. (The legacy
   hand-written `signal-spirit` already spelled `CertaintySelection`/
   `removal_candidates() = Exact(Zero)` — reuse that shape.)
4. Daemon filter: `Query::matches` gains
   `&& self.certainty_selection.matches(&entry.magnitude)`; add
   `default_observation_certainty() = AtLeast(Minimum)` (excludes Zero)
   and `removal_candidates() = Exact(Zero)`.
5. Apply the default floor to **every filtered path, not just `Observe`**
   (operator): `Observe`, `Count`, `PublicRecords`, `PrivateRecords`, and
   `SubscribeIntent` all default to `AtLeast(Minimum)`. `Lookup` is
   exempt — exact-id reads bypass the floor so a Zero record stays
   reviewable/restorable. Default construction (CLI default,
   `RecordSelection → Query`) sets `AtLeast(Minimum)`; removal-candidate
   review uses explicit `Exact(Zero)`. Add coverage across all five
   filtered paths: Zero excluded by default, visible with `Exact(Zero)`,
   and still `Lookup`-able by id.
6. Operator integrates to `main` + redeploys daemon **and** CLI together
   (matched pair; no stored-data migration — `Entry.magnitude` already
   exists and is preserved).
7. **Fix `spirit/INTENT.md` first (operator).** Line 3 still claims the
   repo is "intentionally separate from production `spirit`/`persona-spirit`
   … without disturbing the deployed substrate." That contradicts reality
   — this repo *is* the live `0.4.0` substrate. Correct it on `main`
   (operator owns spirit main) before the repo docs are trusted as
   architectural evidence. (Line 107's `Observe`/`Lookup`/`Count`
   grouping is likewise imprecise — `Lookup` is by-id, not a query plan.)

**Execution: psyche chose spec-only.** This report is the spec; operator
picks it up on `main`. Designer does not author code now. Note Stage 1 is
the larger task — it's a triad-convergence / schema-emission migration of
the production component, not a one-field add.

Open scope forks (psyche's call): (a) certainty only, or also add the
contract-only `RecordedTimeSelection` / `ObservationMode` to the live
query while we're in here; (b) leave the legacy `signal-spirit` crate
as-is (migration/config only) or schedule its reconciliation/retirement.
