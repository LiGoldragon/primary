# Skill — Rust storage and wire (redb + rkyv)

*redb holds component state that must survive a restart. rkyv
is the binary contract between Rust components — both for the
durable values inside redb and for the wire bytes that travel
between processes.*

---

## What this skill is for

Use this skill when designing the durable-state or inter-process
surface of a Rust component. Pairs with `skills/contract-repo.md`
(how the wire contract is organized in repos) and
`skills/rust/methods.md` (where the typed records that travel
through this surface come from).

This is the *living* discipline for these two tools. It
accumulates patterns and anti-patterns over time. When a new way
of misusing redb or rkyv comes up, name it here so it stops
reappearing. When a clean pattern gets validated, add it. The aim
is correct code *by default*, with the surface area of bad
patterns shrinking as the document grows.

For the index pointing at the wider Rust discipline, see
`skills/rust-discipline.md`.

---

## What goes where

The first decision when designing a boundary is: **what
crosses it, and to whom does the other side answer?**

| Boundary | Format | Why |
|---|---|---|
| In-process: actor ↔ actor, method ↔ method | typed Rust values | The type system is the schema. No serialization until something leaves the process. |
| Process ↔ process: daemon ↔ harness, IPC, sockets, pipes between Rust components | **rkyv** archives | Zero-copy reads, content-addressable canonical bytes, bytecheck validation. The binary contract is the wire. |
| Component ↔ disk: queues, transition logs, harness bindings, transcripts, snapshots | **redb** tables of rkyv values | Single embedded store, crash-consistent, snapshot reads, no separate server. |
| Component ↔ human: CLI invocations, debug prints, audit dumps | NOTA text projection | Human-readable; projected from the typed record, never the source of truth. |
| Component ↔ legacy external system | the format the legacy demands | Adapters live at the edge. Internally, the component works in typed Rust; external bytes round-trip through one explicit codec at the boundary. |

The rule: **rkyv is the binary contract for everything
between Rust components.** NOTA is the projection format
when the other side is a human. JSON / serde appears only
at external boundaries that demand it (legacy APIs).

---

## redb — the durable store

Persistent component state lives in redb: router queues,
harness bindings, transition logs, coordination state, anything the
running component mutates and re-reads.

- **Persistent state lives in redb.** Not flat files,
  not JSON files, not bare blobs.
- **Values are rkyv-archived bytes.** Not serde-JSON,
  not hand-rolled binary, not text.
- **One redb file per component.** Each component owns
  its own database. No shared cross-component database.
- **Component state goes through the component-owned Sema layer.**
  Do not create ad hoc registry files, sidecar indexes, JSON
  catalogs, lockfile-like stores, or text manifests for state the
  component mutates and re-reads. If the data is component state,
  declare it as typed Sema tables owned by that component.

```rust
// Wrong — flat-file log as the durable store
fn append_claim(path: &Path, claim: &Claim) -> Result<()> {
    let line = claim.to_text()?;
    OpenOptions::new().append(true).open(path)?.write_all(line.as_bytes())?;
    Ok(())
}

// Right — typed record archived with rkyv, stored in redb
const CLAIMS: TableDefinition<&str, &[u8]> = TableDefinition::new("claims");

let txn = self.db.begin_write()?;
{
    let mut table = txn.open_table(CLAIMS)?;
    let bytes = rkyv::to_bytes::<rancor::Error>(claim)?;
    table.insert(role.as_str(), &bytes[..])?;
}
txn.commit()?;
```

---

## rkyv — the binary contract on the wire (signaling)

The workspace term for the rkyv-archive-on-the-wire pattern
is **signal**, taken from the canonical reference
`~/primary/repos/signal`. The verb is **to signal** — a
component signals another by sending a length-prefixed rkyv
archive on the wire. "Signaling" describes process-to-process
communication in this workspace; "the signal pattern" describes
the discipline this section defines. Cross-machine signaling
(future networked transport) is a deferred extension; today,
signaling is local IPC over Unix sockets, TCP, pipes, or mmap.

When two Rust components talk across a process boundary
— Unix domain socket, TCP, named pipe, message bus,
mmap region — the bytes on the wire are rkyv archives.
Both ends compile against the *same* rkyv feature set
(see lore's `rust/rkyv.md`); they exchange `Archived<T>`
for some shared frame type `T`; framing is a length
prefix per archive.

```rust
// Wrong — JSON between Rust components
let body = serde_json::to_vec(&request)?;
stream.write_all(&body)?;

// Wrong — ad-hoc binary
stream.write_all(&request.id.to_le_bytes())?;
stream.write_all(request.payload.as_bytes())?;

// Right — rkyv frame, length-prefixed
let archived = rkyv::to_bytes::<rancor::Error>(&request)?;
stream.write_all(&(archived.len() as u32).to_be_bytes())?;
stream.write_all(&archived)?;

// Reader (zero-copy validate-on-receive)
let archived = rkyv::access::<ArchivedRequest, rancor::Error>(&buf)?;
let id = archived.id;        // direct read, no allocation
```

The wire schema *is* the framing. Both parties know the
same `Frame` type; the bytes are `Archived<Frame>`. The
discipline:

- **The shared `Frame` type lives in a contract repo.**
  When two or more components speak the same wire, the
  record types are not re-defined per consumer. They live
  in a dedicated crate that every consumer pulls as a
  dependency. See `~/primary/skills/contract-repo.md` for
  the pattern (what belongs in a contract crate, the
  layered-effect-crate shape, when to introduce one).
  `signal` (`~/primary/repos/signal`) is the canonical
  worked example.
- **One frame type per channel.** A socket between two
  components carries one shared `Frame` enum; new
  request kinds are new variants, not new channels.
- **Same feature set both ends.** A crate that adds or
  drops an rkyv feature (`little_endian`,
  `pointer_width_32`, `unaligned`, `bytecheck`) breaks
  archive compatibility silently. Pin the feature set
  exactly per lore's `rust/rkyv.md`.
- **Validate on receive.** Use `rkyv::access` (or
  `from_bytes`) which runs bytecheck. Don't read fields
  out of unvalidated buffers.
- **Newtype the wire form.** `WirePath(Vec<u8>)` over
  `PathBuf`; platform-dependent stdlib types don't
  archive deterministically.
- **No `serde_json` between Rust components, ever.**
  JSON erases the schema; it appears only at external
  boundaries that demand it.

The eventual-Criome direction makes this concrete: the messaging
substrate that lets Persona and the eventual Criome merge is rkyv
on the wire. ("Criome" here means the eventual universal computing
paradigm — see `~/primary/ESSENCE.md` §"Today and eventually" — not
today's `criome` daemon.) That convergence works only because both
sides agree on the same archive contract today.

---

## NOTA — the human-facing projection

NOTA is the project's text syntax. Nexus is a NOTA-using
request/message surface, not a second syntax. In practice,
when request or message text is discussed, it usually means Nexus
records written in NOTA syntax. NOTA is **not the wire between Rust
components.** It is what a typed record *projects to* when a human,
a CLI, or a git diff is on the other side.

- A `Lock` record exists as a typed Rust value. It
  archives to rkyv inside redb. It projects to NOTA
  when written to a `<role>.lock` file. The text
  projection is regenerated from the record; the record
  is never reconstructed *from* the text by parsing
  inside the daemon.
- The CLI form `orchestrate '(ClaimScope ...)'` takes
  one NOTA record on argv (so a human can type it) and
  prints one NOTA record on stdout (so a human can read
  it). Inside the binary, the value travels as typed
  Rust.
- A convenience CLI such as `message` may hide a common Nexus
  wrapper from the user. It still constructs a typed NOTA record
  shape and stays within NOTA syntax.
- Debug dumps, audit logs, error renderings — all NOTA
  projections of typed records.

The asymmetry: humans use NOTA, machines use rkyv. The
codec at the boundary is `nota-codec`; it is the *only*
text codec each crate ships. No second project-wide text
format.

---

## Patterns and anti-patterns

This table is the accumulation surface — when a new
shape comes up in review, add the row.

### Anti-patterns

| Anti-pattern | What it looks like | Why it's wrong | Replace with |
|---|---|---|---|
| Flat-file log as durable state | Append-only `state.log` re-read on startup | No transactions, no atomic updates, parser races writer | redb table with rkyv values |
| Ad hoc registry file as component state | `registry.json`, `components.nota`, or a sidecar text index re-read on startup | Splits truth away from the component's typed store; no transaction boundary, schema guard, or authoritative reader | Component-owned Sema tables in the component's redb |
| JSON between Rust components | `serde_json::to_vec` → socket | Schema erased; can't pattern-match on archive bytes; bytecheck unavailable | rkyv frame + length prefix |
| Ad-hoc binary serialization | Hand-written `to_le_bytes` chains | No schema validation; subtle byte-order bugs; rewriting rkyv badly | rkyv archive |
| NOTA text on the inter-component wire | Daemon ↔ daemon over UDS using NOTA records | NOTA is for human/CLI projection; using it inter-process means re-parsing canonical text in the hot path | rkyv frames; NOTA stays the CLI/lock-file form |
| Storage actor as namespace | `StorageActor` that owns the redb handle and answers "store this" / "fetch that" for everyone | Verb-shaped; the actor owns *storing*, not domain data; each domain actor should own its tables | Each domain actor opens its own tables on the shared `Database` |
| `Arc<Mutex<Database>>` shared across actors | Coarse lock around the whole DB | Defeats redb's transaction model; serializes all writers | One actor per logical data domain; pass values, not handles |
| Blocking work inside a normal actor handler | Handler sleeps, polls, waits on a mutex, runs a command, or performs blocking IO | The actor's mailbox stops receiving pushes; the hidden wait becomes the real lock | Dedicated supervised IO/command/worker actor or actor pool |
| Public ZST actor noun | `ClaimNormalizer` is empty and exported as the domain actor | The public actor name is a label; verbs drift onto the wrong noun | Kameo's `Self IS the actor` shape: put fields on the actor type, methods on `&mut self`; consumers reach for the typed `ActorRef<ClaimNormalizer>` |
| Reading a record from text in the daemon | `Record::from_nota(disk_text)?` inside the running component | The text is a projection, not the source. Drift between typed state and disk text silently | Daemon owns the typed record; text is only a boundary projection |
| Mixed feature set across crates | One crate has `unaligned`, another doesn't | Archives produced by one don't validate in the other; failure is silent (wrong values, not parse error) | Pin the exact rkyv feature string per lore |
| Reordering struct fields casually | Renaming + reordering in one PR | rkyv archives change layout on field reorder within 0.8 — old data unreadable | Append-only fields; treat any layout change as a coordinated upgrade |
| `anyhow` / `eyre` at component boundaries | `Result<T, anyhow::Error>` on a `pub fn` | Erases the typed-failure discipline; callers can't pattern-match | crate's own `Error` enum via thiserror |

### Validated patterns

| Pattern | When to use | Notes |
|---|---|---|
| `TableDefinition<&str, &[u8]>` with rkyv-encoded value | Most component tables | Key shape is domain-typed (e.g. `RoleName`, `MessageId.as_str()`); value is rkyv bytes |
| Single `Frame` enum per channel | Inter-component sockets | New variants for new requests; never a second channel for "the new thing" |
| Length-prefixed framing | TCP / UDS streams | 4-byte big-endian length, then the archive |
| `rkyv::access` on the read path | Hot-path reads where ownership isn't needed | Returns `&Archived<T>`; zero allocation |
| Version-skew guard at boot | Any persisted store or long-lived socket | Known-slot record `(schema_version, wire_version)`; hard-fail on mismatch |
| Sync façade on actor `State` | Tests for components that own redb + rkyv | Per lore's `rust/testing.md` |
| Newtype around platform-fragile stdlib types | `PathBuf`, `OsString`, `SocketAddr` on the wire | `WirePath(Vec<u8>)` shape; deterministic across platforms |

---

## Named exceptions — text-on-disk that stays text

The rule is about *state the component mutates and
re-reads* and *bytes between Rust components*. Some
text-on-disk forms stay text by design and are not state
in the redb sense:

- **Lock-file projections** (per
  `~/primary/protocols/orchestration.md`).
  `<role>.lock` files are human-readable runtime
  coordination state, gitignored — they exist on disk for
  agents to read with `cat` or `tools/orchestrate status`,
  not in version control. The redb store is the in-process
  truth; the lock file is the outward projection
  regenerated from the record.
- **Configuration files.** `Cargo.toml`, `flake.nix`,
  per-repo configs. Inputs, not state.
- **Reports and prose docs.** Markdown is markdown.
- **Interchange artifacts.** A NOTA-line file shared
  across components for one-shot ingestion is
  interchange, not the running component's state.
- **Logs for human eyes.** A line-oriented audit log
  intended for a human reading `tail -f` is a
  projection. The structured log a component re-reads
  on restart is not — that lives in redb.

If a component owns the data and mutates it during
operation, it lives in redb + rkyv. If a component
sends bytes to another Rust component, those bytes are
rkyv archives. The named exceptions above don't satisfy
either condition.

---

## Schema discipline

rkyv archives are schema-fragile. Adding, removing, or
reordering fields changes the archive layout. The
disciplined consequences:

- **No silent backward compatibility.** Old archives
  don't read into new types and vice versa.
- **Version-skew guard.** A known-slot record carrying
  `(schema_version, wire_version)`, checked at boot.
  Hard-fail on mismatch. rkyv's own version handling is
  not enough.
- **Treat schema changes as coordinated upgrades.** A
  field reorder is a breaking change; a field addition
  is too, in 0.8. Plan rollout across every consumer.

For the tool-level details (the canonical feature set
character-for-character, derive-alias pattern,
encode/decode API, `bytecheck` semantics), see lore's
`rust/rkyv.md`. This skill is *what discipline to apply*;
lore is *how the tool works*.

---

## The sema-family pattern

> **Scope: today, not eventually.** This section describes today's
> typed-storage substrate — `sema` (the kernel; rename pending →
> `sema-db`). The eventual `Sema` is broader (universal medium for
> meaning — see `~/primary/ESSENCE.md` §"Today and eventually");
> for Rust today, use what's named here.

The workspace's typed-storage substrate lives in **`sema`**
(the kernel) plus component-owned typed layers. Prefer an internal
module first (`persona-mind/src/tables.rs`, `persona-router/src/tables.rs`,
etc.). Create a dedicated Sema crate only after reuse is real and its
architecture has been explicitly named. Do not create broad umbrella
Sema crates for meta projects just because the meta repo composes
several components. In particular, `persona` is a meta project today;
there is no shared `persona-sema` architecture.

Sema is to state what `signal-core` is to wire, but ownership is
by state-bearing component:

```
signal-core                 sema
  ├─ signal-persona-mind      ├─ mind Sema tables in persona-mind
  ├─ signal-persona-message   ├─ router Sema tables in persona-router
  └─ signal-persona-harness   └─ harness Sema tables in persona-harness
```

`sema` (the kernel) owns: redb file lifecycle, the typed
`Table<K, V: Archive>` wrapper, txn helpers, the standard
`Error` enum, the version-skew guard, and the `Slot(u64)` +
slot-counter utility.

Each component-owned Sema layer owns: its `Schema` constant
(table list + version), its typed table layouts, its open
conventions, and its migration helpers. Records' Rust types
live in the matching `signal-*` contract crate when they cross
a component boundary; purely internal persisted records may live
inside the component.

**New components consuming sema:** add `sema = "..."` to
`Cargo.toml`, declare a `Schema` constant, define typed
tables atop `sema::Table<K, V>`. Don't reinvent the
plumbing. See `/git/github.com/LiGoldragon/sema/ARCHITECTURE.md`
and `~/primary/reports/designer-assistant/17-pre-today-report-cleanup-agglomeration.md`
§2.4 for the current design.

---

## Why this discipline is strict

The rules above feel laborious before the components are
written. They are not laborious *while* the components
are running: a typed wire makes wrong calls fail at
compile time, a typed store makes wrong reads fail at
boot time, and the projection-from-record discipline
makes the disk and the in-memory truth impossible to
disagree.

Each entry in the anti-pattern table is a class of bug
the workspace has either lived through or watched
nearby. Each entry in the validated-pattern table is a
shape that earned its place by surviving real use. The
table grows; the work gets more correct as it grows.

---

## See also

- `skills/rust-discipline.md` — Rust discipline index.
- `skills/contract-repo.md` — how typed contracts are organized
  in repos (kernel extraction, layered effect crates).
- `skills/rust/errors.md` — typed errors at storage and wire
  boundaries.
- `skills/rust/methods.md` — typed records that flow through
  this surface.
- `lore/rust/rkyv.md` — rkyv tool reference (feature pin,
  derive alias, encode/decode API, bytecheck).
- `lore/rust/testing.md` — sync-façade-on-State pattern.
- `~/primary/repos/signal/ARCHITECTURE.md` — the canonical
  signal pattern worked example.
- `/git/github.com/LiGoldragon/sema/ARCHITECTURE.md` — sema kernel
  architecture.
