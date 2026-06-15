# 111 — message direct-delivery fast path: a proposal assessment

*Mid-dialogue, the psyche proposed a new division of labor between `message` and
`router`: [message would pass some messages directly without router, if the agent
knows about another agent by its uid, and that agent is marked as publicly
reachable … then router routes to gated agents, and to agents across network]. This
is a materially different architecture from reports 75/76 (where `message` is a pure
trust membrane and `router` does all routing). This report assesses it — strengths,
open questions, and how it resolves the still-open existence-log question (110 §4 /
report 109) and rides on the just-decided meta-signal policy plane (Spirit Decision
`n775`). The
proposal is under discussion; nothing is recorded as intent yet.*

## Correction — intent cross-check (designer/650)

A prime-designer cross-check read `l3k4` and `17ss` **directly from the store** (this
report had trusted my paraphrase) and corrected the load-bearing claim. `l3k4` is a
**two-clause** Decision: (1) [message creates a log event for the existence of the
message]; (2) [DELIVERY is established only when the router gets the harness-side
acknowledgement; the router is the authoritative source for delivery facts]. `17ss`
reinforces clause 2: [delivery durable on harness-side ack].

So the fast path does **not** "realize `l3k4`" as this report first claimed. The
proposal splits in two against the recorded intent, and the two halves carry
**different intent bars**:

- **X — message owns the existence fact durably.** Realizes `l3k4` **clause 1**. A
  clean extension of recorded intent; dissolves 76.1's fragility. Existence is
  *path-independent* (message is the ingress for everything), so X stands alone and
  needs no fast path to justify it.
- **Y — the direct-delivery fast path** (message owns delivery on the direct path,
  no router, no harness ack). **Contradicts `l3k4` clause 2 and `17ss`.** It is a
  deliberate **supersession** of recorded intent — and per "intent is primordial;
  superseding is always explicit," it requires the psyche to *explicitly override*
  `l3k4`'s delivery-authority clause, a materially higher bar than the body below
  frames.

**My load-bearing sentence ran the implication backward.** I wrote "direct delivery
means message must own durable state, so Q1 → build it." X already forces durable
state; Y is not needed to justify building message. So **Y must stand on its own
cost/benefit, not borrow X's.** Decouple them: bank X now; weigh Y separately.

**Costs of Y this report underweighted** (per 650): (1) Y moves durable state +
the registry *into* the `0660` door that 76.1's whole isolation argument protects —
a trade of isolation for latency, not a clean win; (2) Y **fragments the delivery
ledger** — no single component holds the complete one (open #6 is the sharpest
issue, and both resolutions cost); (3) Y **decentralizes origin-policy enforcement**
— every public agent, not just router, must enforce `MessageOrigin` policy on
direct-delivered stamps (safe only if "public" agents are genuinely origin-agnostic
and low-authority). Plus two correctness questions: **TOCTOU** on the async registry
(a public→private revocation racing an in-flight message), and **recovery-guarantee
asymmetry** (router's durable ledger gives crash-redelivery; a crashing message
mid-direct-delivery is best-effort unless it grows its own redelivery state behind
0660 — two paths with two durability guarantees).

`n775` (meta-signal plane) is confirmed real and load-bearing — that part stands.
The strengths and model below hold **for X**; read every "realizes `l3k4`" /
"delivery splits by path" line through the corrected X/Y split above. (Hygiene:
`l3k4`/`17ss` carry empty referent vectors — tag them `message`/`router` once a
record-mutation path exists.)

## The proposed model

A **two-path** delivery split, by *authority and locality*:

- **Fast path — `message` direct-delivers (no `router`)** when **both**: the sender
  addresses the target agent by its **uid**, and the target is **marked publicly
  reachable** (ungated). `message` already authenticates the sender via
  `SO_PEERCRED`; it would resolve the target uid to its endpoint and deliver
  peer-to-peer.
- **Slow path — `router` routes** for: **gated agents** (delivery that needs
  authority adjudication / a channel grant) and **agents across the network**
  (remote / federated transport).

In one line: `message` handles the *zero-authority, local, public* case; `router`
handles everything that needs **a gate or the network**.

## Why this is a strong model (what I think)

**1. It is a principled trust gradient, not a shortcut.** The untrusted `0660`
ingress door (`message`) only ever direct-delivers where there is **no authority to
abuse** — public agents that anyone could reach anyway. Every case carrying real
authority (gated agents) or crossing a trust-domain (network) goes through the
`0600` authoritative `router` with its durable ledger. So the blast-radius worry
that made 76.1 say "keep separate but it's fragile" is *contained by construction*:
direct delivery cannot leak authority because the fast path has none.

**2. It resolves the "message is under-built" tension decisively.** 76.1's sharpest
finding was that `message` owns no durable fact while intent `l3k4` says it should.
This proposal gives `message` a real job — fast-path delivery — and therefore a
reason for durable state: a delivery/existence record for the messages it delivers
directly. It answers the open Q1 (build the existence-log vs trust-membrane)
**toward build**: `message` becomes feature-bearing.

**3. It makes the two-facts model cleaner, not messier.** With direct delivery, the
fact ownership becomes:

| Fact | Direct (fast) path | Routed (slow) path |
|---|---|---|
| **Existence** (bytes arrived at ingress) | `message` | `message` |
| **Delivery** (target acknowledged) | `message` (it delivers + gets the ack) | `router` (harness/target ack) |

`message` **always** owns existence (it is the ingress for everything) — which is
exactly `l3k4`'s **clause 1** (= Decision X). But "delivery-ownership splits by
path" is **not** a realization of `l3k4` — it *contradicts* clause 2 ([the router is
the authoritative source for delivery facts]) and `17ss`. That half (= Decision Y)
is a supersession, per the correction above. X is the sharper model; Y is a separate
decision the psyche must explicitly make.

**4. It rides on the meta-signal policy plane just decided (Q2).** The "publicly
reachable" mark and the uid→endpoint registry are **owner policy** — declared by the
owner over the meta-signal plane. The two answers compose into one design: the owner
declares, via meta-signal, who is public and reachable; `message` uses that registry
to choose the fast path. No new mechanism — the Q2 plane carries it.

**5. Latency.** It removes a hop (`sender→message→router→target` becomes
`sender→message→target`) for the high-volume local-public case.

## Open questions the psyche needs to settle

These are the load-bearing details before this becomes buildable intent:

1. **What does "publicly reachable" mean, precisely?** Most likely: *ungated* —
   accepts unsolicited messages without a channel grant (gated = `router` must
   adjudicate a grant first). Confirm that "public" ≡ "no channel grant required,"
   and that it is set per-agent by the owner over the meta-signal plane.
2. **Public AND local, or can a public agent be remote?** A publicly-reachable agent
   that lives *across the network* still needs `router` for transport. So the fast
   path is **public AND local**; "remote" (any gating) always routes. Confirm the
   path-selection rule is: `direct ⇔ (public ∧ local ∧ uid-known)`, else `router`.
3. **Discovery / addressing.** How does a sender "know about another agent by its
   uid"? Does it query `message`'s registry, or is there a directory? `message` (via
   its policy plane) holds the public registry and resolves uid→endpoint — but the
   *discovery* surface (how a sender learns who is public) needs definition.
4. **The stamp-trust surface widens.** On the direct path, the *target* agent must
   trust `message`'s `MessageOrigin` stamp (just as `router` trusts it today). So
   every agent that can receive a direct-delivered message must trust `message` as a
   stamper — a wider trust relationship than today (where only `router` consumes the
   stamp). Acceptable, but it makes `message` a trust anchor for the whole local
   public mesh, not just the ingress.
5. **Exactly-once path selection.** Two delivery paths means the direct-vs-router
   decision must be **total and atomic** at `message` so no message is double-sent or
   dropped between paths.
6. **Does `router` still see direct-path existence?** If audit/replay needs a single
   place to see all messages, either `message`'s existence-log is the union surface,
   or direct-path existence is mirrored to `router`. Decide where the *complete*
   ledger lives.

## What it resolves and what it implies

- **Q1 (existence-log): → build it.** Under this model `message` must own durable
  state (existence always; delivery on the direct path), so the "thin trust
  membrane" option (110 §4 Option B) is off the table — `message` becomes a real
  feature-bearing triad component.
- **Q2 (meta-signal plane, Spirit `n775`): confirmed and load-bearing.** The plane
  carries both the owner identity and the public-reachability registry.
- **`message` becomes a 3-plane triad** (Signal + Nexus + SEMA) with a meta tier —
  no longer the 2-plane carve-out report 75 §3.1 recommended. The 75/76 "stateless
  carve-out" framing is superseded by this dialogue.

## Verdict (revised after the 650 cross-check)

**Capture X now; gate Y.** Decision X — message owns the existence fact durably —
realizes `l3k4` clause 1, dissolves 76.1's fragility, and stands on its own
(existence is path-independent). It is the certain win; bank it, and the 75/76
"stateless carve-out" framing is superseded for that reason alone (message becomes a
real, durable component).

Decision Y — the direct-delivery fast path — is **not** an extension of intent; it is
a deliberate **supersession** of `l3k4` clause 2 + `17ss`, and it carries the three
underweighted costs and two correctness questions above (state behind the 0660 door,
a fragmented delivery ledger, distributed origin-policy enforcement; TOCTOU and
recovery-asymmetry). My instinct that the design *coheres* is unchanged — but Y is
worth doing only if the psyche **explicitly supersedes** that intent **and** the
local-public traffic is high-volume enough to justify the hop (the latency case is
asserted, not measured). If Y proceeds, the cleanest containment (650): message's
direct-path record is **existence + a best-effort delivery ack**, the **complete**
delivery ledger stays mirrored in `router` (one audit home), and "public" is
contractually constrained to origin-agnostic, low-authority agents.
