# 111 — signal-clavifaber contract shape

*Designer report. Resolves `primary-9xo`. Names the two relations
between per-host `clavifaber` runs, the long-lived `persona-trust`
component, and host trust-subscribers; sketches the closed root enums,
the authority mints, the transport carve-outs; lists examples-first
NOTA records; flags the split-or-collapse question.*

---

## 0 · TL;DR

Two relations live in the cluster-trust slice of the architecture, and
both should land as typed Signal contracts layered atop `signal-core`:

| Relation | Direction | Cardinality | Authority | Lifecycle |
|---|---|---|---|---|
| **Publication push** — per-host clavifaber to `persona-trust` | host → cluster | many hosts → one cluster; one-shot per host convergence | `persona-trust` mints `Slot<PublicationCommit>` | short-lived, request/reply per submission |
| **Trust distribution** — `persona-trust` to each host subscriber | cluster → host | one cluster → many hosts; long-lived | `persona-trust` is source of truth; subscriber holds cursor | long-lived stream; current-state on connect, then deltas |

**Recommendation**: one repo `signal-clavifaber` with two top-level
channels (publication + trust), not two separate repos. The two channels
share the domain vocabulary (`PublicKeyPublication`, `NodeName`,
`ClusterRevision`, `TrustObservation`) and would duplicate types if
split. §6 names the trade-off.

`signal-core` provides Frame, length-prefix envelope, handshake, auth.
`signal-clavifaber` adds the typed payload vocabulary on top —
layered-effect-crate shape per `skills/contract-repo.md` §"Layered
effect crates."

---

## 1 · Two relations, named in plain English

Per `~/primary/skills/contract-repo.md` §"Contracts name relations":
*"Name the relation in plain English before naming any record."*

### Relation 1 — Publication push (host clavifaber to persona-trust)

A `clavifaber` convergence run on each host completes by submitting one
typed publication record to the long-lived `persona-trust` component.
The submission is **one-shot per convergence**: clavifaber opens a
connection, sends `PublicationSubmission`, receives `PublicationReceipt`
or `PublicationRejection`, closes. Convergence is idempotent —
re-submission of the same `(NodeName, public-material)` is a no-op
commit on `persona-trust`'s side.

```
clavifaber (host probus, one-shot)
  ─ PublicationSubmission ─►  persona-trust (Prometheus, long-lived)
  ◄─ PublicationReceipt ─    persona-trust
```

### Relation 2 — Trust distribution (persona-trust to host subscriber)

Each host that needs to know the current trust state subscribes to
`persona-trust`. The contract is the canonical pushed-subscription
shape per `~/primary/skills/push-not-pull.md` §"Subscription contract":
emit current state on connect, then deltas. No polling.

```
host_subscriber (any persona-host)
  ─ TrustSubscription ─►        persona-trust
  ◄─ TrustSubscriptionReceipt ─ persona-trust  (current state snapshot)
  ◄─ TrustUpdate (event N)     persona-trust  (each committed revision)
  ◄─ TrustUpdate (event N+1)   persona-trust
  ...
```

---

## 2 · Top-level Rust skeleton

The closed root enums per `signal_channel!` macro convention.
Variant-name = payload-name (per the convention landed in designer/107
commit `4505abab`).

```rust
signal_channel! {
    request ClavifaberRequest {
        PublicationSubmission(PublicationSubmission),
        TrustSubscription(TrustSubscription),
    }
    reply ClavifaberReply {
        PublicationReceipt(PublicationReceipt),
        PublicationRejection(PublicationRejection),
        TrustSubscriptionReceipt(TrustSubscriptionReceipt),
        TrustSubscriptionRejection(TrustSubscriptionRejection),
    }
    event ClavifaberEvent {
        TrustUpdate(TrustUpdate),
    }
}
```

The records (one struct per variant payload, all `NotaRecord`-derived):

```rust
pub struct PublicationSubmission {
    pub publication: PublicKeyPublication,
}

pub struct PublicationReceipt {
    pub commit_slot: Slot<PublicationCommit>,
}

pub struct PublicationRejection {
    pub reason: PublicationRejectionReason,
}

pub enum PublicationRejectionReason {
    NodeNameMismatch,
    InvalidPublicMaterial,
    ClusterRegistryUnavailable,
}

pub struct TrustSubscription {
    // intentionally no filter today; subscriber receives the whole
    // cluster-trust state. Filters land later as a typed extension.
}

pub struct TrustSubscriptionReceipt {
    pub current_state: ClusterTrustSnapshot,
}

pub struct TrustSubscriptionRejection {
    pub reason: TrustSubscriptionRejectionReason,
}

pub enum TrustSubscriptionRejectionReason {
    ClusterRegistryUnavailable,
}

pub struct ClusterTrustSnapshot {
    pub revision: ClusterRevision,
    pub observations: Vec<TrustObservation>,
}

pub struct TrustObservation {
    pub node_name: NodeName,
    pub publication: PublicKeyPublication,
    pub commit_slot: Slot<PublicationCommit>,
}

pub struct TrustUpdate {
    pub revision: ClusterRevision,
    pub observation: TrustObservation,
}

// PublicKeyPublication stays defined in clavifaber today and is
// imported here. If pruning the dependency edge becomes important,
// move PublicKeyPublication into signal-clavifaber and have clavifaber
// re-export. That decision can land later; today the existing
// definition in clavifaber works.
pub use clavifaber::PublicKeyPublication;
```

Domain newtypes (per `skills/rust-discipline.md` §"Domain newtypes"):

```rust
pub struct NodeName(String);  // validated: nonempty, no whitespace, ASCII-printable
pub struct ClusterRevision(u64);  // monotonic, persona-trust-supplied
pub struct PublicationCommit;  // marker type for the slot
```

---

## 3 · NOTA examples — falsifiable specifications

Per `skills/contract-repo.md` §"Examples-first round-trip discipline":
*"Every record kind in a contract repo lands as a concrete text example
+ a round-trip test before its Rust definition is final."* Each example
below is one canonical record. Each will land as a round-trip test:

### Publication push

```text
(PublicationSubmission
    (PublicKeyPublication
        probus
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI…"
        (Some "200:0:0:0:0:0:0:1")
        (Some "ed25519:abc…")
        None))
```

```text
(PublicationReceipt 42)
```

(The `42` is the bare `Slot<PublicationCommit>` per ESSENCE
§"Infrastructure mints identity, time, and sender" — slot is a typed
integer, no agent-minted prefix.)

```text
(PublicationRejection NodeNameMismatch)
```

### Trust distribution

```text
(TrustSubscription)
```

```text
(TrustSubscriptionReceipt
    (ClusterTrustSnapshot
        7
        ((TrustObservation probus
            (PublicKeyPublication probus "ssh-ed25519 …" None None None)
            42)
         (TrustObservation cronus
            (PublicKeyPublication cronus "ssh-ed25519 …" None None None)
            41))))
```

```text
(TrustUpdate 8
    (TrustObservation prometheus
        (PublicKeyPublication prometheus "ssh-ed25519 …" None None None)
        43))
```

These examples land verbatim in `tests/round_trip.rs` as the
falsifiable specifications: each example becomes both an encode test
(typed value → NOTA text matches) and a decode test (NOTA text →
typed value matches). If the Rust types drift away from these, the
tests fail.

---

## 4 · Authority — what the receiver mints, what the sender supplies

Per ESSENCE §"Infrastructure mints identity, time, and sender":

| Value | Who mints | Why |
|---|---|---|
| `Slot<PublicationCommit>` | `persona-trust` on commit | Identity beyond content; assigned by the store, returned in reply. Clavifaber never invents it. |
| Commit time of a publication | `persona-trust`'s transition log | Time the cluster registry committed the publication. Lives on the transition log, not on the record body. |
| `ClusterRevision` | `persona-trust` | Monotonic source-of-truth counter; `persona-trust` mints; subscribers receive in events. |
| `NodeName` | `clavifaber` (host hostname) | Content; the host knows its own name. Subject to validation by `persona-trust` (NodeNameMismatch rejection). |
| `PublicKeyPublication` body | `clavifaber` | Content; the host generated/derived its own public material. |
| Sender principal of a `PublicationSubmission` | Connection auth proof, NOT record body | Host TLS / signed handshake establishes who is submitting. Putting `submitting_node` on the record body would be redundant *and* untrustworthy. |
| `TrustSubscription` subscriber identity | Connection auth proof | Same reason. |

A subtle case: the `node_name` field on `PublicKeyPublication` is
content (clavifaber knows its own hostname) — but the *trust* that
this submission really comes from that node is established by the
connection's auth proof, not by the field. `persona-trust` validates
that the auth-proof-derived sender principal matches the
`node_name` field; mismatch yields `NodeNameMismatch` rejection.

This validation is **runtime**, not contract — the contract specifies
the record shape; the runtime enforces "this principal really is that
node," which is environment-dependent. (Per designer/106 §Q-dec-2:
contract for value invariants, runtime for environment facts.)

---

## 5 · Transport — push, with one named carve-out

The default transport is **the canonical persona pattern**: long-lived
unix-domain socket on the cluster's central node (`persona-trust`'s
home), accepting Signal frames over the wire. Each host opens the
socket, sends one `PublicationSubmission`, receives reply, closes.
Trust subscribers open the socket, send `TrustSubscription`, hold the
connection open for streaming events.

Cross-machine traffic uses TCP+TLS once `signal-network`
(`primary-uea`) lands. Until then, host clavifaber runs on the same
machine as `persona-trust` (development) or via SSH tunneling
(production). The contract is transport-agnostic; bytes are bytes.

### Carve-out: file-on-disk + inotify

Per `~/primary/skills/push-not-pull.md` §"Named carve-outs": a
producer that writes a file the consumer watches via `inotify` is a
**kernel push**, not polling. It earns its place when the producer
is naturally file-shaped.

`clavifaber` already writes `publication.nota` to
`/var/lib/clavifaber/publication.nota` per `primary-7a7`'s acceptance
criteria. If `persona-trust` has filesystem access to the host's
publication path (via SSH+NFS, mounted volume, or co-location), it can
`inotify` the path and consume publications without clavifaber needing
to open a socket.

This is the alternative push primitive for Relation 1. Trade-offs:

| Primitive | Pros | Cons |
|---|---|---|
| Direct socket push | Same wire pattern as the rest of persona; works cross-machine; immediate ack so clavifaber knows the submission committed before exiting. | Requires `persona-trust` reachable from each host at convergence time. Failure mode: clavifaber exits 0 with publication uncommitted. |
| File-on-disk + inotify | Decouples per-host clavifaber from `persona-trust` availability. Convergence runner exits clean even if the cluster is down. The publication file is the durable record on the host. | One-way: clavifaber gets no commit acknowledgement; `persona-trust` may take seconds to consume. Requires file-path access (NFS/SSH/mount). |

**My recommendation**: socket push as the canonical relation-1 transport;
inotify as a fallback when `persona-trust` is unreachable. The contract
records (`PublicationSubmission`, `PublicationReceipt`) stay the same
either way — under inotify the "receipt" is asynchronously implicit
(clavifaber trusts that a successful file write will be picked up).

This is a runtime/system-specialist call, not a contract call. The
contract names the typed records; the deployment picks the transport.
Document both in `signal-clavifaber/ARCHITECTURE.md` §"Transport"
when the contract repo lands.

Relation 2 is socket-only — the long-lived subscription stream needs
real bidirectional connection, not file watching.

---

## 6 · The split-or-collapse question

The bead's note framed two contracts. Two structural options:

(a) **One repo, two channels** — `signal-clavifaber` carries both
   relations as separate top-level enums (the skeleton in §2 above).
(b) **Two repos** — `signal-clavifaber-publication` (relation 1) and
   `signal-cluster-trust` (relation 2). Each owns its own channel;
   shared types (`PublicKeyPublication`, `TrustObservation`) duplicate
   or live in a third kernel crate.

Argument for (a): the relations share substantial domain vocabulary
(`PublicKeyPublication`, `NodeName`, `ClusterRevision`,
`TrustObservation`). Duplicating these into two repos creates the
classic kernel-extraction problem prematurely. The two relations also
both have `persona-trust` as one endpoint; pairing them in one repo
makes the `persona-trust` ↔ cluster-host story visible in one file.

Argument for (b): per `skills/contract-repo.md` §"Contracts name
relations" — *"a contract owns one relation."* The two relations have
different directions, different cardinalities, different lifecycle
shapes. A reader inspecting `signal-clavifaber` sees both and has to
decide which they care about; a reader inspecting
`signal-clavifaber-publication` sees one channel.

**My recommendation**: **option (a) — one repo**. The shared domain
vocabulary is load-bearing; splitting forces a kernel-extraction
discussion before the records are even stable. The single-relation
discipline can be revisited if the two channels evolve independently
enough to justify it (kernel-extraction is a later move per
`skills/contract-repo.md` §"Kernel extraction trigger"). Document the
two relations as a §0.5 in the repo's `ARCHITECTURE.md` so the reader
knows what they're looking at.

Pushback path: if the user prefers two contracts (clean
single-relation discipline trumps shared vocabulary), the split is
mechanical. The skeleton in §2 separates cleanly along
`Publication*` vs `Trust*` lines.

---

## 7 · Examples-first plan

Per `skills/contract-repo.md` §"Examples-first round-trip discipline":

1. **First commit** in `signal-clavifaber`: NOTA examples in
   `tests/round_trip.rs` for every record kind named in §3 (six
   examples — `PublicationSubmission`, `PublicationReceipt`,
   `PublicationRejection`, `TrustSubscriptionReceipt`, `TrustUpdate`,
   plus the empty `TrustSubscription`). Each example is a string
   constant + a round-trip test that decodes and re-encodes.
2. **Second commit**: Rust types per §2's skeleton. The round-trip
   tests start passing.
3. **Third commit**: domain newtype validation
   (`NodeName::new`, `ClusterRevision`, etc.) and validation tests
   (`NodeName::new("")` rejects, etc.).
4. **Fourth commit**: `signal_channel!` invocation that ties
   request/reply/event to `signal-core`'s frame and envelope.
5. **Fifth commit**: end-to-end frame-round-trip test —
   `PublicationSubmission` encoded as a full Signal frame, decoded
   back, asserts equality.

The discipline is the same as `signal-persona-mind`'s recent
contract-repo development pattern (per designer/107).

---

## 8 · Follow-up beads

`primary-9xo` closes with this report. New beads for the implementation
thread:

- **`signal-clavifaber` repo creation + examples-first first commit**:
  scaffold per `skills/contract-repo.md`, land the §3 NOTA examples
  as round-trip tests with `todo!()` Rust types. Owner: operator (Rust
  contract-crate scaffolding) or designer (if the examples-first phase
  is the falsifiable-spec lane). My pick: designer-assistant first —
  the examples-first phase is design work; operator picks up after types
  land. File when system-specialist names a target date for `primary-e3c`.
- **`PublicKeyPublication` move question**: today
  `clavifaber::PublicKeyPublication` lives in the runtime crate. Once
  `signal-clavifaber` consumes it, the kernel-extraction trigger fires
  if a third consumer appears. Don't move pre-emptively — wait for the
  third consumer (per `skills/contract-repo.md` §"Kernel extraction
  trigger" — extract when 2+ domain consumers exist). Note for future:
  `signal-clavifaber` is consumer 2; if `signal-cluster-trust` ever
  splits out as a third, move `PublicKeyPublication` into a kernel.

`primary-e3c` (the implementation bead) keeps its existing dependency
edges. Once `primary-9xo` and `primary-rab` close, `primary-e3c`
depends only on `primary-7a7` (per-host clavifaber convergence runner).

---

## See also

- `~/primary/reports/designer/110-cluster-trust-runtime-is-persona.md`
  — sibling report; names `persona-trust` as the cluster-trust runtime
  this contract serves.
- `~/primary/reports/designer/107-contract-enum-naming-pass-mind.md`
  — variant-name = payload-name convention applied here in §2.
- `~/primary/reports/designer-assistant/7-contract-relation-naming-survey.md`
  — the canonical naming standard this report applies.
- `~/primary/skills/contract-repo.md` §"Contracts name relations",
  §"Examples-first round-trip discipline", §"Layered effect crates",
  §"Kernel extraction trigger" — discipline applied throughout.
- `~/primary/skills/push-not-pull.md` §"Subscription contract",
  §"Named carve-outs" — discipline for relation 2 + the inotify
  carve-out in §5.
- `~/primary/ESSENCE.md` §"Infrastructure mints identity, time, and
  sender" — the authority decisions in §4.
- `/git/github.com/LiGoldragon/clavifaber/src/publication.rs:7-13` —
  current `PublicKeyPublication` shape this contract consumes.
