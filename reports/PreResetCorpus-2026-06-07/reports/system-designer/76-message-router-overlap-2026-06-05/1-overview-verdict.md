# 76.1 — Verdict: message and router are NOT redundant — keep separate

Unanimous across four lenses: **keep separate** (authority-surface, durable-fact,
future-pipeline all HIGH confidence; simplicity-cost MEDIUM, "keep separate but know it
is fragile"). No Spirit record, `INTENT.md` section, or design report has *ever*
proposed merging them or framed them as overlapping; the rename history
(`b85b69b persona-message → message`) shows message being **carved out** into its own
identity — the opposite of a merge.

## Answering the three sub-questions directly

**1 — Is message thin *because* router absorbs its state?** No. That framing (mine, in
report 75) was wrong-headed. message is thin because its *job* is the trust-minting
ingress boundary, which is intentionally minimal-authority and stateless. It is not a
component that "would be stateful if router didn't exist" — it is a privilege-separation
membrane that must stay stateless to keep its blast radius bounded.

**2 — Are they redundant; should there be one?** No. They sit at two different trust
depths and own two different durable facts. The overlap is small, asymmetric, and
concentrated in the cheap halves (shared daemon/supervision/CLI boilerplate; the inbox
proxy). The load-bearing reason against merge is not line-count — it is that merging
re-internalizes an untrusted, externally-writable door into the same address space that
holds the durable ledger and the channel-authority core.

**3 — What does message uniquely provide?** The **kernel-anchored trust head**: message
is the only process that `accept()`s the untrusted external connection and so the only
place `SO_PEERCRED` is trustworthy. It converts a forgeable peer uid into typed
`MessageOrigin` (`External(Owner)` / `External(NonOwnerUser(uid))` /
`InternalComponentInstance`) using configured `owner_identity` — never from payload,
never from its own euid. This is irreducible *today*, independent of any unbuilt feature.

## The physics argument (why router structurally CANNOT absorb message)

Router has **zero** peer-credential code (empty grep for `SO_PEERCRED`/`getsockopt`/
`PeerCred` across `router/src`). By the time a frame crosses `router.sock`, it came from
the **message daemon process** — router's `SO_PEERCRED` would read "message," not the
real caller. So router cannot re-derive `External(Owner)` vs `External(NonOwnerUser)`; it
**trusts** `stamped.origin` verbatim (`router.rs:1095`) and refuses client-pre-stamped
submissions. The codebase already models a clean **mint-vs-trust** handoff: message
mints, router trusts. Origin attribution must be minted at the `accept()` of the
caller's own connection — that is message's job by physics, not convention.

## Two genuinely different durable facts (the durable-fact lens)

| | EXISTENCE fact | DELIVERY fact |
|---|---|---|
| Owner (per intent `l3k4`/`17ss`) | message | router |
| Established when | the instant authenticated bytes arrive at ingress | only on harness-side ack |
| Evidence source | the SO_PEERCRED-bearing fd (only message holds it) | the harness channel, one per agent (only router holds it) |
| In router's redb today | `messages` table — 1 row per message, keyed by message-id | `delivery_attempts` / `delivery_results` — N rows, keyed by a separate `delivery_sequence`, carrying `delivered: bool` |

These are different keys, different cardinality (1:N), different lifecycle points, and
different evidentiary sources. A single component cannot honestly own both, because **the
existence-witness must speak before the delivery-acknowledger has anything to say.**

## The security partition is physically real (authority-surface lens)

`message.sock` = **0660** (engine-owner group — the external door); `router.sock` =
**0600** (owner-only). Merge would put the untrusted 0660 door in the same process that
holds channel-grant adjudication and the durable redb store — the textbook
confused-deputy / blast-radius expansion privilege separation exists to prevent. The
permission split is the load-bearing reason the overlap is not collapsed.

## The agent pipeline DEEPENS the split (future-pipeline lens)

End-state is message → router → **agent** → harness (`w4jp`/`gdbf`; `signal-agent`
contract exists, daemon does not yet). agent absorbs router's *harness coupling* and the
ack chain (`AcknowledgementHop::BackendDaemon/AgentDaemon/Router`), so the durable,
attack-worthy surface **grows on the router+agent side** — exactly what you want behind
0600. Meanwhile the provenance message mints rides untouched all the way into the agent
delivery frame (`signal-agent MessageDelivery.ingress_context + connection_class`).
message stays the single SO_PEERCRED head of the whole chain. The split is a trust-depth
gradient (untrusted-ingress / owner-only-authority / backend-abstraction); agent sharpens
the gradient, it does not flatten it. (Federation `b9ao` is a cross-persona layer ABOVE
this wire and does not bear on the merge.)

## The seam that actually matters — message is UNDER-built, not redundant

This is the sharpest finding and it resolves the report-75 imprecision. Intent `l3k4`
assigns the EXISTENCE log event to **message** — but in actual source **message writes
nothing durable**, and the existence record (`messages` table / `StoredMessageRecord`)
is written by **router** on acceptance (`router.rs:1163`). Verified absent in message's
source: no log emission, no event sink, no Sema observation, no existence ledger of any
kind. Message's cleanest differentiator is currently a *gap*.

So the honest seam runs the OPPOSITE direction from merging: the problem is that the
component which is *supposed* to own the existence fact owns no durable record at all.
The fix is to push existence-witnessing **toward** message (realizing `l3k4`), which
deepens the split — not to fuse router's delivery ledger into the ingress boundary.

## The fragility note (simplicity-cost lens, MEDIUM — the one honest caveat)

The merge steelman is not empty. A trust boundary is a per-connection **in-process
function** (`origin_for_peer`, ~60 lines), not inherently a deploy unit. A merged router
*could* bind message.sock at 0660 and its own socket at 0600 in one process, stamp at the
external listener, and keep identical permission isolation — deleting one process, one
deploy/supervise unit, one whole triad (`signal-message` + `meta-signal-message`), a
duplicated daemon/supervision/CLI/codec shell, and a serialize+connect+round-trip on
every message. By line-count and process-count the merge is strictly simpler, and
message's one true differentiator (the `l3k4` existence-log) is verified unbuilt.

Merge still loses — but on *blast-radius* simplicity, not implementation simplicity: you
would pay simplicity in the expensive currency (security/state isolation) to save it in
the cheap currency (one process, mostly-boilerplate LOC). The verdict is therefore
"keep separate, but the workspace should KNOW it is fragile": **message earns its cost as
the isolation boundary, not (yet) as a feature-bearing component.** The recommendation
flips toward an in-process privilege boundary the moment one both (a) stops believing the
address-space isolation is worth a process AND (b) never builds the existence-log.

## What this resolves, and the fork for the psyche

This **resolves report-75 open-decision #2** (does message get a SEMA plane / is it
2-plane or 3-plane). The answer is no longer "recommend stateless 2-plane carve-out" by
default — it is a real choice with a clear axis:

- **Option A — build the existence-log in message (realize `l3k4`).** message gains a
  small existence-event surface (a 3-plane triad, or a Signal+Nexus daemon that emits a
  durable existence event), becoming clearly feature-bearing. This removes the fragility,
  honors `l3k4`'s two-owner split, and means router stops owning the existence fact that
  intent assigns to message. Heavier port; strongest end-state.
- **Option B — keep message a 2-plane pure trust membrane (no existence SEMA).** Justify
  message *entirely* on the privilege-separation / SO_PEERCRED-isolation boundary (which
  is irreducible regardless), and let router keep writing the existence record. Lighter
  port; accepts the standing fragility and a partial-unrealized `l3k4`.

**Either way the answer to the psyche's question is firm: do not merge.** Even Option B
keeps message irreducible — the SO_PEERCRED trust boundary cannot move into router. The
only open choice is whether message *also* becomes the existence-fact owner.

A decision here is durable intent (it would either realize or consciously defer `l3k4`),
so it is the psyche's to make — not inferred.

## See also

- `0-frame-and-method.md` — the question, the workflow method, verified-vs-inferred.
- `reports/system-designer/75-message-router-orchestrate-production-2026-06-05/4-message-production.md`
  — the message port map whose decision #2 this resolves.
- Intent: `l3k4` (existence vs delivery), `17ss` (delivery durable on ack), `w4jp`/`gdbf`
  (agent abstraction), `pb1g` (every component needs a meta slot — message already
  carries supervision + typed-config owner-meta surfaces).
