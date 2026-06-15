# 110 — Psyche answers on the open spirit concept decisions (2026-06-15)

*The psyche answered the four genuinely-open concept questions surfaced by report
109. This report captures the answers: the intent recorded to Spirit, the beads
created, the one answer that was a Correction (record shape), and the full
explanation of the one answer the psyche deferred pending explanation (message
existence-log). Then it re-poses that last decision with the explanation in hand.*

## The four answers, as given

| Question | Answer | Disposition |
|---|---|---|
| Record shape (flat / per-kind / discriminant) | "that intent was misunderstood, should be edited" — meant a *view* or *creation shorthand*, not stored shape; usefulness unsure | **Correction** — Spirit `ezcy`; `20jk`/`f0wm` zeroed |
| CollectRemovalCandidates (combined / pure-extract / both) | Keep combined | **Correction of 3v3r** — Spirit `jrx5`; bead `wk88` |
| Privacy default + private-capture path | Named private form | **Decision** — Spirit `qy15`; bead `v1w7` |
| message existence-log (build / trust-membrane) | "explain" | Explained below; re-posed |

## 1 — Record shape: the per-kind intent was a misread (Correction `ezcy`)

The psyche's per-kind-variant intent (`20jk` Decision, `f0wm` Principle) read, to
the agents who captured them, as a **storage** proposal — "fields vary by record
kind; a private record carries privacy, a public one omits it." The psyche
corrected this: that was not the intent. [that intent was misunderstood, should be
edited. I was talking about a *view* of the record, or a shorthand for creating
one, if that is even useful, which I am unsure of] (the verbatim answer).

So the resolution:

- The **canonical stored Spirit record stays one uniform shape** — no per-kind
  storage variants. The flat shape that production already ships is correct.
- What the psyche actually raised was a **view** of a record, or a **shorthand for
  creating** one — a presentation / ergonomics layer *over* the uniform record,
  not the stored shape.
- Whether such a view/shorthand is **useful is undecided** — the psyche is unsure.
  It is not committed work; it is an open idea held at low conviction.

Captured as **Spirit Correction `ezcy`** (certainty High — the misread is firm;
the view/shorthand usefulness is stated as undecided, so nothing is overclaimed).
`20jk` and `f0wm` are **zeroed** (recoverable removal-candidate marker; lineage
stays visible via `ezcy`; full text tombstoned below). Noted on bead `am9d`
(the named-shorthand-operation ladder) so the view/shorthand idea is parked there,
undecided, rather than driving a redesign.

**The reconciliation with answer 3:** the named private-capture form (answer 3) is
*exactly* one such creation shorthand — and it is the one the psyche **is** sure
is useful. So the picture is coherent: uniform storage; an ergonomic creation
shorthand for the private case (committed); other per-kind views/shorthands
(undecided).

## 2 — CollectRemovalCandidates: keep combined (Correction of `3v3r`)

The psyche chose the **combined** shape: CollectRemovalCandidates is **one guarded
operation** that archives the Zero-certainty candidates and then retracts them in a
single call, with **archive-first safety** — if archiving fails, nothing is
retracted and the affected candidates come back marked archive-failed. Not a
pure-extract operation with destruction split into a separate `Remove`, and not
both roots.

This **refines `3v3r`**, whose wording ("separates the discovery/extraction
concern from the destruction concern in `Remove`") described an emit-only
operation. The separation-of-concern `3v3r` wanted is preserved *inside* the one
operation (archive precedes retract), not by splitting into two roots. This also
matches what the **deployed** CLI already does (archive, then remove) and record
`o70j` (archive before removal). The guardian initially refused the bare Decision
as a `Contradiction` of `3v3r` — correctly — so it is recorded as **Correction `jrx5`
naming `3v3r`**, with the psyche's selection (made against `3v3r`'s own shape
offered as the explicit alternative) as the authorizing testimony.

Bead **`wk88`** tracks the implementation. It reportedly unblocks ~5 downstream
operation designs (archive retrieval `uwo0`, archive-as-sema-database, the GC
path `itn7`, the lifecycle ladder).

## 3 — Privacy: a named private-capture form (Decision `qy15`)

The default record visibility **stays public** (privacy `Zero`). Private capture
gets an **explicit named short-form operation** (e.g. `RecordPrivate` /
`RecordSealed`) so that capturing private material is one deliberate,
hard-to-forget ritual — not a remembered fifth positional field that a hurried
agent omits, silently publishing private substance. Private is opt-in but
unmissable through the named form.

Captured as **Spirit Decision `qy15`**; bead **`v1w7`** tracks it. It belongs in
the named-shorthand-operation ladder (`am9d`) and relates to `dn1e` (the in-place
`ChangePrivacy` operation). It is the concrete realization of the "creation
shorthand" idea from answer 1 — the one the psyche is sure about.

## 4 — message existence-log: the explanation (then re-posed)

The psyche asked to have this one explained before deciding. Full source-grounded
analysis is report 76.1; the essence:

### What `message` and `router` are

`message` and `router` are two separate components in the agent-messaging wire,
sitting at **two different trust depths**, each owning **one different durable
fact**.

- **`message`** is the **trust-minting ingress boundary**. It is the only process
  that `accept()`s the untrusted external connection, so it is the only place
  `SO_PEERCRED` (the kernel-verified caller uid) is trustworthy. It converts a
  forgeable peer uid into a typed `MessageOrigin` (`External(Owner)` /
  `External(NonOwnerUser)` / `InternalComponentInstance`) using the configured
  owner identity — never from the payload. Its socket is `0660` (the external
  door). It holds **no durable ledger** by design (only its deploy-time auth
  policy — see the addendum below) — minimal authority, bounded blast radius.
- **`router`** sits behind `message` at socket `0600` (owner-only). It holds the
  durable `redb` ledger and the channel-grant authority, and it owns the
  **DELIVERY** fact — established only when the harness-side acknowledgement
  arrives. It **trusts** the origin `message` stamped (`router.rs:1095`); it has
  zero peer-credential code, so it structurally *cannot* re-derive the caller's
  identity. message mints, router trusts.

### Addendum (psyche correction): message is not a pure stateless function

The psyche pushed back on "stateless": *message needs to KNOW something to do its
SO_PEERCRED authentication — that is state to begin with.* Correct, and "stateless"
was imprecise. The sharper frame separates three kinds of state a triad component
can hold:

1. **Per-connection session state** — transient, discarded after the request.
   message classifies each connection from the kernel-supplied `SO_PEERCRED` and
   forgets it. (Genuinely stateless here.)
2. **Policy / configuration knowledge** — what message must *know* to attribute
   origin: the `owner_identity` (which uid is the owner) and the
   `component_ingresses` map. This is the state the psyche is naming. It is held in
   memory, **static across messages**, set at deploy via the binary startup config
   (the daemon one-arg rule) — or, arguably, it *should* arrive as authenticated
   **owner policy over a meta-signal plane** (today message has no meta tier; report
   75 §3.5). Either way it is config/policy, not an accumulating ledger.
3. **Durable working state (a SEMA ledger)** — an accumulating durable record. The
   **existence-log** (`l3k4`) is exactly this, and it is the only one message does
   **not** have today.

So message already holds kind-2 state (it is a *knowing, authoritative* component,
not a pure function) — but the A/B decision is specifically about kind-3 (the
durable existence-log). The psyche's instinct cuts two ways and both are useful:

- It **strengthens Option A**: a component already configured and authoritative is
  a natural home for its *own* durable fact — giving it the existence-log is less of
  a stretch than bolting a ledger onto a true stateless function.
- It surfaces a **separate, orthogonal** question worth its own decision: should the
  `owner_identity` arrive as a proper **meta-signal owner policy** (the owner sets
  the trust boundary) rather than baked-in argv config? That is kind-2, independent
  of the existence-log, and in the same spirit of "message must know things."

### The two durable facts (the heart of it)

Intent `l3k4` (recorded, live) splits two facts between the two components:

- **EXISTENCE** — "this message exists / authenticated bytes arrived at ingress."
  By `l3k4` this fact belongs to **`message`**, established the instant authenticated
  bytes arrive (only message holds the `SO_PEERCRED`-bearing fd).
- **DELIVERY** — "this message was delivered." Belongs to **`router`**,
  established only on harness ack (only router holds the harness channel).

They are different keys, different cardinality (1 existence : N delivery attempts),
different lifecycle points, different evidence sources. A single component cannot
honestly own both, because the existence-witness must speak *before* the
delivery-acknowledger has anything to say.

### The seam — and why this is a real fork

Here is the gap: `l3k4` assigns the existence fact to `message`, but **in the
actual source `message` writes nothing durable** — the existence record is written
by **`router`** (`router.rs:1163`). So `message`'s defining differentiator is
currently a **gap**: it is *under-built*, not redundant. (This is why merging the
two was firmly rejected across four analytical lenses in 76.1: merge would pull an
untrusted `0660` door into the same address space as the durable ledger and
channel authority — a textbook blast-radius expansion. Even if `message` never
gains a feature, its `SO_PEERCRED` trust boundary is irreducible.)

So the only open choice is whether `message` *also* becomes the existence-fact
owner that `l3k4` says it should be:

- **Option A — build it.** `message` gains its own durable existence-event surface
  (a small Signal+Nexus daemon, or a 3-plane triad, that emits a durable existence
  event). This **realizes `l3k4`**, makes `message` clearly feature-bearing,
  removes the fragility, and router stops owning a fact intent assigns elsewhere.
  Heavier port; strongest end-state.
- **Option B — trust membrane.** `message` stays a 2-plane pure trust membrane,
  justified entirely on the `SO_PEERCRED` privilege-separation boundary (which is
  irreducible either way); router keeps writing the existence record. Lighter port;
  accepts the standing fragility and a consciously-deferred `l3k4`.

### The honest caveat (the steelman for B / for eventually collapsing it)

A trust boundary is fundamentally a per-connection in-process function (~60 lines),
not inherently its own process. By line-count and process-count, a merged router
binding both sockets (0660 external + 0600 internal) and stamping at the external
listener would be strictly simpler — deleting one process, one deploy unit, one
whole triad, a round-trip per message. Keeping `message` separate buys
**blast-radius** isolation (the expensive currency) at the cost of
**implementation** simplicity (the cheap currency). The verdict "keep separate"
holds — but it is worth knowing it is *fragile*: `message` earns its cost today as
the isolation boundary, not yet as a feature-bearing component. If you both stop
valuing the address-space isolation **and** never build the existence-log, the
honest move would flip to an in-process boundary.

That is why this is genuinely the psyche's call: Option A realizes `l3k4`, Option B
consciously defers it — either is durable intent. It is re-posed in chat.

## Intent recorded this session

| Record | Kind | Substance |
|---|---|---|
| `ezcy` | Correction | record-shape misread: storage stays uniform; the per-kind notion was a view/creation-shorthand, usefulness undecided |
| `qy15` | Decision | named private-capture short-form; default stays public |
| `jrx5` | Correction of `3v3r` | combined archive-then-retract, archive-first safety |
| `20jk`, `f0wm` | → certainty `Zero` | superseded by `ezcy` (tombstoned below) |

## Beads created / touched

- **`wk88`** (P2) — implement CollectRemovalCandidates as the combined
  archive-then-retract guarded op.
- **`v1w7`** (P2) — add the named private-capture short-form
  (`RecordPrivate`/`RecordSealed`).
- **`am9d`** (note) — the record-shape correction parked: view/creation-shorthand
  undecided; uniform storage; `v1w7` is the one sure shorthand.

## Tombstone — records zeroed this session

Preserved per `skills/intent-maintenance.md` before zeroing (recoverable; not
hard-removed):

- **`20jk`** (Decision, Medium, was Minimum importance, domain
  `Technology>Software>Data>Modeling`): [Spirit record fields should vary by record
  kind rather than every record carrying every field - eliminate the fields a given
  kind does not use. Concretely a private-bearing record carries a privacy field
  while an ordinary public record omits it, reducing the total field count and
  giving each kind a tighter purpose-fit shape. A better architecture than the
  current one-shape-fits-all positional record.]
- **`f0wm`** (Principle, Medium, domain `Technology>Software>Data>Modeling`):
  [Spirit intent records should be shaped as specific variants whose fields match
  their semantic needs; private record variants carry privacy data, while public
  record variants should not carry unused privacy fields.]

Superseded by `ezcy`: the variation idea was about a view/creation-shorthand layer,
not stored shape; storage stays uniform.
