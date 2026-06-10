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

Topic, kind, privacy. That's all. `Observe` / `Count` / `PublicRecords` /
`PrivateRecords` / `Lookup` all run through this. **Certainty is never
consulted.** A `Zero`-certainty record comes back from an ordinary query
exactly like a `Maximum` one.

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
explicit certainty-driven sweep. This is a psyche-intent decision — see
the open question in chat.
